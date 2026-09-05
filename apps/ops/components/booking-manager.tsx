'use client';
import Link from 'next/link';
import { useState, type FormEvent } from 'react';
import { apiRequest } from '../lib/api';
import { bookingStatuses, statusLabel, type Booking } from '../lib/bookings';
import { LoadState, useInventory } from './inventory-ui';

export function BookingInbox() {
  const [status, setStatus] = useState('new');
  const {data, error, retry} = useInventory<Booking[]>(`/ops/bookings${status ? `?status=${status}` : ''}`);
  return <><h1>Bookings</h1><p>Newest actionable requests first. These are requests for follow-up, not automatic supplier confirmations.</p><label className="ops-status-filter">Filter by status<select value={status} onChange={event => setStatus(event.target.value)}>{['', ...bookingStatuses].map(value => <option key={value} value={value}>{value ? statusLabel(value) : 'All'}</option>)}</select></label>
    {!data ? <LoadState error={error} retry={retry} /> : !data.length ? <p role="status">No booking requests match this status.</p> : <div className="ops-table-wrap" tabIndex={0} role="region" aria-label="Booking inbox"><table className="ops-booking-table"><caption>Customer requests · internal only</caption><thead><tr>{['Reference', 'Customer', 'Tour', 'Requested date', 'Party', 'Status', 'Submitted', 'Attention'].map(label => <th key={label}>{label}</th>)}</tr></thead><tbody>{data.map(booking => <tr key={booking.id}><td><Link href={`/bookings/${booking.id}`}>{booking.reference}</Link></td><td>{(booking.submitted_contact || booking.customer).first_name} {(booking.submitted_contact || booking.customer).last_name}</td><td>{booking.tour_name}</td><td>{booking.requested_date}</td><td>{booking.quantity}</td><td>{statusLabel(booking.status)}</td><td>{new Date(booking.created_at).toLocaleString()}</td><td>{booking.status === 'new' ? 'Needs follow-up' : '—'}</td></tr>)}</tbody></table></div>}</>;
}

export function BookingDetail({id}: {id: string}) {
  const {data, error, retry} = useInventory<Booking>(`/ops/bookings/${id}`);
  return <><Link href="/bookings">← Bookings</Link><h1>Booking request</h1>{!data ? <LoadState error={error} retry={retry} /> : <BookingRecord key={data.updated_at} booking={data} reload={retry} />}</>;
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
      const result = await apiRequest<Booking>(`/ops/bookings/${booking.id}`, {method: 'PUT', body: JSON.stringify({status, expected_status: current.status, internal_notes: notes || null, trip_status: tripStatus === current.trip.status ? null : tripStatus})});
      setCurrent(result); setSaved(true);
    } catch (error) { setError(error instanceof Error ? error.message : 'Unable to save'); }
    finally { setBusy(false); }
  }
  const contact = booking.submitted_contact || booking.customer;
  return <><h2>{booking.reference}</h2><p>Status: <strong>{statusLabel(current.status)}</strong> · Submitted {new Date(booking.created_at).toLocaleString()}</p>
    <div className="ops-booking-grid"><section><h2>Requested experience</h2><dl><dt>Tour</dt><dd>{booking.tour_name}</dd><dt>Requested date / time</dt><dd>{booking.requested_date} · {booking.requested_time || 'No preferred time'} (Costa Rica local time)</dd><dt>Quantity</dt><dd>{booking.quantity}</dd><dt>Retail price per person</dt><dd>${booking.unit_price} USD</dd><dt>Supplier cost per person</dt><dd>${booking.supplier_unit_cost} USD</dd><dt>Retail total</dt><dd>${booking.retail_total} USD</dd><dt>Gross margin — entire request</dt><dd>${booking.gross_margin} USD</dd></dl><p>Prices are snapshots from submission, not today’s tour pricing.</p></section>
    <section><h2>Submitted contact</h2><p>{contact.first_name} {contact.last_name}<br />{contact.email}<br />{contact.phone || 'No phone supplied'}</p><p>Preferred contact: {contact.preferred_contact_method || 'Not specified'}</p><details><summary>Linked customer record (internal)</summary><p>{booking.customer.first_name} {booking.customer.last_name}<br />{booking.customer.email}<br />{booking.customer.phone}</p><p>{booking.customer.notes || 'No internal customer notes'}</p></details><p>Email matching is not identity verification. Public submissions do not overwrite existing customer details.</p></section>
    <section><h2>Travelers</h2><ul>{booking.travelers.map(traveler => <li key={traveler.id}>{traveler.first_name} {traveler.last_name} — {traveler.traveler_type || 'unknown'}{traveler.date_of_birth ? ` · DOB: ${traveler.date_of_birth}` : ''}</li>)}</ul>{booking.travelers.length < booking.quantity && <p>Additional traveler names need follow-up.</p>}</section>
    <section><h2>Trip</h2><dl><dt>Travel dates</dt><dd>{booking.trip.start_date || 'Not supplied'} → {booking.trip.end_date || 'Not supplied'}</dd><dt>Party size</dt><dd>{booking.trip.party_size}</dd><dt>Trip status</dt><dd>{statusLabel(current.trip.status)}</dd></dl><p>{booking.trip.notes}</p></section></div>
    <section className="ops-booking-notes"><h2>Customer notes</h2><p>{booking.customer_notes || 'No special requests supplied.'}</p></section>
    <form className="ops-editor" onSubmit={save}><fieldset disabled={busy}><legend>Operations follow-up</legend><div className="ops-fields"><label>Reservation status<select name="status" value={status} onChange={event => setStatus(event.target.value)}>{current.allowed_statuses.map(value => <option value={value} key={value}>{statusLabel(value)}</option>)}</select></label><label>Trip status<select name="trip_status" value={tripStatus} onChange={event => setTripStatus(event.target.value)}>{[...new Set([booking.trip.status, 'inquiry', 'planning', 'confirmed', 'completed', 'cancelled'])].map(value => <option value={value} key={value}>{statusLabel(value)}</option>)}</select></label></div><p>Trip status is separate. Change it deliberately after reviewing the whole trip. No supplier message, availability check, or email is sent.</p><label>Internal notes<textarea name="internal_notes" rows={5} maxLength={10000} value={notes} onChange={event => setNotes(event.target.value)} /></label><button type="submit">{busy ? 'Saving…' : 'Save follow-up'}</button></fieldset>{error && <p role="alert">{error} <button type="button" onClick={reload}>Reload booking</button></p>}{saved && <p role="status">Follow-up saved.</p>}</form>
  </>;
}
