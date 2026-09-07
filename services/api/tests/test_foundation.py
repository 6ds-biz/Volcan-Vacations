from datetime import date

import pytest
from sqlalchemy import select

from app.models import Destination, ProductDestination, ProductRate, SupplierAgreement
from app.seed_destinations import seed_reference
from test_inventory import client, create_tour, supplier_data, tour_data
from test_bookings import inspect_db, submit


def destination(client, slug, parent=None):
    body = dict(name=slug, slug=slug, parent_id=parent, destination_type='region')
    response = client.post('/ops/destinations', json=body)
    assert response.status_code == 201, response.text
    return response.json(), body


def agreement(client, supplier_id, **changes):
    data = dict(title='PRIVATE vendor terms', effective_from='2026-01-01', effective_to='2026-12-31', currency='USD') | changes
    response = client.post(f'/ops/suppliers/{supplier_id}/agreements', json=data)
    assert response.status_code == 201, response.text
    return response.json()


def rate(product_id, **changes):
    return dict(product_id=product_id, label='PRIVATE net per person', effective_from='2026-02-01', effective_to='2026-10-31', unit_type='per_person', net_amount='50.01', retail_amount='85.00') | changes


def test_tree_reparent_cycle_missing_parent_and_unique_slug(client):
    root, root_body = destination(client, 'country-anywhere')
    child, child_body = destination(client, 'region-anywhere', root['id'])
    leaf, _ = destination(client, 'zone-anywhere', child['id'])
    assert client.put(f"/ops/destinations/{root['id']}", json=root_body | {'parent_id':leaf['id']}).status_code == 409
    assert client.put(f"/ops/destinations/{child['id']}", json=child_body | {'parent_id':child['id']}).status_code == 409
    assert client.put(f"/ops/destinations/{child['id']}", json=child_body | {'parent_id':9999}).status_code == 404
    assert client.post('/ops/destinations', json=root_body).status_code == 409
    assert client.put(f"/ops/destinations/{child['id']}", json=child_body | {'parent_id':None}).status_code == 200
    rows = client.get('/ops/destinations').json()
    assert len(rows) == 3
    assert next(r for r in rows if r['id'] == root['id'])['parent_id'] is None


def test_multiple_product_destinations_optional_atomic_and_old_tour_update(client):
    tour = create_tour(client)
    path = f"/ops/products/{tour['id']}/destinations"
    assert client.get(path).json() == []
    a, _ = destination(client, 'outside-arenal')
    b, body = destination(client, 'another-region')
    assert len(client.put(path, json={'destination_ids':[a['id'],b['id']]}).json()) == 2
    assert client.put(path, json={'destination_ids':[a['id'],9999]}).status_code == 404
    assert len(client.get(path).json()) == 2
    assert client.put(path, json={'destination_ids':[a['id'],a['id']]}).status_code == 422
    assert client.put(f"/ops/tours/{tour['id']}", json=tour_data(tour['supplier_id'])).status_code == 200
    assert len(client.get(path).json()) == 2
    assert client.put(f"/ops/destinations/{b['id']}", json=body | {'active':False}).status_code == 200
    # Reference status is not inventory publication or a checkout requirement.
    assert client.get('/public/tours/demo-rafting').status_code == 200
    assert client.put(path, json={'destination_ids':[]}).json() == []


def test_supplier_multiple_services_independent_status_and_old_editor(client):
    tour = create_tour(client)
    path = f"/ops/suppliers/{tour['supplier_id']}/foundation"
    assert client.get(path).json() == {'relationship_status':'prospect','service_types':[]}
    profile = {'relationship_status':'rates_requested','service_types':['tour','transportation','hotel']}
    assert client.put(path, json=profile).status_code == 200
    assert client.put(f"/ops/suppliers/{tour['supplier_id']}", json=supplier_data()).status_code == 200
    assert set(client.get(path).json()['service_types']) == set(profile['service_types'])
    assert client.get(path).json()['relationship_status'] == 'rates_requested'
    assert client.get('/public/tours/demo-rafting').status_code == 200
    assert client.put(path, json=profile | {'service_types':['hotel','hotel']}).status_code == 422
    assert client.put(path, json=profile | {'relationship_status':'published'}).status_code == 422


def test_dated_rates_do_not_change_catalog_booking_or_public_privacy(client):
    tour = create_tour(client)
    receipt = submit(client).json()
    before = client.get('/ops/bookings').json()[0]
    row = agreement(client, tour['supplier_id'])
    response = client.post(f"/ops/agreements/{row['id']}/rates", json=rate(tour['id'], net_amount='1.23', retail_amount='999.99'))
    assert response.status_code == 201, response.text
    assert response.json()['net_amount'] == '1.23'
    after = client.get('/ops/bookings').json()[0]
    assert after == before
    assert client.get(f"/ops/tours/{tour['id']}").json()['supplier_cost'] == '50.00'
    public = client.get('/public/tours/demo-rafting').json()
    assert public['retail_price'] == '85.00'
    assert 'PRIVATE' not in str(public) + str(receipt)
    assert not {'relationship_status','service_types','agreements','rates','net_amount','documents','destinations'} & public.keys()


@pytest.mark.parametrize('changes', [
    {'net_amount':-1}, {'net_amount':50.01}, {'net_amount':'1.001'}, {'retail_amount':True},
    {'effective_from':'2025-12-31'}, {'effective_to':'2027-01-01'},
    {'effective_from':'2026-11-01','effective_to':'2026-10-01'}, {'unit_type':'per_package'},
])
def test_invalid_rate_money_dates_and_units(client, changes):
    tour = create_tour(client)
    row = agreement(client, tour['supplier_id'])
    assert client.post(f"/ops/agreements/{row['id']}/rates", json=rate(tour['id'], **changes)).status_code == 422
    assert client.get(f"/ops/agreements/{row['id']}/rates").json() == []


def test_cross_supplier_rates_and_documents_rejected(client):
    tour = create_tour(client)
    other = create_tour(client, slug='other-tour')
    row = agreement(client, tour['supplier_id'])
    assert client.post(f"/ops/agreements/{row['id']}/rates", json=rate(other['id'])).status_code == 422
    path = f"/ops/suppliers/{other['supplier_id']}/documents"
    assert client.post(path, json={'agreement_id':row['id'],'title':'PRIVATE contract','document_type':'contract'}).status_code == 422
    assert client.get(path).json() == []


@pytest.mark.parametrize('reference', [
    {'external_url':'javascript:alert(1)'}, {'external_url':'https://user:secret@example.invalid/contract'},
    {'external_url':'https://example.invalid/contract?token=private'}, {'storage_key':'../secret'},
    {'effective_date':'2026-12-01','expiration_date':'2026-01-01'},
])
def test_document_secret_url_and_invalid_metadata_rejected(client, reference):
    tour = create_tour(client)
    path = f"/ops/suppliers/{tour['supplier_id']}/documents"
    assert client.post(path, json={'title':'Contract','document_type':'contract'} | reference).status_code == 422


def test_document_reference_metadata_only_and_immutable_commercial_records(client):
    tour = create_tour(client)
    row = agreement(client, tour['supplier_id'], currency='CRC')
    path = f"/ops/suppliers/{tour['supplier_id']}/documents"
    response = client.post(path, json={'title':'PRIVATE contract','document_type':'contract','agreement_id':row['id'],
        'external_url':'https://example.invalid/contracts/reference','storage_key':'vendor/contract.pdf'})
    assert response.status_code == 201
    assert client.get(path).json()[0]['agreement_id'] == row['id']
    assert client.put(f"/ops/agreements/{row['id']}", json={'currency':'USD'}).status_code in (404,405)
    assert client.get('/public/suppliers').status_code == 404
    assert client.get('/public/transportation').status_code == 404
    assert client.get('/public/hotels').status_code == 404
    assert client.get('/public/packages').status_code == 404


def test_reference_seed_idempotent_preserves_operator_edits_no_inventory_mapping(client):
    assert inspect_db(seed_reference) == 18
    def edit(db):
        row = db.scalar(select(Destination).where(Destination.slug == 'arenal-la-fortuna'))
        row.name = 'Operator name'; row.active = False
        db.commit()
    inspect_db(edit)
    assert inspect_db(seed_reference) == 0
    rows = client.get('/ops/destinations').json()
    assert next(r for r in rows if r['slug']=='arenal-la-fortuna')['name'] == 'Operator name'
    assert any(r['slug']=='puerto-viejo' for r in rows)
    assert inspect_db(lambda db: db.scalar(select(ProductDestination))) is None
    assert inspect_db(lambda db: db.scalar(select(SupplierAgreement))) is None


def test_reference_seed_conflict_rolls_back_new_rows(client):
    destination(client, 'arenal-la-fortuna')  # wrong parent/type: do not overwrite it
    with pytest.raises(ValueError):
        inspect_db(seed_reference)
    assert len(client.get('/ops/destinations').json()) == 1
