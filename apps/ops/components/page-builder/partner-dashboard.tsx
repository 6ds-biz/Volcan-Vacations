'use client';
import Link from 'next/link';
import type {DashboardData} from '../dashboard';
import {PageHeader,Modules,NeedsAttention,label,useIdentity} from '../ops-ui';
import {MyTasks} from '../tasks';
import {PageSurface} from './page-surface';
export function PartnerDashboard({data}:{data:DashboardData}){
 const user=useIdentity();const slots={
 'new-bookings':<Modules items={[{label:'New Booking Requests',value:data.booking_counts?.new||0,href:'/bookings?view=new'},{label:'Awaiting Supplier',value:data.booking_counts?.awaiting_supplier||0,href:'/bookings?view=awaiting_supplier'},{label:'Ready for Payment',value:data.booking_counts?.ready||0,href:'/bookings?view=ready'},{label:'Paid Bookings',value:data.booking_counts?.paid||0,href:'/bookings?view=paid'}]}/>,
 'needs-attention':<NeedsAttention items={data.attention}/>, 'my-tasks':<MyTasks tasks={data.my_tasks}/>,
 'vendor-work':<section className="dashboard-section"><div className="section-heading"><h2>Vendor Work</h2><Link href="/suppliers">View suppliers →</Link></div><div className="vendor-pipeline">{Object.entries(data.vendor_counts||{}).map(([key,count])=><div key={key}><strong>{count}</strong><span>{label(key)}</span></div>)}</div><small>Active suppliers · current relationship status</small></section>,
 availability:<section className="dashboard-section"><h2>Availability & Inventory</h2><div className="vendor-pipeline"><div><strong>{data.inventory_counts?.active||0}</strong><span>Active tours</span></div><div><strong>{data.inventory_counts?.needs_review||0}</strong><span>Missing image or summary</span></div><div><strong>{data.inventory_counts?.stale_availability||0}</strong><span>Upcoming checks stale</span></div></div><Link href="/availability">Review availability →</Link></section>,
 'supplier-followup':<section className="dashboard-section"><h2>Supplier Follow-up</h2><p>{data.booking_counts?.awaiting_supplier||0} requests await supplier confirmation.</p><Link href="/bookings?view=awaiting_supplier">Open supplier queue →</Link><h3>Shared Work</h3><p>{data.task_counts.shared} open tasks await assignment.</p><Link href="/tasks?shared=true">Open task queue →</Link></section>,
 'transportation-lookup':<section className="dashboard-section"><h2>Transportation Lookup</h2><p>Find routes and schedules; confirm directly with the vendor.</p><Link href="/transportation">Look up transportation →</Link></section>,
 };
 return <div className="dashboard-content execution-dashboard">{user.role==='owner_admin'&&<p><Link href="/">← Owner dashboard</Link> · Preview uses your own permitted live work.</p>}<PageHeader title="Today in Operations" description="Daily booking execution and vendor follow-up" icon="dashboard"/><PageSurface pageType="operations-dashboard" slots={slots} rows={[[[12,['new-bookings']]],[[7,['needs-attention']],[5,['my-tasks']]],[[7,['vendor-work','availability']],[5,['supplier-followup']]]]} context={{dashboard_profile:'Operations'}}/></div>;
}
