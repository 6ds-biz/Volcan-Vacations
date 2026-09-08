import {NextRequest,NextResponse} from 'next/server';
import {websiteApi} from './server';
import {isPageKey} from './registry';
/** Cookie credentials never leave the server; only these scoped operations are proxied. */
export async function editorProxy(request:NextRequest,key:string,action:string){
 const method={draft:'PUT',publish:'POST',restore:'POST',revisions:'GET'}[action];
 if(!method||request.method!==method)return NextResponse.json({detail:'Unknown editor operation.'},{status:404});
 const token=request.cookies.get('vv_website_editor')?.value;
 if(!token||!isPageKey(key))return NextResponse.json({detail:'Reopen Edit from Operations.'},{status:401});
 let body:string|undefined;
 if(method!=='GET'){
  let origin:URL;try{origin=new URL(request.headers.get('origin')||'');}catch{return NextResponse.json({detail:'Same-origin request required.'},{status:403});}
  if(origin.host!==(request.headers.get('x-forwarded-host')||request.headers.get('host'))||!request.headers.get('content-type')?.startsWith('application/json'))return NextResponse.json({detail:'Same-origin JSON request required.'},{status:403});
  body=await request.text();if(body.length>105000)return NextResponse.json({detail:'Layout exceeds the supported size.'},{status:413});
 }
 try{
  const r=await fetch(`${websiteApi()}/website-editor/pages/${key}/${action}`,{method,headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body,cache:'no-store',redirect:'error',signal:AbortSignal.timeout(15000)});
  const data=await r.json();
  return NextResponse.json(r.ok?data:{detail:typeof data.detail==='string'?data.detail:'Check the layout or reopen Edit from Operations.'},{status:r.status,headers:{'Cache-Control':'no-store'}});
 }catch{return NextResponse.json({detail:'Website connection unavailable. Your changes remain in this editor. Reopen to check whether the operation completed before retrying.'},{status:503});}
}
