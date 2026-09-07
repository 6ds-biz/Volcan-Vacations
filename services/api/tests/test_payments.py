"""Provider calls are mocked. These tests do NOT constitute PayPal sandbox validation."""
from copy import deepcopy
from datetime import timedelta
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.exc import IntegrityError

from app.availability_rules import utcnow
from app.main import app
from app.models import Payment, PaymentRefund, PaymentWebhookEvent, Product, Reservation
from app.payment_service import get_paypal
from app.services.paypal import PayPalError
from test_inventory import client, create_tour
from test_bookings import inspect_db, submit
from test_availability import record


class FakePayPal:
    configured = True
    settings = SimpleNamespace(paypal_client_id='TEST-SANDBOX-CLIENT', paypal_client_secret='TEST-PRIVATE-SECRET', paypal_webhook_id='TEST-PRIVATE-WEBHOOK')
    def __init__(self):
        self.orders = {}
        self.keys = {}
        self.creates = 0
        self.captures = 0
        self.verify = True
        self.create_error = None
        self.capture_error = None
        self.refunds = {}
    def require_configuration(self):
        if not self.configured:
            raise PayPalError('SANDBOX_NOT_CONFIGURED', uncertain=False)
    def create_order(self, payment):
        self.require_configuration()
        if payment.idempotency_key not in self.keys:
            self.creates += 1
            order_id = f'ORDER-{self.creates}'
            self.keys[payment.idempotency_key] = order_id
            self.orders[order_id] = {'id': order_id, 'intent': 'CAPTURE', 'status': 'CREATED', 'purchase_units': [{
                'reference_id': payment.external_reference, 'custom_id': payment.external_reference,
                'amount': {'currency_code': payment.currency, 'value': str(payment.amount)}}]}
        if self.create_error:
            error, self.create_error = self.create_error, None
            raise error
        return self.get_order(self.keys[payment.idempotency_key])
    def get_order(self, order_id):
        return deepcopy(self.orders[order_id])
    def approve(self, order_id):
        self.orders[order_id]['status'] = 'APPROVED'
    def capture_order(self, payment):
        if self.capture_error and not self.capture_error.uncertain:
            error, self.capture_error = self.capture_error, None
            raise error
        order = self.orders[payment.provider_order_id]
        if order['status'] != 'COMPLETED':
            self.captures += 1
            order['status'] = 'COMPLETED'
            order['purchase_units'][0]['payments'] = {'captures': [{'id': f'CAPTURE-{self.captures}', 'status': 'COMPLETED',
                'amount': deepcopy(order['purchase_units'][0]['amount']), 'final_capture': True}]}
        if self.capture_error:
            error, self.capture_error = self.capture_error, None
            raise error
        return self.get_order(payment.provider_order_id)
    def get_capture(self, capture_id):
        for order in self.orders.values():
            for capture in order['purchase_units'][0].get('payments', {}).get('captures', []):
                if capture['id'] == capture_id:
                    return deepcopy(capture) | {'supplementary_data': {'related_ids': {'order_id': order['id']}}}
        raise PayPalError('RESOURCE_NOT_FOUND', uncertain=False)
    def get_refund(self, refund_id):
        return self.refunds[refund_id]
    def verify_webhook(self, headers, event):
        return self.verify


@pytest.fixture
def provider(client):
    provider = FakePayPal()
    app.dependency_overrides[get_paypal] = lambda: provider
    return provider


def ready(client):
    tour = create_tour(client)
    submit(client)
    booking = client.get('/ops/bookings').json()[0]
    booking = record(client, booking, 'confirmed', reference='PRIVATE SUPPLIER REFERENCE')
    response = client.post(f"/ops/bookings/{booking['id']}/payment-link", json={'expected_version': booking['version']})
    assert response.status_code == 200, response.text
    token = response.json()['path'].split('#token=')[1]
    return tour, client.get(f"/ops/bookings/{booking['id']}").json(), {'Authorization': 'Bearer ' + token}


def create(client, headers, key=None):
    response = client.post('/public/payments/paypal/order', json={'idempotency_key': key or str(uuid4())}, headers=headers)
    assert response.status_code == 200, response.text
    return response.json()


def capture(client, headers, order):
    response = client.post(f"/public/payments/paypal/{order}/capture", headers=headers)
    assert response.status_code == 200, response.text
    return response.json()


def event_data(order_id, kind='PAYMENT.CAPTURE.COMPLETED', resource_id='CAPTURE-1', event_id=None):
    return {'id': event_id or str(uuid4()), 'event_type': kind, 'resource': {'id': resource_id,
            'supplementary_data': {'related_ids': {'order_id': order_id}}}}


@pytest.mark.parametrize('status,supplier,availability', [
    ('new', 'not_requested', 'unknown'), ('contacted', 'not_requested', 'unknown'),
    ('pending_supplier', 'awaiting_supplier', 'available'), ('cancelled', 'confirmed', 'available'),
    ('completed', 'confirmed', 'available'), ('contacted', 'declined', 'unavailable'),
    ('confirmed', 'alternative_offered', 'available'), ('confirmed', 'awaiting_supplier', 'unavailable')])
def test_ineligible_reservations_cannot_create_payment(client, provider, status, supplier, availability):
    _, booking, headers = ready(client)
    def change(db):
        row = db.get(Reservation, booking['id'])
        row.status, row.supplier_confirmation_status, row.availability_status = status, supplier, availability
        db.commit()
    inspect_db(change)
    response = client.post('/public/payments/paypal/order', json={'idempotency_key': str(uuid4())}, headers=headers)
    assert response.status_code in (404, 409)
    assert provider.creates == 0
    assert inspect_db(lambda db: db.scalar(select(func.count()).select_from(Payment))) == 0


def test_snapshot_amount_and_browser_price_rejection(client, provider):
    tour, booking, headers = ready(client)
    def price(db):
        db.get(Product, tour['id']).retail_price = Decimal('95.00')
        db.commit()
    inspect_db(price)
    assert client.post('/public/payments/paypal/order', headers=headers, json={'idempotency_key': str(uuid4()), 'amount': '1.00'}).status_code == 422
    result = create(client, headers)
    assert result['amount'] == result['amount_due'] == '170.00'
    assert result['amount_paid'] == '0.00' and result['status'] == 'created'
    assert inspect_db(lambda db: db.scalar(select(Payment.amount))) == Decimal('170.00')
    assert provider.orders[result['order_id']]['purchase_units'][0]['amount']['value'] == '170.00'


def test_duplicate_create_capture_and_no_second_checkout_after_paid(client, provider):
    _, booking, headers = ready(client)
    key = str(uuid4())
    first = create(client, headers, key)
    assert create(client, headers, key)['order_id'] == first['order_id']
    assert create(client, headers)['order_id'] == first['order_id']  # another browser still one intent
    assert provider.creates == 1
    provider.approve(first['order_id'])
    paid = capture(client, headers, first['order_id'])
    assert paid['status'] == 'captured' and paid['amount_paid'] == '170.00' and paid['amount_due'] == '0.00'
    assert not paid['eligible'] and not paid['checkout_available']
    assert capture(client, headers, first['order_id']) == paid
    assert provider.captures == 1
    assert client.post('/public/payments/paypal/order', headers=headers, json={'idempotency_key': str(uuid4())}).status_code == 409
    internal = client.get(f"/ops/bookings/{booking['id']}/payment").json()
    assert internal['label'] == 'Paid' and internal['payment']['paid_at'] and internal['payment']['provider_capture_id'] == 'CAPTURE-1'
    assert client.get(f"/ops/bookings/{booking['id']}").json()['payment_received']


def test_cancel_retry_reuses_order_keeps_supplier_and_reservation(client, provider):
    _, booking, headers = ready(client)
    order = create(client, headers)['order_id']
    cancelled = client.post(f'/public/payments/paypal/{order}/cancel', headers=headers).json()
    assert cancelled['status'] == 'cancelled' and cancelled['eligible'] and cancelled['retryable']
    assert 'still awaiting payment' in cancelled['message']
    current = client.get(f"/ops/bookings/{booking['id']}").json()
    assert current['status'] == current['supplier_confirmation_status'] == 'confirmed'
    assert create(client, headers)['order_id'] == order
    provider.approve(order)
    assert capture(client, headers, order)['status'] == 'captured'
    assert provider.creates == provider.captures == 1
    assert client.post(f'/public/payments/paypal/{order}/cancel', headers=headers).json()['status'] == 'captured'


def test_failure_retry_does_not_cancel_reservation(client, provider):
    _, booking, headers = ready(client)
    order = create(client, headers)['order_id']
    provider.approve(order)
    provider.capture_error = PayPalError('INSTRUMENT_DECLINED', uncertain=False)
    failed = capture(client, headers, order)
    assert failed['status'] == 'failed' and failed['retryable']
    assert client.get(f"/ops/bookings/{booking['id']}").json()['status'] == 'confirmed'
    assert capture(client, headers, order)['status'] == 'captured'
    assert provider.captures == 1


def test_lost_create_and_capture_response_reconcile_same_intent(client, provider):
    _, _, headers = ready(client)
    provider.create_error = PayPalError()
    first = create(client, headers)
    assert first['status'] == 'pending' and first['order_id'] is None
    order = create(client, headers)['order_id']
    assert provider.creates == 1
    provider.approve(order)
    provider.capture_error = PayPalError()
    assert capture(client, headers, order)['status'] == 'pending'
    assert capture(client, headers, order)['status'] == 'captured'
    assert provider.captures == 1


def test_old_uncertain_create_never_mints_fresh_order(client, provider):
    _, _, headers = ready(client)
    provider.create_error = PayPalError()
    create(client, headers)
    def old(db):
        db.scalar(select(Payment)).create_started_at = utcnow() - timedelta(hours=7)
        db.commit()
    inspect_db(old)
    result = create(client, headers)
    assert result['status'] == 'failed' and not result['retryable']
    assert provider.creates == 1


def test_signature_failure_duplicate_webhook_and_capture_convergence(client, provider):
    _, booking, headers = ready(client)
    order = create(client, headers)['order_id']
    provider.approve(order)
    paid = capture(client, headers, order)
    notification = event_data(order)
    provider.verify = False
    assert client.post('/webhooks/paypal', json=notification).status_code == 400
    assert inspect_db(lambda db: db.scalar(select(func.count()).select_from(PaymentWebhookEvent))) == 0
    provider.verify = True
    for _ in range(2):
        response = client.post('/webhooks/paypal', json=notification)
        assert response.status_code == 200, response.text
    assert inspect_db(lambda db: db.scalar(select(func.count()).select_from(PaymentWebhookEvent))) == 1
    assert client.get('/public/payments/session', headers=headers).json() == paid
    assert provider.captures == 1
    approved = event_data(order, kind='CHECKOUT.ORDER.APPROVED', resource_id=order)
    assert client.post('/webhooks/paypal', json=approved).status_code == 200
    assert client.get(f"/ops/bookings/{booking['id']}/payment").json()['label'] == 'Paid'


def test_webhook_first_recovers_lost_capture_response(client, provider):
    _, _, headers = ready(client)
    order = create(client, headers)['order_id']
    provider.approve(order)
    provider.capture_error = PayPalError()
    assert capture(client, headers, order)['status'] == 'pending'
    result = client.post('/webhooks/paypal', json=event_data(order))
    assert result.status_code == 200, result.text
    assert capture(client, headers, order)['status'] == 'captured'
    assert provider.captures == 1


def test_refunds_verified_deduplicated_and_not_erased_by_capture_replay(client, provider):
    _, booking, headers = ready(client)
    order = create(client, headers)['order_id']; provider.approve(order)
    capture(client, headers, order)
    for refund_id, amount in [('REFUND-1', '50.00'), ('REFUND-2', '120.00')]:
        provider.refunds[refund_id] = {'id': refund_id, 'status': 'COMPLETED', 'amount': {'currency_code': 'USD', 'value': amount},
            'links': [{'rel': 'up', 'href': 'https://api-m.sandbox.paypal.com/v2/payments/captures/CAPTURE-1'}]}
        for _ in range(2):
            result = client.post('/webhooks/paypal', json=event_data(order, kind='PAYMENT.CAPTURE.REFUNDED', resource_id=refund_id))
            assert result.status_code == 200, result.text
        p = client.get(f"/ops/bookings/{booking['id']}/payment").json()['payment']
        assert p['refunded_amount'] == ('50.00' if refund_id == 'REFUND-1' else '170.00')
        assert p['status'] == ('partially_refunded' if refund_id == 'REFUND-1' else 'refunded')
    assert inspect_db(lambda db: db.scalar(select(func.count()).select_from(PaymentRefund))) == 2
    assert capture(client, headers, order)['status'] == 'refunded'
    assert client.post('/webhooks/paypal', json=event_data(order)).status_code == 200
    assert client.get('/public/payments/session', headers=headers).json()['status'] == 'refunded'


def test_wrong_amount_order_binding_or_capture_is_never_paid(client, provider):
    _, _, headers = ready(client)
    order = create(client, headers)['order_id']
    provider.approve(order)
    provider.orders[order]['purchase_units'][0]['amount']['value'] = '1.00'
    result = capture(client, headers, order)
    assert not result['checkout_available'] and result['amount_paid'] == '0.00'
    assert provider.captures == 0
    assert client.post('/public/payments/paypal/OTHER-ORDER/capture', headers=headers).status_code == 404


def test_token_rotation_revocation_expiration_and_supplier_correction(client, provider):
    _, booking, headers = ready(client)
    for auth in [{}, {'Authorization': 'Bearer 1'}, {'Authorization': 'Bearer ' + 'x' * 43}]:
        assert client.get('/public/payments/session', headers=auth).status_code == 404
    link = client.post(f"/ops/bookings/{booking['id']}/payment-link", json={'expected_version': booking['version']}).json()
    assert client.get('/public/payments/session', headers=headers).status_code == 404
    headers = {'Authorization': 'Bearer ' + link['path'].split('#token=')[1]}
    assert client.get('/public/payments/session', headers=headers).status_code == 200
    booking = client.get(f"/ops/bookings/{booking['id']}").json()
    corrected = record(client, booking, 'declined', notes='Supplier corrected availability')
    assert corrected['status'] == 'contacted'
    assert client.get('/public/payments/session', headers=headers).status_code == 404
    assert client.post('/public/payments/paypal/order', headers=headers, json={'idempotency_key': str(uuid4())}).status_code == 404


def test_expired_link_and_cancelled_reservation_cannot_capture(client, provider):
    _, booking, headers = ready(client)
    order = create(client, headers)['order_id']; provider.approve(order)
    cancelled = client.put(f"/ops/bookings/{booking['id']}", json={'status': 'cancelled', 'expected_status': 'confirmed', 'expected_version': booking['version']})
    assert cancelled.status_code == 200, cancelled.text
    assert client.post(f'/public/payments/paypal/{order}/capture', headers=headers).status_code == 404
    assert provider.captures == 0


def test_public_privacy_no_internal_fields_or_payer_data(client, provider):
    _, _, headers = ready(client)
    before = client.get('/public/payments/session', headers=headers).json()
    created = create(client, headers)
    order = created['order_id']; provider.approve(order)
    provider.orders[order]['payer'] = {'email_address': 'OTHER CUSTOMER PRIVATE EMAIL'}
    paid = capture(client, headers, order)
    for data in [before, created, paid]:
        for text in ['supplier_cost', 'supplier_unit_cost', 'margin', 'internal_notes', 'supplier_confirmation', 'TEST-PRIVATE', 'PRIVATE SUPPLIER', 'OTHER CUSTOMER', 'provider_capture_id', 'paid_at', 'webhook_id', 'debug_id']:
            assert text not in str(data)
    assert 'CAPTURE-1' not in str(paid)


def test_provider_call_success_database_failure_recovers_without_second_charge(client, provider):
    _, _, headers = ready(client)
    order = create(client, headers)['order_id']; provider.approve(order)
    def fail(mapper, connection, target):
        if target.status == 'captured':
            raise IntegrityError('simulated storage failure', {}, Exception('failure'))
    event.listen(Payment, 'before_update', fail)
    try:
        assert client.post(f'/public/payments/paypal/{order}/capture', headers=headers).status_code == 409
    finally:
        event.remove(Payment, 'before_update', fail)
    assert capture(client, headers, order)['status'] == 'captured'
    assert provider.captures == 1


def test_missing_configuration_blocks_provider_and_overdue_link_is_revocable(client, provider):
    _, booking, headers = ready(client)
    provider.configured = False
    result = client.get('/public/payments/session', headers=headers).json()
    assert result['eligible'] and not result['checkout_available'] and result['client_id'] is None
    assert client.post('/public/payments/paypal/order', headers=headers, json={'idempotency_key': str(uuid4())}).status_code == 503
    assert inspect_db(lambda db: db.scalar(select(func.count()).select_from(Payment))) == 0
    revoked = client.post(f"/ops/bookings/{booking['id']}/payment-link/revoke", json={'expected_version': booking['version']})
    assert revoked.status_code == 200
    assert client.get('/public/payments/session', headers=headers).status_code == 404


def test_minimal_provider_post_responses_are_resolved_with_full_order(client, provider, monkeypatch):
    _, _, headers = ready(client)
    original_create, original_capture = provider.create_order, provider.capture_order
    monkeypatch.setattr(provider, 'create_order', lambda payment: {'id': original_create(payment)['id']})
    monkeypatch.setattr(provider, 'capture_order', lambda payment: {'id': original_capture(payment)['id'], 'status': 'COMPLETED'})
    order = create(client, headers)['order_id']; provider.approve(order)
    assert capture(client, headers, order)['status'] == 'captured'


def test_expired_link_does_not_release_confirmed_reservation(client, provider):
    _, booking, headers = ready(client)
    def expire(db):
        row = db.get(Reservation, booking['id'])
        row.payment_token_expires_at = utcnow() - timedelta(seconds=1)
        row.payment_due_at = utcnow() - timedelta(seconds=1)
        db.commit()
    inspect_db(expire)
    assert client.get('/public/payments/session', headers=headers).status_code == 404
    current = client.get(f"/ops/bookings/{booking['id']}").json()
    assert current['status'] == current['supplier_confirmation_status'] == 'confirmed'
    assert client.get(f"/ops/bookings/{booking['id']}/payment").json()['overdue']
