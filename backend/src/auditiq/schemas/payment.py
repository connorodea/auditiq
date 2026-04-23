import uuid

from pydantic import BaseModel, Field


class CheckoutRequest(BaseModel):
    report_id: uuid.UUID
    email: str = Field(..., max_length=255)


class CheckoutResponse(BaseModel):
    checkout_url: str
    checkout_session_id: str
