"""Opt-in PostgreSQL locking test; provider is mocked and no funds move."""
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from decimal import Decimal
from threading import Event
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Base, Payment, PaymentWebhookEvent, Product, Reservation, Supplier
from app.booking_schemas import BookingInput
from app.booking_service import create_request
from app.availability_schemas import SupplierEventInput
from app.availability_service import record_supplier_event
from app.payment_schemas import LinkInput, OrderInput
from app.payment_service import issue_link, create_order, capture_order, webhook
from test_payments import FakePayPal, event_data


@pytest.mark.skipif(os.environ.get('VV_TEST_POSTGRES') != '1', reason='Explicit PostgreSQL integration opt-in required')
def test_postgres_simultaneous_create_capture_and_webhook():
    assert settings.environment == 'development'
    assert settings.database_url.startswith('postgresql')
    schema = 'vv_payment_test_' + uuid4().hex
    admin = create_engine(settings.database_url)
    isolated = None
    try:
        with admin.begin() as db:
            db.execute(text(f'CREATE SCHEMA {schema}'))
        isolated = create_engine(settings.database_url, connect_args={'options': f'-csearch_path={schema}'}, pool_size=10)
        Base.metadata.create_all(isolated)
        with Session(isolated) as db:
            supplier = Supplier(name='DEMO isolated concurrency', supplier_type='tour_operator')
            db.add(supplier); db.flush()
            product = Product(supplier_id=supplier.id, name='DEMO isolated tour', slug='demo-isolated', product_type='tour',
                              retail_price=Decimal('85.00'), supplier_cost=Decimal('50.00'))
            db.add(product); db.commit()
        with Session(isolated) as db:
            create_request(db, BookingInput(idempotency_key=uuid4(), tour_slug='demo-isolated',
                requested_date=date.today() + timedelta(days=30), party_size=1,
                customer={'first_name': 'DEMO', 'last_name': 'Concurrency', 'email': 'demo@example.invalid'},
                travelers=[{'first_name': 'DEMO', 'last_name': 'Concurrency'}]))
        with Session(isolated) as db:
            booking_id = db.scalar(select(Reservation.id)); db.rollback()
            record_supplier_event(db, booking_id, SupplierEventInput(command_id=uuid4(), expected_version=1, event_type='confirmed'))
        with Session(isolated) as db:
            link = issue_link(db, booking_id, LinkInput(expected_version=2))
        token = link['path'].split('#token=')[1]
        provider = FakePayPal()
        def create():
            with Session(isolated) as db:
                return create_order(db, token, OrderInput(idempotency_key=uuid4()), provider)
        with ThreadPoolExecutor(max_workers=8) as pool:
            orders = list(pool.map(lambda _: create(), range(8)))
        assert provider.creates == 1
        assert len({o['order_id'] for o in orders}) == 1
        order = orders[0]['order_id']; provider.approve(order)
        captured = Event()
        original = provider.capture_order
        def signal(payment):
            result = original(payment); captured.set(); return result
        provider.capture_order = signal
        def capture():
            with Session(isolated) as db:
                return capture_order(db, token, order, provider)
        notification = event_data(order)
        def notify():
            assert captured.wait(10)
            with Session(isolated) as db:
                return webhook(db, provider, {}, notification)
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = [pool.submit(capture) for _ in range(4)] + [pool.submit(notify) for _ in range(4)]
            results = [f.result(timeout=30) for f in futures]
        assert all(result['status'] == 'captured' for result in results[:4])
        assert provider.captures == 1
        with Session(isolated) as db:
            assert db.scalar(select(func.count()).select_from(Payment)) == 1
            assert db.scalar(select(func.count()).select_from(PaymentWebhookEvent)) == 1
            assert db.scalar(select(Payment)).paid_at is not None
    finally:
        if isolated:
            isolated.dispose()
        # Only this test's cryptographically named schema is dropped, never public.
        with admin.begin() as db:
            db.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE'))
        admin.dispose()
