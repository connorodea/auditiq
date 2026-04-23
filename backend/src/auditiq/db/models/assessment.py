import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auditiq.db.base import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    session_token: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str | None] = mapped_column(String(255))
    company_name: Mapped[str | None] = mapped_column(String(255))
    industry: Mapped[str] = mapped_column(String(50))
    company_size: Mapped[str | None] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(20), default="in_progress")
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="assessments")  # noqa: F821
    responses: Mapped[list["Response"]] = relationship(  # noqa: F821
        back_populates="assessment", cascade="all, delete-orphan"
    )
    report: Mapped["Report | None"] = relationship(  # noqa: F821
        back_populates="assessment", uselist=False
    )
