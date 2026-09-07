"""Internal reference data only; never included in public booking schemas."""
from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from urllib.parse import urlsplit

from pydantic import Field, HttpUrl, TypeAdapter, field_validator, model_validator

from .inventory_schemas import Input, ReadModel, Money

ServiceType = Literal['tour', 'transportation', 'hotel']
RelationshipStatus = Literal['prospect', 'contacted', 'rates_requested', 'rates_received', 'negotiating', 'contracted', 'active', 'inactive', 'declined']


class DestinationInput(Input):
    parent_id: int | None = Field(default=None, gt=0)
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=240, pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
    destination_type: Literal['country', 'region', 'destination', 'city', 'zone', 'airport']
    description: str | None = Field(default=None, max_length=10000)
    active: bool = True
    sort_order: int = Field(default=0, ge=0, le=2147483647)


class DestinationRead(DestinationInput, ReadModel):
    id: int
    created_at: datetime
    updated_at: datetime


class DestinationLinks(Input):
    destination_ids: list[int] = Field(max_length=100)

    @field_validator('destination_ids')
    @classmethod
    def unique_ids(cls, values):
        if any(v <= 0 for v in values) or len(set(values)) != len(values):
            raise ValueError('Choose distinct positive destination IDs')
        return values


class SupplierFoundation(Input):
    relationship_status: RelationshipStatus
    service_types: list[ServiceType] = Field(max_length=3)

    @field_validator('service_types')
    @classmethod
    def unique_services(cls, values):
        if len(set(values)) != len(values):
            raise ValueError('Choose each service type once')
        return values


class AgreementInput(Input):
    title: str = Field(min_length=1, max_length=200)
    effective_from: date
    effective_to: date | None = None
    currency: Literal['USD', 'CRC'] = 'USD'
    status: Literal['draft', 'in_review', 'approved', 'expired', 'terminated'] = 'draft'
    notes: str | None = Field(default=None, max_length=10000)

    @model_validator(mode='after')
    def dates(self):
        if self.effective_to and self.effective_to < self.effective_from:
            raise ValueError('Agreement end must be on or after its start')
        return self


class AgreementRead(AgreementInput, ReadModel):
    id: int
    supplier_id: int
    created_at: datetime
    updated_at: datetime


class RateInput(Input):
    product_id: int = Field(gt=0)
    label: str = Field(min_length=1, max_length=200)
    effective_from: date
    effective_to: date
    unit_type: Literal['per_person', 'per_vehicle', 'per_night']
    net_amount: Money
    retail_amount: Money | None = None

    @field_validator('net_amount', 'retail_amount', mode='before')
    @classmethod
    def decimal_only(cls, value):
        if isinstance(value, (float, bool)):
            raise ValueError('Send money as a decimal string')
        return value

    @model_validator(mode='after')
    def dates(self):
        if self.effective_to < self.effective_from:
            raise ValueError('Rate end must be on or after its start')
        return self


class RateRead(RateInput, ReadModel):
    id: int
    agreement_id: int
    created_at: datetime
    updated_at: datetime


class DocumentInput(Input):
    agreement_id: int | None = Field(default=None, gt=0)
    document_type: Literal['contract', 'rate_sheet', 'terms', 'cancellation_policy', 'media_kit']
    title: str = Field(min_length=1, max_length=200)
    external_url: str | None = Field(default=None, max_length=2048)
    storage_key: str | None = Field(default=None, max_length=500, pattern=r'^[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]+)*$')
    effective_date: date | None = None
    expiration_date: date | None = None
    notes: str | None = Field(default=None, max_length=10000)

    @field_validator('external_url')
    @classmethod
    def private_reference(cls, value):
        if value is not None:
            TypeAdapter(HttpUrl).validate_python(value)
            url = urlsplit(value)
            if url.scheme != 'https' or url.username or url.password or url.query or url.fragment:
                raise ValueError('Use a stable HTTPS reference without credentials, query or fragment')
        return value

    @field_validator('storage_key')
    @classmethod
    def logical_key(cls, value):
        if value and any(part in ('.', '..') for part in value.split('/')):
            raise ValueError('Storage keys cannot traverse directories')
        return value

    @model_validator(mode='after')
    def dates(self):
        if self.effective_date and self.expiration_date and self.expiration_date < self.effective_date:
            raise ValueError('Document expiration must be on or after its effective date')
        return self


class DocumentRead(DocumentInput, ReadModel):
    id: int
    supplier_id: int
    created_at: datetime
    updated_at: datetime
