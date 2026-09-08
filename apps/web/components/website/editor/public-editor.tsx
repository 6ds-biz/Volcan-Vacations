'use client';
import {useMemo} from 'react';
import PageEditor from '@6ds/page-builder/editor';
import type {MediaAsset,Page} from '@6ds/page-builder/core';
import type {Tour} from '../../../lib/inventory';
import type {PublicPageKey} from '../../../lib/website/registry';
import {defaultLayout,resolvedLayout} from '../../../lib/website/defaults';
import {publicMediaProvider} from '../../../lib/website/media';
import {publicRuntime,sourceFlow} from '../public-canvas';
import {WebsiteContext} from '../public-media';
import {CanvasFrame} from './canvas-frame';
import './editor.css';
export function PublicEditor({pageKey,layout,version,assets,tour,exitUrl}:{pageKey:PublicPageKey;layout:unknown;version:number;assets:MediaAsset[];tour?:Tour;exitUrl:string}){
 const defaults=useMemo(()=>defaultLayout(pageKey),[pageKey]),initial=useMemo(()=>resolvedLayout(layout,pageKey),[layout,pageKey]);
 const media=useMemo(()=>publicMediaProvider(assets),[assets]);const registry=useMemo(()=>publicRuntime(pageKey,tour),[pageKey,tour]);
 const context={device:'desktop' as const,permissions:{role:'owner_admin',permissions:['website.manage']},data:tour?{tour}:{},media};
 const adapter=useMemo(()=>({saveDraft:async(page:Page,expected_version:number)=>{const response=await fetch(`/api/website-editor/pages/${pageKey}/draft`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({page,expected_version}),signal:AbortSignal.timeout(20000)});const value=await response.json();if(!response.ok)throw Error(value.detail||'Draft could not be saved.');return value;}}),[pageKey]);
 return <div className="vv-editor-shell"><h1 className="sr-only">Public website editor</h1><PageEditor initial={initial} defaults={defaults} registry={registry} context={context} version={version} adapter={adapter} surfaceLabels={{base:'Black',panel:'Charcoal',accent:'Warm Ivory',white:'White',transparent:'Transparent'}} exit={()=>window.location.assign(exitUrl)} renderCanvas={(node,device,page,preview)=><CanvasFrame device={device}><WebsiteContext.Provider value={{...context,device}}><main id="main-content" className={`${pageKey==='home'?'home-page ':''}website-runtime${preview&&sourceFlow(page)?' website-source-layout':''}`}>{node}</main></WebsiteContext.Provider></CanvasFrame>}/></div>;
}
