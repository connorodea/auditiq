import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.db.engine import get_db
from auditiq.db.models.assessment import Assessment
from auditiq.db.models.consultant import Consultant
from auditiq.db.models.report import Report
from auditiq.dependencies import get_current_consultant
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class DashboardStats(BaseModel):
    total_assessments: int
    completed_assessments: int
    reports_generated: int
    reports_unlocked: int
    avg_score: float | None


class ClientRow(BaseModel):
    assessment_id: uuid.UUID
    email: str | None
    company_name: str | None
    industry: str
    company_size: str | None
    status: str
    score_overall: int | None
    report_id: uuid.UUID | None
    report_status: str | None
    is_unlocked: bool
    started_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class DashboardResponse(BaseModel):
    stats: DashboardStats
    clients: list[ClientRow]


@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    consultant: Consultant = Depends(get_current_consultant),
    db: AsyncSession = Depends(get_db),
) -> DashboardResponse:
    """Get consultant dashboard with stats and client list."""
    tenant_id = consultant.tenant_id

    # Stats
    total_stmt = (
        select(func.count(Assessment.id))
        .where(Assessment.tenant_id == tenant_id)
    )
    total = (await db.execute(total_stmt)).scalar() or 0

    completed_stmt = (
        select(func.count(Assessment.id))
        .where(Assessment.tenant_id == tenant_id)
        .where(Assessment.status == "completed")
    )
    completed = (await db.execute(completed_stmt)).scalar() or 0

    reports_stmt = (
        select(func.count(Report.id))
        .join(Assessment, Assessment.id == Report.assessment_id)
        .where(Assessment.tenant_id == tenant_id)
        .where(Report.status == "completed")
    )
    reports_gen = (await db.execute(reports_stmt)).scalar() or 0

    unlocked_stmt = (
        select(func.count(Report.id))
        .join(Assessment, Assessment.id == Report.assessment_id)
        .where(Assessment.tenant_id == tenant_id)
        .where(Report.is_unlocked == True)
    )
    unlocked = (await db.execute(unlocked_stmt)).scalar() or 0

    avg_stmt = (
        select(func.avg(Report.score_overall))
        .join(Assessment, Assessment.id == Report.assessment_id)
        .where(Assessment.tenant_id == tenant_id)
        .where(Report.score_overall.isnot(None))
    )
    avg_score = (await db.execute(avg_stmt)).scalar()

    # Client list
    clients_stmt = (
        select(Assessment)
        .where(Assessment.tenant_id == tenant_id)
        .order_by(Assessment.created_at.desc())
        .limit(100)
    )
    result = await db.execute(clients_stmt)
    assessments = list(result.scalars().all())

    client_rows: list[ClientRow] = []
    for a in assessments:
        # Load report if exists
        report_stmt = select(Report).where(Report.assessment_id == a.id)
        report_result = await db.execute(report_stmt)
        report = report_result.scalar_one_or_none()

        client_rows.append(ClientRow(
            assessment_id=a.id,
            email=a.email,
            company_name=a.company_name,
            industry=a.industry,
            company_size=a.company_size,
            status=a.status,
            score_overall=report.score_overall if report else None,
            report_id=report.id if report else None,
            report_status=report.status if report else None,
            is_unlocked=report.is_unlocked if report else False,
            started_at=a.started_at,
            completed_at=a.completed_at,
        ))

    return DashboardResponse(
        stats=DashboardStats(
            total_assessments=total,
            completed_assessments=completed,
            reports_generated=reports_gen,
            reports_unlocked=unlocked,
            avg_score=round(avg_score, 1) if avg_score else None,
        ),
        clients=client_rows,
    )
