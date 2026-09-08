'use client';
import {useEffect,useRef,useState,type ReactNode} from 'react';
import {createPortal} from 'react-dom';
import type {Device} from '@6ds/page-builder/core';
import {SiteHeader} from '../../site-header';
import {SiteFooter} from '../../site-footer';
/** Same-origin blank frame: real CSS viewport breakpoints, no separate auth or draft URL. */
export function CanvasFrame({children,device}:{children:ReactNode;device:Device}){
 const frame=useRef<HTMLIFrameElement>(null),host=useRef<HTMLDivElement>(null);const [body,setBody]=useState<HTMLElement|null>(null),[available,setAvailable]=useState(1000),[height,setHeight]=useState(1000),[ready,setReady]=useState(false);
 const width={desktop:1440,tablet:900,mobile:390}[device],scale=Math.min(1,available/width);
 useEffect(()=>{const doc=frame.current?.contentDocument;if(doc?.readyState==='complete')setBody(doc.body);},[]);
 useEffect(()=>{const node=host.current;if(!node)return;const observer=new ResizeObserver(([e])=>setAvailable(e.contentRect.width));observer.observe(node);return()=>observer.disconnect();},[]);
 useEffect(()=>{body?.style.setProperty('--vv-canvas-scale',String(scale));},[body,scale]);
 useEffect(()=>{if(!body)return;const document=body.ownerDocument;document.documentElement.lang='en';const synchronize=()=>{document.head.querySelectorAll('[data-vv-style]').forEach(n=>n.remove());const pending:Promise<unknown>[]=[];window.document.querySelectorAll('link[rel=stylesheet],style').forEach(n=>{const copy=n.cloneNode(true) as HTMLElement;copy.dataset.vvStyle='';if(n.tagName==='STYLE'){try{copy.textContent=Array.from((n as HTMLStyleElement).sheet?.cssRules||[]).map(r=>r.cssText).join('\n');}catch{/* Inline text already copied. */}}else{pending.push(new Promise(resolve=>{copy.addEventListener('load',resolve,{once:true});copy.addEventListener('error',resolve,{once:true});}));}document.head.appendChild(copy);});Promise.all(pending).then(()=>document.fonts.ready).then(()=>setReady(true));};synchronize();const styles=new MutationObserver(synchronize);styles.observe(window.document.head,{childList:true});const observer=new ResizeObserver(()=>setHeight(Math.ceil(body.getBoundingClientRect().height)));observer.observe(body);return()=>{styles.disconnect();observer.disconnect();};},[body]);
 return <div ref={host} className="vv-frame-host" style={{height:height*scale+4}}>{!ready&&<p role="status">Loading public canvas…</p>}<iframe ref={frame} title={`${device} public website canvas`} className="vv-frame" style={{width,height,left:Math.max(0,(available-width*scale)/2),visibility:ready?'visible':'hidden',transform:`scale(${scale})`}} onLoad={()=>{if(frame.current?.contentDocument)setBody(frame.current.contentDocument.body);}} srcDoc="<!doctype html><html lang='en'><head><title>Volcan Vacations canvas</title></head><body style='margin:0'></body></html>"/>{body&&createPortal(<><div inert><SiteHeader/></div>{children}<div inert><SiteFooter/></div></>,body)}</div>;
}
