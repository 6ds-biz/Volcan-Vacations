"""One immutable checkout intent per reservation; all money comes from snapshots.

Commit request IDs before provider calls. Serialize provider actions with the
same trip/reservation locks used by Operations. Reconcile uncertain outcomes;
never replace an unknown order with a new chargeable order.
"""
import hashlib
import re
import secrets
from datetime import timedelta
from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from .availability_rules import aware, utcnow
from .config import settings
from .models import Payment, PaymentRefund, PaymentWebhookEvent, Reservation, Trip
from .services.paypal import PayPal, PayPalError, money, provider_id

PAID = ('captured', 'refunded', 'partially_refunded')
BLOCKING = ('REVIEW_REQUIRED', 'AMOUNT_MISMATCH', 'INVALID_PROVIDER_RESPONSE', 'ORDER_MISMATCH', 'CAPTURE_MISMATCH', 'BOOKING_CHANGED', 'REFUND_REVIEW')
RETRY_WINDOW = timedelta(hours=5)  # inside PayPal's default six-hour request-ID retention
ZERO = Decimal('0.00')


def get_paypal():
    return PayPal(settings)


def invalidate_payment_link(booking):
    if not booking.ready_for_payment or booking.trip.status in ('cancelled', 'completed'):
        booking.payment_token_hash = None
        booking.payment_token_expires_at = None


def payment_query():
    return select(Payment).options(selectinload(Payment.reservation).selectinload(Reservation.product),
                                  selectinload(Payment.trip).selectinload(Trip.customer))


def payment_for(db, booking, lock=False):
    query = payment_query().where(Payment.reservation_id == booking.id).execution_options(populate_existing=True)
    return db.scalar(query.with_for_update() if lock else query)


def token_booking(db, token, lock=False):
    from .booking_service import get_booking
    if not re.fullmatch(r'[A-Za-z0-9_-]{43}', token or ''):
        raise HTTPException(404, 'Payment link is invalid or expired. Please contact Volcan Vacations.')
    hashed = hashlib.sha256(token.encode()).hexdigest()
    booking_id = db.scalar(select(Reservation.id).where(Reservation.payment_token_hash == hashed))
    if not booking_id:
        raise HTTPException(404, 'Payment link is invalid or expired. Please contact Volcan Vacations.')
    booking = get_booking(db, booking_id, lock=lock)
    if (booking.payment_token_hash != hashed or not booking.payment_token_expires_at or
        aware(booking.payment_token_expires_at) <= utcnow() or booking.status in ('cancelled', 'completed') or booking.trip.status in ('cancelled', 'completed')):
        raise HTTPException(404, 'Payment link is invalid or expired. Please contact Volcan Vacations.')
    return booking


def eligible(booking, payment=None):
    return (booking.ready_for_payment and booking.trip.status not in ('cancelled', 'completed') and
            ZERO < booking.retail_total <= Decimal('9999999999.99') and
            (not booking.payment_due_at or aware(booking.payment_due_at) > utcnow()) and
            not (payment and (payment.paid_at or payment.status in PAID)))


def require_eligible(booking, payment):
    if not eligible(booking, payment):
        raise HTTPException(409, 'This reservation is not eligible for payment. Refresh or contact Volcan Vacations.')


def public_payment(booking, payment, paypal):
    can_pay = eligible(booking, payment)
    status = payment.status if payment else 'ready' if can_pay else 'not_ready'
    amount = payment.amount if payment else booking.retail_total
    paid = amount if payment and payment.paid_at else ZERO
    retryable = can_pay and not (payment and (payment.failure_code in BLOCKING or payment.provider_capture_id))
    messages = {
        'ready': 'Your tour has been confirmed and is ready for payment.',
        'created': 'Your tour has been confirmed and is ready for payment.',
        'approved': 'PayPal approval received. Payment is not received until capture completes.',
        'pending': 'Payment is being checked. Refresh payment status before trying again.',
        'captured': 'Payment received. Thank you. Volcan Vacations will follow up with your tour details.',
        'failed': 'Payment was not completed. Please retry when available or contact Volcan Vacations.',
        'cancelled': 'Payment was not completed. Your confirmed reservation is still awaiting payment.',
        'refunded': 'This payment has been refunded. Please contact Volcan Vacations about your reservation.',
        'partially_refunded': 'This payment has been partially refunded. Please contact Volcan Vacations for details.',
        'not_ready': 'This reservation is not currently ready for payment. Please contact Volcan Vacations.',
    }
    message = messages.get(status, messages['not_ready'])
    if not can_pay and not paid:
        message = messages['not_ready']
    if payment and payment.failure_code in BLOCKING:
        message = 'Payment needs review by Volcan Vacations. Please contact us before trying again.'
    return dict(booking_reference=booking.trip.reference, tour=booking.tour_name_snapshot or booking.product.name,
        date=booking.reservation_date, party_size=booking.quantity, amount=amount, amount_due=ZERO if paid else amount,
        amount_paid=paid, currency=payment.currency if payment else 'USD', provider='PayPal', status=status,
        eligible=can_pay, checkout_available=paypal.configured and retryable, retryable=retryable, message=message,
        client_id=paypal.settings.paypal_client_id if paypal.configured and retryable else None,
        environment='sandbox', order_id=payment.provider_order_id if payment and not paid else None)


def present_payment(payment):
    booking = payment.reservation
    customer = payment.trip.customer
    return dict(id=payment.id, reservation_id=payment.reservation_id, trip_id=payment.trip_id,
        booking_reference=payment.trip.reference, customer=f'{customer.first_name} {customer.last_name}',
        tour=(booking.tour_name_snapshot or booking.product.name) if booking else 'Legacy trip payment',
        **{field: getattr(payment, field) for field in ['amount', 'currency', 'status', 'provider', 'provider_environment',
            'provider_order_id', 'provider_capture_id', 'external_reference', 'failure_code', 'failure_message',
            'reconciliation_required', 'created_at', 'updated_at', 'paid_at', 'refunded_amount']})


def booking_payment(db, booking, paypal):
    payment = payment_for(db, booking)
    can_pay = eligible(booking, payment)
    labels = {'pending': 'Payment Pending', 'created': 'Payment Pending', 'approved': 'Payment Pending', 'captured': 'Paid',
              'failed': 'Payment Failed', 'cancelled': 'Ready for Payment', 'refunded': 'Refunded', 'partially_refunded': 'Partially Refunded'}
    return dict(eligible=can_pay, label=labels.get(payment.status, 'Not Ready') if payment else 'Ready for Payment' if can_pay else 'Not Ready',
        amount_due=ZERO if payment and payment.paid_at else booking.retail_total, currency='USD',
        payment_due_at=booking.payment_due_at, overdue=bool(booking.payment_due_at and aware(booking.payment_due_at) <= utcnow() and not (payment and payment.paid_at)),
        link_active=bool(booking.payment_token_hash and booking.payment_token_expires_at and aware(booking.payment_token_expires_at) > utcnow()),
        sandbox_configured=paypal.configured, webhook_configured=bool(paypal.settings.paypal_webhook_id),
        payment=present_payment(payment) if payment else None)


def issue_link(db, booking_id, payload, revoke=False):
    from .booking_service import get_booking
    with db.begin():
        booking = get_booking(db, booking_id, lock=True)
        if booking.version != payload.expected_version:
            raise HTTPException(409, 'Booking changed. Reload before changing its payment link.')
        if revoke:
            booking.payment_token_hash = None
            booking.payment_token_expires_at = None
            booking.version += 1
            return {'revoked': True}
        payment = payment_for(db, booking, lock=True)
        # A renewed link deliberately resets an expired deadline, not supplier state.
        due = payload.payment_due_at or utcnow() + timedelta(days=7)
        if not utcnow() < aware(due) <= utcnow() + timedelta(days=30):
            raise HTTPException(422, 'Choose a payment deadline within the next 30 days')
        booking.payment_due_at = due
        require_eligible(booking, payment)
        token = secrets.token_urlsafe(32)
        expires = min(aware(due), utcnow() + timedelta(days=7))
        booking.payment_token_hash = hashlib.sha256(token.encode()).hexdigest()
        booking.payment_token_expires_at = expires
        booking.version += 1
        return dict(path='/pay#token=' + token, expires_at=expires)


def failure(payment, error):
    if payment.paid_at:
        # Never downgrade a received payment on a delayed failure/approval event.
        payment.reconciliation_required = True
        return
    payment.status = 'pending' if error.uncertain else 'failed'
    payment.failure_code = 'REVIEW_REQUIRED' if error.code == 'RESOURCE_NOT_FOUND' else error.code
    payment.failure_message = 'PayPal outcome needs reconciliation; retry uses the same intent.' if error.uncertain else 'PayPal could not complete payment. The confirmed reservation has not been cancelled.'
    payment.reconciliation_required = error.uncertain or payment.failure_code in BLOCKING


def merge_order(payment, order, booking):
    """Validate binding and money before applying provider state. Never downgrade paid."""
    order_id = provider_id(order.get('id'))
    if payment.provider_order_id and order_id != payment.provider_order_id:
        raise PayPalError('ORDER_MISMATCH')
    units = order.get('purchase_units', [])
    if not isinstance(units, list) or len(units) != 1 or not isinstance(units[0], dict) or order.get('intent') != 'CAPTURE':
        raise PayPalError('ORDER_MISMATCH')
    unit = units[0]
    if unit.get('custom_id') != payment.external_reference or unit.get('reference_id') != payment.external_reference:
        raise PayPalError('ORDER_MISMATCH')
    if money(unit.get('amount'), payment.currency) != payment.amount:
        raise PayPalError('AMOUNT_MISMATCH')
    payment.provider_order_id = order_id
    payments = unit.get('payments', {})
    if not isinstance(payments, dict):
        raise PayPalError('INVALID_PROVIDER_RESPONSE')
    captures = payments.get('captures', [])
    if not isinstance(captures, list) or len(captures) > 1 or any(not isinstance(c, dict) for c in captures):
        raise PayPalError('CAPTURE_MISMATCH')
    if captures:
        capture = captures[0]
        capture_id = provider_id(capture.get('id'))
        if money(capture.get('amount'), payment.currency) != payment.amount:
            raise PayPalError('AMOUNT_MISMATCH')
        if payment.provider_capture_id and payment.provider_capture_id != capture_id:
            raise PayPalError('CAPTURE_MISMATCH')
        payment.provider_capture_id = capture_id
        state = capture.get('status')
        if state in ('COMPLETED', 'REFUNDED', 'PARTIALLY_REFUNDED'):
            if not payment.paid_at:
                payment.paid_at = utcnow()
            if payment.status not in ('refunded', 'partially_refunded'):
                payment.status = 'captured'
            payment.failure_code = None
            payment.failure_message = None
            payment.reconciliation_required = False
            if state == 'REFUNDED':
                payment.refunded_amount = payment.amount
                payment.status = 'refunded'
            elif state == 'PARTIALLY_REFUNDED':
                payment.status = 'partially_refunded'
                # Refund notifications supply the individually verified refund amounts.
                if payment.refunded_amount == ZERO:
                    payment.failure_code = 'REFUND_REVIEW'
                    payment.failure_message = 'Partial refund reported; awaiting verified refund amounts.'
                    payment.reconciliation_required = True
            if not booking.ready_for_payment or booking.trip.status in ('cancelled', 'completed'):
                payment.failure_code = 'BOOKING_CHANGED'
                payment.failure_message = 'Payment received for a reservation whose fulfillment state changed. Review required.'
                payment.reconciliation_required = True
        elif not payment.paid_at:
            if state in ('DECLINED', 'DENIED', 'FAILED'):
                failure(payment, PayPalError('REVIEW_REQUIRED', uncertain=False))
            else:
                payment.status = 'pending'
                payment.reconciliation_required = True
        return
    if payment.paid_at:
        return
    state = order.get('status')
    if state == 'COMPLETED':
        raise PayPalError('INVALID_PROVIDER_RESPONSE')
    if state in ('CREATED', 'SAVED', 'PAYER_ACTION_REQUIRED', 'APPROVED'):
        payment.status = 'approved' if state == 'APPROVED' else 'created'
        if payment.failure_code not in BLOCKING:
            payment.failure_code = None
            payment.failure_message = None
            payment.reconciliation_required = False
    elif state == 'VOIDED':
        failure(payment, PayPalError('REVIEW_REQUIRED', uncertain=False))
    else:
        raise PayPalError('INVALID_PROVIDER_RESPONSE')


def create_order(db, token, payload, paypal):
    with db.begin():
        booking = token_booking(db, token, lock=True)
        payment = payment_for(db, booking, lock=True)
        require_eligible(booking, payment)
        paypal.require_configuration()
        if payment is None:
            previous = db.scalar(select(Payment.id).where(Payment.idempotency_key == str(payload.idempotency_key)))
            if previous:
                raise HTTPException(409, 'Payment request key is already in use')
            payment = Payment(trip_id=booking.trip_id, reservation_id=booking.id, amount=booking.retail_total,
                currency='USD', payment_method='paypal', provider='paypal', provider_environment='sandbox', status='pending',
                idempotency_key=str(payload.idempotency_key), capture_request_id=str(uuid4()), external_reference=str(uuid4()), create_started_at=utcnow())
            db.add(payment)
            db.flush()
    # Stable intent/request IDs survive a crash or lost provider response.
    with db.begin():
        booking = token_booking(db, token, lock=True)
        payment = payment_for(db, booking, lock=True)
        require_eligible(booking, payment)
        if payment.failure_code in BLOCKING:
            return public_payment(booking, payment, paypal)
        try:
            if payment.provider_order_id:
                merge_order(payment, paypal.get_order(payment.provider_order_id), booking)
            elif not payment.create_started_at or utcnow() - aware(payment.create_started_at) > RETRY_WINDOW:
                raise PayPalError('REVIEW_REQUIRED', uncertain=False)
            else:
                created = paypal.create_order(payment)
                payment.provider_order_id = provider_id(created.get('id'))
                merge_order(payment, paypal.get_order(payment.provider_order_id), booking)
        except PayPalError as error:
            failure(payment, error)
        db.flush()
        return public_payment(booking, payment, paypal)


def capture_order(db, token, order_id, paypal):
    with db.begin():
        booking = token_booking(db, token, lock=True)
        payment = payment_for(db, booking, lock=True)
        if not payment or payment.provider_order_id != order_id:
            raise HTTPException(404, 'Payment order not found')
        if payment.paid_at:
            return public_payment(booking, payment, paypal)
        require_eligible(booking, payment)
        paypal.require_configuration()
        if not payment.capture_started_at:
            payment.capture_started_at = utcnow()
    with db.begin():
        booking = token_booking(db, token, lock=True)
        payment = payment_for(db, booking, lock=True)
        if payment.paid_at:
            return public_payment(booking, payment, paypal)
        require_eligible(booking, payment)
        try:
            merge_order(payment, paypal.get_order(payment.provider_order_id), booking)
            if not payment.paid_at and not payment.provider_capture_id:
                if payment.failure_code in BLOCKING or utcnow() - aware(payment.capture_started_at) > RETRY_WINDOW:
                    raise PayPalError('REVIEW_REQUIRED', uncertain=False)
                if payment.status != 'approved':
                    raise PayPalError('ORDER_NOT_APPROVED', uncertain=False)
                try:
                    captured = paypal.capture_order(payment)
                    if provider_id(captured.get('id')) != payment.provider_order_id:
                        raise PayPalError('ORDER_MISMATCH')
                except PayPalError as error:
                    if error.code != 'ORDER_ALREADY_CAPTURED':
                        raise
                # POST can return a minimal representation. Read the complete
                # authenticated order before validating ownership and money.
                merge_order(payment, paypal.get_order(payment.provider_order_id), booking)
        except PayPalError as error:
            failure(payment, error)
        db.flush()
        return public_payment(booking, payment, paypal)


def cancel_checkout(db, token, order_id, paypal):
    with db.begin():
        booking = token_booking(db, token, lock=True)
        payment = payment_for(db, booking, lock=True)
        if not payment or payment.provider_order_id != order_id:
            raise HTTPException(404, 'Payment order not found')
        if not payment.paid_at and not payment.capture_started_at and not payment.provider_capture_id:
            payment.status = 'cancelled'
        # Keep the same provider order; cancelling a popup is not provider voiding.
        return public_payment(booking, payment, paypal)


def reconcile(db, paypal, *, token=None, booking_id=None):
    from .booking_service import get_booking
    with db.begin():
        booking = token_booking(db, token, lock=True) if token else get_booking(db, booking_id, lock=True)
        payment = payment_for(db, booking, lock=True)
        if payment and payment.provider_order_id:
            try:
                merge_order(payment, paypal.get_order(payment.provider_order_id), booking)
            except PayPalError as error:
                failure(payment, error)
        db.flush()
        return public_payment(booking, payment, paypal) if token else booking_payment(db, booking, paypal)


def list_payments(db, status=None):
    query = payment_query()
    groups = {'pending': ('pending', 'created', 'approved'), 'paid': ('captured',), 'failed': ('failed',), 'refunded': ('refunded', 'partially_refunded')}
    if status:
        query = query.where(Payment.status.in_(groups[status]))
    return [present_payment(p) for p in db.scalars(query.order_by(Payment.created_at.desc(), Payment.id.desc())).all()]


def webhook(db, paypal, headers, event):
    from .booking_service import get_booking
    if not paypal.verify_webhook(headers, event):
        raise HTTPException(400, 'Invalid PayPal webhook signature')
    event_id, kind, resource = event.get('id'), event.get('event_type'), event.get('resource', {})
    if not isinstance(event_id, str) or not 1 <= len(event_id) <= 100 or not isinstance(kind, str) or len(kind) > 100 or not isinstance(resource, dict):
        raise HTTPException(400, 'Invalid webhook event')
    with db.begin():
        if db.scalar(select(PaymentWebhookEvent.id).where(PaymentWebhookEvent.provider_event_id == event_id)):
            return {'received': True}
        relevant = kind in ('CHECKOUT.ORDER.APPROVED', 'CHECKOUT.ORDER.COMPLETED', 'PAYMENT.CAPTURE.COMPLETED',
                            'PAYMENT.CAPTURE.PENDING', 'PAYMENT.CAPTURE.FAILED', 'PAYMENT.CAPTURE.DENIED', 'PAYMENT.CAPTURE.DECLINED', 'PAYMENT.CAPTURE.REFUNDED', 'PAYMENT.CAPTURE.REVERSED')
        if not relevant:
            db.add(PaymentWebhookEvent(provider_event_id=event_id, event_type=kind, outcome='ignored'))
            return {'received': True}
        resource_id = provider_id(resource.get('id'))
        order_id = resource_id if kind.startswith('CHECKOUT.ORDER.') else resource.get('supplementary_data', {}).get('related_ids', {}).get('order_id')
        # Refund notifications often use the refund as resource, linked to capture.
        capture_id = None
        refund = None
        if kind == 'PAYMENT.CAPTURE.REFUNDED':
            refund = paypal.get_refund(resource_id)
            if refund.get('id') != resource_id or refund.get('status') != 'COMPLETED':
                raise HTTPException(503, 'Refund is not yet reconciled; retry notification')
            for link in refund.get('links', []):
                match = re.fullmatch(r'https://api-m\.(?:sandbox\.)?paypal\.com/v2/payments/captures/([A-Za-z0-9_-]+)', link.get('href', ''))
                if link.get('rel') == 'up' and match:
                    capture_id = match.group(1)
            if not capture_id:
                capture_id = refund.get('supplementary_data', {}).get('related_ids', {}).get('capture_id')
            if not capture_id:
                raise HTTPException(503, 'Refund capture link is not yet available')
            capture = paypal.get_capture(capture_id)
            order_id = capture.get('supplementary_data', {}).get('related_ids', {}).get('order_id')
        if not order_id:
            # Capture detail is fetched from the authenticated merchant API.
            capture = paypal.get_capture(resource_id)
            order_id = capture.get('supplementary_data', {}).get('related_ids', {}).get('order_id')
        order = paypal.get_order(provider_id(order_id))
        units = order.get('purchase_units', [])
        reference = units[0].get('custom_id') if len(units) == 1 else None
        payment = db.scalar(select(Payment).where(Payment.provider_order_id == order_id))
        if payment is None and reference:
            payment = db.scalar(select(Payment).where(Payment.external_reference == reference, Payment.provider == 'paypal'))
        if payment is None:
            db.add(PaymentWebhookEvent(provider_event_id=event_id, event_type=kind, resource_id=resource_id, outcome='unrelated'))
            return {'received': True}
        booking = get_booking(db, payment.reservation_id, lock=True)
        payment = payment_for(db, booking, lock=True)
        # Re-check after waiting for concurrent capture/webhook writers.
        if db.scalar(select(PaymentWebhookEvent.id).where(PaymentWebhookEvent.provider_event_id == event_id)):
            return {'received': True}
        order = paypal.get_order(order_id)
        merge_order(payment, order, booking)
        if refund:
            if capture_id != payment.provider_capture_id:
                raise PayPalError('CAPTURE_MISMATCH')
            amount = money(refund.get('amount'), payment.currency)
            previous = db.scalar(select(PaymentRefund).where(PaymentRefund.provider_refund_id == resource_id))
            if previous and (previous.payment_id != payment.id or previous.amount != amount):
                raise PayPalError('AMOUNT_MISMATCH')
            if not previous:
                if amount <= ZERO:
                    raise PayPalError('AMOUNT_MISMATCH')
                db.add(PaymentRefund(payment_id=payment.id, provider_refund_id=resource_id, amount=amount, currency=payment.currency))
                db.flush()
            total = db.scalar(select(func.sum(PaymentRefund.amount)).where(PaymentRefund.payment_id == payment.id)) or ZERO
            if total > payment.amount:
                raise PayPalError('AMOUNT_MISMATCH')
            payment.refunded_amount = max(payment.refunded_amount, total)
            payment.status = 'refunded' if payment.refunded_amount == payment.amount else 'partially_refunded'
            if payment.failure_code == 'REFUND_REVIEW':
                payment.failure_code = None
                payment.failure_message = None
                payment.reconciliation_required = False
        if kind == 'PAYMENT.CAPTURE.REVERSED':
            payment.reconciliation_required = True
            payment.failure_code = 'REVIEW_REQUIRED'
            payment.failure_message = 'PayPal reported a reversal. Review this payment before further action.'
        db.add(PaymentWebhookEvent(provider_event_id=event_id, event_type=kind, payment_id=payment.id, resource_id=resource_id, outcome='applied'))
        db.flush()
        return {'received': True}
