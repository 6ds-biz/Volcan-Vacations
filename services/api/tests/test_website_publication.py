"""Public publication acceptance; all writes use fixture-isolated databases."""
from copy import deepcopy
import pytest
from sqlalchemy import select,func
from app import models as m
from test_inventory import client,create_tour
from test_bookings import inspect_db
from test_public_website import layout,issue,redeem
from test_page_layouts import media_config


def auth(client):return {'Authorization':'Bearer '+redeem(client,issue(client)).json()['token']}
def save(client,page,version=0,headers=None):return client.put('/website-editor/pages/home/draft',headers=headers,json={'page':page,'expected_version':version})
def publish(client,page,version,headers):return client.post('/website-editor/pages/home/publish',headers=headers,json={'page':page,'expected_version':version})
def state(client):return client.get('/ops/website/pages/home').json()

def test_publish_saved_draft_restore_new_and_immutable_history(client):
 h=auth(client);p=layout();assert publish(client,p,0,h).status_code==409
 assert save(client,p,0,h).json()['version']==1
 assert client.get('/public/website/pages/home').json()=={'page':None}
 assert publish(client,p,1,h).json()['version']==2
 first=client.get('/website-editor/pages/home/revisions',headers=h).json()[0];assert first['current']
 changed=layout(config={'heading':'Approved publication'})
 assert publish(client,changed,2,h).status_code==409
 assert save(client,changed,2,h).json()['version']==3
 assert publish(client,changed,3,h).json()['version']==4
 assert client.get('/public/website/pages/home').json()=={'page':changed}
 restored=client.post('/website-editor/pages/home/restore',headers=h,json={'expected_version':4,'revision_id':first['id']})
 assert restored.json()=={'page':p,'version':5}
 rows=client.get('/website-editor/pages/home/revisions',headers=h).json()
 assert [r['number'] for r in rows]==[3,2,1]
 assert [r['current'] for r in rows]==[True,False,False]
 assert rows[0]['restored_from_id']==first['id'] and all(r['actor_name']=='Test owner' for r in rows)
 assert client.get('/public/website/pages/home').json()=={'page':p}
 def inspect(db):
  history=list(db.scalars(select(m.PageLayoutRevision).order_by(m.PageLayoutRevision.number)))
  assert [r.content for r in history]==[p,changed,p]
  assert {r.actor_user_id for r in history}=={db.scalar(select(m.InternalUser.id))}
  history[0].action='tampered'
  with pytest.raises(ValueError,match='immutable'):db.commit()
 inspect_db(inspect)


def test_two_scoped_owner_sessions_stale_save_publish_and_restore_rejected(client):
 a,b=auth(client),auth(client);p=layout();save(client,p,0,a);publish(client,p,1,a)
 revision=client.get('/website-editor/pages/home/revisions',headers=a).json()[0]['id']
 q=layout(config={'heading':'B won'});save(client,q,2,b);publish(client,q,3,b)
 assert save(client,p,2,a).status_code==409
 response=publish(client,p,2,a);assert response.status_code==409 and 'another session' in response.text
 assert client.post('/website-editor/pages/home/restore',headers=a,json={'expected_version':2,'revision_id':revision}).status_code==409
 assert client.get('/public/website/pages/home').json()=={'page':q}
 assert len(client.get('/website-editor/pages/home/revisions',headers=b).json())==2

@pytest.mark.parametrize('mutation',['rights','missing','tablet-rights','mobile-missing','link','private','responsive','context','video-audio','video-controls','video-missing'])
def test_publish_revalidates_persisted_draft_atomically(client,mutation):
 h=auth(client);p=layout();save(client,p,0,h);publish(client,p,1,h)
 bad=layout(config={'media':media_config()});c=bad['sections'][0]['columns'][0]['widgets'][0]['config']
 if mutation=='rights':c['media']['asset']='vv-arenal'
 if mutation=='missing':c['media']['asset']='missing'
 if mutation=='tablet-rights':c['media']['tablet']={'asset':'vv-arenal'}
 if mutation=='mobile-missing':c['media']['mobile']={'asset':'missing'}
 if mutation=='link':c['href']='javascript:alert(1)'
 if mutation=='private':c['supplier_cost']='secret'
 if mutation=='responsive':bad['sections'][0]['responsive']={'mobile':{'width':99}}
 if mutation=='context':bad['page_id']='public-about'
 if mutation=='video-audio':c['media'].update(autoplay=True,muted=False)
 if mutation=='video-controls':c['media']['controls']=False
 if mutation=='video-missing':c['media']['asset']='unsupported-video'
 def poison(db):
  row=db.scalar(select(m.PageLayout));row.draft=bad;db.commit()
 inspect_db(poison)
 before=state(client);response=publish(client,bad,2,h);assert response.status_code==422,response.text
 assert state(client)==before
 assert len(client.get('/website-editor/pages/home/revisions',headers=h).json())==1


def test_publish_rolls_back_revision_and_pointer_on_persistence_error(client,monkeypatch):
 from app.website import routes
 h=auth(client);p=layout();save(client,p,0,h);before=state(client)
 real=routes.publish
 def fail(*args,**kwargs):real(*args,**kwargs);args[0].flush();raise RuntimeError('Simulated transaction failure')
 monkeypatch.setattr(routes,'publish',fail)
 with pytest.raises(RuntimeError):publish(client,p,1,h)
 assert state(client)==before
 assert client.get('/website-editor/pages/home/revisions',headers=h).json()==[]

@pytest.mark.parametrize('decorative',[False,True])
def test_alt_text_and_decorative_publish_rules(client,monkeypatch,decorative):
 from app.website import media
 real=media.catalog
 def without_alt(*args):return [dict(a,alt='') for a in real(*args)]
 monkeypatch.setattr(media,'catalog',without_alt)
 h=auth(client);c=media_config();c.update(alt='',decorative=decorative);p=layout(config={'media':c});save(client,p,0,h)
 response=publish(client,p,1,h);assert response.status_code==(200 if decorative else 422)
 if not decorative:
  c['alt']='Pacific coast at sunset';p=layout(config={'media':c});save(client,p,1,h);assert publish(client,p,2,h).status_code==200


def test_approved_responsive_media_persists_and_reset_restores_source(client):
 h=auth(client);c=media_config();c.update(x=21,y=78,overlay='dark',tablet={'asset':'vv-papagayo','x':72},mobile={'asset':'vv-nosara','y':20},poster='vv-pacific')
 p=layout(config={'media':c});save(client,p,0,h);assert publish(client,p,1,h).status_code==200
 assert client.get('/public/website/pages/home').json()=={'page':p}
 p=layout();save(client,p,2,h);publish(client,p,3,h);assert client.get('/public/website/pages/home').json()=={'page':p}

@pytest.mark.parametrize('operation',['publish','restore','revisions'])
def test_scoped_publication_endpoints_reject_public_and_wrong_scope(client,operation):
 h=auth(client)
 method=client.get if operation=='revisions' else client.post
 kwargs={} if operation=='revisions' else {'json':{'expected_version':0,**({'revision_id':1} if operation=='restore' else {'page':layout()})}}
 client.cookies.clear()
 assert method('/website-editor/pages/home/'+operation,**kwargs).status_code==401
 assert method('/website-editor/pages/about/'+operation,headers=h,**kwargs).status_code==403
 assert method('/website-editor/pages/home/'+operation,headers={'Authorization':'Bearer '+'x'*43},**kwargs).status_code==401

@pytest.mark.parametrize('key,widget',[('home','hero'),('tours','tours-hero'),('tour-detail','tour-hero'),('about','about-hero'),('contact','contact-hero'),('plan-your-trip','page-hero')])
def test_all_public_pages_fail_closed_to_source_and_hide_drafts(client,key,widget):
 def seed(db):db.add(m.PageLayout(page_type='public-'+key,published={'schema_version':999},draft=layout(key,widget,{'heading':'PRIVATE'})));db.commit()
 inspect_db(seed);client.cookies.clear();response=client.get('/public/website/pages/'+key)
 assert response.json()=={'page':None} and 'PRIVATE' not in response.text


def test_shared_published_tour_template_preserves_two_live_products(client):
 one=create_tour(client);two=create_tour(client,name='Second tour',slug='second-tour',retail_price='125')
 before=[client.get('/public/tours/'+t['slug']).json() for t in [one,two]]
 p=layout('tour-detail','tour-hero')
 assert client.put('/ops/website/pages/tour-detail/draft',json={'page':p,'expected_version':0}).status_code==200
 assert client.post('/ops/website/pages/tour-detail/publish',json={'page':p,'expected_version':1}).status_code==200
 assert [client.get('/public/tours/'+t['slug']).json() for t in [one,two]]==before
 payload=client.get('/public/website/pages/tour-detail').json();assert payload=={'page':p}
 assert not any(k in str(payload) for k in ['supplier_cost','customer','actor','revision','token','retail_price'])

@pytest.mark.parametrize('reason',['expired','partner','staff','logout'])
def test_publish_restore_recheck_session_after_editor_open(client,reason):
 from datetime import timedelta
 from app.availability_rules import utcnow
 h=auth(client);p=layout();save(client,p,0,h)
 def revoke(db):
  session=db.scalar(select(m.WebsiteEditSession));user=db.get(m.InternalUser,session.user_id)
  if reason=='expired':session.expires_at=utcnow()-timedelta(seconds=1)
  if reason in ('partner','staff'):user.role='operations_partner' if reason=='partner' else 'staff'
  if reason=='logout':db.delete(db.get(m.InternalSession,session.internal_session_hash))
  db.commit()
 inspect_db(revoke)
 assert publish(client,p,1,h).status_code==401
 assert client.get('/website-editor/pages/home/revisions',headers=h).status_code==401
 assert client.post('/website-editor/pages/home/restore',headers=h,json={'expected_version':1,'revision_id':1}).status_code==401
