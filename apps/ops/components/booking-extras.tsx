'use client';
import {useState,FormEvent} from 'react';
import {useInventory,LoadState} from './inventory-ui';
import {When} from './ops-ui';
import {DirectoryUser} from '../lib/internal';
import {WorkBooking} from './dashboard';
import {apiRequest} from '../lib/api';
export function BookingExtras({id,reload}:{id:number;reload:()=>void}){const people=useInventory<DirectoryUser[]>('/ops/directory');const state=useInventory<WorkBooking>(`/ops/work/bookings/${id}`);const history=useInventory<{id:number;summary:string;actor_name:string;created_at:string}[]>(`/ops/audit?entity_type=booking&entity_id=${id}`);const [error,setError]=useState('');const [busy,setBusy]=useState(false);
 async function assign(e:FormEvent<HTMLFormElement>){e.preventDefault();if(!state.data)return;setBusy(true);setError('');const id=new FormData(e.currentTarget).get('assigned');try{await apiRequest(`/ops/bookings/${state.data.id}/assignment`,{method:'PUT',body:JSON.stringify({assigned_user_id:id?Number(id):null,expected_version:state.data.version})});reload();}catch(e){setError((e as Error).message);}finally{setBusy(false);}}
 return <><section className="ops-confirmation"><h2>Booking assignment</h2>{!people.data||!state.data?<LoadState error={people.error||state.error} retry={()=>{people.retry();state.retry();}}/>:<form className="toolbar" onSubmit={assign}><label>Responsible user<select name="assigned" defaultValue={state.data.assigned_user_id||''}><option value="">Unassigned</option>{people.data.map(p=><option key={p.id} value={p.id}>{p.display_name}</option>)}</select></label><button disabled={busy}>Save assignment</button></form>}{error&&<p role="alert">{error} <button onClick={reload}>Reload booking</button></p>}</section><section className="ops-confirmation"><h2>Booking history</h2>{!history.data?<LoadState error={history.error} retry={history.retry}/>:history.data.length?<ol className="ops-timeline">{history.data.map(h=><li key={h.id}><strong>{h.summary}</strong> by {h.actor_name}<small> · <When value={h.created_at}/></small></li>)}</ol>:<p>No authenticated booking changes recorded. Earlier history remains in the supplier timeline.</p>}</section></>;
}
