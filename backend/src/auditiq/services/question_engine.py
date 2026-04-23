import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.db.models.question import Question
from auditiq.db.models.response import Response


async def get_questions_for_assessment(
    db: AsyncSession,
    industry: str,
) -> list[Question]:
    """Get all applicable questions for an assessment, resolving industry branching.

    Returns questions ordered by sequence. For questions with industry_filter,
    only includes those matching the assessment's industry.
    """
    stmt = select(Question).order_by(Question.sequence)
    result = await db.execute(stmt)
    all_questions = list(result.scalars().all())

    filtered: list[Question] = []
    for q in all_questions:
        # If no industry filter, include for all industries
        if q.industry_filter is None:
            filtered.append(q)
        elif industry in q.industry_filter:
            filtered.append(q)
    return filtered


async def get_next_question(
    db: AsyncSession,
    assessment_id: uuid.UUID,
    industry: str,
) -> Question | None:
    """Get the next unanswered question for the assessment."""
    questions = await get_questions_for_assessment(db, industry)

    # Get already-answered question IDs
    stmt = (
        select(Response.question_id)
        .where(Response.assessment_id == assessment_id)
    )
    result = await db.execute(stmt)
    answered_ids = set(result.scalars().all())

    # Find first unanswered
    for q in questions:
        if q.id not in answered_ids:
            # Check dependency
            if q.depends_on is not None:
                parent_resp = await _get_response_value(db, assessment_id, q.depends_on)
                if parent_resp != q.depends_value:
                    continue
            return q
    return None


async def get_progress(
    db: AsyncSession,
    assessment_id: uuid.UUID,
    industry: str,
) -> dict[str, int]:
    """Get assessment progress."""
    questions = await get_questions_for_assessment(db, industry)
    total = len(questions)

    stmt = (
        select(Response.question_id)
        .where(Response.assessment_id == assessment_id)
    )
    result = await db.execute(stmt)
    answered = len(set(result.scalars().all()))

    return {
        "answered": answered,
        "total": total,
        "percent": round((answered / total) * 100) if total > 0 else 0,
    }


async def _get_response_value(
    db: AsyncSession,
    assessment_id: uuid.UUID,
    question_id: uuid.UUID,
) -> str | None:
    stmt = (
        select(Response.answer_value)
        .where(Response.assessment_id == assessment_id)
        .where(Response.question_id == question_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
