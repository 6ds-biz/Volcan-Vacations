import type {MediaAsset,MediaProvider} from '@6ds/page-builder/core';
import {apiRequest} from '../api';
/** References are supplied by the authenticated catalog, never by layout URLs. */
export function vvMediaProvider():MediaProvider{
 let cache:Promise<MediaAsset[]>|undefined;const approved=new Map<string,string>();
 const all=()=>cache??=(apiRequest<MediaAsset[]>('/ops/page-layouts/media').then(assets=>{assets.forEach(a=>approved.set(a.id,a.source));return assets;}).catch(e=>{cache=undefined;throw e;}));
 return {categories:['General','Destinations','Tours'],list:async(query='',category='')=>(await all()).filter(a=>(!query||(a.filename+' '+a.alt).toLowerCase().includes(query.toLowerCase()))&&(!category||a.tags?.includes(category))),get:async id=>(await all()).find(a=>a.id===id)||null,validateSource:asset=>{if(approved.get(asset.id)!==asset.source)return false;if(/^\/images\/[a-zA-Z0-9/_-]+\.webp$/.test(asset.source))return true;try{const u=new URL(asset.source);return u.protocol==='https:'||u.protocol==='http:'&&u.hostname==='localhost'&&u.port==='3000';}catch{return false;}}};
}
