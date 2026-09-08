from datetime import date, time
from decimal import Decimal
from typing import Annotated, Literal
from urllib.parse import urlsplit
from pydantic import AwareDatetime, Field, field_validator, model_validator
from .inventory_schemas import Input
Money=Annotated[Decimal,Field(ge=0,max_digits=12,decimal_places=2)]

class TransportInput(Input):
    expected_version: int|None=Field(default=None,ge=1)
    @field_validator('source_url',check_fields=False)
    @classmethod
    def validate_source_url(cls,v):
        if v is not None:
            u=urlsplit(v)
            if u.scheme!='https' or not u.hostname or u.username or u.password or u.query or u.fragment: raise ValueError('Use a stable HTTPS source URL without credentials or query strings')
        return v

class NodeInput(TransportInput):
    name: str=Field(min_length=1,max_length=160)
    slug: str=Field(pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$',max_length=180)
    destination_id: int|None=None
    node_type: Literal['airport','city','destination','pickup_zone','hotel','other']
    active: bool=True
    notes: str|None=Field(default=None,max_length=4000)

class RouteInput(TransportInput):
    origin_node_id: int
    destination_node_id: int
    active: bool=True
    estimated_duration_minutes: int|None=Field(default=None,gt=0,le=10080)
    estimated_distance_km: Decimal|None=Field(default=None,gt=0,max_digits=8,decimal_places=2)
    notes: str|None=Field(default=None,max_length=4000)
    review_notes: str|None=Field(default=None,max_length=4000)
    source: Literal['RideCR']='RideCR'
    source_url: str=Field(max_length=2048)
    source_checked_at: AwareDatetime
    @model_validator(mode='after')
    def canonical(self):
        if self.origin_node_id==self.destination_node_id: raise ValueError('Route endpoints must differ')
        if urlsplit(self.source_url).hostname not in ('ridecr.com','www.ridecr.com'): raise ValueError('Canonical routes require official RideCR provenance')
        return self

class ServiceInput(TransportInput):
    supplier_id: int
    route_id: int
    service_type: Literal['shared_shuttle','private_transfer','lake_crossing','other']
    active: bool=True
    booking_method: str=Field(default='manual_vendor_confirmation',min_length=1,max_length=100)
    pickup_notes: str|None=Field(default=None,max_length=4000)
    dropoff_notes: str|None=Field(default=None,max_length=4000)
    luggage_notes: str|None=Field(default=None,max_length=4000)
    child_policy: str|None=Field(default=None,max_length=4000)
    capacity: int|None=Field(default=None,gt=0,le=1000)
    source_url: str|None=Field(default=None,max_length=2048)
    last_verified_at: AwareDatetime|None=None

class ScheduleInput(TransportInput):
    vendor_service_id: int
    departure_time: time
    arrival_time: time|None=None
    estimated_duration_minutes: int|None=Field(default=None,gt=0,le=10080)
    days_of_week: list[Annotated[int,Field(ge=0,le=6)]]=Field(default_factory=list,max_length=7)
    effective_from: date|None=None
    effective_to: date|None=None
    pickup_window_minutes: int|None=Field(default=None,ge=0,le=240)
    seasonal_notes: str|None=Field(default=None,max_length=4000)
    active: bool=True
    source_url: str=Field(max_length=2048)
    last_verified_at: AwareDatetime|None=None
    @model_validator(mode='after')
    def recurrence(self):
        if self.effective_from and self.effective_to and self.effective_to<self.effective_from: raise ValueError('Invalid effective dates')
        if len(set(self.days_of_week))!=len(self.days_of_week): raise ValueError('Duplicate weekdays')
        if any(t and t.tzinfo for t in (self.departure_time,self.arrival_time)): raise ValueError('Use Costa Rica local wall time without an offset')
        return self

class RateInput(TransportInput):
    vendor_service_id: int
    agreement_id: int|None=None
    supersedes_id: int|None=None
    rate_kind: Literal['vendor_rate','public_reference']='vendor_rate'
    unit_basis: Literal['per_person','per_vehicle']='per_person'
    currency: Literal['USD','CRC']='USD'
    vendor_cost: Money|None=None
    vv_retail: Money|None=None
    public_reference_price: Money|None=None
    effective_from: date
    effective_to: date
    notes: str|None=Field(default=None,max_length=4000)
    source_url: str|None=Field(default=None,max_length=2048)
    @field_validator('vendor_cost','vv_retail','public_reference_price',mode='before')
    @classmethod
    def exact_money(cls,v):
        if isinstance(v,float): raise ValueError('Send money as a decimal string')
        return v
    @model_validator(mode='after')
    def boundary(self):
        if self.effective_to<self.effective_from: raise ValueError('Invalid rate dates')
        if self.rate_kind=='public_reference':
            if self.vendor_cost is not None or self.vv_retail is not None or self.public_reference_price is None: raise ValueError('Reference prices are not vendor cost or VV retail')
        elif self.public_reference_price is not None or (self.vendor_cost is None and self.vv_retail is None): raise ValueError('Enter a vendor cost or VV retail; public reference price must be separate')
        return self
