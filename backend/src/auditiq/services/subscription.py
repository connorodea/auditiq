import uuid

import stripe
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.config import settings
from auditiq.db.models.consultant import Consultant


def get_stripe_client() -> stripe.StripeClient:
    return stripe.StripeClient(settings.stripe_secret_key)


async def create_subscription_checkout(
    db: AsyncSession,
    consultant_id: uuid.UUID,
) -> dict[str, str]:
    """Create a Stripe Checkout Session for the $149/mo consultant subscription."""
    stmt = select(Consultant).where(Consultant.id == consultant_id)
    result = await db.execute(stmt)
    consultant = result.scalar_one()

    client = get_stripe_client()

    params: dict = {
        "mode": "subscription",
        "customer_email": consultant.email,
        "line_items": [
            {
                "price": settings.stripe_price_consultant,
                "quantity": 1,
            }
        ],
        "success_url": f"{settings.app_url}/console/billing?session_id={{CHECKOUT_SESSION_ID}}",
        "cancel_url": f"{settings.app_url}/console/billing",
        "metadata": {
            "consultant_id": str(consultant.id),
        },
    }

    # If consultant already has a Stripe customer, reuse it
    if consultant.stripe_customer_id:
        params["customer"] = consultant.stripe_customer_id
        del params["customer_email"]

    session = client.checkout.sessions.create(params=params)

    return {
        "checkout_url": session.url,
        "checkout_session_id": session.id,
    }


async def handle_subscription_event(
    db: AsyncSession,
    event_type: str,
    event_data: dict,
) -> None:
    """Handle Stripe subscription webhook events."""
    if event_type == "checkout.session.completed":
        session = event_data
        if session.get("mode") != "subscription":
            return

        consultant_id = session.get("metadata", {}).get("consultant_id")
        if not consultant_id:
            return

        stmt = select(Consultant).where(Consultant.id == uuid.UUID(consultant_id))
        result = await db.execute(stmt)
        consultant = result.scalar_one_or_none()
        if not consultant:
            return

        consultant.stripe_customer_id = session.get("customer")
        consultant.stripe_subscription_id = session.get("subscription")
        consultant.subscription_status = "active"
        await db.commit()

    elif event_type in (
        "customer.subscription.updated",
        "customer.subscription.deleted",
    ):
        subscription = event_data
        sub_id = subscription.get("id")

        stmt = select(Consultant).where(Consultant.stripe_subscription_id == sub_id)
        result = await db.execute(stmt)
        consultant = result.scalar_one_or_none()
        if not consultant:
            return

        status_map = {
            "active": "active",
            "trialing": "trialing",
            "past_due": "past_due",
            "canceled": "canceled",
            "unpaid": "past_due",
            "incomplete": "inactive",
            "incomplete_expired": "inactive",
        }
        new_status = status_map.get(subscription.get("status", ""), "inactive")
        consultant.subscription_status = new_status
        await db.commit()
