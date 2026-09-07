"""Token-scoped public checkout; Ops endpoints remain development-only."""
import json
from typing import Literal

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from ..booking_service import get_booking
from ..payment_schemas import BookingPayment, LinkInput, OrderInput, OpsPayment, PaymentLink, PublicPayment
from .. import payment_service as service
from ..models import PaymentWebhookEvent
from ..services.paypal import PayPalError
from .ops import private_response

public_router = APIRouter(prefix='/public/payments', tags=['Token-scoped sandbox payments'], dependencies=[Depends(private_response)])
ops_router = APIRouter(prefix='/ops', tags=['Internal payments'], dependencies=[Depends(private_response)])
webhook_router = APIRouter(tags=['Verified PayPal notifications'], dependencies=[Depends(private_response)])


def token(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(404, 'Payment link is invalid or expired. Please contact Volcan Vacations.')
    return authorization[7:]


def provider_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except PayPalError:
        raise HTTPException(503, 'PayPal sandbox is unavailable or requires configuration/reconciliation. Please try again later.') from None
    except IntegrityError:
        raise HTTPException(409, 'Payment changed concurrently. Refresh payment status before retrying.') from None


@public_router.get('/session', response_model=PublicPayment)
def session(token: str = Depends(token), db: Session = Depends(get_db), paypal=Depends(service.get_paypal)):
    booking = service.token_booking(db, token)
    return service.public_payment(booking, service.payment_for(db, booking), paypal)


@public_router.post('/paypal/order', response_model=PublicPayment)
def create(payload: OrderInput, token: str = Depends(token), db: Session = Depends(get_db), paypal=Depends(service.get_paypal)):
    return provider_call(service.create_order, db, token, payload, paypal)


@public_router.post('/paypal/{order_id}/capture', response_model=PublicPayment)
def capture(order_id: str, token: str = Depends(token), db: Session = Depends(get_db), paypal=Depends(service.get_paypal)):
    return provider_call(service.capture_order, db, token, order_id, paypal)


@public_router.post('/paypal/{order_id}/cancel', response_model=PublicPayment)
def cancel(order_id: str, token: str = Depends(token), db: Session = Depends(get_db), paypal=Depends(service.get_paypal)):
    return service.cancel_checkout(db, token, order_id, paypal)


@public_router.post('/reconcile', response_model=PublicPayment)
def reconcile(token: str = Depends(token), db: Session = Depends(get_db), paypal=Depends(service.get_paypal)):
    return provider_call(service.reconcile, db, paypal, token=token)


@ops_router.get('/bookings/{booking_id}/payment', response_model=BookingPayment)
def booking_payment(booking_id: int, db: Session = Depends(get_db), paypal=Depends(service.get_paypal)):
    return service.booking_payment(db, get_booking(db, booking_id), paypal)


@ops_router.post('/bookings/{booking_id}/payment-link', response_model=PaymentLink)
def payment_link(booking_id: int, payload: LinkInput, db: Session = Depends(get_db)):
    return service.issue_link(db, booking_id, payload)


@ops_router.post('/bookings/{booking_id}/payment-link/revoke')
def revoke_link(booking_id: int, payload: LinkInput, db: Session = Depends(get_db)):
    return service.issue_link(db, booking_id, payload, revoke=True)


@ops_router.post('/bookings/{booking_id}/payment/reconcile', response_model=BookingPayment)
def ops_reconcile(booking_id: int, db: Session = Depends(get_db), paypal=Depends(service.get_paypal)):
    return provider_call(service.reconcile, db, paypal, booking_id=booking_id)


@ops_router.get('/payments', response_model=list[OpsPayment])
def payments(status: Literal['pending', 'paid', 'failed', 'refunded'] | None = None, db: Session = Depends(get_db)):
    return service.list_payments(db, status)


@webhook_router.post('/webhooks/paypal')
async def webhook(request: Request, db: Session = Depends(get_db), paypal=Depends(service.get_paypal)):
    raw = bytearray()
    async for chunk in request.stream():
        raw.extend(chunk)
        if len(raw) > 262144:
            raise HTTPException(413, 'Webhook body too large')
    try:
        event = json.loads(raw)
        if not isinstance(event, dict):
            raise ValueError()
    except (ValueError, UnicodeDecodeError):
        raise HTTPException(400, 'Invalid webhook JSON') from None
    # Run blocking provider/DB work off the event loop.
    from starlette.concurrency import run_in_threadpool
    try:
        return await run_in_threadpool(service.webhook, db, paypal, request.headers, event)
    except IntegrityError:
        db.rollback()
        if isinstance(event.get('id'), str) and db.scalar(select(PaymentWebhookEvent.id).where(PaymentWebhookEvent.provider_event_id == event['id'])):
            return {'received': True}
        raise HTTPException(503, 'Webhook reconciliation needs retry') from None
    except PayPalError:
        raise HTTPException(503, 'Webhook verification or reconciliation needs retry') from None
