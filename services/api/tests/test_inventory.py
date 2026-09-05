import os
from decimal import Decimal

os.environ.setdefault('DATABASE_URL', 'sqlite://')

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models import Base, Product


@pytest.fixture
def client():
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    def session():
        with Session(engine) as db:
            yield db
    app.dependency_overrides[get_db] = session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    engine.dispose()


def supplier_data(**changes):
    return dict(name='Demo Supplier', supplier_type='tour_operator', contact_name='Private Contact', email='private@example.invalid', phone='PRIVATE PHONE', website='https://example.invalid', notes='PRIVATE NOTES', active=True, **changes)


def tour_data(supplier_id, **changes):
    data = dict(supplier_id=supplier_id, name='Demo Rafting', slug='demo-rafting', short_description='Demo experience', description='Demo only', category='Adventure', duration='Half day', retail_price='85.00', supplier_cost='50.00', active=True, featured=True)
    return data | changes


def create_tour(client, **changes):
    supplier = client.post('/ops/suppliers', json=supplier_data()).json()
    response = client.post('/ops/tours', json=tour_data(supplier['id'], **changes))
    assert response.status_code == 201, response.text
    return response.json()


def image_data(**changes):
    return dict(image_url='/images/rafting.webp', alt_text='Demo rafting image', sort_order=0, is_primary=False) | changes


def test_health_preserved(client):
    assert client.get('/').status_code == 200
    assert client.get('/health').json()['status'] == 'ok'


def test_public_active_detail_filters_and_boundary(client):
    tour = create_tour(client)
    create_tour(client, slug='inactive-tour', active=False)
    create_tour(client, slug='unfeatured-tour', featured=False, category='Nature')
    response = client.get('/public/tours')
    assert response.status_code == 200
    assert {row['slug'] for row in response.json()} == {'demo-rafting', 'unfeatured-tour'}
    assert len(client.get('/public/tours?featured=true').json()) == 1
    assert len(client.get('/public/tours?category=Nature').json()) == 1
    assert client.get('/public/tours?category=Missing').json() == []
    detail = client.get('/public/tours/demo-rafting')
    assert detail.status_code == 200
    assert detail.json()['retail_price'] == '85.00'
    for result in [response, detail]:
        for private in ['supplier_cost', 'gross_margin', 'supplier_id', 'supplier', 'email', 'phone', 'notes', 'contact_name', 'PRIVATE', 'private@example']:
            assert private not in result.text
    assert client.get('/public/tours/inactive-tour').status_code == 404
    assert client.get('/public/tours/missing').status_code == 404
    assert client.get(f"/ops/tours/{tour['id']}").json()['supplier']['notes'] == 'PRIVATE NOTES'


def test_supplier_create_update_and_missing(client):
    response = client.post('/ops/suppliers', json=supplier_data())
    assert response.status_code == 201
    supplier = response.json()
    payload = supplier_data() | {'name': 'Updated supplier', 'active': False, 'supplier_type': 'hotel', 'website': None}
    response = client.put(f"/ops/suppliers/{supplier['id']}", json=payload)
    assert response.status_code == 200
    assert response.json()['active'] is False
    assert client.get(f"/ops/suppliers/{supplier['id']}").json()['name'] == 'Updated supplier'
    assert len(client.get('/ops/suppliers').json()) == 1
    assert client.get('/ops/suppliers/9999').status_code == 404
    assert client.post('/ops/suppliers', json=payload | {'website': 'javascript:alert(1)'}).status_code == 422


def test_ops_pricing_and_tour_update(client):
    tour = create_tour(client)
    assert tour['gross_margin'] == '35.00'
    assert tour['supplier_cost'] == '50.00'
    payload = tour_data(tour['supplier_id'], retail_price='85.10', supplier_cost='50.03', name='Updated tour', active=False)
    response = client.put(f"/ops/tours/{tour['id']}", json=payload)
    assert response.status_code == 200, response.text
    assert response.json()['gross_margin'] == '35.07'
    assert response.json()['name'] == 'Updated tour'
    assert client.get('/public/tours').json() == []
    assert len(client.get('/ops/tours').json()) == 1
    assert Product(retail_price=Decimal('0.30'), supplier_cost=Decimal('0.10')).gross_margin == Decimal('0.20')


def test_validation_conflicts_and_missing_supplier(client):
    tour = create_tour(client)
    data = tour_data(tour['supplier_id'])
    assert client.post('/ops/tours', json=data).status_code == 409
    for changes in [{'retail_price': '-1'}, {'supplier_cost': '1.001'}, {'retail_price': 85.1}, {'slug': 'Bad Slug'}, {'minimum_age': -1}, {'product_type': 'hotel'}, {'gross_margin': '35'}]:
        assert client.post('/ops/tours', json=data | changes).status_code == 422
    assert client.post('/ops/tours', json=data | {'supplier_id': 99999}).status_code == 404
    assert client.get('/ops/tours/99999').status_code == 404


def test_image_primary_order_ownership_and_removal(client):
    tour = create_tour(client)
    base = f"/ops/tours/{tour['id']}/images"
    first = client.post(base, json=image_data(sort_order=10))
    assert first.status_code == 201
    assert first.json()['is_primary'] is True
    first_id = first.json()['id']
    second = client.post(base, json=image_data(image_url='https://example.invalid/second.jpg', sort_order=5, is_primary=True)).json()
    images = client.get(base).json()
    assert [image['id'] for image in images] == [second['id'], first_id]
    assert sum(image['is_primary'] for image in images) == 1
    assert images[0]['is_primary'] is True
    response = client.put(f'{base}/{first_id}', json=image_data(sort_order=0, is_primary=True, alt_text='Updated alt'))
    assert response.status_code == 200
    detail = client.get('/public/tours/demo-rafting').json()
    assert detail['primary_image']['id'] == first_id
    assert detail['images'][0]['alt_text'] == 'Updated alt'
    other = create_tour(client, slug='other-tour')
    other_base = f"/ops/tours/{other['id']}/images"
    assert client.put(f'{other_base}/{first_id}', json=image_data()).status_code == 404
    assert client.delete(f'{other_base}/{first_id}').status_code == 404
    assert client.delete(f'{base}/{first_id}').status_code == 204
    assert client.get(base).json()[0]['is_primary'] is True
    assert client.delete(f"{base}/{second['id']}").status_code == 204
    assert client.get('/public/tours/demo-rafting').json()['primary_image'] is None
    assert client.get(base).json() == []


@pytest.mark.parametrize('url', ['javascript:alert(1)', 'file:///etc/passwd', '//example.invalid/image.png', '/images/../private', 'https://user:pass@example.invalid/image.jpg'])
def test_unsafe_image_urls(client, url):
    tour = create_tour(client)
    assert client.post(f"/ops/tours/{tour['id']}/images", json=image_data(image_url=url)).status_code == 422
