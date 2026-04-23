import secrets
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.db.engine import get_db
from auditiq.db.models.assessment import Assessment
from auditiq.db.models.report import Report
from auditiq.db.models.response import Response
from auditiq.db.models.tenant import Tenant
from auditiq.schemas.assessment import (
    INDUSTRIES,
    AssessmentCreate,
    AssessmentResponse,
    AssessmentStatus,
    CompleteAssessmentRequest,
    CompleteAssessmentResult,
    ProgressInfo,
    QuestionOption,
    QuestionOut,
    SubmitResponseRequest,
    SubmitResponseResult,
)
from auditiq.services.question_engine import get_next_question, get_progress
from auditiq.services.scoring import calculate_all_scores, DimensionScore

router = APIRouter()


def _generate_session_token() -> str:
    return f"aiq_sess_{secrets.token_hex(24)}"


def _question_to_out(q) -> QuestionOut:
    options = None
    if q.options:
        options = [
            QuestionOption(value=o["value"], label=o["label"], score=o["score"])
            for o in q.options
        ]
    return QuestionOut(
        id=q.id,
        sequence=q.sequence,
        dimension=q.dimension,
        question_text=q.question_text,
        question_type=q.question_type,
        options=options,
        help_text=q.help_text,
    )


@router.get("/industries")
async def list_industries() -> list[str]:
    return INDUSTRIES


@router.post("", status_code=201, response_model=AssessmentResponse)
async def create_assessment(
    body: AssessmentCreate,
    db: AsyncSession = Depends(get_db),
) -> AssessmentResponse:
    if body.industry not in INDUSTRIES:
        raise HTTPException(status_code=400, detail=f"Invalid industry: {body.industry}")

    # Get default tenant
    stmt = select(Tenant).where(Tenant.slug == "app")
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=500, detail="Default tenant not configured")

    session_token = _generate_session_token()

    assessment = Assessment(
        tenant_id=tenant.id,
        session_token=session_token,
        industry=body.industry,
        company_name=body.company_name,
        company_size=body.company_size,
    )
    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)

    # Get first question
    first_q = await get_next_question(db, assessment.id, assessment.industry)
    progress = await get_progress(db, assessment.id, assessment.industry)

    return AssessmentResponse(
        assessment_id=assessment.id,
        session_token=session_token,
        total_questions=progress["total"],
        first_question=_question_to_out(first_q) if first_q else None,
    )


@router.get("/{session_token}", response_model=AssessmentStatus)
async def get_assessment(
    session_token: str,
    db: AsyncSession = Depends(get_db),
) -> AssessmentStatus:
    stmt = select(Assessment).where(Assessment.session_token == session_token)
    result = await db.execute(stmt)
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    progress = await get_progress(db, assessment.id, assessment.industry)

    return AssessmentStatus(
        assessment_id=assessment.id,
        status=assessment.status,
        industry=assessment.industry,
        company_name=assessment.company_name,
        company_size=assessment.company_size,
        progress=ProgressInfo(**progress),
        started_at=assessment.started_at,
    )


@router.get("/{session_token}/questions/next", response_model=QuestionOut | None)
async def next_question(
    session_token: str,
    db: AsyncSession = Depends(get_db),
) -> QuestionOut | None:
    stmt = select(Assessment).where(Assessment.session_token == session_token)
    result = await db.execute(stmt)
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    q = await get_next_question(db, assessment.id, assessment.industry)
    return _question_to_out(q) if q else None


@router.post("/{session_token}/responses", response_model=SubmitResponseResult)
async def submit_response(
    session_token: str,
    body: SubmitResponseRequest,
    db: AsyncSession = Depends(get_db),
) -> SubmitResponseResult:
    stmt = select(Assessment).where(Assessment.session_token == session_token)
    result = await db.execute(stmt)
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if assessment.status != "in_progress":
        raise HTTPException(status_code=400, detail="Assessment already completed")

    # Upsert response
    stmt = select(Response).where(
        Response.assessment_id == assessment.id,
        Response.question_id == body.question_id,
    )
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        existing.answer_value = body.answer_value
        existing.answer_text = body.answer_text
    else:
        response = Response(
            assessment_id=assessment.id,
            question_id=body.question_id,
            answer_value=body.answer_value,
            answer_text=body.answer_text,
        )
        db.add(response)

    await db.commit()

    # Get next question and progress
    next_q = await get_next_question(db, assessment.id, assessment.industry)
    progress = await get_progress(db, assessment.id, assessment.industry)

    return SubmitResponseResult(
        saved=True,
        progress=ProgressInfo(**progress),
        next_question=_question_to_out(next_q) if next_q else None,
    )


@router.post("/{session_token}/complete", response_model=CompleteAssessmentResult)
async def complete_assessment(
    session_token: str,
    body: CompleteAssessmentRequest,
    db: AsyncSession = Depends(get_db),
) -> CompleteAssessmentResult:
    stmt = select(Assessment).where(Assessment.session_token == session_token)
    result = await db.execute(stmt)
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if assessment.status == "completed":
        # Return existing report
        stmt = select(Report).where(Report.assessment_id == assessment.id)
        result = await db.execute(stmt)
        report = result.scalar_one_or_none()
        if report:
            return CompleteAssessmentResult(
                report_id=report.id,
                status=report.status,
                scores_preview=_build_scores_preview(report),
                estimated_time_seconds=0,
            )

    # Update assessment
    assessment.email = body.email
    assessment.status = "completed"

    # Calculate scores from responses
    from auditiq.db.models.question import Question

    stmt = select(Response).where(Response.assessment_id == assessment.id)
    result = await db.execute(stmt)
    responses = list(result.scalars().all())

    stmt = select(Question)
    result = await db.execute(stmt)
    questions = {q.id: q for q in result.scalars().all()}

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
        responses_by_dimension.setdefault(dim, []).append({
            "answer_score": answer_score,
            "weight": float(q.weight),
        })

    scores = calculate_all_scores(responses_by_dimension)

    # Create report
    report = Report(
        assessment_id=assessment.id,
        score_overall=scores["overall"],
        status="pending",
    )
    for dim_name in [
        "data_readiness", "process_maturity", "tech_infrastructure",
        "team_capability", "strategic_alignment",
    ]:
        ds = scores.get(dim_name)
        if isinstance(ds, DimensionScore):
            setattr(report, f"score_{dim_name}", ds.normalized)

    db.add(report)
    await db.commit()
    await db.refresh(report)

    return CompleteAssessmentResult(
        report_id=report.id,
        status="pending",
        scores_preview=_build_scores_preview(report),
        estimated_time_seconds=15,
    )


def _build_scores_preview(report: Report) -> dict[str, int | str]:
    from auditiq.services.scoring import get_maturity_level

    preview: dict[str, int | str] = {}
    if report.score_overall is not None:
        preview["overall"] = report.score_overall
        preview["overall_level"] = get_maturity_level(report.score_overall)
    for dim in [
        "data_readiness", "process_maturity", "tech_infrastructure",
        "team_capability", "strategic_alignment",
    ]:
        val = getattr(report, f"score_{dim}", None)
        if val is not None:
            preview[dim] = val
    return preview
