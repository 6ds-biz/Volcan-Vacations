"""PayPal Orders v2 / Payments v2 adapter. No live calls in Milestone 5.

No raw provider bodies, credentials or payer data leave this module as errors.
"""
import re
from decimal import Decimal, InvalidOperation

import httpx


class PayPalError(Exception):
    def __init__(self, code='PROVIDER_UNAVAILABLE', *, uncertain=True):
        self.code = code
        self.uncertain = uncertain
        super().__init__(code)


class PayPal:
    BASES = {'sandbox': 'https://api-m.sandbox.paypal.com', 'live': 'https://api-m.paypal.com'}

    def __init__(self, settings):
        self.settings = settings
        self.base = self.BASES.get(settings.paypal_environment, '')
        self.token = None

    @property
    def configured(self):
        return self.settings.paypal_environment == 'sandbox' and self.settings.paypal_currency == 'USD' and bool(self.settings.paypal_client_id and self.settings.paypal_client_secret)

    def require_configuration(self):
        if not self.configured:
            raise PayPalError('SANDBOX_NOT_CONFIGURED', uncertain=False)

    def _send(self, method, path, *, data=None, payload=None, headers=None, auth=None):
        self.require_configuration()
        try:
            with httpx.Client(timeout=httpx.Timeout(12, connect=3), follow_redirects=False) as client:
                response = client.request(method, self.base + path, data=data, json=payload, headers=headers, auth=auth)
            if response.status_code >= 400:
                # Only explicitly safe, documented issue codes are retained.
                code = 'PROVIDER_UNAVAILABLE'
                try:
                    issues = {d.get('issue') for d in response.json().get('details', [])}
                    for known in ['INSTRUMENT_DECLINED', 'ORDER_NOT_APPROVED', 'ORDER_ALREADY_CAPTURED', 'TRANSACTION_REFUSED', 'RESOURCE_NOT_FOUND']:
                        if known in issues:
                            code = known
                            break
                except (ValueError, AttributeError, TypeError):
                    pass
                certain = response.status_code in (400, 401, 403, 404, 422) and code in ('INSTRUMENT_DECLINED', 'ORDER_NOT_APPROVED', 'TRANSACTION_REFUSED', 'RESOURCE_NOT_FOUND')
                raise PayPalError(code, uncertain=not certain)
            if not 200 <= response.status_code < 300 or len(response.content) > 2_000_000:
                raise PayPalError('INVALID_PROVIDER_RESPONSE')
            result = response.json()
            if not isinstance(result, dict):
                raise PayPalError('INVALID_PROVIDER_RESPONSE')
            return result
        except (httpx.HTTPError, ValueError):
            raise PayPalError('PROVIDER_UNAVAILABLE') from None

    def _request(self, method, path, *, payload=None, request_id=None):
        if not self.token:
            result = self._send('POST', '/v1/oauth2/token', data={'grant_type': 'client_credentials'}, auth=(self.settings.paypal_client_id or '', self.settings.paypal_client_secret or ''))
            token = result.get('access_token')
            if not isinstance(token, str) or not token:
                raise PayPalError('INVALID_PROVIDER_RESPONSE')
            self.token = token
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json', 'Prefer': 'return=representation'}
        if request_id:
            headers['PayPal-Request-Id'] = request_id
        return self._send(method, path, payload=payload, headers=headers)

    def create_order(self, payment):
        return self._request('POST', '/v2/checkout/orders', request_id=payment.idempotency_key, payload={
            'intent': 'CAPTURE',
            'purchase_units': [{'reference_id': payment.external_reference, 'custom_id': payment.external_reference,
                'invoice_id': payment.external_reference, 'description': 'Volcan Vacations confirmed tour',
                'amount': {'currency_code': payment.currency, 'value': f'{payment.amount:.2f}'}}],
            'payment_source': {'paypal': {'experience_context': {'brand_name': 'Volcan Vacations',
                'shipping_preference': 'NO_SHIPPING', 'user_action': 'PAY_NOW'}}},
        })

    def get_order(self, order_id):
        return self._request('GET', '/v2/checkout/orders/' + provider_id(order_id))

    def capture_order(self, payment):
        return self._request('POST', f'/v2/checkout/orders/{provider_id(payment.provider_order_id)}/capture',
                             payload={}, request_id=payment.capture_request_id)

    def get_capture(self, capture_id):
        return self._request('GET', '/v2/payments/captures/' + provider_id(capture_id))

    def get_refund(self, refund_id):
        return self._request('GET', '/v2/payments/refunds/' + provider_id(refund_id))

    def verify_webhook(self, headers, event):
        if not self.settings.paypal_webhook_id:
            raise PayPalError('WEBHOOK_NOT_CONFIGURED', uncertain=False)
        mapping = {'auth_algo': 'paypal-auth-algo', 'cert_url': 'paypal-cert-url', 'transmission_id': 'paypal-transmission-id',
                   'transmission_sig': 'paypal-transmission-sig', 'transmission_time': 'paypal-transmission-time'}
        if any(not headers.get(key) or len(headers.get(key)) > 2048 for key in mapping.values()):
            return False
        # cert_url is sent to PayPal for verification; never fetched by this API.
        result = self._request('POST', '/v1/notifications/verify-webhook-signature', payload={
            **{key: headers[value] for key, value in mapping.items()}, 'webhook_id': self.settings.paypal_webhook_id, 'webhook_event': event})
        return result.get('verification_status') == 'SUCCESS'


def provider_id(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', value):
        raise PayPalError('INVALID_PROVIDER_RESPONSE')
    return value


def money(value, currency):
    if not isinstance(value, dict) or value.get('currency_code') != currency or not isinstance(value.get('value'), str):
        raise PayPalError('AMOUNT_MISMATCH')
    try:
        result = Decimal(value['value'])
        if not result.is_finite() or result < 0 or result != result.quantize(Decimal('0.01')):
            raise PayPalError('AMOUNT_MISMATCH')
        return result
    except (InvalidOperation, ValueError):
        raise PayPalError('AMOUNT_MISMATCH') from None
