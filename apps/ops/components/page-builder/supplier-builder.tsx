'use client';
import Link from 'next/link';
import type {ReactNode} from 'react';
import {PageSurface} from './page-surface';
import {useInventory,LoadState} from '../inventory-ui';
import {ContactActions,When,label} from '../ops-ui';
import type {Supplier} from '../../lib/inventory';
import type {Task} from '../../lib/internal';
type Agreement={id:number;title:string;status:string;currency:string;effective_from:string|null;effective_to:string|null};
export function SupplierBuilder({id,supplier,overview,relationship,foundation}:{id:string;supplier:Supplier;overview:ReactNode;relationship:ReactNode;foundation:{relationship_status:string;service_types:string[]}|null}){
 const agreements=useInventory<Agreement[]>(`/ops/suppliers/${id}/agreements`);
 const slots={
 'supplier-overview':overview,
 'contact-information':<section className="ops-confirmation"><h2>Contact information</h2><p>{supplier.contact_name||supplier.name}</p><p>{supplier.email} · {supplier.phone}</p><ContactActions email={supplier.email} phone={supplier.phone}/></section>,
 'relationship-status':relationship,
 capabilities:<section className="ops-confirmation"><h2>Capabilities</h2>{foundation?<p>{foundation.service_types.map(label).join(' · ')||'No capabilities recorded'}</p>:<p>Relationship details unavailable.</p>}</section>,
 agreements:<section className="ops-confirmation"><h2>Agreements</h2>{!agreements.data?<LoadState error={agreements.error} retry={agreements.retry}/>:agreements.data.length?<ul>{agreements.data.map(a=><li key={a.id}>{a.title} · {label(a.status)} · {a.effective_from||'No start'} → {a.effective_to||'No end'}</li>)}</ul>:<p>No agreements recorded.</p>}<Link href={`/agreements?supplier=${id}`}>Manage agreements →</Link></section>,
 rates:<section className="ops-confirmation"><h2>Rates</h2>{agreements.data?.length?agreements.data.map(a=><AgreementRates key={a.id} agreement={a}/>):<p>No agreement rate records available.</p>}<Link href={`/agreements?supplier=${id}`}>Manage agreements and rates →</Link></section>,
 'open-tasks':<EntityTasks kind="supplier" id={id}/>,
 notes:<section className="ops-confirmation"><h2>Supplier notes</h2><p className="ops-preserve-text">{supplier.notes||'No internal notes.'}</p><a href="#supplier-notes">Edit supplier notes →</a></section>,
 history:<EntityHistory kind="supplier" id={id}/>,
 };
 return <PageSurface pageType="supplier-detail" slots={slots} rows={[[[12,['supplier-overview','relationship-status']]]]} context={{supplier_id:Number(id)}}/>;
}
function AgreementRates({agreement}:{agreement:Agreement}){const state=useInventory<{id:number;label:string;unit_type:string;net_amount:string;retail_amount:string|null;effective_from:string;effective_to:string}[]>(`/ops/agreements/${agreement.id}/rates`);return <section><h3>{agreement.title}</h3>{!state.data?<LoadState error={state.error} retry={state.retry}/>:state.data.length?<ul>{state.data.map(r=><li key={r.id}>{r.label} · {label(r.unit_type)} · Net {r.net_amount} · Retail {r.retail_amount??'—'} {agreement.currency} · {r.effective_from} → {r.effective_to}</li>)}</ul>:<p>No rates recorded for this agreement.</p>}</section>;}
export function EntityTasks({kind,id}:{kind:string;id:string|number}){const state=useInventory<Task[]>(`/ops/tasks?related_entity_type=${kind}&related_entity_id=${id}`);return <section className="ops-confirmation"><h2>Related Tasks</h2>{!state.data?<LoadState error={state.error} retry={state.retry}/>:state.data.filter(t=>!['completed','cancelled'].includes(t.status)).length?<ul>{state.data.filter(t=>!['completed','cancelled'].includes(t.status)).map(t=><li key={t.id}><Link href={`/tasks?task=${t.id}`}>{t.title}</Link> · {label(t.status)}</li>)}</ul>:<p>No open tasks for this record.</p>}</section>;}
export function EntityHistory({kind,id}:{kind:string;id:string|number}){const state=useInventory<{id:number;summary:string;actor_name:string;created_at:string}[]>(`/ops/audit?entity_type=${kind}&entity_id=${id}`);return <section className="ops-confirmation"><h2>Authenticated history</h2>{!state.data?<LoadState error={state.error} retry={state.retry}/>:state.data.length?<ul>{state.data.map(a=><li key={a.id}>{a.summary} · {a.actor_name} · <When value={a.created_at}/></li>)}</ul>:<p>No authenticated changes recorded.</p>}</section>;}
