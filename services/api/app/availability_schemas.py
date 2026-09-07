from datetime import date as Date, datetime, time, timedelta
from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, Field, field_validator, model_validator
from .inventory_schemas import Input, ReadModel, SupplierRead
from .availability_rules import utcnow

AvailabilityStatus = Literal['unknown', 'available', 'limited', 'unavailable', 'closed']
AvailabilitySource = Literal['manual', 'supplier', 'api', 'inventory']
EventType = Literal['contacted', 'follow_up', 'confirmed', 'declined', 'alternative_offered', 'availability_checked', 'note']


def not_future(value):
    if value and value > utcnow() + timedelta(minutes=5):
        raise ValueError('Checked/contact time cannot be in the future (5 minute clock tolerance)')
    return value


class AvailabilityInput(Input):
    product_id: int = Field(gt=0)
    date: Date
    status: AvailabilityStatus = 'unknown'
    source: AvailabilitySource = 'manual'
    capacity: int | None = Field(default=None, ge=0, le=2147483647, strict=True)
    remaining_capacity: int | None = Field(default=None, ge=0, le=2147483647, strict=True)
    notes: str | None = Field(default=None, max_length=10000)
    last_checked_at: AwareDatetime | None = None

    _checked = field_validator('last_checked_at')(not_future)

    @model_validator(mode='after')
    def capacity_valid(self):
        if self.capacity is not None and self.remaining_capacity is not None and self.remaining_capacity > self.capacity:
            raise ValueError('Remaining capacity cannot exceed capacity')
        if self.status in ('available', 'limited') and (self.capacity == 0 or self.remaining_capacity == 0):
            raise ValueError('Zero capacity cannot be marked available or limited')
        if self.status != 'unknown' and self.last_checked_at is None:
            raise ValueError('Record when known availability was checked')
        return self


class AvailabilityUpdate(AvailabilityInput):
    expected_version: int = Field(ge=1)


class AvailabilityRead(ReadModel):
    id: int
    product_id: int
    tour_name: str
    supplier_id: int
    supplier_name: str
    date: Date
    status: AvailabilityStatus
    source: AvailabilitySource
    capacity: int | None
    remaining_capacity: int | None
    notes: str | None
    last_checked_at: datetime | None
    stale: bool
    version: int
    created_at: datetime
    updated_at: datetime


class PublicAvailability(ReadModel):
    date: Date
    status: AvailabilityStatus
    request_required: Literal[True] = True


class SupplierEventInput(Input):
    command_id: UUID
    expected_version: int = Field(ge=1)
    event_type: EventType
    contact_method: Literal['phone', 'email', 'whatsapp', 'supplier_portal', 'other'] | None = None
    operator_identifier: str | None = Field(default=None, max_length=120)
    occurred_at: AwareDatetime = Field(default_factory=utcnow)
    reference: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=10000)
    availability_status: AvailabilityStatus | None = None
    alternative_product_id: int | None = Field(default=None, gt=0)
    alternative_date: Date | None = None
    alternative_time: time | None = None

    _occurred = field_validator('occurred_at')(not_future)

    @model_validator(mode='after')
    def event_fields(self):
        if self.event_type in ('contacted', 'follow_up') and not self.contact_method:
            raise ValueError('A contact method is required to record supplier contact')
        if self.event_type in ('availability_checked',) and self.availability_status is None:
            raise ValueError('Select the reservation availability status')
        if self.event_type == 'confirmed' and self.availability_status not in (None, 'available'):
            raise ValueError('Supplier confirmation requires available reservation availability')
        if self.event_type == 'declined' and self.availability_status not in (None, 'unavailable'):
            raise ValueError('Supplier decline requires unavailable reservation availability')
        if self.event_type not in ('availability_checked', 'confirmed', 'declined') and self.availability_status is not None:
            raise ValueError('Use the availability check action to change availability')
        alternatives = (self.alternative_product_id, self.alternative_date, self.alternative_time)
        if self.event_type != 'alternative_offered' and any(value is not None for value in alternatives):
            raise ValueError('Alternative details require an alternative offered event')
        if self.event_type == 'alternative_offered' and not (any(value is not None for value in alternatives) or self.notes):
            raise ValueError('Describe the alternative or provide another tour/date/time')
        if self.event_type == 'note' and not self.notes:
            raise ValueError('A note is required')
        if self.alternative_date and self.alternative_date < utcnow().date():
            raise ValueError('Alternative date cannot be in the past')
        if self.alternative_time and self.alternative_time.tzinfo:
            raise ValueError('Alternative time must be Costa Rica local time without an offset')
        return self


class SupplierEventRead(ReadModel):
    actor_user_id: int | None = None
    actor_display_name: str | None = None
    id: int
    supplier_id: int
    event_type: str
    contact_method: str | None
    operator_identifier: str | None
    status: str
    reservation_status: str
    availability_status: str
    reference: str | None
    notes: str | None
    alternative_product_id: int | None
    alternative_tour_name: str | None
    alternative_date: Date | None
    alternative_time: time | None
    occurred_at: datetime
    created_at: datetime


class ConfirmationRead(ReadModel):
    supplier: SupplierRead
    availability_status: AvailabilityStatus
    supplier_confirmation_status: str
    supplier_confirmation_reference: str | None
    supplier_contacted_at: datetime | None
    supplier_confirmed_at: datetime | None
    supplier_response_notes: str | None
    ready_for_payment: bool
    needs_attention: bool
    version: int
    product_availability: AvailabilityRead | None
    supplier_events: list[SupplierEventRead]
