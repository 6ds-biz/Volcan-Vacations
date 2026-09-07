from fastapi import APIRouter, Depends
from typing import Literal
from sqlalchemy.orm import Session
from ..database import get_db
from ..booking_schemas import BookingInput, BookingRead, BookingReceipt, BookingUpdate, ReservationStatus
from ..booking_service import create_request, get_booking, list_bookings, present_booking, update_booking
from .ops import private_response

public_router = APIRouter(prefix='/public', tags=['Booking requests'], dependencies=[Depends(private_response)])
ops_router = APIRouter(prefix='/ops', tags=['Internal booking follow-up'], dependencies=[Depends(private_response)])


@public_router.post('/booking-requests', response_model=BookingReceipt, status_code=201)
def submit_request(payload: BookingInput, db: Session = Depends(get_db)):
    return create_request(db, payload)


@ops_router.get('/bookings', response_model=list[BookingRead])
def booking_list(status: ReservationStatus | None = None, needs_attention: bool | None = None,
                 supplier_status: Literal['not_requested', 'awaiting_supplier', 'confirmed', 'declined', 'alternative_offered'] | None = None,
                 db: Session = Depends(get_db)):
    return list_bookings(db, status, needs_attention, supplier_status)


@ops_router.get('/bookings/{booking_id}', response_model=BookingRead)
def booking_detail(booking_id: int, db: Session = Depends(get_db)):
    return present_booking(get_booking(db, booking_id))


@ops_router.put('/bookings/{booking_id}', response_model=BookingRead)
def booking_update(booking_id: int, payload: BookingUpdate, db: Session = Depends(get_db)):
    return update_booking(db, booking_id, payload)
