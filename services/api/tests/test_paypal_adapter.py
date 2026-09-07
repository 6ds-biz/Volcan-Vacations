"""HTTP protocol tests using httpx.MockTransport, never real PayPal."""
import json
from decimal import Decimal
from types import SimpleNamespace

import httpx
import pytest

from app.services.paypal import PayPal, PayPalError, money


def config(**changes):
    return SimpleNamespace(**(dict(paypal_environment='sandbox', paypal_currency='USD', paypal_client_id='test-client',
        paypal_client_secret='test-private-secret', paypal_webhook_id='test-webhook') | changes))


def transport(monkeypatch, handler):
    original = httpx.Client
    monkeypatch.setattr(httpx, 'Client', lambda **kwargs: original(transport=httpx.MockTransport(handler), **kwargs))


def test_oauth_order_amount_and_distinct_stable_request_ids(monkeypatch):
    requests = []
    def handle(request):
        requests.append(request)
        if request.url.path == '/v1/oauth2/token':
            assert request.headers['authorization'].startswith('Basic ')
            assert request.content == b'grant_type=client_credentials'
            return httpx.Response(200, json={'access_token': 'private-oauth-token'})
        assert request.url.host == 'api-m.sandbox.paypal.com'
        assert request.headers['authorization'] == 'Bearer private-oauth-token'
        return httpx.Response(201, json={'id': 'ORDER-1', 'status': 'CREATED'})
    transport(monkeypatch, handle)
    paypal = PayPal(config())
    payment = SimpleNamespace(idempotency_key='create-request-uuid', capture_request_id='capture-request-uuid',
        provider_order_id='ORDER-1', external_reference='binding-uuid', amount=Decimal('170.00'), currency='USD')
    paypal.create_order(payment); paypal.capture_order(payment)
    body = json.loads(requests[1].content)
    assert body['purchase_units'][0]['amount'] == {'currency_code': 'USD', 'value': '170.00'}
    assert body['purchase_units'][0]['custom_id'] == 'binding-uuid'
    assert requests[1].headers['paypal-request-id'] == 'create-request-uuid'
    assert requests[2].headers['paypal-request-id'] == 'capture-request-uuid'
    assert len(requests) == 3


@pytest.mark.parametrize('changes', [{'paypal_environment': 'live'}, {'paypal_client_secret': None}, {'paypal_currency': 'CRC'}, {'paypal_environment': 'invalid'}])
def test_live_or_incomplete_configuration_never_calls_network(monkeypatch, changes):
    def forbidden(request):
        pytest.fail('Network must not run')
    transport(monkeypatch, forbidden)
    paypal = PayPal(config(**changes))
    assert not paypal.configured
    with pytest.raises(PayPalError, match='SANDBOX_NOT_CONFIGURED'):
        paypal.get_order('ORDER-1')


def test_signature_verification_uses_server_webhook_id_and_paypal_result(monkeypatch):
    calls = []
    def handle(request):
        if request.url.path == '/v1/oauth2/token':
            return httpx.Response(200, json={'access_token': 'test-token'})
        calls.append(request)
        body = json.loads(request.content)
        assert request.url.path == '/v1/notifications/verify-webhook-signature'
        assert body['webhook_id'] == 'test-webhook'
        assert body['transmission_id'] == 'transmission'
        assert body['webhook_event'] == {'id': 'EVENT-1'}
        return httpx.Response(200, json={'verification_status': 'SUCCESS' if len(calls) == 1 else 'FAILURE'})
    transport(monkeypatch, handle)
    paypal = PayPal(config())
    headers = {'paypal-auth-algo': 'SHA256withRSA', 'paypal-cert-url': 'https://api.sandbox.paypal.com/certificate',
        'paypal-transmission-id': 'transmission', 'paypal-transmission-sig': 'signature', 'paypal-transmission-time': '2026-09-05T00:00:00Z'}
    assert paypal.verify_webhook(headers, {'id': 'EVENT-1'})
    assert not paypal.verify_webhook(headers, {'id': 'EVENT-1'})
    assert not paypal.verify_webhook({}, {'id': 'EVENT-1'})
    assert len(calls) == 2


def test_timeouts_and_provider_debug_details_are_not_exposed(monkeypatch):
    def timeout(request):
        raise httpx.ReadTimeout('PRIVATE RAW PROVIDER DETAILS')
    transport(monkeypatch, timeout)
    with pytest.raises(PayPalError) as caught:
        PayPal(config()).get_order('ORDER-1')
    assert caught.value.uncertain and 'PRIVATE' not in str(caught.value)


@pytest.mark.parametrize('amount', [{'currency_code': 'EUR', 'value': '1.00'}, {'currency_code': 'USD', 'value': 1.0},
    {'currency_code': 'USD', 'value': 'NaN'}, {'currency_code': 'USD', 'value': '-1'}, {'currency_code': 'USD', 'value': '0.001'}])
def test_invalid_provider_money_is_rejected(amount):
    with pytest.raises(PayPalError):
        money(amount, 'USD')
