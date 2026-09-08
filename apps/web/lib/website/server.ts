import 'server-only';
import {cache} from 'react';
import type {Tour} from '../inventory';
export const websiteApi=()=>process.env.WEBSITE_API_URL||process.env.NEXT_PUBLIC_API_URL||'';
export async function publicGet(path:string){const base=websiteApi();if(!base)return null;try{const response=await fetch(base+path,{cache:'no-store',redirect:'error',signal:AbortSignal.timeout(3000)});return response.ok?await response.json():null;}catch{return null;}}
export const getPublicTour=cache(async(slug:string):Promise<Tour|null>=>/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)?publicGet('/public/tours/'+encodeURIComponent(slug)):null);
