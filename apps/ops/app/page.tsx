import Link from 'next/link';

export default function OpsHome() {
  return <><h1>Operations Dashboard</h1><p>Follow up on booking requests and manage tour inventory. Changes are stored through the API in PostgreSQL.</p><div className="ops-dashboard"><section><h2>Booking requests</h2><p>Review customer and traveler details, snapshotted pricing, and follow-up status.</p><Link className="ops-button" href="/bookings">Open booking inbox</Link></section><section><h2>Tours</h2><p>Create experiences, maintain internal pricing, and choose what appears publicly.</p><Link className="ops-button" href="/tours">Manage tours</Link></section><section><h2>Suppliers</h2><p>Maintain supplier contacts and private operational notes.</p><Link className="ops-button" href="/suppliers">Manage suppliers</Link></section></div><p>Development seed data is illustrative only. Booking requests are not automatic confirmations. Payments, availability checks, and email sending remain deferred.</p></>;
}
