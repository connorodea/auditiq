import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auditiq.db.base import Base


class Response(Base):
    __tablename__ = "responses"
    __table_args__ = (
        UniqueConstraint("assessment_id", "question_id", name="uq_response_assessment_question"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    assessment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessments.id", ondelete="CASCADE"))
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id"))
    answer_value: Mapped[str] = mapped_column(String(255))
    answer_text: Mapped[str | None] = mapped_column(Text)
    answered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    assessment: Mapped["Assessment"] = relationship(back_populates="responses")  # noqa: F821
