"""Server-side presentation validation. No business queries or executable config."""
import json,re,math
from fastapi import HTTPException

PAGES={
 'owner-dashboard':{'business-health','needs-attention','my-tasks','vendor-pipeline','inventory','recent-payments','visual-feature'},
 'operations-dashboard':{'my-tasks','needs-attention','new-bookings','supplier-followup','availability','vendor-work','transportation-lookup'},
 'booking-detail':{'booking-summary','customer','travelers','trip','availability','supplier-confirmation','payment','related-tasks','notes','history'},
 'supplier-detail':{'supplier-overview','contact-information','relationship-status','capabilities','agreements','rates','open-tasks','notes','history'},
 'transportation-detail':{'route-summary','origin-destination','vendor-services','schedules','rates','freshness','related-tasks','notes','history'},
}
CORE={'heading','text','divider','spacer','metric','list','media'}
PRESENTATION={'order':None,'width':None,'visible':[True,False],'spacing':['none','small','normal','large'],'align':['start','center','end','stretch'],'density':['normal','compact'],'surface':['transparent','base','panel','accent'],'container':['full','contained'],'border':['none','subtle']}
MEDIA_KEYS={'asset','alt','decorative','fit','x','y','ratio','radius','overlay','tablet','mobile','autoplay','muted','loop','controls','poster'}
def fail(message='Invalid page layout.'):raise HTTPException(422,message)
def obj(v,allowed,required=None):
 if not isinstance(v,dict) or set(v)-set(allowed) or set(allowed if required is None else required)-set(v):fail('Unknown or missing presentation fields.')
def plain(v,limit=2000):
 if not isinstance(v,str) or len(v)>limit or '<' in v or '>' in v:fail('Use bounded plain text.')
def num(v,lo,hi,integer=False):
 if type(v) not in (int,float) or not math.isfinite(v) or not lo<=v<=hi or integer and type(v)!=int:fail('Invalid numeric presentation setting.')
def enum(v,allowed):
 if not any(type(v)==type(x) and v==x for x in allowed):fail('Unsupported presentation setting.')
def ref(v):
 if v is not None and (not isinstance(v,str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9:_-]{0,159}',v)):fail('Invalid media reference.')
def media(c):
 obj(c,MEDIA_KEYS);plain(c['alt'],500)
 for k in ('asset','poster'):ref(c[k])
 for k in ('x','y'):num(c[k],0,100)
 for k,values in {'fit':['cover','contain'],'ratio':['wide','square','portrait','natural'],'radius':['none','small','large'],'overlay':['none','light','medium','dark']}.items():enum(c[k],values)
 for k in ('decorative','autoplay','muted','loop','controls'):enum(c[k],[True,False])
 if c['autoplay'] and not c['muted'] or not c['controls']:fail('Video requires controls; autoplay requires muted audio.')
 for d in ('tablet','mobile'):
  obj(c[d],{'asset','x','y'},[])
  for k,v in c[d].items():ref(v) if k=='asset' else num(v,0,100)
def validate_layout(page,page_type):
 if page_type not in PAGES:raise HTTPException(404,'Unsupported page type.')
 if len(json.dumps(page))>100000:fail('Layout exceeds 100 KB.')
 obj(page,{'schema_version','page_id','sections'})
 if type(page['schema_version'])!=int or page['schema_version']!=1 or page['page_id']!=page_type:fail('Unsupported schema version or page context.')
 seen=set();widgets=set();media_configs=[]
 def common(e,extra):
  obj(e,{'id','presentation','responsive'}|set(extra));key=e['id']
  if not isinstance(key,str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}',key) or key in seen:fail('Element IDs must be unique.')
  seen.add(key)
  if len(seen)>250:fail('Too many page elements.')
  obj(e['presentation'],PRESENTATION);obj(e['responsive'],{'desktop','tablet','mobile'},[])
  for p in [e['presentation'],*e['responsive'].values()]:
   obj(p,PRESENTATION,[])
   for k,v in p.items():
    if k=='order':num(v,0,1000,True)
    elif k=='width':num(v,1,12,True)
    else:enum(v,PRESENTATION[k])
 if not isinstance(page['sections'],list) or len(page['sections'])>30:fail('Invalid sections.')
 for s in page['sections']:
  common(s,{'columns'})
  if not isinstance(s['columns'],list) or not 1<=len(s['columns'])<=12:fail('Sections require 1–12 columns.')
  for c in s['columns']:
   common(c,{'widgets'})
   if not isinstance(c['widgets'],list) or len(c['widgets'])>50:fail('Invalid widgets.')
   for w in c['widgets']:
    common(w,{'type','config'});t=w['type'];config=w['config']
    if not isinstance(t,str) or t not in PAGES[page_type]|CORE:fail('Widget not allowed on this page.')
    if t=='visual-feature':
     if t in widgets:fail('Business widgets cannot be duplicated.')
     widgets.add(t);media(config);media_configs.append(config)
    elif t not in CORE:
     if t in widgets:fail('Business widgets cannot be duplicated.')
     widgets.add(t);obj(config,[])
    elif t=='media':media(config);media_configs.append(config)
    elif t in ('heading','text','list'):
     obj(config,{'text','level'} if t=='heading' else {'text'});plain(config['text'],200 if t=='heading' else 2000)
     if t=='heading':enum(config['level'],['h2','h3','h4'])
    elif t=='metric':
     obj(config,{'label','value'});plain(config['label'],120);plain(config['value'],60)
    elif t=='spacer':obj(config,{'size'});enum(config['size'],['small','normal','large'])
    else:obj(config,[])
 return media_configs
