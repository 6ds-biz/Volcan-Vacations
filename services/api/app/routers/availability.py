"""Internal commands require authenticated Operations capabilities."""
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..availability_schemas import AvailabilityInput, AvailabilityUpdate, AvailabilityRead, AvailabilityStatus, PublicAvailability, SupplierEventInput
from ..availability_service import list_availability, save_availability, public_availability, record_supplier_event, booking_summary
from ..booking_schemas import BookingRead
from ..database import get_db
from .ops import private_response

ops_router = APIRouter(prefix='/ops', tags=['Internal availability'], dependencies=[Depends(private_response)])
public_router = APIRouter(prefix='/public', tags=['Public availability'], dependencies=[Depends(private_response)])


@ops_router.get('/availability', response_model=list[AvailabilityRead])
def availability_list(date_from: date | None = None, date_to: date | None = None,
                      product_id: int | None = Query(None, gt=0), supplier_id: int | None = Query(None, gt=0),
                      status: AvailabilityStatus | None = None, db: Session = Depends(get_db)):
    return list_availability(db, date_from, date_to, product_id, supplier_id, status)


@ops_router.post('/availability', response_model=AvailabilityRead, status_code=201)
def availability_create(payload: AvailabilityInput, db: Session = Depends(get_db)):
    return save_availability(db, payload)


@ops_router.put('/availability/{availability_id}', response_model=AvailabilityRead)
def availability_update(availability_id: int, payload: AvailabilityUpdate, db: Session = Depends(get_db)):
    return save_availability(db, payload, availability_id)


@ops_router.post('/bookings/{booking_id}/supplier-events', response_model=BookingRead)
def supplier_event(booking_id: int, payload: SupplierEventInput, db: Session = Depends(get_db)):
    return record_supplier_event(db, booking_id, payload)


@ops_router.get('/booking-summary', response_model=dict[str, int])
def summary(db: Session = Depends(get_db)):
    return booking_summary(db)


@public_router.get('/tours/{slug}/availability', response_model=PublicAvailability)
def availability_public(slug: str, date: date, db: Session = Depends(get_db)):
    return public_availability(db, slug, date)
