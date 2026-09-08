from copy import deepcopy
import pytest
from sqlalchemy import select,func
from app import models as m
from app.page_layout_schema import PRESENTATION
from test_inventory import client,create_tour,image_data
from test_internal import add_user,signin
from test_bookings import inspect_db

def base(key):
 return dict(id=key,presentation=dict(order=0,width=12,visible=True,spacing='none',align='stretch',density='normal',surface='transparent',container='full',border='none'),responsive={})
def page(kind='owner-dashboard',widget='business-health'):
 return dict(schema_version=1,page_id=kind,sections=[dict(**base('s1'),columns=[dict(**base('c1'),widgets=[dict(**base('w1'),type=widget,config={})])])])
def media_config(asset='vv-pacific'):
 return dict(asset=asset,alt='',decorative=False,fit='cover',x=50,y=50,ratio='wide',radius='small',overlay='none',tablet={},mobile={},autoplay=False,muted=True,loop=False,controls=True,poster=None)
def write(client,path,p=None,version=0,method='post'):
 return getattr(client,method)('/ops/page-layouts/'+path,json=dict(expected_version=version,page=p or page()))
def test_owner_draft_is_separate_from_published(client):
 assert client.get('/ops/page-layouts/owner-dashboard').json()==dict(version=0,published=None,draft=None)
 assert write(client,'owner-dashboard/draft',method='put').json()['version']==1
 current=client.get('/ops/page-layouts/owner-dashboard').json();assert current['published'] is None and current['draft']==page()
 assert client.get('/ops/page-layouts/owner-dashboard/revisions').json()==[]

def test_publish_actor_and_immutable_revision(client):
 assert write(client,'owner-dashboard/publish').status_code==200
 state=client.get('/ops/page-layouts/owner-dashboard').json();assert state['published']==page()
 revision=client.get('/ops/page-layouts/owner-dashboard/revisions').json()[0];assert revision['number']==1 and revision['actor_name']=='Test owner'
 def mutate(db):
  r=db.get(m.PageLayoutRevision,revision['id']);r.content={};db.commit()
 with pytest.raises(ValueError,match='immutable'):inspect_db(mutate)
 assert client.get('/ops/page-layouts/owner-dashboard').json()['published']==page()

def test_restore_creates_new_revision_and_preserves_history(client):
 write(client,'owner-dashboard/publish');old=client.get('/ops/page-layouts/owner-dashboard/revisions').json()[0]
 changed=page();changed['sections'][0]['responsive']['tablet']={'width':6}
 assert write(client,'owner-dashboard/publish',changed,1).status_code==200
 response=client.post('/ops/page-layouts/owner-dashboard/restore',json=dict(expected_version=2,revision_id=old['id']));assert response.status_code==200 and response.json()['page']==page()
 revisions=client.get('/ops/page-layouts/owner-dashboard/revisions').json();assert [r['number'] for r in revisions]==[3,2,1];assert revisions[0]['action']=='restored'

def test_stale_draft_publish_and_restore_rejected(client):
 write(client,'owner-dashboard/publish');r=client.get('/ops/page-layouts/owner-dashboard/revisions').json()[0]
 assert write(client,'owner-dashboard/publish').status_code==409
 assert write(client,'owner-dashboard/draft',method='put').status_code==409
 assert client.post('/ops/page-layouts/owner-dashboard/restore',json=dict(expected_version=0,revision_id=r['id'])).status_code==409
 assert len(client.get('/ops/page-layouts/owner-dashboard/revisions').json())==1

@pytest.mark.parametrize('role',['operations_partner','staff'])
def test_non_owner_denied_all_editing_even_with_owner_profile(client,role):
 add_user(role,'Owner');signin(client,role)
 for action,method in [('draft','put'),('publish','post')]:assert write(client,'transportation-detail/'+action,page('transportation-detail','rates'),method=method).status_code==403
 assert client.get('/ops/page-layouts/transportation-detail/revisions').status_code==403
 assert client.post('/ops/page-layouts/transportation-detail/restore',json=dict(expected_version=0,revision_id=1)).status_code==403
 assert client.get('/ops/page-layouts/owner-dashboard').status_code==403

def test_staff_can_read_transport_template_without_private_draft(client):
 assert write(client,'transportation-detail/draft',page('transportation-detail','rates'),method='put').status_code==200
 add_user();signin(client)
 assert client.get('/ops/page-layouts/transportation-detail').json()==dict(version=1,published=None)
 assert client.get('/ops/page-layouts/booking-detail').status_code==403
 assert client.get('/ops/page-layouts/supplier-detail').status_code==403

@pytest.mark.parametrize('mutation',['unknown-widget','wrong-page','duplicate-id','width','device','config','html','version','duplicate-business','context'])
def test_invalid_layout_rejected_atomically(client,mutation):
 p=page();w=p['sections'][0]['columns'][0]['widgets'][0]
 if mutation=='unknown-widget':w['type']='script'
 elif mutation=='wrong-page':w['type']='rates'
 elif mutation=='duplicate-id':w['id']='c1'
 elif mutation=='width':p['sections'][0]['presentation']['width']=13
 elif mutation=='device':p['sections'][0]['responsive']['watch']={}
 elif mutation=='config':w['config']['supplier_cost']='123'
 elif mutation=='html':w.update(type='heading',config={'text':'<script>alert(1)</script>','level':'h2'})
 elif mutation=='version':p['schema_version']=2
 elif mutation=='duplicate-business':p['sections'][0]['columns'][0]['widgets'].append(dict(**base('w2'),type='business-health',config={}))
 elif mutation=='context':p['booking_id']=42
 assert write(client,'owner-dashboard/publish',p).status_code==422
 assert client.get('/ops/page-layouts/owner-dashboard').json()['version']==0

def test_media_focal_and_responsive_override_saved(client):
 p=page(widget='media');p['sections'][0]['columns'][0]['widgets'][0]['config']=media_config();p['sections'][0]['columns'][0]['widgets'][0]['config']['mobile']={'asset':'vv-nosara','x':77,'y':25}
 assert write(client,'owner-dashboard/publish',p).status_code==200
 assert client.get('/ops/page-layouts/owner-dashboard').json()['published']==p

@pytest.mark.parametrize('field,value',[('x',101),('overlay','url(x)'),('asset','https://evil.example/image'),('asset','missing-image'),('autoplay',True),('controls',False)])
def test_invalid_media_or_video_rejected(client,field,value):
 p=page(widget='media');c=media_config();c[field]=value
 if field=='autoplay':c['muted']=False
 p['sections'][0]['columns'][0]['widgets'][0]['config']=c
 assert write(client,'owner-dashboard/publish',p).status_code==422

def test_rights_review_draft_allowed_publish_rejected(client):
 assets=client.get('/ops/page-layouts/media').json();assert next(a for a in assets if a['id']=='vv-arenal')['rights_status']=='NEEDS_RIGHTS_REVIEW'
 p=page(widget='media');p['sections'][0]['columns'][0]['widgets'][0]['config']=media_config('vv-arenal')
 assert write(client,'owner-dashboard/draft',p,method='put').status_code==200
 assert write(client,'owner-dashboard/publish',p,1).status_code==422
 assert client.get('/ops/page-layouts/owner-dashboard').json()['published'] is None

def test_product_image_metadata_has_no_inferred_rights_or_private_fields(client):
 tour=create_tour(client);image=client.post(f"/ops/tours/{tour['id']}/images",json=image_data()).json()
 response=client.get('/ops/page-layouts/media');assert response.status_code==200
 assert any(a['id']==f"product-image:{image['id']}" and a['rights_status']=='NEEDS_RIGHTS_REVIEW' for a in response.json())
 assert not any(k in response.text for k in ['supplier_cost','PRIVATE NOTES','password_hash'])

def test_corrupt_published_layout_falls_back_to_no_published(client):
 write(client,'owner-dashboard/publish')
 def corrupt(db):db.scalar(select(m.PageLayout)).published={'schema_version':999};db.commit()
 inspect_db(corrupt)
 assert client.get('/ops/page-layouts/owner-dashboard').json()['published'] is None

def test_layout_context_cannot_reference_other_revision(client):
 write(client,'owner-dashboard/publish');r=client.get('/ops/page-layouts/owner-dashboard/revisions').json()[0]
 response=client.post('/ops/page-layouts/transportation-detail/restore',json=dict(expected_version=0,revision_id=r['id']));assert response.status_code==404

def test_layout_audit_does_not_modify_business_records(client):
 tour=create_tour(client)
 def snapshot(db):return [(x.id,str(x.retail_price),str(x.supplier_cost),x.name) for x in db.scalars(select(m.Product))]
 before=inspect_db(snapshot);write(client,'owner-dashboard/draft',method='put');write(client,'owner-dashboard/publish',version=1)
 assert inspect_db(snapshot)==before
 def audit(db):return [(a.action,a.actor_user_id) for a in db.scalars(select(m.InternalAudit).where(m.InternalAudit.entity_type=='page_layout'))]
 events=inspect_db(audit);assert {a for a,_ in events}=={'draft_saved','published'} and all(actor for _,actor in events)

def test_authentication_csrf_and_unknown_page(client):
 assert write(client,'unknown/publish').status_code==404
 assert client.post('/ops/page-layouts/owner-dashboard/publish',json=dict(page=page(),expected_version=0),headers={'X-CSRF-Token':'invalid'}).status_code==403
 client.cookies.clear();assert client.get('/ops/page-layouts/owner-dashboard').status_code==401


@pytest.fixture(autouse=True)
def legacy_persistence_harness(client):
 """Exercise preserved persistence regressions; legacy routes are not deployed."""
 from fastapi import Depends
 from app.internal_auth import require_ops
 from app.routers.page_layouts import router
 original=list(client.app.router.routes)
 client.app.include_router(router,dependencies=[Depends(require_ops)])
 yield
 client.app.router.routes=original
