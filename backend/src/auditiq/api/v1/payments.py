import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.config import settings
from auditiq.db.engine import get_db
from auditiq.db.models.consultant import Consultant
from auditiq.dependencies import get_current_consultant
from auditiq.schemas.payment import CheckoutRequest, CheckoutResponse
from auditiq.services.stripe_service import create_checkout_session, handle_checkout_completed
from auditiq.services.subscription import (
    create_subscription_checkout,
    handle_subscription_event,
)

router = APIRouter()


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(
    body: CheckoutRequest,
    db: AsyncSession = Depends(get_db),
) -> CheckoutResponse:
    """Create Stripe Checkout for one-time report unlock ($47)."""
    result = await create_checkout_session(db, body.report_id, body.email)
    return CheckoutResponse(
        checkout_url=result["checkout_url"],
        checkout_session_id=result["checkout_session_id"],
    )


@router.post("/subscribe")
async def create_subscription(
    consultant: Consultant = Depends(get_current_consultant),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Create Stripe Checkout for consultant subscription ($149/mo)."""
    result = await create_subscription_checkout(db, consultant.id)
    return result


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event["type"]
    event_data = event["data"]["object"]

    # One-time payment (report unlock)
    if event_type == "checkout.session.completed":
        if event_data.get("mode") == "payment":
            await handle_checkout_completed(db, event_data)
        elif event_data.get("mode") == "subscription":
            await handle_subscription_event(db, event_type, event_data)

    # Subscription lifecycle events
    elif event_type in (
        "customer.subscription.updated",
        "customer.subscription.deleted",
    ):
        await handle_subscription_event(db, event_type, event_data)

    return {"status": "ok"}
