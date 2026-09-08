'use client';
import {useEffect,useMemo,useRef,useState,type ReactNode} from 'react';
import dynamic from 'next/dynamic';
import {validatePage,type Page,type Revision,type RevisionAdapter} from '@6ds/page-builder/core';
import {PageRenderer,useDevice} from '@6ds/page-builder/runtime';
import {vvRegistry} from '../../lib/page-builder/registry';
import {defaultPage} from '../../lib/page-builder/defaults';
import {vvMediaProvider} from '../../lib/page-builder/media';
import {apiRequest} from '../../lib/api';
import {useIdentity} from '../ops-ui';
const Editor=dynamic(()=>import('@6ds/page-builder/editor'),{ssr:false,loading:()=> <p role="status">Loading page editor…</p>});
type LayoutState={version:number;published:Page|null;draft?:Page|null};
export function PageSurface({pageType,slots,rows,context}:{pageType:string;slots:Record<string,ReactNode>;rows:[number,string[]][][];context:Record<string,unknown>}){
 const user=useIdentity(),device=useDevice();const [state,setState]=useState<LayoutState>({version:0,published:null}),[loaded,setLoaded]=useState(false),[editing,setEditing]=useState(false),[notice,setNotice]=useState('');const entry=useRef<HTMLButtonElement>(null);
 const registry=vvRegistry(pageType,slots),defaults=defaultPage(pageType,rows,registry);const media=useMemo(vvMediaProvider,[]);const base='/ops/page-layouts/'+pageType;
 function valid(value:Page|null|undefined){if(!value)return defaults;try{return validatePage(value,registry,pageType);}catch{return defaults;}}
 useEffect(()=>{let active=true;setLoaded(false);apiRequest<LayoutState>(base).then(value=>{if(active){setState(value);setLoaded(true);setNotice('');}}).catch(()=>{if(active){setState({version:0,published:null});setLoaded(false);setNotice('Published layout unavailable. Showing the approved default.');}});return()=>{active=false;};},[base]);
 // Retire only the former temporary Studio draft; never read it as a publication.
 useEffect(()=>{if(user.role==='owner_admin')try{localStorage.removeItem('vv-layout-studio-owner-v1');}catch{/* Storage can be unavailable; runtime uses server layouts. */}},[user.role]);
 const renderContext={device,permissions:user,data:context,media};
 const adapter:RevisionAdapter={saveDraft:(page,version)=>apiRequest(base+'/draft',{method:'PUT',body:JSON.stringify({page,expected_version:version})}),publish:(page,version)=>apiRequest(base+'/publish',{method:'POST',body:JSON.stringify({page,expected_version:version})}),revisions:()=>apiRequest<Revision[]>(base+'/revisions'),restore:(id,version)=>apiRequest(base+'/restore',{method:'POST',body:JSON.stringify({revision_id:id,expected_version:version})})};
 async function exit(){setEditing(false);try{setState(await apiRequest(base));setLoaded(true);}catch{setNotice('Published layout unavailable. Showing the approved default.');setState({version:0,published:null});}requestAnimationFrame(()=>entry.current?.focus());}
 return <>{!editing&&user.role==='owner_admin'&&<div className="vv-builder-entry"><button type="button" ref={entry} disabled={!loaded} onClick={()=>setEditing(true)}>Edit Page</button><small>Owner presentation controls</small></div>}{notice&&<p role="status">{notice}</p>}{editing&&user.role==='owner_admin'?<Editor key={pageType} initial={valid(state.draft||state.published)} defaults={defaults} registry={registry} context={renderContext} version={state.version} adapter={adapter} exit={exit}/>:<PageRenderer page={valid(state.published)} fallback={defaults} registry={registry} context={renderContext}/>}</>;
}
