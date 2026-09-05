"""Explicit, insert-only booking examples. No startup seeding or email."""
import argparse
from datetime import date, timedelta
from uuid import NAMESPACE_URL, uuid5
from sqlalchemy import select
from .booking_schemas import BookingInput, BookingUpdate
from .booking_service import create_request, update_booking
from .config import settings
from .database import SessionLocal
from .models import Product, Reservation


def seed():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--confirm-demo', action='store_true', required=True)
    parser.parse_args()
    if settings.environment != 'development':
        raise SystemExit('Booking seed refused: ENVIRONMENT must be development.')
    with SessionLocal() as db:
        tour = db.scalar(select(Product).where(Product.slug == 'whitewater-rafting', Product.active.is_(True), Product.product_type == 'tour'))
        if not tour:
            raise SystemExit('Seed inventory first: active whitewater-rafting is required.')
    for status in ['new', 'contacted', 'confirmed', 'cancelled']:
        key = str(uuid5(NAMESPACE_URL, f'volcan-vacations/demo-booking-v1/{status}'))
        with SessionLocal() as db:
            exists = db.scalar(select(Reservation.id).where(Reservation.submission_key == key))
        if exists:
            print(f'Skipped existing demo booking: {status} (no overwrite)')
            continue
        payload = BookingInput.model_validate(dict(idempotency_key=key, tour_slug='whitewater-rafting',
            requested_date=str(date.today() + timedelta(days=30)), party_size=2,
            customer=dict(first_name='DEMO', last_name=f'{status.title()} Visitor', email=f'demo-booking-{status}@example.invalid'),
            travelers=[dict(first_name='DEMO', last_name=f'{status.title()} Visitor', traveler_type='adult'), dict(first_name='DEMO Companion', last_name=status.title(), traveler_type='adult')],
            customer_notes='DEVELOPMENT DEMO ONLY — not a real booking or confirmed supplier offer.'))
        with SessionLocal() as db:
            receipt = create_request(db, payload)
            row_id = db.scalar(select(Reservation.id).where(Reservation.submission_key == key))
            db.rollback()
            update_booking(db, row_id, BookingUpdate(status=status, expected_status='new', internal_notes='DEMO status example only; no supplier was contacted and no email was sent.'))
        print(f'Created DEMO {status}: {receipt.reference}')


if __name__ == '__main__':
    seed()
