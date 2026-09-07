from __future__ import annotations

from datetime import datetime, time
from decimal import Decimal
from typing import List

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, JSON, Numeric, String, Text, Time, UniqueConstraint, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = (CheckConstraint('email = lower(trim(email))', name='ck_customers_normalized_email'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    preferred_contact_method: Mapped[str | None] = mapped_column(String(30), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)

    travelers: Mapped[List['Traveler']] = relationship('Traveler', back_populates='customer', cascade='all, delete-orphan')
    trips: Mapped[List['Trip']] = relationship('Trip', back_populates='customer', cascade='all, delete-orphan')


class Traveler(Base):
    __tablename__ = 'travelers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[Date | None] = mapped_column(Date, nullable=True)
    traveler_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)

    customer: Mapped['Customer'] = relationship('Customer', back_populates='travelers')


class Supplier(Base):
    __tablename__ = 'suppliers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    supplier_type: Mapped[str] = mapped_column(String(80), nullable=False)
    contact_name: Mapped[str | None] = mapped_column(String(140), nullable=True)
    email: Mapped[str | None] = mapped_column(String(180), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(60), nullable=True)
    website: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)

    products: Mapped[List['Product']] = relationship('Product', back_populates='supplier', cascade='all, delete-orphan')


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint('retail_price >= 0', name='ck_products_retail_nonnegative'),
        CheckConstraint('supplier_cost >= 0', name='ck_products_cost_nonnegative'),
        CheckConstraint('minimum_age IS NULL OR minimum_age >= 0', name='ck_products_age_nonnegative'),
        Index('ix_products_public', 'product_type', 'active', 'featured'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey('suppliers.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(220), nullable=False)
    slug: Mapped[str] = mapped_column(String(240), nullable=False, unique=True)
    short_description: Mapped[str] = mapped_column(String(500), default='', server_default='', nullable=False)
    category: Mapped[str] = mapped_column(String(80), default='Uncategorized', server_default='Uncategorized', nullable=False)
    duration: Mapped[str] = mapped_column(String(120), default='', server_default='', nullable=False)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('false'), nullable=False)
    location: Mapped[str | None] = mapped_column(String(220), nullable=True)
    minimum_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(80), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    product_type: Mapped[str] = mapped_column(String(80), nullable=False)
    retail_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    supplier_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)

    supplier: Mapped['Supplier'] = relationship('Supplier', back_populates='products')
    availability: Mapped[List['Availability']] = relationship('Availability', back_populates='product', cascade='all, delete-orphan')
    reservations: Mapped[List['Reservation']] = relationship('Reservation', back_populates='product', cascade='all, delete-orphan')
    images: Mapped[List['ProductImage']] = relationship('ProductImage', back_populates='product', cascade='all, delete-orphan', order_by='(ProductImage.sort_order, ProductImage.id)')

    @property
    def gross_margin(self) -> Decimal:
        return self.retail_price - self.supplier_cost

    @property
    def primary_image(self) -> ProductImage | None:
        return next((image for image in self.images if image.is_primary), None)


class ProductImage(Base):
    __tablename__ = 'product_images'
    __table_args__ = (
        CheckConstraint('sort_order >= 0', name='ck_product_images_order_nonnegative'),
        Index('ix_product_images_order', 'product_id', 'sort_order', 'id'),
        Index('uq_product_images_primary', 'product_id', unique=True,
              postgresql_where=text('is_primary'), sqlite_where=text('is_primary')),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    image_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    alt_text: Mapped[str] = mapped_column(String(300), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default='0', nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('false'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)
    product: Mapped['Product'] = relationship('Product', back_populates='images')


class Trip(Base):
    __tablename__ = 'trips'
    __table_args__ = (
        CheckConstraint('party_size > 0', name='ck_trips_party_size'),
        CheckConstraint('start_date IS NULL OR end_date IS NULL OR end_date >= start_date', name='ck_trips_dates'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    reference: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    start_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    party_size: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default='1')
    status: Mapped[str] = mapped_column(String(60), nullable=False, default='inquiry', server_default='inquiry')
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)

    customer: Mapped['Customer'] = relationship('Customer', back_populates='trips')
    reservations: Mapped[List['Reservation']] = relationship('Reservation', back_populates='trip', cascade='all, delete-orphan')
    payments: Mapped[List['Payment']] = relationship('Payment', back_populates='trip', cascade='all, delete-orphan')
    traveler_links: Mapped[List['TripTraveler']] = relationship('TripTraveler', cascade='all, delete-orphan', order_by='TripTraveler.position')


class TripTraveler(Base):
    __tablename__ = 'trip_travelers'
    trip_id: Mapped[int] = mapped_column(ForeignKey('trips.id', ondelete='CASCADE'), primary_key=True)
    traveler_id: Mapped[int] = mapped_column(ForeignKey('travelers.id', ondelete='CASCADE'), primary_key=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    traveler: Mapped['Traveler'] = relationship('Traveler')


class Reservation(Base):
    __tablename__ = 'reservations'
    __table_args__ = (
        CheckConstraint('quantity > 0', name='ck_reservations_quantity'),
        Index('ix_reservations_inbox', 'status', 'created_at'),
        CheckConstraint("availability_status IN ('unknown','available','limited','unavailable','closed')", name='ck_reservation_availability_status'),
        CheckConstraint("supplier_confirmation_status IN ('not_requested','awaiting_supplier','confirmed','declined','alternative_offered')", name='ck_reservation_supplier_status'),
        CheckConstraint("supplier_confirmation_status != 'confirmed' OR availability_status = 'available'", name='ck_reservation_confirmation_available'),
        CheckConstraint('version > 0', name='ck_reservation_version'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey('trips.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    reservation_date: Mapped[Date] = mapped_column(Date, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(80), nullable=False, default='new', server_default='new')
    supplier_id: Mapped[int] = mapped_column(ForeignKey('suppliers.id'), nullable=False)
    availability_status: Mapped[str] = mapped_column(String(30), default='unknown', server_default='unknown', nullable=False)
    supplier_confirmation_status: Mapped[str] = mapped_column(String(30), default='not_requested', server_default='not_requested', nullable=False)
    supplier_confirmation_reference: Mapped[str | None] = mapped_column(String(200), nullable=True)
    supplier_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    supplier_contacted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    supplier_response_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, server_default='1', nullable=False)
    payment_token_hash: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    payment_token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    payment_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    requested_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    customer_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    internal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tour_name_snapshot: Mapped[str | None] = mapped_column(String(220), nullable=True)
    contact_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    submission_key: Mapped[str | None] = mapped_column(String(36), nullable=True, unique=True)
    submission_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    submission_receipt: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    supplier_unit_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)

    trip: Mapped['Trip'] = relationship('Trip', back_populates='reservations')
    product: Mapped['Product'] = relationship('Product', back_populates='reservations')
    supplier: Mapped['Supplier'] = relationship('Supplier')
    payment: Mapped['Payment | None'] = relationship('Payment', back_populates='reservation', uselist=False)
    supplier_events: Mapped[List['SupplierConfirmationEvent']] = relationship('SupplierConfirmationEvent', back_populates='reservation', order_by='SupplierConfirmationEvent.id')

    @property
    def ready_for_payment(self) -> bool:
        return self.status == 'confirmed' and self.supplier_confirmation_status == 'confirmed' and self.availability_status == 'available'

    @property
    def needs_attention(self) -> bool:
        return self.status not in ('cancelled', 'completed') and (self.status in ('new', 'contacted', 'pending_supplier') or self.supplier_confirmation_status != 'confirmed')

    @property
    def gross_margin(self) -> Decimal:
        return (self.unit_price - self.supplier_unit_cost) * self.quantity

    @property
    def retail_total(self) -> Decimal:
        return self.unit_price * self.quantity


class Payment(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        CheckConstraint('amount >= 0', name='ck_payment_amount'),
        CheckConstraint('refunded_amount >= 0 AND refunded_amount <= amount', name='ck_payment_refunded_amount'),
        CheckConstraint("status IN ('pending','created','approved','captured','failed','cancelled','refunded','partially_refunded')", name='ck_payment_status'),
        CheckConstraint("provider != 'paypal' OR (reservation_id IS NOT NULL AND currency = 'USD' AND provider_environment = 'sandbox' AND amount > 0)", name='ck_payment_paypal_scope'),
        Index('ix_payment_status_created', 'status', 'created_at'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey('trips.id'), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    reservation_id: Mapped[int | None] = mapped_column(ForeignKey('reservations.id'), unique=True, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default='USD', server_default='USD', nullable=False)
    provider: Mapped[str] = mapped_column(String(30), default='manual', server_default='manual', nullable=False)
    provider_environment: Mapped[str | None] = mapped_column(String(20), nullable=True)
    provider_order_id: Mapped[str | None] = mapped_column(String(80), unique=True, nullable=True)
    provider_capture_id: Mapped[str | None] = mapped_column(String(80), unique=True, nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(36), unique=True, nullable=True)
    capture_request_id: Mapped[str | None] = mapped_column(String(36), unique=True, nullable=True)
    create_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    capture_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_code: Mapped[str | None] = mapped_column(String(80), nullable=True)
    failure_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    refunded_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'), server_default='0', nullable=False)
    reconciliation_required: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('false'), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(80), nullable=False, default='pending')
    external_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)

    trip: Mapped['Trip'] = relationship('Trip', back_populates='payments')
    reservation: Mapped['Reservation | None'] = relationship('Reservation', back_populates='payment')


class Availability(Base):
    __tablename__ = 'availabilities'
    __table_args__ = (
        UniqueConstraint('product_id', 'date', name='uq_availability_product_date'),
        CheckConstraint("status IN ('unknown','available','limited','unavailable','closed')", name='ck_availability_status'),
        CheckConstraint("source IN ('manual','supplier','api','inventory')", name='ck_availability_source'),
        CheckConstraint('capacity IS NULL OR capacity >= 0', name='ck_availability_capacity'),
        CheckConstraint('remaining_capacity IS NULL OR remaining_capacity >= 0', name='ck_availability_remaining'),
        CheckConstraint('capacity IS NULL OR remaining_capacity IS NULL OR remaining_capacity <= capacity', name='ck_availability_remaining_capacity'),
        CheckConstraint("status NOT IN ('available','limited') OR ((capacity IS NULL OR capacity > 0) AND (remaining_capacity IS NULL OR remaining_capacity > 0))", name='ck_availability_positive_inventory'),
        CheckConstraint('version > 0', name='ck_availability_version'),
        Index('ix_availability_date_status', 'date', 'status'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    remaining_capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(80), nullable=False, default='unknown', server_default='unknown')
    source: Mapped[str] = mapped_column(String(30), nullable=False, default='manual', server_default='manual')
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, server_default='1', nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)

    product: Mapped['Product'] = relationship('Product', back_populates='availability')


class SupplierConfirmationEvent(Base):
    __tablename__ = 'supplier_confirmation_events'
    __table_args__ = (
        UniqueConstraint('reservation_id', 'command_id', name='uq_supplier_event_command'),
        CheckConstraint("event_type IN ('contacted','follow_up','confirmed','declined','alternative_offered','availability_checked','note')", name='ck_supplier_event_type'),
        CheckConstraint("contact_method IS NULL OR contact_method IN ('phone','email','whatsapp','supplier_portal','other')", name='ck_supplier_event_method'),
        Index('ix_supplier_event_timeline', 'reservation_id', 'id'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reservation_id: Mapped[int] = mapped_column(ForeignKey('reservations.id'), nullable=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey('suppliers.id'), nullable=False)
    event_type: Mapped[str] = mapped_column(String(30), nullable=False)
    contact_method: Mapped[str | None] = mapped_column(String(30), nullable=True)
    operator_identifier: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    reservation_status: Mapped[str] = mapped_column(String(80), nullable=False)
    availability_status: Mapped[str] = mapped_column(String(30), nullable=False)
    reference: Mapped[str | None] = mapped_column(String(200), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    alternative_product_id: Mapped[int | None] = mapped_column(ForeignKey('products.id'), nullable=True)
    alternative_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    alternative_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), nullable=False)
    command_id: Mapped[str] = mapped_column(String(36), nullable=False)
    command_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    reservation: Mapped['Reservation'] = relationship('Reservation', back_populates='supplier_events')
    supplier: Mapped['Supplier'] = relationship('Supplier')
    alternative_product: Mapped['Product | None'] = relationship('Product')


class PaymentWebhookEvent(Base):
    __tablename__ = 'payment_webhook_events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_event_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payment_id: Mapped[int | None] = mapped_column(ForeignKey('payments.id'), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    outcome: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PaymentRefund(Base):
    __tablename__ = 'payment_refunds'
    __table_args__ = (CheckConstraint('amount > 0', name='ck_payment_refund_positive'),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey('payments.id'), nullable=False, index=True)
    provider_refund_id: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
