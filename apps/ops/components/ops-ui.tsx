'use client';
import Link from 'next/link';
import {createContext,useContext,Children,cloneElement,isValidElement,useRef,useEffect,useState,useId,useSyncExternalStore,type ReactNode} from 'react';
import type {Identity} from '../lib/server-session';
export const IdentityContext=createContext<Identity|null>(null);
export function useIdentity(){const user=useContext(IdentityContext);if(!user)throw new Error('Operations session required');return user;}
export function Icon({name='work'}:{name?:string}) {
 const paths:Record<string,string>={transportation:'M4 16V6h16v10 M4 10h16 M7 16a2 2 0 1 0 0 4 2 2 0 0 0 0-4 M17 16a2 2 0 1 0 0 4 2 2 0 0 0 0-4 M9 6v4 M15 6v4',dashboard:'M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z',tasks:'M9 5h12 M9 12h12 M9 19h12 M3 5l1 1 2-3 M3 12l1 1 2-3 M3 19l1 1 2-3',bookings:'M5 5h14v16H5z M8 2v6 M16 2v6 M5 10h14',tours:'M2 20 9 5l4 8 3-5 6 12z M7 10l2 2 2-2',suppliers:'M3 21V8l9-5 9 5v13 M8 21v-7h8v7 M7 9h2 M15 9h2',payments:'M3 5h18v14H3z M3 9h18 M7 15h4',users:'M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8 M2 21v-2a7 7 0 0 1 14 0v2 M17 4a4 4 0 0 1 0 8 M19 15a5 5 0 0 1 3 6',work:'M5 3h14v18H5z M8 8h8 M8 12h8 M8 16h5'};
 return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={paths[name]||paths.work}/></svg>;
}
export function PageHeader({title,description,icon,children}:{title:string;description:string;icon?:string;children?:React.ReactNode}){return <header className="page-header"><span className="icon-tile"><Icon name={icon}/></span><div><span className="page-eyebrow">Operations</span><h1>{title}</h1><p>{description}</p></div>{children&&<div className="header-actions">{children}</div>}</header>;}
export function Modules({items}:{items:{label:string;value:number;onClick?:()=>void;href?:string;active?:boolean;icon?:string;hint?:string;tone?:string}[]}){return <div className="status-modules">{items.map(item=>{const content=<>{item.icon&&<span className={`metric-icon tone-${item.tone||'gold'}`}><Icon name={item.icon}/></span>}<span>{item.label}</span><strong>{item.value}</strong>{item.hint&&<small className="metric-hint">{item.hint}</small>}{item.icon&&<span className="metric-arrow" aria-hidden="true">›</span>}</>;return item.href?<Link className={item.icon?'health-module':undefined} key={item.label} href={item.href}>{content}</Link>:item.onClick?<button key={item.label} className={item.active?'selected':''} onClick={item.onClick} aria-pressed={!!item.active}>{content}</button>:<div key={item.label}>{content}</div>;})}</div>;}
/** Keep a single semantic table; selected execution lists become labelled compact rows on phones. */
export function Table({label,headings,children,empty,responsive='scroll',phoneOmit=[]}:{label:string;headings:string[];children:React.ReactNode;empty?:boolean;responsive?:'rows'|'scroll';phoneOmit?:string[]}){
 const rows=Children.map(children,row=>isValidElement<{children:ReactNode;role?:string}>(row)?cloneElement(row,{role:'row',children:Children.map(row.props.children,(cell,i)=>isValidElement<{role?:string;'data-label'?:string;'data-phone-hidden'?:boolean}>(cell)?cloneElement(cell,{role:'cell','data-label':headings[i],'data-phone-hidden':phoneOmit.includes(headings[i])}):cell)}):row);
 return empty?<p className="empty-state" role="status">No records match. Adjust your filters or create a record when ready.</p>:<div className={`ops-table-wrap ${responsive==='rows'?'execution-table':''}`} role="region" aria-label={label} tabIndex={0}><table role="table"><caption>{label}</caption><thead role="rowgroup"><tr role="row">{headings.map(h=><th data-phone-hidden={phoneOmit.includes(h)} role="columnheader" key={h} scope="col">{h}</th>)}</tr></thead><tbody role="rowgroup">{rows}</tbody></table></div>;
}
export function FilterPanel({children}:{children:ReactNode}){const [open,setOpen]=useState(false);const id=useId();return <div className={`filter-panel${open?' is-open':''}`}><button type="button" className="filter-toggle" aria-expanded={open} aria-controls={id} onClick={()=>setOpen(!open)}>{open?'Hide search & filters':'Search & filters'}</button><div id={id} className="toolbar">{children}</div></div>;}
const phoneQuery='(max-width: 600px)';
function subscribePhone(callback:()=>void){const media=window.matchMedia(phoneQuery);media.addEventListener('change',callback);return()=>media.removeEventListener('change',callback);}
export function usePhone(){return useSyncExternalStore(subscribePhone,()=>window.matchMedia(phoneQuery).matches,()=>false);}
/** Newly opened editors are brought into view even when launched far down a route or task list. */
export function useFormFocus(){const ref=useRef<HTMLFormElement>(null);useEffect(()=>{const form=ref.current;if(form){form.scrollIntoView({block:'start'});form.querySelector<HTMLElement>('input:not([type="hidden"]):not(:disabled),select:not(:disabled),textarea')?.focus({preventScroll:true});}},[]);return ref;}
export function ContactActions({email,phone}:{email?:string|null;phone?:string|null}){
 const cleanEmail=email?.trim();const validEmail=cleanEmail&&/^[^\s@?&#]+@[^\s@?&#]+\.[^\s@?&#]+$/.test(cleanEmail);
 const cleanPhone=phone?.trim();const digits=cleanPhone?.replace(/[\s().-]/g,'');const validPhone=cleanPhone&&/^[+\d\s().-]+$/.test(cleanPhone)&&digits&&/^\+?\d{7,15}$/.test(digits);
 if(!validEmail&&!validPhone)return null;
 return <div className="contact-actions" role="group" aria-label="Contact actions">{validPhone&&<a href={`tel:${digits}`}>Call</a>}{validEmail&&<a href={`mailto:${encodeURIComponent(cleanEmail)}`}>Email</a>}</div>;
}
export function label(value:string){return value.replace(/_/g,' ').replace(/^./,c=>c.toUpperCase());}
export function When({value}:{value:string|null}){return <>{value?new Date(value).toLocaleString(undefined,{dateStyle:'medium',timeStyle:'short'}):'—'}</>;}
export type Attention={key:string;label:string;count:number;href:string};
export function NeedsAttention({items}:{items:Attention[]}){return <section className="dashboard-section"><div className="section-heading"><h2>Needs Attention</h2><small>Separate work queues</small></div>{items.length?<ul className="attention-list">{items.map(i=><li key={i.key}><Link href={i.href}><span>{i.label}</span><strong>{i.count}</strong><span aria-hidden="true">→</span></Link></li>)}</ul>:<p className="empty-state">No outstanding attention items.</p>}</section>;}
