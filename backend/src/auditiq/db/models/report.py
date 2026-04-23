import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auditiq.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assessments.id"), unique=True
    )

    # Scores (0-100 per dimension)
    score_data_readiness: Mapped[int | None] = mapped_column(Integer)
    score_process_maturity: Mapped[int | None] = mapped_column(Integer)
    score_tech_infrastructure: Mapped[int | None] = mapped_column(Integer)
    score_team_capability: Mapped[int | None] = mapped_column(Integer)
    score_strategic_alignment: Mapped[int | None] = mapped_column(Integer)
    score_overall: Mapped[int | None] = mapped_column(Integer)

    # Generated content
    report_json: Mapped[dict | None] = mapped_column(JSONB)
    teaser_json: Mapped[dict | None] = mapped_column(JSONB)
    is_unlocked: Mapped[bool] = mapped_column(Boolean, default=False)

    # PDF
    pdf_url: Mapped[str | None] = mapped_column(Text)
    pdf_generated: Mapped[bool] = mapped_column(Boolean, default=False)

    # Meta
    status: Mapped[str] = mapped_column(String(20), default="pending")
    claude_model: Mapped[str | None] = mapped_column(String(50))
    claude_tokens: Mapped[int | None] = mapped_column(Integer)
    generation_time_ms: Mapped[int | None] = mapped_column(Integer)
    error_message: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    assessment: Mapped["Assessment"] = relationship(back_populates="report")  # noqa: F821
    payments: Mapped[list["Payment"]] = relationship(back_populates="report")  # noqa: F821
