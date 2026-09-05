"""Shared transactional boundary for manual operations and future adapters.

Date availability is a checked snapshot, not an allotment or booking guarantee.
Supplier events affect one reservation, never shared inventory or the whole trip.
"""
import hashlib
import json
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from .availability_rules import aware, is_stale, utcnow
from .models import Availability, Product, Reservation, SupplierConfirmationEvent


def present_availability(row):
    return dict(id=row.id, product_id=row.product_id, tour_name=row.product.name,
                supplier_id=row.product.supplier_id, supplier_name=row.product.supplier.name,
                date=row.date, status=row.status, source=row.source, capacity=row.capacity,
                remaining_capacity=row.remaining_capacity, notes=row.notes,
                last_checked_at=row.last_checked_at, stale=is_stale(row.last_checked_at),
                version=row.version, created_at=row.created_at, updated_at=row.updated_at)


def present_confirmation(booking):
    availability = next((row for row in booking.product.availability if row.date == booking.reservation_date), None)
    events = [dict(id=e.id, supplier_id=e.supplier_id, event_type=e.event_type,
        contact_method=e.contact_method, operator_identifier=e.operator_identifier,
        status=e.status, reservation_status=e.reservation_status, availability_status=e.availability_status,
        reference=e.reference, notes=e.notes, alternative_product_id=e.alternative_product_id,
        alternative_tour_name=e.alternative_product.name if e.alternative_product else None,
        alternative_date=e.alternative_date, alternative_time=e.alternative_time,
        occurred_at=e.occurred_at, created_at=e.created_at) for e in booking.supplier_events]
    return dict(supplier=booking.supplier, availability_status=booking.availability_status,
        supplier_confirmation_status=booking.supplier_confirmation_status,
        supplier_confirmation_reference=booking.supplier_confirmation_reference,
        supplier_contacted_at=booking.supplier_contacted_at, supplier_confirmed_at=booking.supplier_confirmed_at,
        supplier_response_notes=booking.supplier_response_notes, version=booking.version,
        ready_for_payment=booking.ready_for_payment, needs_attention=booking.needs_attention,
        product_availability=present_availability(availability) if availability else None, supplier_events=events)


def availability_query():
    return select(Availability).options(selectinload(Availability.product).selectinload(Product.supplier))


def list_availability(db, date_from=None, date_to=None, product_id=None, supplier_id=None, status=None):
    if date_from and date_to and date_to < date_from:
        raise HTTPException(422, 'End date must be on or after start date')
    query = availability_query().join(Product)
    for condition, value in ((Availability.date >= date_from if date_from else None, date_from),
                             (Availability.date <= date_to if date_to else None, date_to),
                             (Availability.product_id == product_id, product_id),
                             (Product.supplier_id == supplier_id, supplier_id), (Availability.status == status, status)):
        if value is not None:
            query = query.where(condition)
    return [present_availability(row) for row in db.scalars(query.order_by(Availability.date, Availability.product_id)).all()]


def save_availability(db, payload, availability_id=None):
    try:
        with db.begin():
            product = db.scalar(select(Product).where(Product.id == payload.product_id, Product.product_type == 'tour'))
            if not product:
                raise HTTPException(404, 'Tour not found')
            if availability_id is None:
                row = Availability(**payload.model_dump())
                db.add(row)
            else:
                row = db.scalar(select(Availability).where(Availability.id == availability_id).with_for_update())
                if row is None:
                    raise HTTPException(404, 'Availability record not found')
                if row.version != payload.expected_version:
                    raise HTTPException(409, 'Availability changed. Reload before saving.')
                if row.product_id != payload.product_id or row.date != payload.date:
                    raise HTTPException(409, 'A saved availability record cannot be moved to another tour/date. Add a date instead.')
                for key, value in payload.model_dump(exclude={'expected_version'}).items():
                    setattr(row, key, value)
                row.version += 1
            db.flush()
            row_id = row.id
    except IntegrityError:
        raise HTTPException(409, 'This tour/date already exists or the inventory values conflict. Reload and edit the existing date.')
    return present_availability(db.scalar(availability_query().where(Availability.id == row_id)))


def public_availability(db, slug, day):
    product = db.scalar(select(Product).where(Product.slug == slug, Product.active.is_(True), Product.product_type == 'tour'))
    if not product:
        raise HTTPException(404, 'Tour not found')
    row = db.scalar(select(Availability).where(Availability.product_id == product.id, Availability.date == day))
    return dict(date=day, status=row.status if row and not is_stale(row.last_checked_at) else 'unknown', request_required=True)


def record_supplier_event(db, booking_id, payload):
    # Import locally to keep presentation helpers usable by booking_service.
    from .booking_service import get_booking, present_booking
    excluded = {'command_id'}
    if 'occurred_at' not in payload.model_fields_set:
        excluded.add('occurred_at')  # server-generated time must not change an identical retry's fingerprint
    canonical = json.dumps(payload.model_dump(mode='json', exclude=excluded), sort_keys=True, separators=(',', ':'))
    fingerprint = hashlib.sha256(canonical.encode()).hexdigest()
    try:
        with db.begin():
            booking = get_booking(db, booking_id, lock=True)
            previous = next((e for e in booking.supplier_events if e.command_id == str(payload.command_id)), None)
            if previous:
                if previous.command_hash != fingerprint:
                    raise HTTPException(409, 'This action key was used for different details')
                return present_booking(booking)
            if booking.version != payload.expected_version:
                raise HTTPException(409, 'Booking changed. Reload before recording this action.')
            kind = payload.event_type
            if booking.status in ('cancelled', 'completed') and kind != 'note':
                raise HTTPException(409, 'Only timeline notes can be added to a cancelled or completed reservation')
            state_events = [e for e in booking.supplier_events if e.event_type != 'note']
            if kind != 'note' and state_events and aware(payload.occurred_at) < max(aware(e.occurred_at) for e in state_events):
                raise HTTPException(409, 'A state-changing event cannot predate the latest recorded action. Add historical context as a note.')
            if payload.alternative_product_id:
                alternative = db.scalar(select(Product).where(Product.id == payload.alternative_product_id,
                    Product.product_type == 'tour', Product.active.is_(True)))
                if not alternative:
                    raise HTTPException(422, 'Choose an active alternative tour')
            if booking.supplier_confirmation_status == 'confirmed' and kind in ('contacted', 'confirmed', 'declined', 'alternative_offered') and not payload.notes:
                raise HTTPException(409, 'Explain the correction to this supplier confirmation in the notes. Previous confirmation stays in history.')
            if kind == 'contacted':
                if booking.supplier_confirmation_status in ('confirmed', 'declined', 'alternative_offered'):
                    booking.availability_status = 'unknown'
                booking.status = 'pending_supplier'
                booking.supplier_confirmation_status = 'awaiting_supplier'
                booking.supplier_contacted_at = payload.occurred_at
                booking.supplier_confirmation_reference = None
                booking.supplier_confirmed_at = None
            elif kind == 'follow_up':
                if booking.supplier_confirmation_status != 'awaiting_supplier':
                    raise HTTPException(409, 'Record initial supplier contact before a follow-up')
                booking.status = 'pending_supplier'
                booking.supplier_contacted_at = payload.occurred_at
            elif kind == 'confirmed':
                booking.status = 'confirmed'
                booking.availability_status = 'available'
                booking.supplier_confirmation_status = 'confirmed'
                booking.supplier_confirmation_reference = payload.reference
                booking.supplier_confirmed_at = payload.occurred_at
            elif kind in ('declined', 'alternative_offered'):
                booking.status = 'contacted'
                booking.supplier_confirmation_status = kind
                if kind == 'declined':
                    booking.availability_status = 'unavailable'
                booking.supplier_confirmation_reference = None
                booking.supplier_confirmed_at = None
            elif kind == 'availability_checked':
                if booking.supplier_confirmation_status == 'confirmed' and payload.availability_status != 'available':
                    raise HTTPException(409, 'Supplier is confirmed. Record a decline or renewed contact with a corrective note first.')
                if booking.supplier_confirmation_status == 'declined' and payload.availability_status != 'unavailable':
                    raise HTTPException(409, 'Supplier declined this request. Record renewed supplier contact before changing availability.')
                booking.availability_status = payload.availability_status
            if kind in ('confirmed', 'declined', 'alternative_offered'):
                booking.supplier_response_notes = payload.notes
            booking.version += 1
            event = SupplierConfirmationEvent(reservation_id=booking.id, supplier_id=booking.supplier_id,
                event_type=kind, contact_method=payload.contact_method, operator_identifier=payload.operator_identifier,
                status=booking.supplier_confirmation_status, reservation_status=booking.status,
                availability_status=booking.availability_status, reference=payload.reference, notes=payload.notes,
                alternative_product_id=payload.alternative_product_id, alternative_date=payload.alternative_date,
                alternative_time=payload.alternative_time, occurred_at=payload.occurred_at,
                command_id=str(payload.command_id), command_hash=fingerprint)
            db.add(event)
            db.flush()
        db.expire_all()
    except IntegrityError:
        raise HTTPException(409, 'Unable to record this action atomically. Reload before retrying.')
    return present_booking(get_booking(db, booking_id))


def booking_summary(db):
    start = utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    count = lambda *conditions: db.scalar(select(func.count()).select_from(Reservation).where(*conditions))
    active = Reservation.status.notin_(('cancelled', 'completed'))
    attention = (Reservation.status.in_(('new', 'contacted', 'pending_supplier')) | (Reservation.supplier_confirmation_status != 'confirmed'))
    return dict(new_requests=count(Reservation.status == 'new'),
        awaiting_supplier=count(active, Reservation.supplier_confirmation_status == 'awaiting_supplier'),
        confirmed_today=count(Reservation.status == 'confirmed', Reservation.supplier_confirmation_status == 'confirmed',
                              Reservation.supplier_confirmed_at >= start, Reservation.supplier_confirmed_at < start + timedelta(days=1)),
        needs_attention=count(active, attention))
