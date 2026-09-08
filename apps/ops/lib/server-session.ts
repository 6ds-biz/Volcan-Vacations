import 'server-only';
import {cookies} from 'next/headers';
export const internalApi = () => process.env.OPS_API_URL || (process.env.OPS_ENVIRONMENT === 'development' ? 'http://localhost:8000' : '');
export type Identity = {appearance:'light'|'dark'|'system'; id:number; display_name:string; email:string; role:string; dashboard_profile:string; permissions:string[]; must_change_password:boolean};
export async function session(): Promise<Identity|null> {
  const token=(await cookies()).get('vv_ops_session')?.value;
  if (!token || !internalApi()) return null;
  const response=await fetch(`${internalApi()}/ops/auth/me`,{headers:{Cookie:`vv_ops_session=${token}`},cache:'no-store',signal:AbortSignal.timeout(10000)}).catch(()=>null);
  return response?.ok ? (await response.json()).user : null;
}
