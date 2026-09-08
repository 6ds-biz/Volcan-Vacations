"""Owner-authored presentation drafts and atomic publication; never business state."""
from copy import deepcopy
from urllib.parse import urlsplit
from fastapi import APIRouter,Depends,HTTPException,Request
from pydantic import BaseModel,ConfigDict,Field,StrictInt
from sqlalchemy import select,func,event
from ..database import get_db
from .. import models as m
from ..permissions import can
from ..page_layout_schema import PAGES,validate_layout

router=APIRouter(prefix='/ops/page-layouts',tags=['Page builder'])
STATIC=[
 dict(id='vv-pacific',type='image',source='/images/builder/pacific-sunset-temporary.webp',filename='pacific-sunset-temporary.webp',mime_type='image/webp',width=1536,height=1024,alt='Illustrative Pacific sunset over golden sand and a wooded coastal headland.',rights_status='APPROVED',provenance='Existing VV generated placeholder; docs/public-homepage/coastal-media.md. Illustrative, not a documentary photograph.',tags=['Destinations']),
 dict(id='vv-papagayo',type='image',source='/images/builder/papagayo-temporary.webp',filename='papagayo-temporary.webp',mime_type='image/webp',width=1536,height=1024,alt='Illustrative blue Pacific cove framed by wooded headlands.',rights_status='APPROVED',provenance='Existing VV generated placeholder; docs/public-homepage/coastal-media.md.',tags=['Destinations']),
 dict(id='vv-nosara',type='image',source='/images/builder/nosara-temporary.webp',filename='nosara-temporary.webp',mime_type='image/webp',width=1536,height=1024,alt='Illustrative surfers walking along a Pacific beach beside coastal forest.',rights_status='APPROVED',provenance='Existing VV generated placeholder; docs/public-homepage/coastal-media.md.',tags=['Destinations']),
 dict(id='vv-arenal',type='image',source='/images/arenal.webp',filename='arenal.webp',mime_type='image/webp',width=1536,height=1024,alt='Arenal volcano and surrounding Costa Rica rainforest.',rights_status='NEEDS_RIGHTS_REVIEW',provenance='Existing Operations image. No asset-level rights record supplied; review before new publication.',tags=['General']),
]

def owner(request):
 if request.state.actor['role']!='owner_admin':raise HTTPException(403,'Only an Owner may edit, publish or restore layouts.')
def page_access(page_type,request):
 if page_type not in PAGES:raise HTTPException(404,'Unsupported page type.')
 actor=request.state.actor
 if page_type=='owner-dashboard' and actor['role']!='owner_admin':raise HTTPException(403,'Owner dashboard required.')
 capability={'operations-dashboard':'bookings.read','booking-detail':'bookings.read','supplier-detail':'suppliers.read','transportation-detail':'transport.read'}.get(page_type)
 if capability and not can(actor,capability):raise HTTPException(403,'This page is unavailable for your role.')

def media_catalog(db,request):
 assets=deepcopy(STATIC)
 base=request.app.state.config.public_web_url or ('http://localhost:3000' if request.app.state.config.environment=='development' else '')
 for image in db.scalars(select(m.ProductImage).join(m.Product).where(m.Product.active.is_(True)).order_by(m.ProductImage.id)):
  source=image.image_url
  if source.startswith('/images/') and not '..' in source:source=base+source if base else ''
  parsed=urlsplit(source)
  if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password:continue
  if parsed.scheme=='http' and not (request.app.state.config.environment=='development' and parsed.hostname=='localhost'):continue
  mime={'.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.avif':'image/avif'}.get('.'+parsed.path.rsplit('.',1)[-1].lower())
  if mime not in ('image/webp','image/jpeg','image/png','image/avif'):continue
  assets.append(dict(id=f'product-image:{image.id}',type='image',source=source,filename=parsed.path.rsplit('/',1)[-1],mime_type=mime,width=None,height=None,alt=image.alt_text,rights_status='NEEDS_RIGHTS_REVIEW',provenance='Existing ProductImage reference. Rights metadata has not been supplied.',tags=['Tours']))
 return assets

@router.get('/media')
def assets(request:Request,search:str='',category:str='',db=Depends(get_db)):
 return [a for a in media_catalog(db,request) if (not search or search[:120].lower() in (a['filename']+' '+a['alt']).lower()) and (not category or category in a['tags'])]

class LayoutWrite(BaseModel):
 model_config=ConfigDict(extra='forbid')
 expected_version:StrictInt=Field(ge=0)
 page:dict
class Restore(BaseModel):
 model_config=ConfigDict(extra='forbid')
 expected_version:StrictInt=Field(ge=0)
 revision_id:StrictInt=Field(gt=0)

def validated(page,page_type,db,request,publishing=False):
 configs=validate_layout(page,page_type)
 if configs:
  catalog={a['id']:a for a in media_catalog(db,request)}
  for c in configs:
   ids={c['asset'],c['poster'],*(c[d].get('asset',c['asset']) for d in ('tablet','mobile'))}-{None}
   for key in ids:
    a=catalog.get(key)
    if not a:raise HTTPException(422,'Media reference is missing or unavailable.')
    if publishing and a['rights_status']!='APPROVED':raise HTTPException(422,'Selected media needs rights review before publication.')
    if publishing and not c['decorative'] and not (c['alt'].strip() or a['alt'].strip()):raise HTTPException(422,'Meaningful media requires alt text.')
 return deepcopy(page)

def lock_layout(db,page_type,expected):
 if db.bind.dialect.name=='postgresql':
  from sqlalchemy.dialects.postgresql import insert
 else:
  from sqlalchemy.dialects.sqlite import insert
 db.execute(insert(m.PageLayout).values(page_type=page_type).on_conflict_do_nothing(index_elements=['page_type']))
 row=db.scalar(select(m.PageLayout).where(m.PageLayout.page_type==page_type).with_for_update())
 if row.version!=expected:raise HTTPException(409,'Layout changed in another session. Exit and reload before saving or publishing.')
 return row

def audit(db,row,actor,action):
 db.add(m.InternalAudit(actor_user_id=actor,entity_type='page_layout',entity_id=row.id,action=action,summary=f'{row.page_type}: {action}'))
def publish(db,row,page,actor,action='published',restored=None):
 number=(db.scalar(select(func.max(m.PageLayoutRevision.number)).where(m.PageLayoutRevision.layout_id==row.id)) or 0)+1
 db.add(m.PageLayoutRevision(layout_id=row.id,number=number,content=deepcopy(page),actor_user_id=actor,action=action,restored_from_id=restored))
 row.published=deepcopy(page);row.draft=deepcopy(page);row.updated_by_user_id=actor;row.version+=1;audit(db,row,actor,action)

@router.get('/{page_type}')
def current(page_type:str,request:Request,db=Depends(get_db)):
 page_access(page_type,request);row=db.scalar(select(m.PageLayout).where(m.PageLayout.page_type==page_type))
 published=row.published if row else None
 try:
  if published:validate_layout(published,page_type)
 except HTTPException:published=None
 result=dict(version=row.version if row else 0,published=published)
 if request.state.actor['role']=='owner_admin':result['draft']=row.draft if row else None
 return result

@router.put('/{page_type}/draft')
def save_draft(page_type:str,payload:LayoutWrite,request:Request,db=Depends(get_db)):
 owner(request);page_access(page_type,request)
 with db.begin():
  page=validated(payload.page,page_type,db,request);row=lock_layout(db,page_type,payload.expected_version)
  row.draft=page;row.version+=1;row.updated_by_user_id=request.state.actor['id'];audit(db,row,row.updated_by_user_id,'draft_saved')
 return dict(version=row.version)

@router.post('/{page_type}/publish')
def publish_layout(page_type:str,payload:LayoutWrite,request:Request,db=Depends(get_db)):
 owner(request);page_access(page_type,request)
 with db.begin():
  page=validated(payload.page,page_type,db,request,True);row=lock_layout(db,page_type,payload.expected_version);publish(db,row,page,request.state.actor['id'])
 return dict(version=row.version)

@router.get('/{page_type}/revisions')
def revisions(page_type:str,request:Request,db=Depends(get_db)):
 owner(request);page_access(page_type,request)
 rows=db.execute(select(m.PageLayoutRevision,m.InternalUser.display_name).select_from(m.PageLayoutRevision).join(m.PageLayout,m.PageLayout.id==m.PageLayoutRevision.layout_id).join(m.InternalUser,m.InternalUser.id==m.PageLayoutRevision.actor_user_id).where(m.PageLayout.page_type==page_type).order_by(m.PageLayoutRevision.number.desc())).all()
 return [dict(id=r.id,number=r.number,created_at=r.created_at,actor_name=name,action=r.action) for r,name in rows]

@router.post('/{page_type}/restore')
def restore(page_type:str,payload:Restore,request:Request,db=Depends(get_db)):
 owner(request);page_access(page_type,request)
 with db.begin():
  row=lock_layout(db,page_type,payload.expected_version);revision=db.get(m.PageLayoutRevision,payload.revision_id)
  if not revision or revision.layout_id!=row.id:raise HTTPException(404,'Revision not found for this page.')
  page=validated(revision.content,page_type,db,request,True);publish(db,row,page,request.state.actor['id'],'restored',revision.id)
 return dict(version=row.version,page=page)

@event.listens_for(m.PageLayoutRevision,'before_update')
@event.listens_for(m.PageLayoutRevision,'before_delete')
def immutable_revision(*args):raise ValueError('Page layout revisions are immutable.')
