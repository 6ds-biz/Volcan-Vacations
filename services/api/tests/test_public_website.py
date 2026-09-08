from copy import deepcopy
from datetime import timedelta
import pytest
from sqlalchemy import select
from app import models as m
from app.availability_rules import utcnow
from app.internal_auth import digest
from app.website.schema import PAGES,validate_public_layout
from test_inventory import client,create_tour
from test_internal import add_user,signin
from test_bookings import inspect_db

def layout(key='home',widget='hero',config=None):
 def element(id):return dict(id=id,presentation=dict(order=0,width=12,visible=True,spacing='none',align='stretch',density='normal',surface='transparent',container='full',border='none'),responsive={})
 return dict(schema_version=1,page_id='public-'+key,sections=[dict(**element('s'),columns=[dict(**element('c'),widgets=[dict(**element('w'),type=widget,config=config or {})])])])

def test_owner_page_manager_and_media(client):
 create_tour(client)
 rows=client.get('/ops/website/pages').json();assert [r['key'] for r in rows]==list(PAGES)
 assert all(r['published_status']=='Source default' for r in rows)
 assert next(r for r in rows if r['key']=='tour-detail')['public_url'].endswith('/tours/demo-rafting')
 assets=client.get('/ops/website/media').json();assert any(a['rights_status']=='APPROVED' for a in assets);assert any(a['rights_status']=='NEEDS_RIGHTS_REVIEW' for a in assets)
 assert all('provenance'in a and 'width'in a for a in assets)
 assert client.get('/ops/website/pages/home/revisions').json()==[]

@pytest.mark.parametrize('role',['operations_partner','staff'])
def test_roles_cannot_manage_website_even_with_owner_profile(client,role):
 add_user(role,'Owner');signin(client,role)
 for path in ['pages','media','pages/home','pages/home/revisions']:assert client.get('/ops/website/'+path).status_code==403
 for path in ['publish','restore','edit-session']:assert client.post('/ops/website/pages/home/'+path,json={}).status_code==403
 assert client.put('/ops/website/pages/home/draft',json={'expected_version':0,'page':layout()}).status_code==403

@pytest.mark.parametrize('path',['pages','media','pages/home','pages/home/revisions'])
def test_visitor_cannot_manage_website(client,path):
 client.cookies.clear();assert client.get('/ops/website/'+path).status_code==401

@pytest.mark.parametrize('key',list(PAGES))
def test_public_page_types_have_private_draft_and_public_fallback(client,key):
 page=layout(key,PAGES[key][2][0]);assert client.put(f'/ops/website/pages/{key}/draft',json={'expected_version':0,'page':page}).status_code==200
 assert client.get('/ops/website/pages/'+key).json()['draft']==page
 client.cookies.clear();assert client.get('/public/website/pages/'+key).json()=={'page':None}

@pytest.mark.parametrize('key,widget,config',[('home','supplier-confirmation',{}),('home','hero',{'supplier_cost':'20'}),('tours','tour-grid',{'retail_price':'1'}),('tours','tour-grid',{'active':True}),('tour-detail','price-request',{'tour':{'slug':'hidden'}}),('tour-detail','tour-hero',{'customer_email':'private'}),('contact','contact-form',{'action':'https://example.invalid'}),('home','button',{'href':'javascript:alert(1)'}),('home','hero',{'surface':'green'}),('home','hero',{'media':{'source':'https://example.invalid'}})])
def test_inventory_context_and_configuration_boundary(client,key,widget,config):
 assert client.put(f'/ops/website/pages/{key}/draft',json={'expected_version':0,'page':layout(key,widget,config)}).status_code==422

@pytest.mark.parametrize('count',[0,13,True,1.2])
def test_inventory_count_is_bounded(client,count):
 assert client.put('/ops/website/pages/tours/draft',json={'expected_version':0,'page':layout('tours','tour-grid',{'limit':count})}).status_code==422

def test_safe_presentation_config(client):
 page=layout('tours','tour-grid',{'limit':4,'heading':'Explore Costa Rica','surface':'ivory','space':'xl'})
 assert client.put('/ops/website/pages/tours/draft',json={'expected_version':0,'page':page}).status_code==200

def test_public_payload_allowlist_and_invalid_fallback(client):
 def seed(db):
  owner=db.scalar(select(m.InternalUser));db.add(m.PageLayout(page_type='public-home',draft=layout(config={'heading':'PRIVATE DRAFT'}),published=layout(),updated_by_user_id=owner.id));db.commit()
 inspect_db(seed);client.cookies.clear()
 result=client.get('/public/website/pages/home');assert result.json()=={'page':layout()}
 assert not any(x in result.text for x in ['PRIVATE','actor','updated_by','email','draft','revision'])
 def poison(db):
  row=db.scalar(select(m.PageLayout).where(m.PageLayout.page_type=='public-home'));row.published=layout(config={'internal_notes':'PRIVATE'});db.commit()
 inspect_db(poison);assert client.get('/public/website/pages/home').json()=={'page':None}
 assert client.get('/public/website/pages/owner-dashboard').status_code==422
 assert client.get('/ops/page-layouts/owner-dashboard').status_code==404

def test_public_media_has_no_unreviewed_or_internal_metadata(client):
 create_tour(client);assets=client.get('/public/website/media').json()
 assert assets and all(a['rights_status']=='APPROVED' for a in assets)
 assert all('photographer'not in a and 'provenance'not in a for a in assets)
 assert all(a['source'].startswith('/images/coast/') for a in assets)

def test_rights_cannot_be_forged(client):
 from test_page_layouts import media_config
 config=media_config('vv-arenal');page=layout('home','media',config)
 assert client.put('/ops/website/pages/home/draft',json={'expected_version':0,'page':page}).status_code==200
 # Verify foundational validation only; full publish/restore acceptance is Part 3.
 from app.website.media import validate_media
 def check(db):
  from types import SimpleNamespace
  request=SimpleNamespace(app=client.app)
  from fastapi import HTTPException
  with pytest.raises(HTTPException) as error:validate_media([config],db,request,True)
  assert error.value.status_code==422
 inspect_db(check)
 config['rights_status']='APPROVED'
 assert client.put('/ops/website/pages/home/draft',json={'expected_version':1,'page':layout('home','media',config)}).status_code==422

def issue(client,key='home'):
 response=client.post(f'/ops/website/pages/{key}/edit-session',json={});assert response.status_code==200,response.text
 return response.json()['url'].split('#ticket=')[1]

def redeem(client,ticket):return client.post('/website-editor/redeem',headers={'Authorization':'Bearer '+ticket})

def test_handoff_is_one_use_page_scoped_and_not_ops_auth(client):
 ticket=issue(client);response=redeem(client,ticket);assert response.status_code==200
 secret=response.json()['token'];assert secret!=ticket and response.json()['page_key']=='home'
 assert redeem(client,ticket).status_code==401
 client.cookies.clear();headers={'Authorization':'Bearer '+secret}
 assert client.get('/website-editor/pages/home',headers=headers).status_code==200
 assert client.get('/website-editor/pages/about',headers=headers).status_code==403
 assert client.get('/ops/website/pages',headers=headers).status_code==401
 assert client.get('/website-editor/pages/home?edit=true').status_code==401
 assert client.get('/website-editor/pages/home',headers={'Authorization':'Bearer '+ticket}).status_code==401

@pytest.mark.parametrize('reason',['expired-ticket','expired-canvas','revoked-session','inactive-owner','changed-role'])
def test_expired_or_revoked_handoffs_fail(client,reason):
 ticket=issue(client);secret=redeem(client,ticket).json()['token'] if reason!='expired-ticket' else None
 def alter(db):
  row=db.get(m.WebsiteEditSession,digest(ticket));user=db.get(m.InternalUser,row.user_id)
  if reason=='expired-ticket':row.ticket_expires_at=utcnow()-timedelta(seconds=1)
  if reason=='expired-canvas':row.expires_at=utcnow()-timedelta(seconds=1)
  if reason=='revoked-session':db.delete(db.get(m.InternalSession,row.internal_session_hash))
  if reason=='inactive-owner':user.active=False
  if reason=='changed-role':user.role='staff'
  db.commit()
 inspect_db(alter)
 response=redeem(client,ticket) if not secret else client.get('/website-editor/pages/home',headers={'Authorization':'Bearer '+secret})
 assert response.status_code==401

def test_handoff_requires_existing_csrf(client):
 client.headers.pop('X-CSRF-Token');assert client.post('/ops/website/pages/home/edit-session',json={}).status_code==403

def test_operations_layout_routes_are_deactivated(client):
 for method,path in [('get','/ops/page-layouts/owner-dashboard'),('put','/ops/page-layouts/booking-detail/draft'),('post','/ops/page-layouts/transportation-detail/publish')]:
  assert getattr(client,method)(path).status_code==404

def test_layouts_do_not_change_inventory(client):
 tour=create_tour(client);before=client.get('/public/tours/'+tour['slug']).json()
 assert client.put('/ops/website/pages/tour-detail/draft',json={'expected_version':0,'page':layout('tour-detail','price-request',{'heading':'Request your date'})}).status_code==200
 assert client.get('/public/tours/'+tour['slug']).json()==before

# Part 2 scoped draft writes. Publication/revision acceptance remains Part 3.
def test_canvas_saves_private_draft_and_audit_without_ops_cookie(client):
 ticket=issue(client);secret=redeem(client,ticket).json()['token'];client.cookies.clear()
 headers={'Authorization':'Bearer '+secret}
 page=layout(config={'heading':'PRIVATE EDITOR DRAFT'})
 saved=client.put('/website-editor/pages/home/draft',headers=headers,json={'expected_version':0,'page':page})
 assert saved.status_code==200,saved.text
 assert client.get('/public/website/pages/home').json()=={'page':None}
 assert client.get('/website-editor/pages/home',headers=headers).json()['page']==page
 assert client.get('/website-editor/pages/home/media',headers=headers).status_code==200
 assert client.put('/website-editor/pages/about/draft',headers=headers,json={'expected_version':0,'page':layout('about','about-hero')}).status_code==403
 assert client.get('/website-editor/pages/about/media',headers=headers).status_code==403
 assert client.post('/website-editor/pages/home/publish',headers=headers,json={}).status_code==404
 def inspect(db):
  row=db.scalar(select(m.PageLayout));event=db.scalar(select(m.InternalAudit).where(m.InternalAudit.action=='draft_saved'))
  assert event.actor_user_id==row.updated_by_user_id
  assert db.scalar(select(m.PageLayoutRevision)) is None
 inspect_db(inspect)

@pytest.mark.parametrize('reason',['expired','inactive','partner','staff','logout'])
def test_canvas_draft_rechecks_owner_and_parent_session(client,reason):
 ticket=issue(client);secret=redeem(client,ticket).json()['token']
 def revoke(db):
  row=db.get(m.WebsiteEditSession,digest(ticket));user=db.get(m.InternalUser,row.user_id)
  if reason=='expired':row.expires_at=utcnow()-timedelta(seconds=1)
  if reason=='inactive':user.active=False
  if reason in ('partner','staff'):user.role='operations_partner' if reason=='partner' else 'staff'
  if reason=='logout':db.delete(db.get(m.InternalSession,row.internal_session_hash))
  db.commit()
 inspect_db(revoke)
 headers={'Authorization':'Bearer '+secret}
 assert client.put('/website-editor/pages/home/draft',headers=headers,json={'expected_version':0,'page':layout()}).status_code==401
 assert client.get('/website-editor/pages/home/media',headers=headers).status_code==401

@pytest.mark.parametrize('href',['/tours/demo?date=2026-10-20','#coast','https://example.com/coast','mailto:info@volcanvacations.com','tel:+5065550100'])
def test_editor_safe_public_links(client,href):
 assert client.put('/ops/website/pages/home/draft',json={'expected_version':0,'page':layout(config={'href':href})}).status_code==200

@pytest.mark.parametrize('href',['javascript:alert(1)','data:text/html,test','//evil.invalid','https://user:secret@example.com','mailto:a@b.com?body=%0asecret','/\\evil.invalid','https://example.com/ bad'])
def test_editor_unsafe_links_rejected(client,href):
 assert client.put('/ops/website/pages/home/draft',json={'expected_version':0,'page':layout(config={'href':href})}).status_code==422

@pytest.mark.parametrize('widget,config',[('image-text',{'layout':'image-right','heading':'Coast','copy':'Public copy','href':'/contact'}),('full-width-media',{'height':'large','subheadline':'Costa Rica'}),('hero',{'subheadline':'Explore Costa Rica'})])
def test_editor_public_config_extensions(client,widget,config):
 page=layout('home',widget,config);page['sections'][0]['presentation']['surface']='white'
 assert client.put('/ops/website/pages/home/draft',json={'expected_version':0,'page':page}).status_code==200
