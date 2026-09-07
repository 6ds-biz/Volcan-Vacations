from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, Field
from .inventory_schemas import Input, ReadModel

PaymentStatus = Literal['pending', 'created', 'approved', 'captured', 'failed', 'cancelled', 'refunded', 'partially_refunded']


class OrderInput(Input):
    idempotency_key: UUID


class LinkInput(Input):
    expected_version: int = Field(ge=1)
    payment_due_at: AwareDatetime | None = None


class PaymentLink(ReadModel):
    path: str
    expires_at: datetime


class PublicPayment(ReadModel):
    booking_reference: str
    tour: str
    date: date
    party_size: int
    amount: Decimal
    amount_due: Decimal
    amount_paid: Decimal
    currency: str
    provider: Literal['PayPal'] = 'PayPal'
    status: str
    eligible: bool
    checkout_available: bool
    retryable: bool
    message: str
    client_id: str | None
    environment: Literal['sandbox'] = 'sandbox'
    order_id: str | None = None


class OpsPayment(ReadModel):
    id: int
    reservation_id: int | None
    trip_id: int
    booking_reference: str
    customer: str
    tour: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    provider: str
    provider_environment: str | None
    provider_order_id: str | None
    provider_capture_id: str | None
    external_reference: str | None
    failure_code: str | None
    failure_message: str | None
    reconciliation_required: bool
    created_at: datetime
    updated_at: datetime
    paid_at: datetime | None
    refunded_amount: Decimal


class BookingPayment(ReadModel):
    eligible: bool
    label: str
    amount_due: Decimal
    currency: str
    payment_due_at: datetime | None
    overdue: bool
    link_active: bool
    sandbox_configured: bool
    webhook_configured: bool
    payment: OpsPayment | None
