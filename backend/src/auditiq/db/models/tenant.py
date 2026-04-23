import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auditiq.db.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(63), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    logo_url: Mapped[str | None] = mapped_column(Text)
    primary_color: Mapped[str] = mapped_column(String(7), default="#2563EB")
    accent_color: Mapped[str] = mapped_column(String(7), default="#7C3AED")
    cta_text: Mapped[str] = mapped_column(
        String(255), default="Get Your AI Readiness Report"
    )
    cta_url: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    assessments: Mapped[list["Assessment"]] = relationship(back_populates="tenant")  # noqa: F821
