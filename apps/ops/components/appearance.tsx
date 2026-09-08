'use client';
import {createContext,useContext,useEffect,useState} from 'react';
import {apiRequest} from '../lib/api';
export type Appearance='light'|'dark'|'system';
const Context=createContext<{value:Appearance;save:(value:Appearance)=>Promise<void>}|null>(null);
export function AppearanceProvider({initial,children}:{initial:Appearance;children:React.ReactNode}){
 const [value,setValue]=useState(initial);
 useEffect(()=>{const media=window.matchMedia('(prefers-color-scheme: dark)');const apply=()=>{document.documentElement.dataset.theme=value==='system'?(media.matches?'dark':'light'):value;};apply();media.addEventListener('change',apply);return()=>media.removeEventListener('change',apply);},[value]);
 async function save(next:Appearance){await apiRequest('/ops/auth/appearance',{method:'PUT',body:JSON.stringify({appearance:next})});document.cookie=`vv_ops_appearance=${next}; Path=/; Max-Age=31536000; SameSite=Lax${location.protocol==='https:'?'; Secure':''}`;setValue(next);}
 return <Context.Provider value={{value,save}}>{children}</Context.Provider>;
}
export function AppearanceSetting(){const context=useContext(Context)!;const [busy,setBusy]=useState(false);const [message,setMessage]=useState('');const [error,setError]=useState('');return <section className="dashboard-section appearance-setting"><h2>Appearance</h2><p className="muted">Choose your workspace appearance. System follows your device.</p><label>Appearance<select aria-label="Appearance" value={context.value} disabled={busy} onChange={async e=>{setBusy(true);setMessage('');setError('');try{await context.save(e.target.value as Appearance);setMessage('Appearance saved to your account.');}catch(e){setError((e as Error).message);}finally{setBusy(false);}}}><option value="light">Light</option><option value="dark">Dark</option><option value="system">System</option></select></label>{message&&<p role="status">{message}</p>}{error&&<p role="alert">{error}</p>}</section>;}
