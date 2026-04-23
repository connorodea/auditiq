import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.db.engine import get_db
from auditiq.db.models.report import Report
from auditiq.schemas.report import ReportOut, ReportStatusOut
from auditiq.services.report_generator import generate_report

router = APIRouter()


@router.get("/{report_id}", response_model=ReportOut)
async def get_report(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ReportOut:
    stmt = select(Report).where(Report.id == report_id)
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Return teaser or full based on unlock status
    report_content = None
    if report.is_unlocked and report.report_json:
        report_content = report.report_json
    elif report.teaser_json:
        report_content = report.teaser_json

    return ReportOut(
        id=report.id,
        assessment_id=report.assessment_id,
        score_overall=report.score_overall,
        score_data_readiness=report.score_data_readiness,
        score_process_maturity=report.score_process_maturity,
        score_tech_infrastructure=report.score_tech_infrastructure,
        score_team_capability=report.score_team_capability,
        score_strategic_alignment=report.score_strategic_alignment,
        is_unlocked=report.is_unlocked,
        status=report.status,
        report_content=report_content,
        created_at=report.created_at,
    )


@router.get("/{report_id}/status", response_model=ReportStatusOut)
async def get_report_status(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ReportStatusOut:
    stmt = select(Report).where(Report.id == report_id)
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return ReportStatusOut(
        status=report.status,
        is_unlocked=report.is_unlocked,
        score_overall=report.score_overall,
    )


@router.post("/{report_id}/generate", response_model=ReportStatusOut)
async def trigger_generation(
    report_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> ReportStatusOut:
    stmt = select(Report).where(Report.id == report_id)
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status == "completed":
        return ReportStatusOut(
            status=report.status,
            is_unlocked=report.is_unlocked,
            score_overall=report.score_overall,
        )

    # Generate in background
    background_tasks.add_task(_generate_report_task, report_id)

    return ReportStatusOut(
        status="generating",
        is_unlocked=False,
        score_overall=report.score_overall,
    )


async def _generate_report_task(report_id: uuid.UUID) -> None:
    """Background task to generate report via Claude API."""
    from auditiq.db.engine import async_session

    async with async_session() as db:
        try:
            await generate_report(db, report_id)
        except Exception as e:
            stmt = select(Report).where(Report.id == report_id)
            result = await db.execute(stmt)
            report = result.scalar_one_or_none()
            if report:
                report.status = "failed"
                report.error_message = str(e)
                await db.commit()
