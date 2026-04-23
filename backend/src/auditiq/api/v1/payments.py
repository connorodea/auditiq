import uuid

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.config import settings
from auditiq.db.engine import get_db
from auditiq.schemas.payment import CheckoutRequest, CheckoutResponse
from auditiq.services.stripe_service import create_checkout_session, handle_checkout_completed

router = APIRouter()


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(
    body: CheckoutRequest,
    db: AsyncSession = Depends(get_db),
) -> CheckoutResponse:
    result = await create_checkout_session(db, body.report_id, body.email)
    return CheckoutResponse(
        checkout_url=result["checkout_url"],
        checkout_session_id=result["checkout_session_id"],
    )


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

    if event["type"] == "checkout.session.completed":
        await handle_checkout_completed(db, event["data"]["object"])

    return {"status": "ok"}
