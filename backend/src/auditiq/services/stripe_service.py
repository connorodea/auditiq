import uuid

import stripe
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.config import settings
from auditiq.db.models.payment import Payment
from auditiq.db.models.report import Report


def get_stripe_client() -> stripe.StripeClient:
    return stripe.StripeClient(settings.stripe_secret_key)


async def create_checkout_session(
    db: AsyncSession,
    report_id: uuid.UUID,
    email: str,
) -> dict[str, str]:
    """Create a Stripe Checkout Session for report unlock."""
    client = get_stripe_client()

    session = client.checkout.sessions.create(
        params={
            "mode": "payment",
            "customer_email": email,
            "line_items": [
                {
                    "price": settings.stripe_price_report,
                    "quantity": 1,
                }
            ],
            "success_url": f"{settings.app_url}/report/{report_id}/full?session_id={{CHECKOUT_SESSION_ID}}",
            "cancel_url": f"{settings.app_url}/report/{report_id}",
            "metadata": {
                "report_id": str(report_id),
            },
        }
    )

    # Record payment intent
    payment = Payment(
        report_id=report_id,
        assessment_id=(
            await db.execute(
                select(Report.assessment_id).where(Report.id == report_id)
            )
        ).scalar_one(),
        stripe_checkout_id=session.id,
        email=email,
        amount_cents=4700,
        status="pending",
    )
    db.add(payment)
    await db.commit()

    return {
        "checkout_url": session.url,
        "checkout_session_id": session.id,
    }


async def handle_checkout_completed(
    db: AsyncSession,
    session_data: dict,
) -> None:
    """Handle successful Stripe checkout — unlock the report."""
    checkout_id = session_data["id"]
    report_id = session_data["metadata"]["report_id"]

    # Update payment
    stmt = select(Payment).where(Payment.stripe_checkout_id == checkout_id)
    result = await db.execute(stmt)
    payment = result.scalar_one_or_none()
    if payment:
        payment.status = "completed"
        payment.stripe_payment_intent = session_data.get("payment_intent")
        payment.stripe_customer_id = session_data.get("customer")

    # Unlock report
    stmt = select(Report).where(Report.id == uuid.UUID(report_id))
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()
    if report:
        report.is_unlocked = True

    await db.commit()
