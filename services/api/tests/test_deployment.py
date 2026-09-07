"""Hosted routing/configuration checks. No external providers or live databases."""
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.config import Settings, settings
from app.main import app, create_app
from test_inventory import client
from test_payments import ready


def hosted_settings(**changes):
    return Settings(_env_file=None, **(dict(
        environment='preview', database_url='postgresql://demo:example@db.invalid/preview',
        allowed_origins='https://preview.example.invalid', allowed_origin_regex=None,
        public_web_url='https://preview.example.invalid', paypal_environment='sandbox',
    ) | changes))


@pytest.mark.parametrize('environment', ['preview', 'production'])
def test_hosted_api_has_no_operations_routes(environment):
    hosted = create_app(hosted_settings(environment=environment))
    ops_paths = {route.path for route in app.routes if route.path.startswith('/ops')}
    assert ops_paths
    with TestClient(hosted) as http:
        assert http.get('/health').json() == {'status': 'ok', 'service': 'volcan-vacations-api'}
        for path in ops_paths:
            concrete = path.replace('{supplier_id}', '1').replace('{tour_id}', '1').replace('{image_id}', '1').replace('{booking_id}', '1').replace('{availability_id}', '1')
            assert http.get(concrete).status_code == 404
            assert http.post(concrete, json={}).status_code == 404
        paths = http.get('/openapi.json').json()['paths']
        assert not any(path.startswith('/ops') for path in paths)
        assert '/public/tours' in paths
        assert '/public/booking-requests' in paths
        assert '/public/payments/session' in paths
        assert '/webhooks/paypal' in paths
        assert http.get('/public/payments/session').status_code == 404


def test_hosted_cors_allows_only_configured_origin():
    with TestClient(create_app(hosted_settings(allowed_origins='https://preview.example.invalid/'))) as http:
        headers = {'Origin': 'https://preview.example.invalid',
                   'Access-Control-Request-Method': 'POST',
                   'Access-Control-Request-Headers': 'Authorization,Content-Type'}
        allowed = http.options('/public/payments/session', headers=headers)
        assert allowed.status_code == 200
        assert allowed.headers['access-control-allow-origin'] == headers['Origin']
        assert 'access-control-allow-credentials' not in allowed.headers
        blocked = http.options('/public/payments/session', headers=headers | {'Origin': 'https://unlisted.example.invalid'})
        assert blocked.status_code == 400
        assert 'access-control-allow-origin' not in blocked.headers


@pytest.mark.parametrize('changes', [
    {'allowed_origins': '*'},
    {'allowed_origins': 'http://localhost:3000'},
    {'allowed_origins': 'https://anything.app.github.dev'},
    {'allowed_origins': 'https://preview.example.invalid/path'},
    {'allowed_origin_regex': '.*'},
    {'public_web_url': 'https://user:password@example.invalid'},
    {'public_web_url': 'https://example.invalid/pay#token=example'},
    {'public_web_url': 'https://anything.app.github.dev'},
    {'paypal_environment': 'live'},
    {'database_url': 'sqlite://'},
    {'environment': 'develpment'},
])
def test_hosted_configuration_rejects_unsafe_values(changes):
    with pytest.raises(ValidationError):
        hosted_settings(**changes)


def test_bootstrap_can_start_without_known_website_origin():
    config = hosted_settings(public_web_url=None, allowed_origins='')
    assert config.allowed_origins_list == []
    assert config.public_web_url is None


def test_database_url_normalization_and_safe_representation():
    config = hosted_settings(database_url='postgres://demo:private%25password@db.invalid/preview')
    assert config.database_url.startswith('postgresql://')
    assert 'private%25password' not in repr(config)


def test_payment_link_uses_configured_public_origin(client, monkeypatch):
    monkeypatch.setattr(settings, 'public_web_url', 'https://preview.example.invalid')
    _, booking, _ = ready(client)
    response = client.post(f"/ops/bookings/{booking['id']}/payment-link", json={'expected_version': booking['version']})
    assert response.status_code == 200
    assert response.json()['path'].startswith('https://preview.example.invalid/pay#token=')
    assert len(response.json()['path'].split('#token=')[1]) == 43


def test_hosted_link_without_base_url_does_not_mutate_booking(client, monkeypatch):
    _, booking, _ = ready(client)
    monkeypatch.setattr(settings, 'environment', 'preview')
    monkeypatch.setattr(settings, 'ops_web_url', 'https://ops.example.invalid')
    client.headers['Origin'] = 'https://ops.example.invalid'
    monkeypatch.setattr(settings, 'public_web_url', None)
    response = client.post(f"/ops/bookings/{booking['id']}/payment-link", json={'expected_version': booking['version']})
    assert response.status_code == 503
    assert client.get(f"/ops/bookings/{booking['id']}").json()['version'] == booking['version']
