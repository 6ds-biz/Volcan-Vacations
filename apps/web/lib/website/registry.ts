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
export type Editorial={heading?:string;copy?:string;eyebrow?:string;media?:MediaConfig;href?:string;label?:string;limit?:number;surface?:string;accent?:string;typography?:string;space?:string};
const basic=['heading','text','divider','spacer','media','image-text','full-width-media','button'];
export function publicRegistry(key:PublicPageKey):Registry{
 const registry:Registry={};for(const name of basic)if(coreRegistry[name])registry[name]={...coreRegistry[name],pages:['public-'+key]};
 for(const name of new Set<string>([...pageTypes[key],'image-text','full-width-media','button'])){
  const allowed=['heading','copy','eyebrow','media',...Object.keys(publicTokens),...(['button','cta','final-cta'].includes(name)?['href','label']:[]),...(['featured-experiences','tour-grid','related-tours'].includes(name)?['limit']:[])];
  registry[name]={type:name,label:name.split('-').map(x=>x[0].toUpperCase()+x.slice(1)).join(' '),category:basic.includes(name)?'Basic':'Public '+key,icon:name,defaultConfig:{},fields:[{key:'heading',label:'Heading',kind:'text'},{key:'copy',label:'Supporting copy',kind:'text'}],devices,duplicate:basic.includes(name),context:key==='tour-detail'&&!basic.includes(name)?['tour']:[],pages:['public-'+key],allowed:()=>true,validate:c=>{keys(c,allowed,[]);for(const field of ['heading','copy','eyebrow','label'])if(field in c)text(c[field],field==='copy'?2000:200);for(const [field,values]of Object.entries(publicTokens))if(field in c&&!(values as readonly unknown[]).includes(c[field]))throw Error('Unsupported public design token.');if('limit'in c&&(typeof c.limit!=='number'||!Number.isInteger(c.limit)||c.limit<1||c.limit>12))throw Error('Item count must be between 1 and 12.');if('href'in c&&(typeof c.href!=='string'||! /^(\/(?:tours|plan-your-trip|about|contact|request)?(?:#[a-zA-Z0-9_-]+)?|#[a-zA-Z0-9_-]+)$/.test(c.href)))throw Error('Use an approved public link.');if('media'in c){if(!c.media||typeof c.media!=='object'||Array.isArray(c.media))throw Error('Invalid media.');validateMedia(c.media as unknown as Record<string,unknown>);}}};
 }
 return registry;
}
