import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TenantOut(BaseModel):
    id: uuid.UUID
    slug: str
    name: str
    logo_url: str | None
    primary_color: str
    accent_color: str
    cta_text: str
    cta_url: str | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TenantUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    logo_url: str | None = None
    primary_color: str | None = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")
    accent_color: str | None = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")
    cta_text: str | None = Field(None, max_length=255)
    cta_url: str | None = None


class TenantPublic(BaseModel):
    """Public tenant info exposed to the frontend via subdomain lookup."""
    slug: str
    name: str
    logo_url: str | None
    primary_color: str
    accent_color: str
    cta_text: str
    cta_url: str | None

    model_config = {"from_attributes": True}
