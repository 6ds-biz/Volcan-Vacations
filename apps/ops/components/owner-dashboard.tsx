'use client';
import Link from 'next/link';
import {Modules,NeedsAttention,PageHeader,label,When} from './ops-ui';
import {MyTasks} from './tasks';
import type {DashboardData} from './dashboard';
import {PageSurface} from './page-builder/page-surface';

/** Existing live Owner modules supplied to the reusable presentation renderer. */
export function OwnerDashboard({data}:{data:DashboardData}){
 const modules={
  'business-health':<Modules items={data.booking_counts?[
   {label:'New Booking Requests',icon:'work',tone:'blue',hint:'Awaiting review',value:data.booking_counts.new,href:'/bookings?view=new'},
   {label:'Awaiting Supplier',icon:'users',tone:'gold',hint:'Needs follow-up',value:data.booking_counts.awaiting_supplier,href:'/bookings?view=awaiting_supplier'},
   {label:'Ready for Payment',icon:'payments',tone:'positive',hint:'Customer action needed',value:data.booking_counts.ready,href:'/bookings?view=ready'},
   {label:'Paid Bookings',icon:'tasks',tone:'complete',hint:'Payment received',value:data.booking_counts.paid,href:'/bookings?view=paid'},
  ]:[]}/>,
  'needs-attention':<NeedsAttention items={data.attention}/>,
  'my-tasks':<MyTasks tasks={data.my_tasks}/>,
  'vendor-pipeline':data.vendor_counts&&<section className="dashboard-section"><div className="section-heading"><h2>Vendor Pipeline</h2><Link href="/suppliers">View suppliers →</Link></div><div className="vendor-pipeline">{Object.entries(data.vendor_counts).map(([key,count])=><div key={key}><strong>{count}</strong><span>{label(key)}</span></div>)}</div><small>Active suppliers · current relationship status</small></section>,
  'inventory':data.inventory_counts&&<section className="dashboard-section"><h2>Inventory</h2><div className="vendor-pipeline"><div><strong>{data.inventory_counts.active}</strong><span>Active tours</span></div><div><strong>{data.inventory_counts.needs_review}</strong><span>Missing image or summary</span></div><div><strong>{data.inventory_counts.stale_availability}</strong><span>Upcoming checks stale</span></div></div><Link href="/availability">Review availability →</Link></section>,
  'recent-payments':<section className="dashboard-section"><div className="section-heading"><h2>Recent Payments</h2><Link href="/payments">View payments →</Link></div>{data.recent_payments?.length?<ul className="task-compact">{data.recent_payments.map(p=><li key={p.id}><Link href={p.reservation_id?`/bookings/${p.reservation_id}`:'/payments'}>${p.amount} {p.currency} · {label(p.status)}</Link><small><When value={p.paid_at}/></small></li>)}</ul>:<p>No payments received.</p>}</section>,
 };
 return <div className="dashboard-content owner-content">
  <Link href="/?dashboard=operations">Operations Partner layout →</Link><PageHeader title="Business Overview" description="Bookings, vendor relationships and work requiring attention" icon="dashboard"/>
  <PageSurface pageType="owner-dashboard" slots={modules} rows={[[[12,['business-health']]],[[7,['needs-attention','vendor-pipeline','inventory']],[5,['my-tasks','recent-payments','visual-feature']]]]} context={{dashboard_profile:'Owner'}}/>
 </div>;
}
