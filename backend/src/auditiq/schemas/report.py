import uuid
from datetime import datetime

from pydantic import BaseModel


class ReportOut(BaseModel):
    id: uuid.UUID
    assessment_id: uuid.UUID
    score_overall: int | None
    score_data_readiness: int | None
    score_process_maturity: int | None
    score_tech_infrastructure: int | None
    score_team_capability: int | None
    score_strategic_alignment: int | None
    is_unlocked: bool
    status: str
    report_content: dict | None = None  # teaser_json or report_json based on unlock
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportStatusOut(BaseModel):
    status: str
    is_unlocked: bool
    score_overall: int | None
