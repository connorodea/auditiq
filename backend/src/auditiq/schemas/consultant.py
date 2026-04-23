import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ConsultantRegister(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=255)
    company_name: str = Field(..., min_length=1, max_length=255)


class ConsultantLogin(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=1)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    consultant: "ConsultantOut"


class ConsultantOut(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    company_name: str | None
    tenant_id: uuid.UUID
    subscription_status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ConsultantUpdate(BaseModel):
    full_name: str | None = None
    company_name: str | None = None
