from datetime import date, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.exc import IntegrityError

from app.availability_rules import utcnow
from app.models import Availability, Product, Reservation, SupplierConfirmationEvent
from test_inventory import client, create_tour
from test_bookings import inspect_db, payload, submit


def availability(tour, **changes):
    return dict(product_id=tour['id'], date=str(date.today() + timedelta(days=30)), status='available', source='manual',
                last_checked_at=utcnow().isoformat(), notes='PRIVATE INVENTORY NOTE') | changes


def booking(client):
    tour = create_tour(client)
    submit(client)
    return tour, client.get('/ops/bookings').json()[0]


def command(row, kind, **changes):
    return dict(command_id=str(uuid4()), expected_version=row['version'], event_type=kind, occurred_at=utcnow().isoformat()) | changes


def record(client, row, kind, **changes):
    response = client.post(f"/ops/bookings/{row['id']}/supplier-events", json=command(row, kind, **changes))
    assert response.status_code == 200, response.text
    return response.json()


def test_create_edit_nullable_capacity_and_unique_date(client):
    tour = create_tour(client)
    data = availability(tour)
    response = client.post('/ops/availability', json=data)
    assert response.status_code == 201, response.text
    row = response.json()
    assert row['capacity'] is row['remaining_capacity'] is None
    assert not row['stale'] and row['version'] == 1
    assert client.post('/ops/availability', json=data).status_code == 409
    edit = data | dict(expected_version=1, status='limited', capacity=12, remaining_capacity=2, source='supplier')
    updated = client.put(f"/ops/availability/{row['id']}", json=edit)
    assert updated.status_code == 200, updated.text
    assert updated.json()['remaining_capacity'] == 2 and updated.json()['version'] == 2
    assert client.put(f"/ops/availability/{row['id']}", json=edit).status_code == 409
    assert client.put(f"/ops/availability/{row['id']}", json=edit | dict(expected_version=2, date='2099-01-01')).status_code == 409
    assert len(client.get('/ops/availability').json()) == 1


@pytest.mark.parametrize('changes', [dict(capacity=-1), dict(remaining_capacity=-1), dict(capacity=2, remaining_capacity=3),
    dict(capacity=0), dict(remaining_capacity=0), dict(capacity=2.5), dict(status='sold_out'), dict(source='magic'),
    dict(last_checked_at=None), dict(last_checked_at='2099-01-01T00:00:00Z'), dict(last_checked_at='2026-01-01T00:00:00'), dict(capacity=2147483648)])
def test_inventory_validation(client, changes):
    tour = create_tour(client)
    assert client.post('/ops/availability', json=availability(tour, **changes)).status_code == 422
    assert client.get('/ops/availability').json() == []


def test_unknown_unavailable_freshness_filters_and_public_allowlist(client):
    tour = create_tour(client)
    day = availability(tour)['date']
    path = f"/public/tours/{tour['slug']}/availability?date={day}"
    assert client.get(path).json() == dict(date=day, status='unknown', request_required=True)
    row = client.post('/ops/availability', json=availability(tour, status='unknown', last_checked_at=None)).json()
    assert row['status'] == 'unknown' and row['stale']
    for status in ['unavailable', 'closed', 'limited', 'available']:
        response = client.put(f"/ops/availability/{row['id']}", json=availability(tour, status=status, expected_version=row['version']))
        assert response.status_code == 200, response.text
        row = response.json()
        public = client.get(path)
        assert public.json() == dict(date=day, status=status, request_required=True)
        assert public.headers['cache-control'] == 'no-store'
    stale = client.put(f"/ops/availability/{row['id']}", json=availability(tour, expected_version=row['version'], last_checked_at=(utcnow() - timedelta(hours=25)).isoformat())).json()
    assert stale['status'] == 'available' and stale['stale']
    assert client.get(path).json()['status'] == 'unknown'
    filters = f"date_from={day}&date_to={day}&product_id={tour['id']}&supplier_id={tour['supplier_id']}&status=available"
    assert len(client.get('/ops/availability?' + filters).json()) == 1
    assert client.get('/ops/availability?status=unknown').json() == []
    assert client.get('/ops/availability?date_from=2099-02-01&date_to=2099-01-01').status_code == 422
    assert client.get('/public/tours/missing/availability?date=' + day).status_code == 404
    assert client.get(path.replace(day, 'invalid')).status_code == 422


def test_contact_available_awaiting_confirmed_ready_and_preserved_reference(client):
    tour, row = booking(client)
    assert (row['status'], row['availability_status'], row['supplier_confirmation_status']) == ('new', 'unknown', 'not_requested')
    assert row['product_availability'] is None and row['needs_attention'] and not row['ready_for_payment']
    row = record(client, row, 'contacted', contact_method='whatsapp', notes='PRIVATE CONTACT', operator_identifier='DEMO operator')
    assert (row['status'], row['availability_status'], row['supplier_confirmation_status']) == ('pending_supplier', 'unknown', 'awaiting_supplier')
    assert row['supplier_contacted_at'] and row['supplier_events'][0]['contact_method'] == 'whatsapp'
    row = record(client, row, 'availability_checked', availability_status='available')
    assert (row['status'], row['availability_status'], row['supplier_confirmation_status']) == ('pending_supplier', 'available', 'awaiting_supplier')
    assert not row['ready_for_payment']
    row = record(client, row, 'follow_up', contact_method='phone', notes='Asked for reference')
    row = record(client, row, 'confirmed', reference='PRIVATE-REF-123', notes='PRIVATE RESPONSE')
    assert (row['status'], row['availability_status'], row['supplier_confirmation_status']) == ('confirmed', 'available', 'confirmed')
    assert row['ready_for_payment'] and not row['needs_attention'] and row['supplier_confirmed_at']
    assert row['trip']['status'] == 'inquiry'
    row = record(client, row, 'note', notes='Customer follow-up next')
    assert row['supplier_confirmation_reference'] == 'PRIVATE-REF-123'
    assert row['supplier_response_notes'] == 'PRIVATE RESPONSE'
    assert [e['event_type'] for e in row['supplier_events']] == ['contacted', 'availability_checked', 'follow_up', 'confirmed', 'note']
    assert row['supplier_events'][3]['reference'] == 'PRIVATE-REF-123'
    assert client.get('/ops/bookings?needs_attention=true').json() == []
    assert client.get('/ops/booking-summary').json() == dict(new_requests=0, awaiting_supplier=0, confirmed_today=1, needs_attention=0)
    # General date can subsequently sell out without erasing a held booking.
    assert client.post('/ops/availability', json=availability(tour, status='unavailable', remaining_capacity=0)).status_code == 201
    current = client.get(f"/ops/bookings/{row['id']}").json()
    assert current['ready_for_payment'] and current['product_availability']['status'] == 'unavailable'
    assert current['availability_status'] == 'available'


def test_decline_alternative_keeps_original_request_trip_pricing_and_history(client):
    tour, original = booking(client)
    row = record(client, original, 'contacted', contact_method='email')
    row = record(client, row, 'declined', notes='No space on this departure')
    assert (row['status'], row['availability_status'], row['supplier_confirmation_status']) == ('contacted', 'unavailable', 'declined')
    assert row['needs_attention'] and not row['ready_for_payment']
    other = create_tour(client, slug='alternative-tour')
    row = record(client, row, 'alternative_offered', alternative_product_id=other['id'], alternative_date=str(date.today() + timedelta(days=31)), alternative_time='10:30', notes='Ask customer about this option')
    assert row['supplier_confirmation_status'] == 'alternative_offered'
    for key in ['product_id', 'tour_name', 'requested_date', 'requested_time', 'unit_price', 'supplier_unit_cost', 'retail_total', 'gross_margin', 'trip']:
        assert row[key] == original[key]
    assert [e['event_type'] for e in row['supplier_events']] == ['contacted', 'declined', 'alternative_offered']
    assert row['supplier_events'][-1]['alternative_product_id'] == other['id']
    assert client.get('/ops/booking-summary').json()['needs_attention'] == 1
    assert len(client.get('/ops/bookings?supplier_status=alternative_offered').json()) == 1


def test_contradictions_correction_and_terminal_guards(client):
    _, row = booking(client)
    path = f"/ops/bookings/{row['id']}"
    assert client.put(path, json=dict(status='confirmed', expected_status='new')).status_code == 409
    row = record(client, row, 'confirmed', reference='KEEP IN HISTORY')
    for kind, fields in [('availability_checked', dict(availability_status='unavailable')), ('declined', {}), ('contacted', {})]:
        assert client.post(path + '/supplier-events', json=command(row, kind, contact_method='phone', **fields)).status_code == 409
    row = record(client, row, 'declined', notes='Supplier corrected mistaken confirmation')
    assert not row['ready_for_payment'] and row['supplier_confirmation_reference'] is None
    assert row['supplier_events'][0]['reference'] == 'KEEP IN HISTORY'
    assert client.post(path + '/supplier-events', json=command(row, 'availability_checked', availability_status='available')).status_code == 409
    row = record(client, row, 'contacted', contact_method='phone', notes='Recheck original request')
    assert row['availability_status'] == 'unknown'
    row = record(client, row, 'confirmed', reference='NEW REFERENCE')
    cancelled = client.put(path, json=dict(status='cancelled', expected_status='confirmed', expected_version=row['version'])).json()
    assert not cancelled['ready_for_payment'] and not cancelled['needs_attention']
    assert client.post(path + '/supplier-events', json=command(cancelled, 'confirmed')).status_code == 409
    assert record(client, cancelled, 'note', notes='Cancellation context')['supplier_confirmation_reference'] == 'NEW REFERENCE'


def test_versions_and_idempotent_supplier_commands(client):
    _, row = booking(client)
    path = f"/ops/bookings/{row['id']}"
    data = command(row, 'contacted', contact_method='whatsapp')
    first = client.post(path + '/supplier-events', json=data)
    assert first.status_code == 200, first.text
    assert client.post(path + '/supplier-events', json=data).json() == first.json()
    assert client.post(path + '/supplier-events', json=data | {'notes': 'Different command'}).status_code == 409
    assert client.post(path + '/supplier-events', json=command(row, 'declined')).status_code == 409
    assert client.put(path, json=dict(status='pending_supplier', expected_status='pending_supplier', expected_version=1, internal_notes='stale')).status_code == 409
    assert len(client.get(path).json()['supplier_events']) == 1
    assert client.get(path).json()['internal_notes'] is None


def test_multirow_event_failure_rolls_back_state_version_and_history(client):
    _, row = booking(client)
    row = record(client, row, 'contacted', contact_method='phone')
    def fail(*args):
        raise IntegrityError('simulated event insert failure', {}, Exception('failure'))
    event.listen(SupplierConfirmationEvent, 'before_insert', fail)
    try:
        response = client.post(f"/ops/bookings/{row['id']}/supplier-events", json=command(row, 'confirmed', reference='NOT SAVED'))
        assert response.status_code == 409
    finally:
        event.remove(SupplierConfirmationEvent, 'before_insert', fail)
    assert client.get(f"/ops/bookings/{row['id']}").json() == row


@pytest.mark.parametrize('kind, changes', [('contacted', {}), ('follow_up', {}), ('note', {}), ('alternative_offered', {}),
    ('confirmed', {'availability_status': 'unavailable'}), ('declined', {'availability_status': 'available'}),
    ('availability_checked', {}), ('note', {'notes': 'test', 'alternative_date': '2099-01-01'}),
    ('alternative_offered', {'alternative_date': '2000-01-01'}), ('confirmed', {'occurred_at': '2099-01-01T00:00:00Z'})])
def test_event_field_validation(client, kind, changes):
    _, row = booking(client)
    assert client.post(f"/ops/bookings/{row['id']}/supplier-events", json=command(row, kind, **changes)).status_code == 422
    assert client.get(f"/ops/bookings/{row['id']}").json()['supplier_events'] == []


def test_chronology_legacy_confirmation_and_supplier_snapshot(client):
    tour, row = booking(client)
    def legacy(db):
        booking = db.get(Reservation, row['id'])
        booking.status = 'confirmed'  # old milestone 3 confirmation is not supplier verification
        other = create_tour(client, slug='new-supplier-tour')
        db.get(Product, tour['id']).supplier_id = other['supplier_id']
        db.commit()
    inspect_db(legacy)
    row = client.get(f"/ops/bookings/{row['id']}").json()
    assert not row['ready_for_payment'] and row['needs_attention']
    assert row['supplier']['id'] == tour['supplier_id']
    row = record(client, row, 'contacted', contact_method='other')
    assert row['supplier_events'][-1]['supplier_id'] == tour['supplier_id']
    old = (utcnow() - timedelta(days=1)).isoformat()
    assert client.post(f"/ops/bookings/{row['id']}/supplier-events", json=command(row, 'confirmed', occurred_at=old)).status_code == 409
    assert record(client, row, 'note', occurred_at=old, notes='Historical context')['status'] == 'pending_supplier'


def test_public_privacy_and_immutable_receipt_after_confirmation(client):
    tour = create_tour(client)
    data = payload()
    receipt = submit(client, data).json()
    row = client.get('/ops/bookings').json()[0]
    row = record(client, row, 'confirmed', reference='PRIVATE-REFERENCE', notes='PRIVATE RESPONSE')
    client.post('/ops/availability', json=availability(tour, capacity=12, remaining_capacity=7))
    assert submit(client, data).json() == receipt
    for response in [client.get('/public/tours'), client.get('/public/tours/demo-rafting'),
                     client.get('/public/tours/demo-rafting/availability?date=' + data['requested_date']), submit(client, data)]:
        for private in ['PRIVATE', 'supplier_cost', 'supplier_unit_cost', 'gross_margin', 'supplier_confirmation', 'supplier_events',
                        'capacity', 'last_checked_at', 'supplier_contacted_at', 'operator_identifier', 'private@example.invalid']:
            assert private not in response.text
    assert client.get(f"/public/bookings/{row['id']}").status_code == 404
    assert client.delete(f"/ops/bookings/{row['id']}/supplier-events/1").status_code in (404, 405)


def test_identical_retry_without_explicit_event_time_is_idempotent(client):
    _, row = booking(client)
    data = dict(command_id=str(uuid4()), expected_version=row['version'], event_type='contacted', contact_method='phone')
    path = f"/ops/bookings/{row['id']}/supplier-events"
    first = client.post(path, json=data)
    assert first.status_code == 200, first.text
    assert client.post(path, json=data).json() == first.json()
    assert len(client.get(f"/ops/bookings/{row['id']}").json()['supplier_events']) == 1
