import {NextRequest,NextResponse} from 'next/server';
import {websiteApi} from '../../../../lib/website/server';
export async function POST(request:NextRequest){
 const origin=request.headers.get('origin');let parsed:URL|null=null;try{parsed=origin?new URL(origin):null;}catch{/* Reject malformed origins. */}const host=request.headers.get('x-forwarded-host')||request.headers.get('host');
 if(!origin||!parsed||parsed.host!==host||!request.headers.get('content-type')?.startsWith('application/json'))return NextResponse.json({detail:'Same-origin JSON request required.'},{status:403});
 const raw=await request.text();if(raw.length>512)return NextResponse.json({detail:'Invalid handoff.'},{status:400});let ticket;try{const data=JSON.parse(raw);if(Object.keys(data).join(',')!=='ticket')throw Error();ticket=data.ticket;}catch{return NextResponse.json({detail:'Invalid handoff.'},{status:400});}
 if(typeof ticket!=='string'||!/^[A-Za-z0-9_-]{43}$/.test(ticket))return NextResponse.json({detail:'Invalid handoff.'},{status:400});
 try{const result=await fetch(websiteApi()+'/website-editor/redeem',{method:'POST',headers:{Authorization:'Bearer '+ticket},cache:'no-store',redirect:'error',signal:AbortSignal.timeout(10000)});if(!result.ok)return NextResponse.json({detail:'Handoff expired or unavailable. Reopen from Operations.'},{status:401});const session=await result.json();const response=NextResponse.json({page_key:session.page_key},{headers:{'Cache-Control':'no-store','Referrer-Policy':'no-referrer'}});response.cookies.set('vv_website_editor',session.token,{httpOnly:true,sameSite:'strict',secure:parsed.protocol==='https:',path:'/',maxAge:session.expires_in});return response;}catch{return NextResponse.json({detail:'Website connection unavailable.'},{status:503});}
}
