"""Atomic public intake and controlled internal follow-up; no payments/email."""
import hashlib
import json
import secrets
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import case, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from .booking_schemas import BookingReceipt
from .models import Customer, Product, Reservation, SupplierConfirmationEvent, Traveler, Trip, TripTraveler
from .availability_service import present_confirmation

TRANSITIONS = {
    'new': ['contacted', 'cancelled'],
    'contacted': ['cancelled'],
    'pending_supplier': ['contacted', 'cancelled'],
    'confirmed': ['completed', 'cancelled'],
    'cancelled': [], 'completed': [],
}
MESSAGE = 'Your request has been received. Volcan Vacations will review the details and confirm availability before payment is collected. No payment has been taken.'


def new_reference():
    return f"VV-{datetime.now(timezone.utc):%y%m%d}-{secrets.token_hex(6).upper()}"


def create_request(db, payload):
    key = str(payload.idempotency_key)
    canonical = json.dumps(payload.model_dump(mode='json', exclude={'idempotency_key'}), sort_keys=True, separators=(',', ':'))
    fingerprint = hashlib.sha256(canonical.encode()).hexdigest()
    for attempt in range(3):
        try:
            with db.begin():
                previous = db.scalar(select(Reservation).where(Reservation.submission_key == key))
                if previous:
                    if previous.submission_hash != fingerprint:
                        raise HTTPException(409, 'This submission key was already used for different details. Start a new request.')
                    return BookingReceipt.model_validate(previous.submission_receipt)
                product = db.scalar(select(Product).where(Product.slug == payload.tour_slug, Product.active.is_(True), Product.product_type == 'tour').with_for_update())
                if not product:
                    raise HTTPException(404, 'This tour is not currently accepting requests')
                customer = db.scalar(select(Customer).where(Customer.email == payload.customer.email).with_for_update())
                if customer is None:
                    customer = Customer(**payload.customer.model_dump())
                    db.add(customer)
                    db.flush()
                # Email is not proof of ownership: never overwrite an existing
                # customer's identity, notes, or contact details from public input.
                # Preserve this request's submitted contact separately for follow-up.
                trip = Trip(customer_id=customer.id, reference=new_reference(), name='Costa Rica tour request',
                            start_date=payload.start_date, end_date=payload.end_date, party_size=payload.party_size, status='inquiry')
                db.add(trip)
                db.flush()
                for position, participant in enumerate(payload.travelers):
                    matches = db.scalars(select(Traveler).where(
                        Traveler.customer_id == customer.id,
                        func.lower(Traveler.first_name) == participant.first_name.lower(),
                        func.lower(Traveler.last_name) == participant.last_name.lower(),
                        Traveler.date_of_birth == participant.date_of_birth,
                        Traveler.traveler_type == participant.traveler_type,
                    )).all()
                    traveler = matches[0] if len(matches) == 1 else Traveler(customer_id=customer.id, **participant.model_dump())
                    db.add(traveler)
                    db.flush()
                    trip.traveler_links.append(TripTraveler(traveler_id=traveler.id, position=position))
                receipt = BookingReceipt(reference=trip.reference, status='new', tour_name=product.name,
                    requested_date=payload.requested_date, party_size=payload.party_size,
                    customer_name=f'{payload.customer.first_name} {payload.customer.last_name}', message=MESSAGE)
                reservation = Reservation(trip_id=trip.id, product_id=product.id, supplier_id=product.supplier_id, reservation_date=payload.requested_date,
                    requested_time=payload.requested_time, quantity=payload.party_size, status='new',
                    unit_price=product.retail_price, supplier_unit_cost=product.supplier_cost,
                    tour_name_snapshot=product.name, contact_snapshot=payload.customer.model_dump(mode='json'),
                    customer_notes=payload.customer_notes, submission_key=key, submission_hash=fingerprint,
                    submission_receipt=receipt.model_dump(mode='json'))
                db.add(reservation)
                db.flush()
            # Future acknowledgement queue/outbox hook belongs AFTER this commit.
            # No email is sent or claimed in Milestone 3.
            return receipt
        except IntegrityError:
            # Unique reference, email, or idempotency races: retry the entire
            # transaction. The context manager has rolled back every partial row.
            if attempt == 2:
                raise HTTPException(409, 'Unable to complete the request. Retry with the same submission key.')


def booking_query():
    return select(Reservation).options(
        selectinload(Reservation.product).selectinload(Product.availability),
        selectinload(Reservation.product).selectinload(Product.supplier),
        selectinload(Reservation.supplier),
        selectinload(Reservation.supplier_events).selectinload(SupplierConfirmationEvent.alternative_product),
        selectinload(Reservation.trip).selectinload(Trip.customer),
        selectinload(Reservation.trip).selectinload(Trip.traveler_links).selectinload(TripTraveler.traveler),
    )


def get_booking(db, booking_id, lock=False):
    query = booking_query().where(Reservation.id == booking_id)
    reservation = db.scalar(query.with_for_update() if lock else query)
    if reservation is None:
        raise HTTPException(404, 'Booking not found')
    return reservation


def present_booking(reservation):
    return dict(id=reservation.id, reference=reservation.trip.reference, status=reservation.status,
        allowed_statuses=[reservation.status, *TRANSITIONS.get(reservation.status, [])],
        created_at=reservation.created_at, updated_at=reservation.updated_at,
        tour_name=reservation.tour_name_snapshot or reservation.product.name, product_id=reservation.product_id,
        requested_date=reservation.reservation_date, requested_time=reservation.requested_time, quantity=reservation.quantity,
        unit_price=reservation.unit_price, supplier_unit_cost=reservation.supplier_unit_cost,
        retail_total=reservation.retail_total, gross_margin=reservation.gross_margin,
        customer=reservation.trip.customer, submitted_contact=reservation.contact_snapshot,
        travelers=[link.traveler for link in reservation.trip.traveler_links], trip=reservation.trip,
        customer_notes=reservation.customer_notes, internal_notes=reservation.internal_notes,
        **present_confirmation(reservation))


def list_bookings(db, status=None, needs_attention=None, supplier_status=None):
    query = booking_query()
    if status:
        query = query.where(Reservation.status == status)
    if supplier_status:
        query = query.where(Reservation.supplier_confirmation_status == supplier_status)
    actionable = case((Reservation.status.in_(['new', 'contacted', 'pending_supplier']), 0), else_=1)
    return [present_booking(row) for row in db.scalars(query.order_by(actionable, Reservation.created_at.desc(), Reservation.id.desc())).all()
            if needs_attention is None or row.needs_attention == needs_attention]


def update_booking(db, booking_id, payload):
    with db.begin():
        booking = get_booking(db, booking_id, lock=True)
        if payload.expected_version is not None and payload.expected_version != booking.version:
            raise HTTPException(409, 'Booking changed since this page loaded. Reload before saving.')
        if booking.status != payload.expected_status:
            raise HTTPException(409, 'Status changed since this page loaded. Reload before saving.')
        if payload.status != booking.status and payload.status not in TRANSITIONS.get(booking.status, []):
            raise HTTPException(409, 'That status transition is not allowed')
        booking.status = payload.status
        booking.version += 1
        booking.internal_notes = payload.internal_notes
        if payload.trip_status:
            booking.trip.status = payload.trip_status
        # Opening a booking or changing reservation status never auto-confirms a trip.
        booking.trip.updated_at = datetime.now(timezone.utc)
        db.flush()
    return present_booking(get_booking(db, booking_id))
