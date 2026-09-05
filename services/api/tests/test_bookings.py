from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.main import app
from app.models import Customer, Product, Reservation, Traveler, Trip, TripTraveler
from test_inventory import client, create_tour


def payload(**changes):
    return dict(idempotency_key=str(uuid4()), tour_slug='demo-rafting',
        requested_date=str(date.today() + timedelta(days=30)), requested_time='09:30',
        customer=dict(first_name='Demo', last_name='Visitor', email='  DEMO@Example.invalid ', phone='555-0100'),
        party_size=2,
        travelers=[dict(first_name='Demo', last_name='Visitor', traveler_type='adult'), dict(first_name='Junior', last_name='Visitor', traveler_type='child')],
        customer_notes='Demo special request') | changes


def inspect_db(fn):
    generator = app.dependency_overrides[get_db]()
    db = next(generator)
    try:
        return fn(db)
    finally:
        generator.close()


def submit(client, data=None):
    response = client.post('/public/booking-requests', json=data or payload())
    assert response.status_code == 201, response.text
    return response


def test_creates_entire_graph_and_private_snapshot(client):
    create_tour(client)
    response = submit(client)
    receipt = response.json()
    assert receipt['reference'].startswith('VV-')
    assert receipt['status'] == 'new'
    assert receipt['party_size'] == 2
    assert 'confirm availability' in receipt['message']
    assert set(receipt) == {'reference', 'status', 'tour_name', 'requested_date', 'party_size', 'customer_name', 'message'}
    def verify(db):
        assert db.scalar(select(func.count()).select_from(Customer)) == 1
        assert db.scalar(select(func.count()).select_from(Trip)) == 1
        assert db.scalar(select(func.count()).select_from(Reservation)) == 1
        assert db.scalar(select(func.count()).select_from(Traveler)) == 2
        assert db.scalar(select(func.count()).select_from(TripTraveler)) == 2
        booking = db.scalar(select(Reservation))
        assert booking.trip.reference == receipt['reference']
        assert booking.trip.status == 'inquiry'
        assert booking.quantity == booking.trip.party_size == 2
        assert booking.trip.customer.email == 'demo@example.invalid'
        assert booking.unit_price == Decimal('85.00')
        assert booking.supplier_unit_cost == Decimal('50.00')
        assert booking.gross_margin == Decimal('70.00')
        assert {link.traveler.first_name for link in booking.trip.traveler_links} == {'Demo', 'Junior'}
    inspect_db(verify)


def test_snapshots_do_not_follow_product_changes(client):
    create_tour(client)
    data = payload()
    receipt = submit(client, data).json()
    def change_price(db):
        tour = db.scalar(select(Product))
        tour.retail_price = Decimal('999.00')
        tour.supplier_cost = Decimal('900.00')
        tour.name = 'Changed product name'
        db.commit()
    inspect_db(change_price)
    booking = client.get('/ops/bookings').json()[0]
    assert booking['unit_price'] == '85.00'
    assert booking['supplier_unit_cost'] == '50.00'
    assert booking['gross_margin'] == '70.00'
    assert booking['tour_name'] == 'Demo Rafting'
    assert submit(client, data).json() == receipt


@pytest.mark.parametrize('changes', [dict(active=False), dict(product_type='hotel')])
def test_unavailable_or_non_tour_rejected(client, changes):
    create_tour(client)
    def change(db):
        product = db.scalar(select(Product))
        for key, value in changes.items():
            setattr(product, key, value)
        db.commit()
    inspect_db(change)
    assert client.post('/public/booking-requests', json=payload()).status_code == 404
    assert inspect_db(lambda db: db.scalar(select(func.count()).select_from(Customer))) == 0


@pytest.mark.parametrize('changes', [
    {'party_size': 0}, {'party_size': -1}, {'party_size': 51}, {'party_size': 1}, {'party_size': 2.0},
    {'requested_date': '2020-02-30'}, {'requested_date': '2000-01-01'}, {'travelers': []},
    {'start_date': '2099-02-01', 'end_date': '2099-01-01'},
    {'customer': {'first_name': ' ', 'last_name': 'Test', 'email': 'invalid'}},
    {'internal_notes': 'must reject'}, {'unit_price': '1.00'},
    {'travelers': [{'first_name': 'Demo', 'last_name': 'Child', 'date_of_birth': '2099-01-01'}]},
    {'customer': {'first_name': 'Demo', 'last_name': 'Test', 'email': 'demo@example.invalid', 'notes': 'PRIVATE INJECTION'}},
])
def test_public_validation(client, changes):
    create_tour(client)
    assert client.post('/public/booking-requests', json=payload(**changes)).status_code == 422


def test_idempotency_and_different_payload_conflict(client):
    create_tour(client)
    data = payload()
    first = submit(client, data).json()
    assert submit(client, data).json() == first
    assert client.post('/public/booking-requests', json=data | {'customer_notes': 'Changed'}).status_code == 409
    assert inspect_db(lambda db: db.scalar(select(func.count()).select_from(Reservation))) == 1


def test_normalized_customer_and_exact_traveler_reuse_without_overwrite(client):
    create_tour(client)
    first = payload()
    submit(client, first)
    def private_notes(db):
        customer = db.scalar(select(Customer))
        customer.notes = 'PRIVATE CUSTOMER NOTES'
        db.commit()
    inspect_db(private_notes)
    second = payload(customer=dict(first_name='Submitted', last_name='Different', email='demo@example.invalid', phone='NEW PHONE'))
    receipt = submit(client, second).json()
    assert receipt['customer_name'] == 'Submitted Different'
    def verify(db):
        assert db.scalar(select(func.count()).select_from(Customer)) == 1
        assert db.scalar(select(func.count()).select_from(Traveler)) == 2
        assert db.scalar(select(func.count()).select_from(TripTraveler)) == 4
        customer = db.scalar(select(Customer))
        assert customer.first_name == 'Demo'
        assert customer.phone == '555-0100'
        assert customer.notes == 'PRIVATE CUSTOMER NOTES'
    inspect_db(verify)
    detail = client.get('/ops/bookings').json()[0]
    assert detail['submitted_contact']['first_name'] == 'Submitted'


def test_atomic_rollback_when_reservation_insert_fails(client):
    create_tour(client)
    def fail_insert(*args):
        raise IntegrityError('simulated constraint violation', {}, Exception('failure'))
    event.listen(Reservation, 'before_insert', fail_insert)
    try:
        assert client.post('/public/booking-requests', json=payload()).status_code == 409
    finally:
        event.remove(Reservation, 'before_insert', fail_insert)
    for model in [Customer, Traveler, Trip, TripTraveler, Reservation]:
        assert inspect_db(lambda db: db.scalar(select(func.count()).select_from(model))) == 0


def test_ops_inbox_detail_status_notes_and_public_privacy(client):
    create_tour(client)
    data = payload()
    receipt = submit(client, data).json()
    booking = client.get('/ops/bookings?status=new').json()[0]
    assert booking['reference'] == receipt['reference']
    assert len(booking['travelers']) == 2
    assert booking['retail_total'] == '170.00'
    assert booking['gross_margin'] == '70.00'
    path = f"/ops/bookings/{booking['id']}"
    assert client.get(path).json()['status'] == 'new'  # reading does not confirm
    updated = client.put(path, json={'status': 'contacted', 'expected_status': 'new', 'internal_notes': 'PRIVATE FOLLOW-UP'} )
    assert updated.status_code == 200, updated.text
    assert client.get('/ops/bookings?status=new').json() == []
    assert client.get('/ops/bookings?status=contacted').json()[0]['internal_notes'] == 'PRIVATE FOLLOW-UP'
    assert client.get(path).json()['trip']['status'] == 'inquiry'
    assert client.put(path, json={'status': 'completed', 'expected_status': 'contacted'}).status_code == 409
    assert client.put(path, json={'status': 'confirmed', 'expected_status': 'new'}).status_code == 409
    confirmed = client.put(path, json={'status': 'confirmed', 'expected_status': 'contacted', 'internal_notes': 'PRIVATE FOLLOW-UP', 'trip_status': 'planning'})
    assert confirmed.status_code == 200
    assert confirmed.json()['trip']['status'] == 'planning'
    assert client.get('/ops/bookings/99999').status_code == 404
    assert submit(client, data).json() == receipt  # immutable, safe own receipt
    for url in ['/public/booking-requests', f"/public/bookings/{booking['id']}", '/public/customers']:
        assert client.get(url).status_code in [404, 405]
    for text in [client.get('/public/tours').text, submit(client, data).text]:
        for private in ['supplier_unit_cost', 'supplier_cost', 'gross_margin', 'internal_notes', 'PRIVATE FOLLOW-UP', 'email', 'phone']:
            assert private not in text


def test_reference_collision_rolls_back_and_retries(client, monkeypatch):
    from app import booking_service
    create_tour(client)
    first = submit(client).json()
    original = booking_service.new_reference
    references = iter([first['reference'], original()])
    monkeypatch.setattr(booking_service, 'new_reference', lambda: next(references))
    second = submit(client, payload(customer={'first_name': 'Second', 'last_name': 'Demo', 'email': 'second@example.invalid'})).json()
    assert second['reference'] != first['reference']
    assert inspect_db(lambda db: db.scalar(select(func.count()).select_from(Trip))) == 2
    assert inspect_db(lambda db: db.scalar(select(func.count()).select_from(Customer))) == 2
