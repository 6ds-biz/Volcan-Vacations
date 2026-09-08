"""Owner website management and strictly public, published presentation delivery."""
from copy import deepcopy
from datetime import timedelta
import secrets
from fastapi import APIRouter,Depends,HTTPException,Request,Response
from sqlalchemy import select,delete
from ..database import get_db
from .. import models as m
from ..internal_auth import COOKIE,digest
from ..availability_rules import utcnow,aware
from ..routers.page_layouts import owner,LayoutWrite,Restore,lock_layout,publish,audit
from .schema import PAGES,storage_key,validate_public_layout
from .media import catalog,validate_media

management=APIRouter(prefix='/ops/website',tags=['Website management'])
public=APIRouter(prefix='/public/website',tags=['Public website'])
bridge=APIRouter(prefix='/website-editor',tags=['Scoped website canvas'])

def checked(page,key,db,request,publishing=False):
 validate_media(validate_public_layout(page,key),db,request,publishing)
 return deepcopy(page)

def page_state(db,key):
 return db.scalar(select(m.PageLayout).where(m.PageLayout.page_type==storage_key(key)))

def website_origin(request):
 value=request.app.state.config.public_web_url
 if not value and request.app.state.config.environment=='development':value='http://localhost:3000'
 if not value:raise HTTPException(503,'Public website origin is not configured.')
 return value

@management.get('/pages')
def pages(request:Request,db=Depends(get_db)):
 owner(request);rows=[]
 for key,(title,path,_) in PAGES.items():
  row=page_state(db,key)
  latest=db.scalar(select(m.PageLayoutRevision).where(m.PageLayoutRevision.layout_id==row.id).order_by(m.PageLayoutRevision.number.desc())) if row else None
  user=db.get(m.InternalUser,latest.actor_user_id) if latest else None
  preview_path=path
  if key=='tour-detail':
   slug=db.scalar(select(m.Product.slug).where(m.Product.active.is_(True),m.Product.product_type=='tour').order_by(m.Product.id))
   preview_path='/tours/'+slug if slug else '/tours'
  rows.append(dict(key=key,title=title,path=path,published_status='Published' if row and row.published else 'Source default',draft_status='Unpublished changes' if row and row.draft!=row.published else 'No unpublished changes',last_published=latest.created_at if latest else None,published_by=user.display_name if user else None,public_url=website_origin(request)+preview_path))
 return rows

@management.get('/media')
def media_manager(request:Request,db=Depends(get_db)):
 owner(request);return catalog(db,request)

@management.get('/pages/{key}')
def current(key:str,request:Request,db=Depends(get_db)):
 owner(request);row=page_state(db,key)
 return dict(version=row.version if row else 0,draft=row.draft if row else None,published=row.published if row else None)

@management.put('/pages/{key}/draft')
def draft(key:str,payload:LayoutWrite,request:Request,db=Depends(get_db)):
 owner(request)
 with db.begin():
  page=checked(payload.page,key,db,request);row=lock_layout(db,storage_key(key),payload.expected_version)
  row.draft=page;row.version+=1;row.updated_by_user_id=request.state.actor['id'];audit(db,row,row.updated_by_user_id,'draft_saved')
 return dict(version=row.version)

# Generic publication architecture remains available to the authenticated manager.
# No publication/restore controls or end-to-end acceptance are introduced in Part 1.
@management.post('/pages/{key}/publish')
def publish_page(key:str,payload:LayoutWrite,request:Request,db=Depends(get_db)):
 owner(request)
 with db.begin():
  page=checked(payload.page,key,db,request,True);row=lock_layout(db,storage_key(key),payload.expected_version);publish(db,row,page,request.state.actor['id'])
 return dict(version=row.version)

@management.get('/pages/{key}/revisions')
def revisions(key:str,request:Request,db=Depends(get_db)):
 owner(request);row=page_state(db,key)
 if not row:return []
 records=db.execute(select(m.PageLayoutRevision,m.InternalUser.display_name).join(m.InternalUser,m.InternalUser.id==m.PageLayoutRevision.actor_user_id).where(m.PageLayoutRevision.layout_id==row.id).order_by(m.PageLayoutRevision.number.desc())).all()
 return [dict(id=r.id,number=r.number,created_at=r.created_at,actor_name=name,action=r.action) for r,name in records]

@management.post('/pages/{key}/restore')
def restore(key:str,payload:Restore,request:Request,db=Depends(get_db)):
 owner(request)
 with db.begin():
  row=lock_layout(db,storage_key(key),payload.expected_version);revision=db.get(m.PageLayoutRevision,payload.revision_id)
  if not revision or revision.layout_id!=row.id:raise HTTPException(404,'Revision not found.')
  page=checked(revision.content,key,db,request,True);publish(db,row,page,request.state.actor['id'],'restored',revision.id)
 return dict(page=page,version=row.version)

@public.get('/pages/{key}')
def published(key:str,request:Request,response:Response,db=Depends(get_db)):
 response.headers['Cache-Control']='no-store'
 row=page_state(db,key);page=None
 if row and row.published:
  try:page=checked(row.published,key,db,request,True)
  except HTTPException:pass
 return dict(page=page)  # No drafts, revisions, actors or private state.

@public.get('/media')
def public_media(request:Request,response:Response,db=Depends(get_db)):
 response.headers['Cache-Control']='no-store'
 fields=('id','type','source','filename','mime_type','width','height','alt','rights_status','tags')
 return [{k:a[k] for k in fields} for a in catalog(db,request) if a['rights_status']=='APPROVED']

@management.post('/pages/{key}/edit-session')
def issue(key:str,request:Request,response:Response,db=Depends(get_db)):
 owner(request);page_type=storage_key(key);origin=website_origin(request);ticket=secrets.token_urlsafe(32);now=utcnow()
 with db.begin():
  db.execute(delete(m.WebsiteEditSession).where(m.WebsiteEditSession.expires_at<=now))
  db.add(m.WebsiteEditSession(ticket_hash=digest(ticket),internal_session_hash=digest(request.cookies[COOKIE]),user_id=request.state.actor['id'],page_type=page_type,ticket_expires_at=now+timedelta(seconds=60),expires_at=now+timedelta(minutes=15)))
 response.headers['Cache-Control']='no-store'
 return dict(url=f'{origin}/website-editor/{key}#ticket={ticket}',expires_in=60)

def active_owner(db,row):
 parent=db.get(m.InternalSession,row.internal_session_hash) if row else None
 user=db.get(m.InternalUser,row.user_id) if row else None
 if not row or not parent or parent.user_id!=row.user_id or aware(parent.expires_at)<=utcnow() or not user or not user.active or user.role!='owner_admin' or user.must_change_password or aware(row.expires_at)<=utcnow():raise HTTPException(401,'Website edit session expired. Reopen from Operations.')

def bearer(request):
 value=request.headers.get('authorization','')
 if not value.startswith('Bearer ') or len(value[7:])!=43:raise HTTPException(401,'A scoped website edit session is required.')
 return digest(value[7:])

@bridge.post('/redeem')
def redeem(request:Request,response:Response,db=Depends(get_db)):
 token=bearer(request)
 with db.begin():
  row=db.scalar(select(m.WebsiteEditSession).where(m.WebsiteEditSession.ticket_hash==token).with_for_update());active_owner(db,row)
  if row.redeemed_at or aware(row.ticket_expires_at)<=utcnow():raise HTTPException(401,'Website handoff expired or already used.')
  secret=secrets.token_urlsafe(32);row.canvas_hash=digest(secret);row.redeemed_at=utcnow()
 response.headers['Cache-Control']='no-store'
 return dict(token=secret,page_key=row.page_type.removeprefix('public-'),expires_in=900)

@bridge.get('/pages/{key}')
def canvas(key:str,request:Request,response:Response,db=Depends(get_db)):
 token=bearer(request);page_type=storage_key(key)
 row=db.scalar(select(m.WebsiteEditSession).where(m.WebsiteEditSession.canvas_hash==token));active_owner(db,row)
 if row.page_type!=page_type or not row.redeemed_at:raise HTTPException(403,'Edit session does not cover this page.')
 layout=page_state(db,key);page=None
 if layout:
  candidate=layout.draft or layout.published
  if candidate:
   try:page=checked(candidate,key,db,request)
   except HTTPException:pass
 response.headers['Cache-Control']='no-store'
 return dict(page=page,page_key=key,version=layout.version if layout else 0)
