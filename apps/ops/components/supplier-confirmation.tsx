'use client';
import Link from 'next/link';
import {useRef, useState, type FormEvent} from 'react';
import {apiRequest} from '../lib/api';
import {availabilityStatuses, localDateTime, timeLabel} from '../lib/availability';
import {statusLabel, type Booking} from '../lib/bookings';
import type {Tour} from '../lib/inventory';
import {LoadState, useInventory} from './inventory-ui';

const actions = [
  ['contacted', 'Contact Supplier — record contact'], ['follow_up', 'Record follow-up'],
  ['availability_checked', 'Mark reservation availability'], ['confirmed', 'Supplier Confirmed'],
  ['declined', 'Supplier Declined'], ['alternative_offered', 'Offer Alternative'], ['note', 'Add timeline note'],
];

export function SupplierConfirmation({booking, reload}: {booking: Booking; reload: () => void}) {
  const [action, setAction] = useState('contacted');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  // A retry of unchanged form details reuses its command key, including after a
  // timeout. The API deduplicates it before checking the reservation version.
  const pending = useRef<{fingerprint: string; body: string} | null>(null);
  const tours = useInventory<Tour[]>('/ops/tours');
  const availability = booking.product_availability;
  const terminal = ['cancelled', 'completed'].includes(booking.status);
  async function record(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError('');
    const form = new FormData(event.currentTarget);
    const value = (key: string) => String(form.get(key) || '') || null;
    try {
      const payload = {expected_version: booking.version, event_type: terminal ? 'note' : action,
        contact_method: value('contact_method'), operator_identifier: value('operator_identifier'),
        occurred_at: new Date(String(value('occurred_at'))).toISOString(), reference: value('reference'), notes: value('notes'),
        ...(action === 'availability_checked' && !terminal ? {availability_status: value('availability_status')} : {}),
        ...(action === 'alternative_offered' && !terminal ? {alternative_product_id: value('alternative_product_id') ? Number(value('alternative_product_id')) : null, alternative_date: value('alternative_date'), alternative_time: value('alternative_time')} : {})};
      const fingerprint = JSON.stringify(payload);
      if (!pending.current || pending.current.fingerprint !== fingerprint) pending.current = {fingerprint, body: JSON.stringify({...payload, command_id: crypto.randomUUID()})};
      await apiRequest<Booking>(`/ops/bookings/${booking.id}/supplier-events`, {method: 'POST', body: pending.current.body});
      pending.current = null; reload();
    } catch (error) {setError(error instanceof Error ? error.message : 'Unable to record supplier action');}
    finally {setBusy(false);}
  }
  return <section className="ops-confirmation" aria-labelledby="supplier-confirmation-title"><h2 id="supplier-confirmation-title">Availability &amp; Supplier Confirmation</h2>
    <p>{booking.tour_name} · {booking.requested_date} · {booking.requested_time || 'No preferred time'} (Costa Rica local time)</p>
    <div className="ops-booking-grid"><section><h3>Tour / date availability</h3><p><strong>{statusLabel(availability?.status || 'unknown')}</strong> · {availability ? `Source: ${statusLabel(availability.source)}` : 'No recorded date check'}</p><p>Last checked: {timeLabel(availability?.last_checked_at ?? null)}</p>{availability?.stale && <p className="ops-attention">Availability may be stale — check again before relying on it.</p>}
      {availability && <p>Capacity: {availability.capacity ?? 'Unknown'} · Remaining: {availability.remaining_capacity ?? 'Unknown'}</p>}
      {availability?.notes && <p className="ops-preserve-text">{availability.notes}</p>}
      <Link href={`/availability?product_id=${booking.product_id}`}>Manage tour/date availability</Link><p>General availability is a separate snapshot. It does not confirm this reservation or allocate capacity.</p>
      {availability && availability.supplier_id !== booking.supplier.id && <p className="ops-attention">This tour now uses {availability.supplier_name}. The request retains its original supplier below. Check this request directly with that supplier.</p>}
    </section><section><h3>Supplier for this request</h3><p><strong>{booking.supplier.name}</strong>{!booking.supplier.active && ' (inactive)'}<br />{booking.supplier.contact_name || 'No contact name'}<br />{booking.supplier.email || 'No email recorded'}<br />{booking.supplier.phone || 'No phone recorded'}</p><p>Latest contact: {timeLabel(booking.supplier_contacted_at)}</p><p>Confirmation received: {timeLabel(booking.supplier_confirmed_at)}</p><p>Reference: <strong>{booking.supplier_confirmation_reference || 'None recorded'}</strong></p>{booking.supplier_response_notes && <p className="ops-preserve-text">{booking.supplier_response_notes}</p>}</section></div>
    <div className="ops-confirmation-state" data-testid="confirmation-state"><p>Reservation availability: <strong>{statusLabel(booking.availability_status)}</strong></p><p>Supplier confirmation: <strong>{statusLabel(booking.supplier_confirmation_status)}</strong></p>{booking.ready_for_payment ? <p className="ops-badge"><strong>{booking.payment_received ? 'Supplier requirements satisfied' : 'Ready for Payment'}</strong> · See Payment for checkout status.</p> : <p>Not ready for payment.</p>}{booking.needs_attention && <p className="ops-attention">Needs Attention{booking.supplier_confirmation_status === 'declined' ? ' — Alternative Needed' : ''}</p>}</div>
    <form className="ops-editor" onSubmit={record}><fieldset disabled={busy}><legend>Record supplier action</legend><p>Record communication that has taken place. This form does not send a message.</p><div className="ops-fields"><label>Action<select name="event_type" value={terminal ? 'note' : action} onChange={e => {setAction(e.target.value); setError('');}}>{actions.filter(([kind]) => !terminal || kind === 'note').map(([kind, label]) => <option key={kind} value={kind}>{label}</option>)}</select></label>
      <label>Occurred at (your local time)<input type="datetime-local" name="occurred_at" required defaultValue={localDateTime()} /></label>
      <label>Contact method<select name="contact_method" required={!terminal && ['contacted', 'follow_up'].includes(action)}><option value="">Not applicable</option>{['phone', 'email', 'whatsapp', 'supplier_portal', 'other'].map(s => <option key={s} value={s}>{s === 'whatsapp' ? 'WhatsApp' : statusLabel(s)}</option>)}</select></label>
      <label>Operator identifier (optional)<input name="operator_identifier" maxLength={120} /></label>
      {action === 'availability_checked' && !terminal && <label>Reservation availability<select name="availability_status">{availabilityStatuses.map(s => <option key={s} value={s}>{statusLabel(s)}</option>)}</select><small>Available / limited / unavailable apply to this request. Use Manage tour/date availability for general date checks.</small></label>}
      {action === 'confirmed' && !terminal && <label>Supplier confirmation reference (optional)<input name="reference" maxLength={200} /></label>}
      {action === 'alternative_offered' && !terminal && <><label>Alternative tour (optional)<select name="alternative_product_id"><option value="">Same tour / describe in note</option>{tours.data?.filter(t => t.active).map(t => <option key={t.id} value={t.id}>{t.name}</option>)}</select></label><label>Alternative date (optional)<input name="alternative_date" type="date" min={new Date().toISOString().slice(0, 10)} /></label><label>Alternative time (Costa Rica local)<input name="alternative_time" type="time" /></label></>}
    </div>{action === 'alternative_offered' && !tours.data && <LoadState error={tours.error} retry={tours.retry} />}
    {booking.supplier_confirmation_status === 'confirmed' && <p className="ops-attention">Changing a supplier confirmation requires a corrective note. The original confirmation remains in the timeline.</p>}
    {action === 'alternative_offered' && <p>An alternative is a proposal. The original requested tour, dates and prices stay unchanged.</p>}
    <label>Response / notes<textarea name="notes" rows={3} maxLength={10000} required={terminal || action === 'note' || (booking.supplier_confirmation_status === 'confirmed' && ['contacted', 'confirmed', 'declined', 'alternative_offered'].includes(action))} /></label><button type="submit">{busy ? 'Recording…' : 'Record action'}</button></fieldset>{error && <p role="alert">{error} <button type="button" onClick={reload}>Reload booking</button></p>}</form>
    <h3>Supplier contact timeline</h3>{!booking.supplier_events.length ? <p>No supplier actions recorded.</p> : <ol className="ops-timeline">{booking.supplier_events.map(event => <li key={event.id}><strong>{statusLabel(event.event_type)}</strong> · {timeLabel(event.occurred_at)}{event.contact_method && ` · ${event.contact_method === 'whatsapp' ? 'WhatsApp' : statusLabel(event.contact_method)}`}{event.operator_identifier && ` · ${event.operator_identifier}`}<p>Reservation: {statusLabel(event.reservation_status)} · Availability: {statusLabel(event.availability_status)} · Supplier: {statusLabel(event.status)}</p>{event.reference && <p>Reference: {event.reference}</p>}{(event.alternative_tour_name || event.alternative_date || event.alternative_time) && <p>Proposed alternative: {event.alternative_tour_name || booking.tour_name} · {event.alternative_date || 'Date to discuss'} · {event.alternative_time || 'Time to discuss'}</p>}{event.notes && <p className="ops-preserve-text">{event.notes}</p>}<small>Recorded {timeLabel(event.created_at)}</small></li>)}</ol>}
  </section>;
}
