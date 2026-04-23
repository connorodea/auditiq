import json
import time
import uuid

import anthropic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.config import settings
from auditiq.db.models.assessment import Assessment
from auditiq.db.models.question import Question
from auditiq.db.models.report import Report
from auditiq.db.models.response import Response
from auditiq.prompts.report_system import SYSTEM_PROMPT
from auditiq.prompts.report_user import USER_PROMPT_TEMPLATE
from auditiq.services.scoring import (
    DimensionScore,
    calculate_all_scores,
    estimate_roi,
    get_industry_benchmark,
)


def format_responses_for_prompt(
    responses: list[Response],
    questions: dict[uuid.UUID, Question],
) -> str:
    """Convert raw responses into readable context for Claude."""
    lines: list[str] = []
    for resp in responses:
        q = questions.get(resp.question_id)
        if q is None:
            continue
        answer_label = resp.answer_value
        if q.options:
            for opt in q.options:
                if opt["value"] == resp.answer_value:
                    answer_label = opt["label"]
                    break
        lines.append(f"Q{q.sequence}. {q.question_text}")
        lines.append(f"   Answer: {answer_label}")
        if resp.answer_text:
            lines.append(f"   Additional context: {resp.answer_text}")
        lines.append("")
    return "\n".join(lines)


def extract_teaser(full_report: dict) -> dict:
    """Extract the free preview subset from the full report."""
    return {
        "executive_summary": full_report.get("executive_summary", {}),
        "dimension_analysis": [
            {
                "dimension": d["dimension"],
                "title": d["title"],
                "score": d["score"],
                "level": d["level"],
                "analysis": d["analysis"].split(". ")[0] + "." if d.get("analysis") else "",
                "strengths": [],
                "gaps": [],
                "priority": d.get("priority", "medium"),
            }
            for d in full_report.get("dimension_analysis", [])
        ],
        "opportunity_zones_count": len(full_report.get("opportunity_zones", [])),
        "opportunity_zones_preview": [
            {"title": oz["title"], "impact": oz["impact"], "effort": oz["effort"]}
            for oz in full_report.get("opportunity_zones", [])[:2]
        ],
        "has_roadmap": True,
        "has_roi_analysis": True,
        "next_steps_count": len(full_report.get("next_steps", [])),
    }


async def generate_report(db: AsyncSession, report_id: uuid.UUID) -> Report:
    """Generate the AI report using Claude API."""
    # Load report with assessment
    stmt = select(Report).where(Report.id == report_id)
    result = await db.execute(stmt)
    report = result.scalar_one()

    stmt = select(Assessment).where(Assessment.id == report.assessment_id)
    result = await db.execute(stmt)
    assessment = result.scalar_one()

    # Load responses
    stmt = select(Response).where(Response.assessment_id == assessment.id)
    result = await db.execute(stmt)
    responses = list(result.scalars().all())

    # Load questions
    stmt = select(Question)
    result = await db.execute(stmt)
    questions = {q.id: q for q in result.scalars().all()}

    # Calculate scores
    responses_by_dimension: dict[str, list[dict[str, float]]] = {}
    for resp in responses:
        q = questions.get(resp.question_id)
        if q is None:
            continue
        dim = q.dimension
        answer_score = 0
        if q.options:
            for opt in q.options:
                if opt["value"] == resp.answer_value:
                    answer_score = opt["score"]
                    break
        if dim not in responses_by_dimension:
            responses_by_dimension[dim] = []
        responses_by_dimension[dim].append({
            "answer_score": answer_score,
            "weight": float(q.weight),
        })

    scores = calculate_all_scores(responses_by_dimension)

    # Save scores to report
    for dim_name in [
        "data_readiness", "process_maturity", "tech_infrastructure",
        "team_capability", "strategic_alignment",
    ]:
        dim_score = scores.get(dim_name)
        if isinstance(dim_score, DimensionScore):
            setattr(report, f"score_{dim_name}", dim_score.normalized)
    report.score_overall = scores["overall"]

    # Build prompt
    benchmark = get_industry_benchmark(assessment.industry)
    overall_score = scores["overall"]
    diff = overall_score - benchmark["median_overall"]

    dim_data = {}
    for dim_name in [
        "data_readiness", "process_maturity", "tech_infrastructure",
        "team_capability", "strategic_alignment",
    ]:
        ds = scores.get(dim_name)
        if isinstance(ds, DimensionScore):
            dim_data[f"score_{dim_name}"] = ds.normalized
            dim_data[f"level_{dim_name}"] = ds.level

    user_prompt = USER_PROMPT_TEMPLATE.format(
        industry=assessment.industry,
        company_size=assessment.company_size or "Unknown",
        company_name=assessment.company_name or "the company",
        score_overall=overall_score,
        level_overall=scores["overall_level"],
        formatted_responses=format_responses_for_prompt(responses, questions),
        industry_median=benchmark["median_overall"],
        industry_top_quartile=benchmark["top_quartile"],
        vs_median=f"{'+'if diff > 0 else ''}{diff} points {'above' if diff > 0 else 'below'} median",
        **dim_data,
    )

    # Call Claude API
    report.status = "generating"
    await db.commit()

    start_time = time.monotonic()

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    message = await client.messages.create(
        model=settings.claude_model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    elapsed_ms = round((time.monotonic() - start_time) * 1000)

    # Parse response
    raw_text = message.content[0].text
    report_json = json.loads(raw_text)

    # Save to report
    report.report_json = report_json
    report.teaser_json = extract_teaser(report_json)
    report.status = "completed"
    report.claude_model = settings.claude_model
    report.claude_tokens = message.usage.input_tokens + message.usage.output_tokens
    report.generation_time_ms = elapsed_ms

    await db.commit()
    await db.refresh(report)

    return report
