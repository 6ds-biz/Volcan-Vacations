from copy import deepcopy
from datetime import date,time,timedelta
from decimal import Decimal
from sqlalchemy import select,func
import pytest
from app import models as m
from app.import_transportation import import_catalog,load_catalog
from app.transport_service import search,stale
from app.availability_rules import utcnow
from test_inventory import client,create_tour
from test_bookings import inspect_db,submit
from test_internal import add_user,signin

BASE='/ops/transportation'

def catalog(client):
    def seed(db):
        r=import_catalog(db,load_catalog());db.commit();return r
    result=inspect_db(seed)
    assert result['routes_created']==24
    return client.get(BASE+'/routes').json()

def first_service(client):
    rows=catalog(client)
    return rows[0]['services'][0]

def schedule_data(service,**changes):
    return dict(vendor_service_id=service['id'],departure_time='13:30',days_of_week=[0],effective_from='2026-09-01',effective_to='2026-09-30',source_url='https://ridecr.com/shuttle/',last_verified_at=utcnow().isoformat(),active=True)|changes

def rate_data(service,**changes):
    return dict(vendor_service_id=service['id'],rate_kind='vendor_rate',unit_basis='per_person',currency='USD',vendor_cost='40.00',vv_retail='55.00',effective_from='2026-09-01',effective_to='2026-09-30')|changes

def test_nodes_direction_and_duplicate_protection(client):
    a=client.post(BASE+'/nodes',json=dict(name='A',slug='a',node_type='airport')).json()
    b=client.post(BASE+'/nodes',json=dict(name='B',slug='b',node_type='destination')).json()
    assert client.post(BASE+'/nodes',json=dict(name='Duplicate',slug='a',node_type='airport')).status_code==409
    data=dict(origin_node_id=a['id'],destination_node_id=b['id'],source_url='https://ridecr.com/shuttle/',source_checked_at=utcnow().isoformat())
    assert client.post(BASE+'/routes',json=data).status_code==201
    assert client.post(BASE+'/routes',json=data).status_code==409
    assert client.post(BASE+'/routes',json=data|dict(origin_node_id=b['id'],destination_node_id=a['id'])).status_code==201
    assert client.post(BASE+'/routes',json=data|dict(destination_node_id=a['id'])).status_code==422
    assert client.post(BASE+'/routes',json=data|dict(source_url='https://www.interbusonline.com/our-routes/')).status_code==422
    assert client.post(BASE+'/nodes',json=dict(name='Missing geography',slug='missing',node_type='city',destination_id=999999)).status_code==404

def test_import_idempotent_overlap_only_preserves_manual_edits(client):
    routes=catalog(client)
    assert len(routes)==24
    assert sum(len(r['services']) for r in routes)==30
    assert sum(len(s['schedules']) for r in routes for s in r['services'])==35
    overlap={(r['origin']['slug'],r['destination']['slug']) for r in routes for s in r['services'] if s['supplier_name']=='Interbus'}
    assert overlap=={('la-fortuna','guapiles'),('la-fortuna','monteverde'),('la-fortuna','tamarindo'),('guapiles','la-fortuna'),('manuel-antonio','la-fortuna'),('manuel-antonio','monteverde')}
    def repeat(db):
        supplier=db.scalar(select(m.Supplier).where(m.Supplier.name=='RideCR'));supplier.notes='Keep private relationship';supplier.relationship_status='contracted'
        schedule=db.scalar(select(m.TransportSchedule));schedule.departure_time=time(6,17);schedule.active=False
        db.commit()
        report=import_catalog(db,load_catalog());db.commit()
        assert all(report[k]==0 for k in report)
        assert supplier.notes=='Keep private relationship' and supplier.relationship_status=='contracted'
        assert schedule.departure_time==time(6,17) and not schedule.active
        assert db.scalar(select(func.count()).select_from(m.TransportRate))==0
    inspect_db(repeat)

@pytest.mark.parametrize('kind',['shared_shuttle','private_transfer','lake_crossing'])
def test_vendor_service_types_and_linkage(client,kind):
    s=first_service(client)
    data=dict(supplier_id=s['supplier_id'],route_id=s['route_id'],service_type=kind)
    response=client.post(BASE+'/services',json=data)
    assert response.status_code==(409 if kind=='shared_shuttle' else 201)
    assert client.post(BASE+'/services',json=data|dict(route_id=99999)).status_code==404

def test_search_weekday_dates_inactive_ready_capacity_and_timezone(client):
    service=first_service(client)
    # Isolate the test recurrence from the imported departures.
    def clear(db):
        for s in db.scalars(select(m.TransportSchedule)):s.active=False
        db.commit()
    inspect_db(clear)
    response=client.post(BASE+'/schedules',json=schedule_data(service));assert response.status_code==201,response.text
    schedule=response.json()
    route=client.get(BASE+f'/routes/{service["route_id"]}').json()
    query=dict(origin=route['origin']['id'],destination=route['destination']['id'],travel_date='2026-09-07',party_size=4)
    def lookup(**kw):return client.get(BASE+'/search',params=query|kw).json()
    result=lookup();assert len(result)==1 and result[0]['availability']=='unknown'
    assert result[0]['departure_at'].endswith('-06:00')
    assert lookup(travel_date='2026-09-08')==[]
    assert lookup(travel_date='2026-10-05')==[]
    assert lookup(ready_time='13:31')==[]
    assert len(lookup(ready_time='13:30'))==1
    assert lookup(ready_time='13:20',buffer_minutes=11)==[]
    assert lookup(ready_time='23:00',buffer_minutes=120)==[]
    assert client.get(BASE+'/search',params=query|dict(ready_time='13:00+01:00')).status_code==422
    def capacity(db):
        db.get(m.VendorTransportService,service['id']).capacity=3;db.commit()
    inspect_db(capacity);assert lookup()==[];assert len(lookup(party_size=3))==1
    assert client.put(BASE+f'/schedules/{schedule["id"]}',json=schedule_data(service,active=False,expected_version=schedule['version'])).status_code==200
    assert lookup(party_size=1)==[]

def test_interbus_unknown_recurrence_is_not_recommended(client):
    rows=catalog(client);route=next(r for r in rows if r['origin']['slug']=='la-fortuna' and r['destination']['slug']=='monteverde')
    result=client.get(BASE+'/search',params=dict(origin=route['origin']['id'],destination=route['destination']['id'],travel_date='2026-09-07',party_size=1)).json()
    assert result and all(r['supplier_name']=='RideCR' for r in result)
    interbus=next(s for s in route['services'] if s['supplier_name']=='Interbus')
    assert interbus['schedules'][0]['days_of_week']==[]
    assert interbus['schedules'][0]['needs_review']

def test_dated_rate_revision_and_reference_boundary(client):
    service=first_service(client)
    first=client.post(BASE+'/rates',json=rate_data(service));assert first.status_code==201,first.text
    assert first.json()['vendor_cost']=='40.00'
    second=client.post(BASE+'/rates',json=rate_data(service,vendor_cost='45.00',supersedes_id=first.json()['id']));assert second.status_code==201
    assert client.post(BASE+'/rates',json=rate_data(service,supersedes_id=first.json()['id'])).status_code==409
    assert client.post(BASE+'/rates',json=rate_data(service,rate_kind='public_reference',public_reference_price='70.00')).status_code==422
    reference=client.post(BASE+'/rates',json=rate_data(service,rate_kind='public_reference',vendor_cost=None,vv_retail=None,public_reference_price='70.00'));assert reference.status_code==201
    assert reference.json()['vendor_cost'] is None and reference.json()['vv_retail'] is None
    assert client.post(BASE+'/rates',json=rate_data(service,effective_to='2026-08-01')).status_code==422
    assert client.post(BASE+'/rates',json=rate_data(service,vendor_cost=40.1)).status_code==422
    def snapshot(db):assert db.get(m.TransportRate,first.json()['id']).vendor_cost==Decimal('40.00')
    inspect_db(snapshot)

def test_agreement_supplier_currency_date_bounds_and_private_unit(client):
    service=first_service(client)
    agreement=client.post(f'/ops/suppliers/{service["supplier_id"]}/agreements',json=dict(title='Test rate reference',effective_from='2026-09-01',effective_to='2026-09-30',currency='USD')).json()
    assert client.post(BASE+'/rates',json=rate_data(service,agreement_id=agreement['id'])).status_code==201
    assert client.post(BASE+'/rates',json=rate_data(service,agreement_id=agreement['id'],currency='CRC')).status_code==422
    assert client.post(BASE+'/rates',json=rate_data(service,agreement_id=agreement['id'],effective_to='2026-10-01')).status_code==422
    private=client.post(BASE+'/services',json=dict(supplier_id=service['supplier_id'],route_id=service['route_id'],service_type='private_transfer')).json()
    assert client.post(BASE+'/rates',json=rate_data(private)).status_code==422
    assert client.post(BASE+'/rates',json=rate_data(private,unit_basis='per_vehicle')).status_code==201

def test_freshness_and_controlled_tasks_idempotent(client):
    service=first_service(client)
    old=utcnow()-timedelta(days=31)
    assert stale(old) and stale(None) and not stale(utcnow())
    result=client.post(BASE+'/schedules',json=schedule_data(service,last_verified_at=old.isoformat()));assert result.status_code==201
    # Relative dates ensure this task test continues working after the source retrieval date.
    today=utcnow().date()
    client.post(BASE+'/rates',json=rate_data(service,effective_from=today.isoformat(),effective_to=(today+timedelta(days=10)).isoformat()))
    first=client.post(BASE+'/review-tasks');assert first.status_code==200 and first.json()['tasks_created']>=2
    assert client.post(BASE+'/review-tasks').json()['tasks_created']==0
    tasks=client.get('/ops/tasks').json()
    assert any(t['related_entity_type']=='transport_route' for t in tasks)
    assert any(t['title']=='Request updated transport rate' for t in tasks)

@pytest.mark.parametrize('role',['owner_admin','operations_partner','staff'])
def test_transport_role_and_public_boundaries(client,role):
    service=first_service(client);client.post(BASE+'/rates',json=rate_data(service))
    if role!='owner_admin':add_user(role);signin(client,role)
    detail=client.get(BASE+f'/routes/{service["route_id"]}');assert detail.status_code==200
    if role=='staff':
        for key in ('vendor_cost','vv_retail','rates_missing','agreement_id'):assert key not in detail.text
        assert client.post(BASE+'/rates',json=rate_data(service)).status_code==403
        assert client.post(BASE+'/review-tasks').status_code==403
        assert client.get(BASE+'/context').status_code==403
    else:
        assert 'vendor_cost' in detail.text
        assert client.post(BASE+'/rates',json=rate_data(service)).status_code==201
    assert client.get('/public/transportation/routes').status_code==404
    client.cookies.clear();assert client.get(BASE+'/routes').status_code==401

def test_existing_tour_booking_and_payment_economics_unchanged(client):
    tour=create_tour(client);booking=submit(client);assert booking.status_code==201
    before=client.get('/ops/bookings').json();tour_before=client.get(f'/ops/tours/{tour["id"]}').json()
    catalog(client)
    assert client.get('/ops/bookings').json()==before
    assert client.get(f'/ops/tours/{tour["id"]}').json()==tour_before
    assert client.get('/public/tours').status_code==200

def test_schedule_version_and_invalid_recurrence(client):
    s=first_service(client);data=schedule_data(s)
    assert client.post(BASE+'/schedules',json=data|dict(days_of_week=[7])).status_code==422
    assert client.post(BASE+'/schedules',json=data|dict(days_of_week=[1,1])).status_code==422
    assert client.post(BASE+'/schedules',json=data|dict(departure_time='12:00+02:00')).status_code==422
    row=client.post(BASE+'/schedules',json=data).json()
    assert client.put(BASE+f'/schedules/{row["id"]}',json=data).status_code==409
    update=data|dict(expected_version=row['version'],departure_time='14:00')
    assert client.put(BASE+f'/schedules/{row["id"]}',json=update).status_code==200
    assert client.put(BASE+f'/schedules/{row["id"]}',json=update).status_code==409
    history=client.get(f'/ops/audit?entity_type=transport_route&entity_id={s["route_id"]}').json()
    assert history and all(h['actor_name']=='Test owner' for h in history)

@pytest.mark.parametrize('inactive',['route','node','supplier'])
def test_inactive_route_node_or_vendor_excludes_search(client,inactive):
    rows=catalog(client);route=rows[0]
    query=dict(origin=route['origin']['id'],destination=route['destination']['id'],travel_date='2026-09-14',party_size=1)
    assert client.get(BASE+'/search',params=query).json()
    def disable(db):
        model,id=(m.CanonicalTransportRoute,route['id']) if inactive=='route' else (m.TransportNode,route['origin']['id']) if inactive=='node' else (m.Supplier,route['services'][0]['supplier_id'])
        db.get(model,id).active=False;db.commit()
    inspect_db(disable)
    assert client.get(BASE+'/search',params=query).json()==[]


def test_postgres_transport_constraints_and_import():
    import os
    from uuid import uuid4
    from sqlalchemy import create_engine,text
    from sqlalchemy.orm import Session
    from sqlalchemy.exc import IntegrityError
    from app.config import settings
    if os.environ.get('VV_TEST_POSTGRES')!='1':pytest.skip('Explicit PostgreSQL integration opt-in required')
    assert settings.environment=='development' and settings.database_url.startswith('postgresql')
    schema='vv_transport_test_'+uuid4().hex;admin=create_engine(settings.database_url);isolated=None
    try:
        with admin.begin() as db:db.execute(text(f'CREATE SCHEMA {schema}'))
        isolated=create_engine(settings.database_url,connect_args={'options':f'-csearch_path={schema}'})
        m.Base.metadata.create_all(isolated)
        with Session(isolated) as db:
            assert import_catalog(db,load_catalog())['routes_created']==24;db.commit()
            assert not any(import_catalog(db,load_catalog()).values());db.commit()
            route=db.scalar(select(m.CanonicalTransportRoute));service=db.scalar(select(m.VendorTransportService))
            route_values=dict(origin_node_id=route.origin_node_id,destination_node_id=route.destination_node_id,source='RideCR',source_url=route.source_url,source_checked_at=route.source_checked_at)
            service_id=service.id
        with Session(isolated) as db,pytest.raises(IntegrityError):
            db.add(m.CanonicalTransportRoute(**route_values));db.commit()
        with Session(isolated) as db,pytest.raises(IntegrityError):
            db.add(m.TransportRate(vendor_service_id=service_id,rate_kind='public_reference',unit_basis='per_person',currency='USD',vendor_cost=Decimal('10.00'),public_reference_price=Decimal('50.00'),effective_from=date(2026,9,1),effective_to=date(2026,9,30)));db.commit()
        with Session(isolated) as db:
            db.add(m.TransportRate(vendor_service_id=service_id,rate_kind='vendor_rate',unit_basis='per_person',currency='USD',vendor_cost=Decimal('10.25'),effective_from=date(2026,9,1),effective_to=date(2026,9,30)));db.commit()
            assert db.scalar(select(m.TransportRate)).vendor_cost==Decimal('10.25')
    finally:
        if isolated:isolated.dispose()
        with admin.begin() as db:db.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE'))
        admin.dispose()
