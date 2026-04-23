import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auditiq.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reports.id"))
    assessment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessments.id"))

    # Stripe
    stripe_checkout_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    stripe_payment_intent: Mapped[str | None] = mapped_column(String(255), unique=True)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(255))

    amount_cents: Mapped[int] = mapped_column(Integer, default=4700)
    currency: Mapped[str] = mapped_column(String(3), default="usd")
    status: Mapped[str] = mapped_column(String(20), default="pending")
    email: Mapped[str | None] = mapped_column(String(255))

    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    report: Mapped["Report"] = relationship(back_populates="payments")  # noqa: F821
