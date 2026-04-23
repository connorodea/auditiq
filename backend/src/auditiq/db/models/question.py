import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from auditiq.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    sequence: Mapped[int] = mapped_column(Integer)
    dimension: Mapped[str] = mapped_column(String(50))  # data_readiness, process_maturity, etc.
    question_text: Mapped[str] = mapped_column(Text)
    question_type: Mapped[str] = mapped_column(String(20), default="single_choice")
    options: Mapped[dict | None] = mapped_column(JSONB)
    weight: Mapped[float] = mapped_column(Numeric(3, 2), default=1.0)
    industry_filter: Mapped[list[str] | None] = mapped_column(ARRAY(String(50)))
    depends_on: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("questions.id"))
    depends_value: Mapped[str | None] = mapped_column(String(50))
    help_text: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
