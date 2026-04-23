import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class AssessmentCreate(BaseModel):
    industry: str = Field(..., min_length=1, max_length=50)
    company_name: str | None = Field(None, max_length=255)
    company_size: str | None = Field(None, pattern=r"^(1-10|11-50|51-200|201-1000|1000\+)$")


class AssessmentResponse(BaseModel):
    assessment_id: uuid.UUID
    session_token: str
    total_questions: int
    first_question: "QuestionOut | None" = None

    model_config = {"from_attributes": True}


class AssessmentStatus(BaseModel):
    assessment_id: uuid.UUID
    status: str
    industry: str
    company_name: str | None
    company_size: str | None
    progress: "ProgressInfo"
    started_at: datetime

    model_config = {"from_attributes": True}


class ProgressInfo(BaseModel):
    answered: int
    total: int
    percent: int


class SubmitResponseRequest(BaseModel):
    question_id: uuid.UUID
    answer_value: str = Field(..., min_length=1, max_length=255)
    answer_text: str | None = None


class SubmitResponseResult(BaseModel):
    saved: bool
    progress: ProgressInfo
    next_question: "QuestionOut | None" = None


class CompleteAssessmentRequest(BaseModel):
    email: str = Field(..., max_length=255)


class CompleteAssessmentResult(BaseModel):
    report_id: uuid.UUID
    status: str
    scores_preview: dict[str, int | str]
    estimated_time_seconds: int = 15


class QuestionOption(BaseModel):
    value: str
    label: str
    score: int


class QuestionOut(BaseModel):
    id: uuid.UUID
    sequence: int
    dimension: str
    question_text: str
    question_type: str
    options: list[QuestionOption] | None = None
    help_text: str | None = None

    model_config = {"from_attributes": True}


# Supported industries
INDUSTRIES = [
    "healthcare",
    "finance",
    "retail",
    "ecommerce",
    "manufacturing",
    "professional_services",
    "technology",
    "education",
    "real_estate",
    "construction",
    "logistics",
    "hospitality",
    "legal",
    "other",
]
