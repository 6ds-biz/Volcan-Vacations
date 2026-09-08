import {NextRequest,NextResponse} from 'next/server';
import {websiteApi} from '../../../../../../lib/website/server';
import {isPageKey} from '../../../../../../lib/website/registry';
export async function PUT(request:NextRequest,{params}:{params:Promise<{key:string}>}){
 const {key}=await params;const token=request.cookies.get('vv_website_editor')?.value;
 let origin:URL;try{origin=new URL(request.headers.get('origin')||'');}catch{return NextResponse.json({detail:'Same-origin request required.'},{status:403});}
 if(origin.host!==(request.headers.get('x-forwarded-host')||request.headers.get('host'))||!request.headers.get('content-type')?.startsWith('application/json'))return NextResponse.json({detail:'Same-origin JSON request required.'},{status:403});
 if(!token||!isPageKey(key))return NextResponse.json({detail:'Reopen Edit from Operations.'},{status:401});
 const body=await request.text();if(body.length>105000)return NextResponse.json({detail:'Draft exceeds the supported size.'},{status:413});
 try{const r=await fetch(websiteApi()+'/website-editor/pages/'+key+'/draft',{method:'PUT',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body,cache:'no-store',redirect:'error',signal:AbortSignal.timeout(15000)});const data=await r.json();return NextResponse.json(r.ok?{version:data.version}:{detail:typeof data.detail==='string'?data.detail:'Draft could not be saved. Check the layout or reopen Edit.'},{status:r.status,headers:{'Cache-Control':'no-store'}});}catch{return NextResponse.json({detail:'Draft connection unavailable. Your unsaved changes remain in this editor.'},{status:503});}
}
