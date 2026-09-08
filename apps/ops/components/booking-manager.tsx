'use client';
import {ContactActions} from './ops-ui';
import Link from 'next/link';
import {PageHeader} from './ops-ui';
import {RelatedTasks} from './tasks';
import {BookingExtras} from './booking-extras';
import { useState, type FormEvent } from 'react';
import { apiRequest } from '../lib/api';
import { bookingStatuses, statusLabel, type Booking } from '../lib/bookings';
import { LoadState, useInventory } from './inventory-ui';
import { SupplierConfirmation } from './supplier-confirmation';
import { PaymentPanel } from './payment-manager';
import {PageSurface} from './page-builder/page-surface';

export function BookingInbox() {
  const [status, setStatus] = useState('');
  const [attention, setAttention] = useState(true);
  const [supplierStatus, setSupplierStatus] = useState('');
  const {data, error, retry} = useInventory<Booking[]>(`/ops/bookings?${new URLSearchParams({... (status ? {status} : {}), ...(attention ? {needs_attention: 'true'} : {}), ...(supplierStatus ? {supplier_status: supplierStatus} : {})})}`);
  return <><h1>Bookings</h1><p>Newest actionable requests first. These are requests for follow-up, not automatic supplier confirmations.</p><label className="ops-status-filter">Filter by status<select value={status} onChange={event => setStatus(event.target.value)}>{['', ...bookingStatuses].map(value => <option key={value} value={value}>{value ? statusLabel(value) : 'All'}</option>)}</select></label>
    <label className="ops-check"><input type="checkbox" checked={attention} onChange={e => setAttention(e.target.checked)} />Needs Attention only</label><label className="ops-status-filter">Supplier confirmation filter<select value={supplierStatus} onChange={e => setSupplierStatus(e.target.value)}><option value="">All supplier states</option>{['not_requested', 'awaiting_supplier', 'confirmed', 'declined', 'alternative_offered'].map(s => <option key={s} value={s}>{statusLabel(s)}</option>)}</select></label>
    {!data ? <LoadState error={error} retry={retry} /> : !data.length ? <p role="status">No booking requests match this status.</p> : <div className="ops-table-wrap" tabIndex={0} role="region" aria-label="Booking inbox"><table className="ops-booking-table"><caption>Customer requests · internal only</caption><thead><tr>{['Reference', 'Customer', 'Tour', 'Requested date', 'Party', 'Status / availability', 'Submitted', 'Supplier / attention'].map(label => <th key={label}>{label}</th>)}</tr></thead><tbody>{data.map(booking => <tr key={booking.id}><td><Link href={`/bookings/${booking.id}`}>{booking.reference}</Link></td><td>{(booking.submitted_contact || booking.customer).first_name} {(booking.submitted_contact || booking.customer).last_name}</td><td>{booking.tour_name}</td><td>{booking.requested_date}</td><td>{booking.quantity}</td><td>{statusLabel(booking.status)}<br /><span className="ops-badge">{statusLabel(booking.availability_status)}</span></td><td>{new Date(booking.created_at).toLocaleString()}</td><td>{statusLabel(booking.supplier_confirmation_status)}{booking.needs_attention && <p className="ops-attention">Needs Attention{booking.supplier_confirmation_status === 'declined' ? ' — Alternative Needed' : ''}</p>}{booking.payment_received ? <p className="ops-badge">{statusLabel(booking.payment_status || 'Paid')}</p> : booking.ready_for_payment && <p className="ops-badge">Ready for Payment</p>}</td></tr>)}</tbody></table></div>}</>;
}

export function BookingDetail({id}: {id: string}) {
  const {data, error, retry} = useInventory<Booking>(`/ops/bookings/${id}`);
  return <><Link href="/bookings">← Bookings</Link><PageHeader title="Booking Detail" description="Request, supplier confirmation and payment history" icon="bookings"/>{!data ? <LoadState error={error} retry={retry} /> : <BookingRecord key={data.version} booking={data} reload={retry} />}</>;
}

function BookingRecord({booking, reload}: {booking: Booking; reload: () => void}) {
  const [status, setStatus] = useState(booking.status);
  const [tripStatus, setTripStatus] = useState(booking.trip.status);
  const [notes, setNotes] = useState(booking.internal_notes || '');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [saved, setSaved] = useState(false);
  const [current, setCurrent] = useState(booking);
  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError(''); setSaved(false);
    try {
      const result = await apiRequest<Booking>(`/ops/bookings/${booking.id}`, {method: 'PUT', body: JSON.stringify({status, expected_status: current.status, expected_version: current.version, internal_notes: notes || null, trip_status: tripStatus === current.trip.status ? null : tripStatus})});
      setCurrent(result); setSaved(true);
    } catch (error) { setError(error instanceof Error ? error.message : 'Unable to save'); }
    finally { setBusy(false); }
  }
  const contact = booking.submitted_contact || booking.customer;
  const slots={
 'booking-summary':<section><h2>Requested experience</h2><dl><dt>Tour</dt><dd>{booking.tour_name}</dd><dt>Requested date / time</dt><dd>{booking.requested_date} · {booking.requested_time || 'No preferred time'} (Costa Rica local time)</dd><dt>Quantity</dt><dd>{booking.quantity}</dd><dt>Retail price per person</dt><dd>${booking.unit_price} USD</dd><dt>Supplier cost per person</dt><dd>${booking.supplier_unit_cost} USD</dd><dt>Retail total</dt><dd>${booking.retail_total} USD</dd><dt>Gross margin — entire request</dt><dd>${booking.gross_margin} USD</dd></dl><p>Prices are snapshots from submission, not today’s tour pricing.</p></section>,
 customer:<section id="booking-contact"><h2>Submitted contact</h2><p>{contact.first_name} {contact.last_name}<br />{contact.email}<br />{contact.phone || 'No phone supplied'}</p><ContactActions email={contact.email} phone={contact.phone}/><p>Preferred contact: {contact.preferred_contact_method || 'Not specified'}</p><details><summary>Linked customer record (internal)</summary><p>{booking.customer.first_name} {booking.customer.last_name}<br />{booking.customer.email}<br />{booking.customer.phone}</p><p>{booking.customer.notes || 'No internal customer notes'}</p></details><p>Email matching is not identity verification. Public submissions do not overwrite existing customer details.</p></section>, travelers:<section><h2>Travelers</h2><ul>{booking.travelers.map(traveler => <li key={traveler.id}>{traveler.first_name} {traveler.last_name} — {traveler.traveler_type || 'unknown'}{traveler.date_of_birth ? ` · DOB: ${traveler.date_of_birth}` : ''}</li>)}</ul>{booking.travelers.length < booking.quantity && <p>Additional traveler names need follow-up.</p>}</section>, trip:<section><h2>Trip</h2><dl><dt>Travel dates</dt><dd>{booking.trip.start_date || 'Not supplied'} → {booking.trip.end_date || 'Not supplied'}</dd><dt>Party size</dt><dd>{booking.trip.party_size}</dd><dt>Trip status</dt><dd>{statusLabel(current.trip.status)}</dd></dl><p>{booking.trip.notes}</p></section>,
 availability:<section className="ops-confirmation"><h2>Availability</h2><p>{statusLabel(current.availability_status)}</p><p>Requested date: {booking.requested_date}. Confirm with the supplier before payment.</p></section>,
 'supplier-confirmation':<div id="booking-supplier"><SupplierConfirmation key={current.version} booking={current} reload={reload}/></div>,
 payment:<div id="booking-payment"><PaymentPanel booking={current} onBookingChange={setCurrent}/></div>,
 'related-tasks':<div id="booking-tasks"><RelatedTasks bookingId={booking.id}/></div>,
 notes:<><section className="ops-booking-notes"><h2>Customer notes</h2><p>{booking.customer_notes || 'No special requests supplied.'}</p></section><form id="booking-followup" className="ops-editor" onSubmit={save}><fieldset disabled={busy}><legend>Operations follow-up</legend><div className="ops-fields"><label>Reservation status<select name="status" value={status} onChange={event => setStatus(event.target.value)}>{current.allowed_statuses.map(value => <option value={value} key={value}>{statusLabel(value)}</option>)}</select></label><label>Trip status<select name="trip_status" value={tripStatus} onChange={event => setTripStatus(event.target.value)}>{[...new Set([booking.trip.status, 'inquiry', 'planning', 'confirmed', 'completed', 'cancelled'])].map(value => <option value={value} key={value}>{statusLabel(value)}</option>)}</select></label></div><p>Trip status is separate. Change it deliberately after reviewing the whole trip. No supplier message, availability check, or email is sent.</p><label>Internal notes<textarea name="internal_notes" rows={5} maxLength={10000} value={notes} onChange={event => setNotes(event.target.value)} /></label><button type="submit">{busy ? 'Saving…' : 'Save follow-up'}</button></fieldset>{error && <p role="alert">{error} <button type="button" onClick={reload}>Reload booking</button></p>}{saved && <p role="status">Follow-up saved.</p>}</form></>,
 history:<div id="booking-history"><BookingExtras id={booking.id} reload={reload}/></div>,
 };
 return <><h2>{booking.reference}</h2><p>Status: <strong>{statusLabel(current.status)}</strong> · Submitted {new Date(booking.created_at).toLocaleString()}</p>
    <nav className="record-jumps" aria-label="Booking sections"><a href="#booking-contact">Customer</a><a href="#booking-supplier">Availability / supplier</a><a href="#booking-payment">Payment</a><a href="#booking-tasks">Tasks</a><a href="#booking-followup">Notes / status</a><a href="#booking-history">History</a></nav>{current.needs_attention&&<p className="ops-attention">Needs Attention · {statusLabel(current.supplier_confirmation_status)}</p>}<PageSurface pageType="booking-detail" slots={slots} rows={[[[6,['booking-summary']],[6,['customer']]],[[6,['travelers']],[6,['trip']]],[[12,['supplier-confirmation','payment','related-tasks','notes','history']]]]} context={{booking_id:booking.id}}/></>;
}
