'use client';
import {useState,FormEvent} from 'react';
import {apiRequest} from '../lib/api';
export function Logout(){const [error,setError]=useState('');return <><button onClick={async()=>{try{await apiRequest('/ops/auth/logout',{method:'POST',body:'{}'});window.location.assign('/login');}catch(e){setError((e as Error).message);}}}>Logout</button>{error&&<p role="alert">{error}</p>}</>;}
export function AuthForm({change=false}:{change?:boolean}) {
 const [error,setError]=useState('');const [busy,setBusy]=useState(false);
 async function submit(event:FormEvent<HTMLFormElement>){event.preventDefault();setBusy(true);setError('');const data=new FormData(event.currentTarget);
 try{const result=await apiRequest<{user:{must_change_password:boolean}}>(change?'/ops/auth/password':'/ops/auth/login',{method:'POST',body:JSON.stringify(change?{current_password:data.get('password'),new_password:data.get('new_password')}:{email:data.get('email'),password:data.get('password')})});window.location.assign(change?'/login':result.user.must_change_password?'/change-password':'/');}catch(e){setError((e as Error).message);setBusy(false);}}
 return <form className="ops-form" onSubmit={submit}>{!change&&<label>Email<input name="email" type="email" autoComplete="username" required maxLength={180}/></label>}<label>{change?'Current password':'Password'}<input name="password" type="password" autoComplete="current-password" required maxLength={128}/></label>{change&&<label>New password (at least 15 characters)<input name="new_password" type="password" autoComplete="new-password" minLength={15} maxLength={128} required/></label>}{error&&<p role="alert">{error}</p>}<button disabled={busy}>{busy?'Please wait…':change?'Change password and sign out':'Sign in'}</button></form>;
}
