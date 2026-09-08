from __future__ import annotations

from datetime import date, datetime, time
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
    __table_args__ = (CheckConstraint("relationship_status IN ('prospect','contacted','rates_requested','rates_received','negotiating','contracted','active','inactive','declined')", name='ck_supplier_relationship_status'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    supplier_type: Mapped[str] = mapped_column(String(80), nullable=False)
    relationship_status: Mapped[str] = mapped_column(String(30), default='prospect', server_default='prospect', nullable=False)
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
    assigned_user_id: Mapped[int | None] = mapped_column(ForeignKey('internal_users.id'), nullable=True, index=True)
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
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey('internal_users.id'), nullable=True)
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
    actor: Mapped['InternalUser | None'] = relationship('InternalUser')

    @property
    def actor_display_name(self):
        return self.actor.display_name if self.actor else None


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


# Additive platform foundation. No foundation rate is used by checkout yet.
class FoundationTimestamps:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Destination(FoundationTimestamps, Base):
    __tablename__ = 'destinations'
    __table_args__ = (
        CheckConstraint('parent_id IS NULL OR parent_id != id', name='ck_destination_parent'),
        CheckConstraint("destination_type IN ('country','region','destination','city','zone','airport')", name='ck_destination_type'),
        CheckConstraint('sort_order >= 0', name='ck_destination_sort'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('destinations.id'), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(240), unique=True, nullable=False)
    destination_type: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text('true'), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default='0', nullable=False)
    parent: Mapped['Destination | None'] = relationship('Destination', remote_side='Destination.id', back_populates='children')
    children: Mapped[List['Destination']] = relationship('Destination', back_populates='parent')


class ProductDestination(Base):
    __tablename__ = 'product_destinations'
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), primary_key=True)
    destination_id: Mapped[int] = mapped_column(ForeignKey('destinations.id'), primary_key=True)


class SupplierService(Base):
    __tablename__ = 'supplier_services'
    __table_args__ = (CheckConstraint("service_type IN ('tour','transportation','hotel')", name='ck_supplier_service_type'),)
    supplier_id: Mapped[int] = mapped_column(ForeignKey('suppliers.id'), primary_key=True)
    service_type: Mapped[str] = mapped_column(String(30), primary_key=True)


class SupplierAgreement(FoundationTimestamps, Base):
    __tablename__ = 'supplier_agreements'
    __table_args__ = (
        CheckConstraint('effective_to IS NULL OR effective_to >= effective_from', name='ck_agreement_dates'),
        CheckConstraint("status IN ('draft','in_review','approved','expired','terminated')", name='ck_agreement_status'),
        CheckConstraint("currency IN ('USD','CRC')", name='ck_agreement_currency'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey('suppliers.id'), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    effective_from: Mapped[Date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[Date | None] = mapped_column(Date, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default='USD', server_default='USD', nullable=False)
    status: Mapped[str] = mapped_column(String(30), default='draft', server_default='draft', nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class ProductRate(FoundationTimestamps, Base):
    """Dated fixed-unit commercial reference, not an executable pricing engine."""
    __tablename__ = 'product_rates'
    __table_args__ = (
        CheckConstraint('effective_to >= effective_from', name='ck_product_rate_dates'),
        CheckConstraint('net_amount >= 0 AND (retail_amount IS NULL OR retail_amount >= 0)', name='ck_product_rate_money'),
        CheckConstraint("unit_type IN ('per_person','per_vehicle','per_night')", name='ck_product_rate_unit'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agreement_id: Mapped[int] = mapped_column(ForeignKey('supplier_agreements.id'), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    effective_from: Mapped[Date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[Date] = mapped_column(Date, nullable=False)
    unit_type: Mapped[str] = mapped_column(String(30), nullable=False)
    net_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    retail_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)


class SupplierDocument(FoundationTimestamps, Base):
    __tablename__ = 'supplier_documents'
    __table_args__ = (
        CheckConstraint("document_type IN ('contract','rate_sheet','terms','cancellation_policy','media_kit')", name='ck_supplier_document_type'),
        CheckConstraint('effective_date IS NULL OR expiration_date IS NULL OR expiration_date >= effective_date', name='ck_supplier_document_dates'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey('suppliers.id'), nullable=False, index=True)
    agreement_id: Mapped[int | None] = mapped_column(ForeignKey('supplier_agreements.id'), nullable=True)
    document_type: Mapped[str] = mapped_column(String(30), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    external_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    storage_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    effective_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    expiration_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class InternalUser(FoundationTimestamps, Base):
    __tablename__ = 'internal_users'
    __table_args__ = (
        CheckConstraint("role IN ('owner_admin','operations_partner','staff')", name='ck_internal_user_role'),
        CheckConstraint("dashboard_profile IN ('Owner','Operations','Staff')", name='ck_internal_user_profile'),
        CheckConstraint("appearance IN ('light','dark','system')", name='ck_internal_user_appearance'),
        CheckConstraint('email = lower(trim(email))', name='ck_internal_user_email'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(140), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text('true'), nullable=False)
    dashboard_profile: Mapped[str] = mapped_column(String(30), nullable=False)
    appearance: Mapped[str] = mapped_column(String(10), default='dark', server_default='dark', nullable=False)
    must_change_password: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('false'), nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class InternalSession(Base):
    __tablename__ = 'internal_sessions'
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('internal_users.id'), nullable=False, index=True)
    csrf_token: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)


class LoginGuard(Base):
    __tablename__ = 'internal_login_guards'
    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0, server_default='0', nullable=False)
    window_started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class OpsTask(FoundationTimestamps, Base):
    __tablename__ = 'ops_tasks'
    __table_args__ = (
        CheckConstraint("status IN ('open','in_progress','waiting','completed','cancelled')", name='ck_ops_task_status'),
        CheckConstraint("priority IN ('low','normal','high','urgent')", name='ck_ops_task_priority'),
        CheckConstraint("source IN ('manual','system_generated')", name='ck_ops_task_source'),
        CheckConstraint("queue_role IN ('operations','owner_admin')", name='ck_ops_task_queue'),
        CheckConstraint("(related_entity_type IS NULL AND related_entity_id IS NULL) OR (related_entity_type IN ('booking','supplier','tour','payment','availability','agreement','customer','transport_route') AND related_entity_id IS NOT NULL AND related_entity_id > 0)", name='ck_ops_task_related'),
        CheckConstraint('version > 0', name='ck_ops_task_version'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    assigned_user_id: Mapped[int | None] = mapped_column(ForeignKey('internal_users.id'), nullable=True, index=True)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey('internal_users.id'), nullable=True)
    completed_by_user_id: Mapped[int | None] = mapped_column(ForeignKey('internal_users.id'), nullable=True)
    related_entity_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    related_entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    priority: Mapped[str] = mapped_column(String(20), default='normal', server_default='normal', nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='open', server_default='open', nullable=False)
    source: Mapped[str] = mapped_column(String(30), default='manual', server_default='manual', nullable=False)
    queue_role: Mapped[str] = mapped_column(String(30), default='operations', server_default='operations', nullable=False)
    system_key: Mapped[str | None] = mapped_column(String(180), unique=True, nullable=True)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, server_default='1', nullable=False)


class InternalAudit(Base):
    __tablename__ = 'internal_audit'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey('internal_users.id'), nullable=True, index=True)
    entity_type: Mapped[str] = mapped_column(String(40), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(30), nullable=False)
    summary: Mapped[str] = mapped_column(String(240), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

# Additive transportation tables share the existing metadata and domain identities.
class TransportNode(FoundationTimestamps, Base):
    __tablename__='transport_nodes'
    __table_args__=(CheckConstraint("node_type IN ('airport','city','destination','pickup_zone','hotel','other')",name='ck_transport_node_type'),)
    id: Mapped[int]=mapped_column(primary_key=True)
    destination_id: Mapped[int|None]=mapped_column(ForeignKey('destinations.id'))
    name: Mapped[str]=mapped_column(String(160))
    slug: Mapped[str]=mapped_column(String(180),unique=True)
    node_type: Mapped[str]=mapped_column(String(30))
    active: Mapped[bool]=mapped_column(Boolean,default=True,server_default=text('true'))
    notes: Mapped[str|None]=mapped_column(Text)
    version: Mapped[int]=mapped_column(default=1,server_default='1')

class CanonicalTransportRoute(FoundationTimestamps, Base):
    __tablename__='transport_routes'
    __table_args__=(UniqueConstraint('origin_node_id','destination_node_id',name='uq_transport_direction'),CheckConstraint('origin_node_id != destination_node_id',name='ck_transport_distinct_nodes'),CheckConstraint('estimated_duration_minutes IS NULL OR estimated_duration_minutes > 0',name='ck_transport_route_duration'),CheckConstraint('estimated_distance_km IS NULL OR estimated_distance_km > 0',name='ck_transport_route_distance'))
    id: Mapped[int]=mapped_column(primary_key=True)
    origin_node_id: Mapped[int]=mapped_column(ForeignKey('transport_nodes.id'))
    destination_node_id: Mapped[int]=mapped_column(ForeignKey('transport_nodes.id'))
    active: Mapped[bool]=mapped_column(Boolean,default=True,server_default=text('true'))
    estimated_duration_minutes: Mapped[int|None]=mapped_column(Integer)
    estimated_distance_km: Mapped[Decimal|None]=mapped_column(Numeric(8,2))
    notes: Mapped[str|None]=mapped_column(Text)
    source: Mapped[str]=mapped_column(String(40),default='RideCR')
    source_url: Mapped[str]=mapped_column(String(2048))
    source_checked_at: Mapped[datetime]=mapped_column(DateTime(timezone=True))
    review_notes: Mapped[str|None]=mapped_column(Text)
    version: Mapped[int]=mapped_column(default=1,server_default='1')

class VendorTransportService(FoundationTimestamps, Base):
    __tablename__='transport_services'
    __table_args__=(UniqueConstraint('supplier_id','route_id','service_type',name='uq_transport_vendor_service'),CheckConstraint("service_type IN ('shared_shuttle','private_transfer','lake_crossing','other')",name='ck_transport_service_type'),CheckConstraint('capacity IS NULL OR capacity > 0',name='ck_transport_capacity'))
    id: Mapped[int]=mapped_column(primary_key=True)
    supplier_id: Mapped[int]=mapped_column(ForeignKey('suppliers.id'))
    route_id: Mapped[int]=mapped_column(ForeignKey('transport_routes.id'))
    product_id: Mapped[int|None]=mapped_column(ForeignKey('products.id'),unique=True)
    service_type: Mapped[str]=mapped_column(String(30))
    active: Mapped[bool]=mapped_column(Boolean,default=True,server_default=text('true'))
    booking_method: Mapped[str]=mapped_column(String(100),default='manual_vendor_confirmation')
    pickup_notes: Mapped[str|None]=mapped_column(Text)
    dropoff_notes: Mapped[str|None]=mapped_column(Text)
    luggage_notes: Mapped[str|None]=mapped_column(Text)
    child_policy: Mapped[str|None]=mapped_column(Text)
    capacity: Mapped[int|None]=mapped_column(Integer)
    source_url: Mapped[str|None]=mapped_column(String(2048))
    last_verified_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    version: Mapped[int]=mapped_column(default=1,server_default='1')

class TransportSchedule(FoundationTimestamps, Base):
    __tablename__='transport_schedules'
    __table_args__=(CheckConstraint('days_mask BETWEEN 0 AND 127',name='ck_transport_weekdays'),CheckConstraint('effective_from IS NULL OR effective_to IS NULL OR effective_to >= effective_from',name='ck_transport_schedule_dates'),CheckConstraint('estimated_duration_minutes IS NULL OR estimated_duration_minutes > 0',name='ck_transport_schedule_duration'),CheckConstraint('pickup_window_minutes IS NULL OR pickup_window_minutes >= 0',name='ck_transport_pickup_window'))
    id: Mapped[int]=mapped_column(primary_key=True)
    vendor_service_id: Mapped[int]=mapped_column(ForeignKey('transport_services.id'),index=True)
    departure_time: Mapped[time]=mapped_column(Time)
    arrival_time: Mapped[time|None]=mapped_column(Time)
    estimated_duration_minutes: Mapped[int|None]=mapped_column(Integer)
    days_mask: Mapped[int]=mapped_column(Integer,default=0,server_default='0')
    effective_from: Mapped[date|None]=mapped_column(Date)
    effective_to: Mapped[date|None]=mapped_column(Date)
    pickup_window_minutes: Mapped[int|None]=mapped_column(Integer)
    seasonal_notes: Mapped[str|None]=mapped_column(Text)
    active: Mapped[bool]=mapped_column(Boolean,default=True,server_default=text('true'))
    source_url: Mapped[str]=mapped_column(String(2048))
    last_verified_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    import_key: Mapped[str|None]=mapped_column(String(200),unique=True)
    version: Mapped[int]=mapped_column(default=1,server_default='1')

class TransportRate(FoundationTimestamps, Base):
    __tablename__='transport_rates'
    __table_args__=(CheckConstraint('effective_to >= effective_from',name='ck_transport_rate_dates'),CheckConstraint("unit_basis IN ('per_person','per_vehicle')",name='ck_transport_rate_unit'),CheckConstraint("currency IN ('USD','CRC')",name='ck_transport_rate_currency'),CheckConstraint("(rate_kind = 'vendor_rate' AND public_reference_price IS NULL AND (vendor_cost IS NOT NULL OR vv_retail IS NOT NULL)) OR (rate_kind = 'public_reference' AND vendor_cost IS NULL AND vv_retail IS NULL AND public_reference_price IS NOT NULL)",name='ck_transport_price_boundary'),CheckConstraint('(vendor_cost IS NULL OR vendor_cost >= 0) AND (vv_retail IS NULL OR vv_retail >= 0) AND (public_reference_price IS NULL OR public_reference_price >= 0)',name='ck_transport_positive_rates'))
    id: Mapped[int]=mapped_column(primary_key=True)
    vendor_service_id: Mapped[int]=mapped_column(ForeignKey('transport_services.id'),index=True)
    agreement_id: Mapped[int|None]=mapped_column(ForeignKey('supplier_agreements.id'))
    supersedes_id: Mapped[int|None]=mapped_column(ForeignKey('transport_rates.id'),unique=True)
    rate_kind: Mapped[str]=mapped_column(String(30))
    unit_basis: Mapped[str]=mapped_column(String(30))
    currency: Mapped[str]=mapped_column(String(3))
    vendor_cost: Mapped[Decimal|None]=mapped_column(Numeric(12,2))
    vv_retail: Mapped[Decimal|None]=mapped_column(Numeric(12,2))
    public_reference_price: Mapped[Decimal|None]=mapped_column(Numeric(12,2))
    effective_from: Mapped[date]=mapped_column(Date)
    effective_to: Mapped[date]=mapped_column(Date)
    notes: Mapped[str|None]=mapped_column(Text)
    source_url: Mapped[str|None]=mapped_column(String(2048))
