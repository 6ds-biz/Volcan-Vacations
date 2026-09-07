import {NextRequest, NextResponse} from 'next/server';
import {internalApi} from '../../../../lib/server-session';
export const dynamic='force-dynamic';
async function proxy(request:NextRequest,{params}:{params:Promise<{path:string[]}>}) {
  const {path}=await params;
  if (!path.length || path.some(p=> !/^[a-zA-Z0-9_-]+$/.test(p))) return NextResponse.json({detail:'Invalid route'},{status:400});
  const base=internalApi();
  if (!base) return NextResponse.json({detail:'Operations connection is not configured'},{status:503});
  const headers=new Headers();
  for (const key of ['cookie','content-type','origin','x-csrf-token']) {const value=request.headers.get(key);if(value)headers.set(key,value);}
  const write=!['GET','HEAD'].includes(request.method);
  if (write && !request.headers.get('content-type')?.startsWith('application/json')) return NextResponse.json({detail:'JSON required'},{status:415});
  if (Number(request.headers.get('content-length')||0)>1048576) return NextResponse.json({detail:'Request too large'},{status:413});
  try {
    const body=write ? await request.text() : undefined;
    if (body && body.length>1048576) return NextResponse.json({detail:'Request too large'},{status:413});
    const response=await fetch(`${base}/ops/${path.join('/')}${request.nextUrl.search}`,{method:request.method,headers,body,cache:'no-store',redirect:'error',signal:AbortSignal.timeout(45000)});
    const output=new Headers({'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});
    if(response.headers.get('content-type'))output.set('Content-Type',response.headers.get('content-type')!);
    for(const value of response.headers.getSetCookie()) output.append('Set-Cookie',value);
    return new Response(response.body,{status:response.status,headers:output});
  } catch {return NextResponse.json({detail:'Operations is temporarily unavailable. Please retry.'},{status:503});}
}
export {proxy as GET,proxy as POST,proxy as PUT,proxy as PATCH,proxy as DELETE};
