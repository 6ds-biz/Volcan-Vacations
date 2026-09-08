"""Public website presentation allowlist, independent of inventory and Operations layouts."""
from copy import deepcopy
from ..page_layout_schema import validate_layout, obj, plain, enum, num, media, fail, CORE

PAGES={
 'home':('Home','/', ['hero','arenal-feature','featured-experiences','benefits','trip-planning','pacific-coast','coastal-destinations','kinds-of-adventure','how-it-works','final-cta']),
 'tours':('Tours','/tours',['tours-hero','tour-grid','category-intro','destination-intro','cta']),
 'tour-detail':('Tour Detail Template','/tours/[slug]',['tour-hero','tour-overview','description','price-request','duration-details','included','bring','gallery','availability','destination','related-tours','cta']),
 'plan-your-trip':('Plan Your Trip','/plan-your-trip',['page-hero','intro','planning-form','image-text','benefits','cta']),
 'about':('About','/about',['about-hero','about-story','values','local-expertise','cta']),
 'contact':('Contact','/contact',['contact-hero','contact-information','contact-form','contact-content','cta']),
}
BASIC={'heading','text','divider','spacer','media','image-text','full-width-media','button'}
TOKENS={'surface':['black','charcoal','ivory','white','transparent'],'accent':['gold','gold-light'],'typography':['display','heading','subheading','body','small','script'],'space':['none','small','medium','large','xl']}

def storage_key(key):
 if key not in PAGES:fail('Unsupported public website page.')
 return 'public-'+key

def validate_public_layout(page,key):
 """Reuse the structural validator; validate consumer widget config before projection."""
 import json
 if len(json.dumps(page))>100000:fail('Layout exceeds 100 KB.')
 expected=storage_key(key)
 if not isinstance(page,dict) or page.get('page_id')!=expected:fail('Wrong public page context.')
 projected=deepcopy(page);media_configs=[];seen=set()
 # Traverse only validated container types; structural validation still owns bounds/IDs.
 for s in projected.get('sections',[]) if isinstance(projected.get('sections'),list) else []:
  if not isinstance(s,dict):fail()
  for col in s.get('columns',[]) if isinstance(s.get('columns'),list) else []:
   if not isinstance(col,dict):fail()
   for w in col.get('widgets',[]) if isinstance(col.get('widgets'),list) else []:
    if not isinstance(w,dict):fail()
    t=w.get('type');c=w.get('config')
    if not isinstance(t,str) or t not in BASIC|set(PAGES[key][2]):fail('Widget not allowed on this public page.')
    if t not in BASIC:
     if t in seen:fail('Page features and business forms cannot be duplicated.')
     seen.add(t)
    if t in CORE:
     if t=='media':media(c);media_configs.append(c)
     continue
    allowed={'heading','copy','eyebrow','media','surface','accent','typography','space'}
    if t in ('button','cta','final-cta'):allowed|={'href','label'}
    if t in ('featured-experiences','tour-grid','related-tours'):allowed|={'limit'}
    obj(c,allowed,[])
    for field in ('heading','copy','eyebrow','label'):
     if field in c:plain(c[field],2000 if field=='copy' else 200)
    for field,values in TOKENS.items():
     if field in c:enum(c[field],values)
    if 'limit' in c:num(c['limit'],1,12,True)
    if 'href' in c:
     import re
     if not isinstance(c['href'],str) or not re.fullmatch(r'/(?:tours|plan-your-trip|about|contact|request)?(?:#[a-zA-Z0-9_-]+)?|#[a-zA-Z0-9_-]+',c['href']):fail('Use an approved public navigation target.')
    if 'media' in c:media(c['media']);media_configs.append(c['media'])
    # Structural reuse without allowing any Operations-specific widget or config through.
    w['type']='divider';w['config']={}
 # validate_layout accepts an explicit registry; never mutate its global Operations registry.
 validate_layout(projected,expected,page_registry={expected:set()})
 return media_configs
