import {Children,cloneElement,isValidElement,type ReactNode,type ReactElement} from 'react';
import {PageHero,Eyebrow,LinkButton} from '../ui';
import {ScenicImage} from '../scenic-image';
import {ConfiguredMedia} from './public-media';
import type {Editorial} from '../../lib/website/registry';
export type {Editorial};
/** Bounded editorial overrides; forms and inventory components keep their own logic. */
export function editorial(node:ReactElement,config:Editorial):ReactElement{
 if(!Object.keys(config).length)return node;
 let heading=false,copy=false,eyebrow=false,image=false;
 function visit(n:ReactNode):ReactNode{
  if(!isValidElement<Record<string,unknown>>(n))return n;
  if(n.type===PageHero)return cloneElement(n,{...(config.heading!==undefined?{title:config.heading}:{}),...(config.copy!==undefined?{intro:config.copy}:{}),...(config.eyebrow!==undefined?{eyebrow:config.eyebrow}:{}),...(config.media?{media:config.media}:{}),...(config.subheadline?{subheadline:config.subheadline}:{})});
  if(!image&&n.type==='picture'&&config.media){image=true;return <ConfiguredMedia config={config.media} scenic/>;}
  if(!image&&n.type===ScenicImage&&config.media){image=true;return <ConfiguredMedia config={config.media} scenic/>;}
  if(!heading&&['h1','h2','h3'].includes(String(n.type))&&(config.heading!==undefined||config.subheadline!==undefined)){heading=true;const title=cloneElement(n,{},config.heading??n.props.children as ReactNode);return config.subheadline?<>{title}<p className="website-subheadline">{config.subheadline}</p></>:title;}
  if(!eyebrow&&n.type===Eyebrow&&config.eyebrow!==undefined){eyebrow=true;return cloneElement(n,{},config.eyebrow);}
  if(!copy&&n.type==='p'&&n.props.className!=='hero-categories'&&config.copy!==undefined){copy=true;return cloneElement(n,{},config.copy);}
  if(n.type===LinkButton&&(config.href||config.label))return cloneElement(n,{...(config.href?{href:config.href}:{})},config.label||n.props.children as ReactNode);
  if(n.type==='form')return n;
  return n.props.children?cloneElement(n,{},Children.map(n.props.children as ReactNode,visit)):n;
 }
 const result=visit(node) as ReactElement<Record<string,unknown>>;
 const classes=[result.props.className,...Object.keys(config).filter(k=>['surface','accent','typography','space'].includes(k)).map(k=>`website-${k}-${config[k as keyof Editorial]}`)].filter(Boolean).join(' ');
 return cloneElement(result,{className:classes});
}
