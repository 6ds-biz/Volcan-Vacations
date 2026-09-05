from datetime import date, datetime, time
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import Field, field_validator, model_validator
from .inventory_schemas import Input, ReadModel

ReservationStatus = Literal['new', 'contacted', 'pending_supplier', 'confirmed', 'cancelled', 'completed']
TripStatus = Literal['inquiry', 'planning', 'confirmed', 'completed', 'cancelled']


class ContactInput(Input):
    first_name: str = Field(min_length=1, max_length=120)
    last_name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=3, max_length=180, pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    phone: str | None = Field(default=None, max_length=50)
    preferred_contact_method: Literal['email', 'phone', 'whatsapp'] | None = None

    @field_validator('email')
    @classmethod
    def normalize_email(cls, value):
        return value.strip().lower()

    @model_validator(mode='after')
    def contact_method(self):
        if self.preferred_contact_method in ['phone', 'whatsapp'] and not self.phone:
            raise ValueError('Provide a phone number for phone or WhatsApp contact')
        return self


class TravelerInput(Input):
    first_name: str = Field(min_length=1, max_length=120)
    last_name: str = Field(min_length=1, max_length=120)
    date_of_birth: date | None = None
    traveler_type: Literal['adult', 'child', 'infant', 'unknown'] = 'unknown'

    @field_validator('date_of_birth')
    @classmethod
    def dob_not_future(cls, value):
        if value and value > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return value


class BookingInput(Input):
    idempotency_key: UUID
    tour_slug: str = Field(min_length=1, max_length=240)
    requested_date: date
    requested_time: time | None = None
    customer: ContactInput
    start_date: date | None = None
    end_date: date | None = None
    party_size: int = Field(ge=1, le=50, strict=True)
    travelers: list[TravelerInput] = Field(min_length=1, max_length=50)
    customer_notes: str | None = Field(default=None, max_length=4000)

    @model_validator(mode='after')
    def valid_trip(self):
        if self.requested_date < date.today():
            raise ValueError('Requested date cannot be in the past')
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError('Departure must be on or after arrival')
        if (self.start_date and self.requested_date < self.start_date) or (self.end_date and self.requested_date > self.end_date):
            raise ValueError('Requested date must fall within the supplied trip dates')
        if len(self.travelers) > self.party_size:
            raise ValueError('Traveler count cannot exceed party size')
        identities = [(t.first_name.lower(), t.last_name.lower(), t.date_of_birth) for t in self.travelers]
        if len(identities) != len(set(identities)):
            raise ValueError('Each named traveler must be listed once; contact us if names and birth dates are identical')
        if self.requested_time and self.requested_time.tzinfo is not None:
            raise ValueError('Preferred time must be a local Costa Rica time without a timezone')
        return self


class BookingReceipt(ReadModel):
    reference: str
    status: Literal['new']
    tour_name: str
    requested_date: date
    party_size: int
    customer_name: str
    message: str


class BookingUpdate(Input):
    status: ReservationStatus
    expected_status: str = Field(max_length=80)
    internal_notes: str | None = Field(default=None, max_length=10000)
    trip_status: TripStatus | None = None


class CustomerRead(ReadModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str | None
    preferred_contact_method: str | None
    notes: str | None


class TravelerRead(ReadModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date | None
    traveler_type: str | None


class TripRead(ReadModel):
    id: int
    reference: str
    name: str | None
    start_date: date | None
    end_date: date | None
    party_size: int
    status: str
    notes: str | None


class BookingRead(ReadModel):
    id: int
    reference: str
    status: str
    allowed_statuses: list[str]
    created_at: datetime
    updated_at: datetime
    tour_name: str
    product_id: int
    requested_date: date
    requested_time: time | None
    quantity: int
    unit_price: Decimal
    supplier_unit_cost: Decimal
    retail_total: Decimal
    gross_margin: Decimal
    customer: CustomerRead
    submitted_contact: ContactInput | None
    travelers: list[TravelerRead]
    trip: TripRead
    customer_notes: str | None
    internal_notes: str | None
