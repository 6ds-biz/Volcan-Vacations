"""Catalog adapter only; no ingestion, rights inference or external fetching."""
from ..routers.page_layouts import media_catalog as existing_catalog

def catalog(db,request):
 assets=existing_catalog(db,request)
 for a in assets:
  a['source']=a['source'].replace('/images/builder/','/images/coast/')
  a['orientation']='landscape' if a['width'] and a['height'] and a['width']>a['height'] else None
  a['destination']=None;a['tour']=None;a['duplicate_hash']=None;a['recommended_use']=None;a['photographer']=None
 for key,label,alt in [('las-catalinas','Las Catalinas','Illustrative coastal village beside the Pacific.'),('tamarindo','Tamarindo','Illustrative Pacific bay at sunset.')]:
  assets.append(dict(id='vv-'+key,type='image',source=f'/images/coast/{key}-temporary.webp',filename=f'{key}-temporary.webp',mime_type='image/webp',width=1536,height=1024,alt=alt,rights_status='APPROVED',provenance='Existing generated VV illustration: docs/public-homepage/coastal-media.md.',tags=['Destinations'],destination=label,orientation='landscape'))
 return assets

def validate_media(configs,db,request,publishing=False):
 import re
 from fastapi import HTTPException
 assets={a['id']:a for a in catalog(db,request)}
 for c in configs:
  refs={c['asset'],c['poster'],*(c[d].get('asset',c['asset']) for d in ('tablet','mobile'))}-{None}
  for key in refs:
   a=assets.get(key)
   if not a:raise HTTPException(422,'Media reference is unavailable.')
   if publishing and not re.fullmatch(r'/videos/[a-zA-Z0-9/_-]+\.(mp4|webm)' if a['type']=='video' else r'/images/[a-zA-Z0-9/_-]+\.(webp|png|jpe?g|avif)',a['source']):raise HTTPException(422,'Media source is unsupported by the public renderer.')
   if key==c['poster'] and a['type']!='image':raise HTTPException(422,'Video poster must be an approved image.')
   if publishing and a['rights_status']!='APPROVED':raise HTTPException(422,'Media requires rights review before publication.')
   if publishing and not c['decorative'] and not (c['alt'].strip() or a['alt'].strip()):raise HTTPException(422,'Meaningful media needs alt text.')
