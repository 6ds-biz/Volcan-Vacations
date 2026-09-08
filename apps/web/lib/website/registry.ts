import {safePublicLink} from './links';
import {coreRegistry,devices,keys,text,validateMedia,type Registry,type MediaConfig} from '@6ds/page-builder/core';
export const pageTypes={
 home:['hero','arenal-feature','featured-experiences','benefits','trip-planning','pacific-coast','coastal-destinations','kinds-of-adventure','how-it-works','final-cta'],
 tours:['tours-hero','tour-grid','category-intro','destination-intro','cta'],
 'tour-detail':['tour-hero','tour-overview','description','price-request','duration-details','included','bring','gallery','availability','destination','related-tours','cta'],
 'plan-your-trip':['page-hero','intro','planning-form','image-text','benefits','cta'],
 about:['about-hero','about-story','values','local-expertise','cta'],
 contact:['contact-hero','contact-information','contact-form','contact-content','cta'],
} as const;
export type PublicPageKey=keyof typeof pageTypes;
export const isPageKey=(value:string):value is PublicPageKey=>Object.prototype.hasOwnProperty.call(pageTypes,value);
export const publicTokens={surface:['black','charcoal','ivory','white','transparent'],accent:['gold','gold-light'],typography:['display','heading','subheading','body','small','script'],space:['none','small','medium','large','xl']} as const;
export type Editorial={heading?:string;copy?:string;eyebrow?:string;media?:MediaConfig;href?:string;label?:string;limit?:number;surface?:string;accent?:string;typography?:string;space?:string;subheadline?:string;layout?:string;height?:string};
export const mediaWidgets=new Set(['hero','arenal-feature','pacific-coast','coastal-destinations','kinds-of-adventure','final-cta','tours-hero','tour-hero','gallery','page-hero','about-hero','about-story','local-expertise','contact-hero','cta','image-text','full-width-media']);
const basic=['heading','text','divider','spacer','media','image-text','full-width-media','button'];
export function publicRegistry(key:PublicPageKey):Registry{
 const registry:Registry={};for(const name of basic)if(coreRegistry[name])registry[name]={...coreRegistry[name],pages:['public-'+key]};
 for(const name of new Set<string>([...pageTypes[key],'image-text','full-width-media','button'])){
  const allowed=['heading','copy','eyebrow','subheadline','media',...Object.keys(publicTokens),...(['button','cta','final-cta','hero','arenal-feature','trip-planning','pacific-coast','image-text','full-width-media'].includes(name)?['href','label']:[]),...(name==='image-text'?['layout']:[]),...(name==='full-width-media'?['height']:[]),...(['featured-experiences','tour-grid','related-tours'].includes(name)?['limit']:[])];
  registry[name]={mediaKey:mediaWidgets.has(name)?'media':undefined,type:name,label:name.split('-').map(x=>x[0].toUpperCase()+x.slice(1)).join(' '),category:basic.includes(name)?'Basic':'Public '+key,icon:name,defaultConfig:{},fields:[{key:'eyebrow',label:'Eyebrow',kind:'text' as const},{key:'heading',label:'Headline',kind:'text' as const},{key:'subheadline',label:'Subheadline',kind:'text' as const},{key:'copy',label:'Body',kind:'text' as const},...(allowed.includes('href')?[{key:'label',label:'CTA label',kind:'text' as const},{key:'href',label:'CTA link',kind:'text' as const}]:[]),...(allowed.includes('limit')?[{key:'limit',label:'Item count',kind:'number' as const,min:1,max:12}]:[]),...(name==='image-text'?[{key:'layout',label:'Image position',kind:'choice' as const,options:['image-left','image-right']}]:[]),...(name==='full-width-media'?[{key:'height',label:'Height preset',kind:'choice' as const,options:['small','medium','large']}]:[])].filter(f=>name!=='button'||['label','href'].includes(f.key)),devices,duplicate:basic.includes(name),context:key==='tour-detail'&&!basic.includes(name)?['tour']:[],pages:['public-'+key],allowed:()=>true,validate:c=>{keys(c,allowed,[]);for(const field of ['heading','copy','eyebrow','subheadline','label'])if(field in c)text(c[field],field==='copy'?2000:200);for(const [field,values]of Object.entries(publicTokens))if(field in c&&!(values as readonly unknown[]).includes(c[field]))throw Error('Unsupported public design token.');if('limit'in c&&(typeof c.limit!=='number'||!Number.isInteger(c.limit)||c.limit<1||c.limit>12))throw Error('Item count must be between 1 and 12.');if('href'in c&&!safePublicLink(c.href))throw Error('Use an internal, HTTPS, mailto or tel link.');if('layout'in c&&!['image-left','image-right'].includes(String(c.layout)))throw Error('Invalid image position.');if('height'in c&&!['small','medium','large'].includes(String(c.height)))throw Error('Invalid media height.');if('media'in c){if(!c.media||typeof c.media!=='object'||Array.isArray(c.media))throw Error('Invalid media.');validateMedia(c.media as unknown as Record<string,unknown>);}}};
 }
 return registry;
}
