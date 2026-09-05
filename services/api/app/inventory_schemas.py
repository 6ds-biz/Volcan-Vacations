"""Separate public allowlists from internal input/output contracts."""
from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal
import re

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, TypeAdapter, field_validator

Money = Annotated[Decimal, Field(ge=0, max_digits=12, decimal_places=2)]


class Input(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)


class SupplierInput(Input):
    name: str = Field(min_length=1, max_length=200)
    supplier_type: Literal['tour_operator', 'transportation', 'hotel', 'other'] = 'tour_operator'
    contact_name: str | None = Field(default=None, max_length=140)
    email: str | None = Field(default=None, max_length=180, pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    phone: str | None = Field(default=None, max_length=60)
    website: str | None = Field(default=None, max_length=2048)
    notes: str | None = Field(default=None, max_length=10000)
    active: bool = True

    @field_validator('website')
    @classmethod
    def website_url(cls, value):
        if value is not None:
            parsed = TypeAdapter(HttpUrl).validate_python(value)
            if parsed.username or parsed.password:
                raise ValueError('URLs must not contain credentials')
        return value


class ReadModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SupplierRead(SupplierInput, ReadModel):
    id: int
    created_at: datetime
    updated_at: datetime


class TourInput(Input):
    supplier_id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=220)
    slug: str = Field(min_length=1, max_length=240, pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
    short_description: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=30000)
    product_type: Literal['tour'] = 'tour'
    category: str = Field(min_length=1, max_length=80)
    duration: str = Field(min_length=1, max_length=120)
    retail_price: Money
    supplier_cost: Money
    active: bool = False
    featured: bool = False
    location: str | None = Field(default=None, max_length=220)
    minimum_age: int | None = Field(default=None, ge=0, le=120)
    difficulty: str | None = Field(default=None, max_length=80)

    @field_validator('retail_price', 'supplier_cost', mode='before')
    @classmethod
    def decimal_strings(cls, value):
        if isinstance(value, (float, bool)):
            raise ValueError('Send money as a decimal string, e.g. "85.00"')
        return value


class ImageInput(Input):
    image_url: str = Field(min_length=1, max_length=2048)
    alt_text: str = Field(min_length=1, max_length=300)
    sort_order: int = Field(default=0, ge=0, le=2147483647)
    is_primary: bool = False

    @field_validator('image_url')
    @classmethod
    def safe_url(cls, value):
        # Public-site-relative demo assets or HTTP(S) URLs; never fetched by the API.
        if re.fullmatch(r'/images/[a-zA-Z0-9_/-]+\.(?:webp|png|jpe?g|avif|gif)', value):
            return value
        parsed = TypeAdapter(HttpUrl).validate_python(value)
        if parsed.username or parsed.password:
            raise ValueError('Image URLs must not contain credentials')
        return value


class ImageRead(ReadModel):
    id: int
    image_url: str
    alt_text: str
    sort_order: int
    is_primary: bool
    created_at: datetime
    updated_at: datetime


class PublicTour(ReadModel):
    name: str
    slug: str
    short_description: str
    description: str | None
    category: str
    duration: str
    retail_price: Decimal
    location: str | None
    difficulty: str | None
    minimum_age: int | None
    featured: bool
    primary_image: ImageRead | None
    images: list[ImageRead]


class OpsTour(PublicTour):
    id: int
    supplier_id: int
    supplier: SupplierRead
    supplier_cost: Decimal
    gross_margin: Decimal
    product_type: str
    active: bool
    created_at: datetime
    updated_at: datetime
