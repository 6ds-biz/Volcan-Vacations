import type {Metadata} from 'next';
import {cookies} from 'next/headers';
import {notFound} from 'next/navigation';
import {isPageKey} from '../../../lib/website/registry';
import {publicGet,websiteApi} from '../../../lib/website/server';
import {PublicCanvas} from '../../../components/website/public-canvas';
import {WebsiteHandoff} from '../../../components/website/handoff';
import '../../home.css';
export const metadata:Metadata={title:'Website canvas',robots:{index:false,follow:false},referrer:'no-referrer'};
export const dynamic='force-dynamic';
export default async function Canvas({params}:{params:Promise<{key:string}>}){const {key}=await params;if(!isPageKey(key))notFound();const token=(await cookies()).get('vv_website_editor')?.value;let state=null;
 if(token){try{const r=await fetch(websiteApi()+'/website-editor/pages/'+key,{headers:{Authorization:'Bearer '+token},cache:'no-store',redirect:'error',signal:AbortSignal.timeout(10000)});if(r.ok)state=await r.json();}catch{/* Expired/unavailable sessions never expose drafts. */}}
 if(!state)return <main id="main-content"><WebsiteHandoff/></main>;
 const [assets,tours]=await Promise.all([publicGet('/public/website/media'),key==='tour-detail'?publicGet('/public/tours'):null]);
 return <main id="main-content"><WebsiteHandoff silent/><aside className="website-canvas-notice"><h1>Public website canvas · {key}</h1><p>Secure foundation preview. Visual editing is Part 2; publishing acceptance is Part 3. No changes can be made here yet.</p></aside><div inert className={`website-canvas-readonly${key==='home'?' home-page':''}`}><PublicCanvas pageKey={key} layout={state.page} assets={Array.isArray(assets)?assets:[]} tour={Array.isArray(tours)?tours[0]:undefined}/></div></main>;
}
