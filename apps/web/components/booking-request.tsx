'use client';
import Link from 'next/link';
import { useEffect, useRef, useState, type FormEvent } from 'react';
import { apiCredentials, requireApiUrl } from '../lib/api';
import type { Tour } from '../lib/inventory';
import { TourPhoto } from './tour-photo';

type Receipt = {reference: string; status: 'new'; tour_name: string; requested_date: string; party_size: number; customer_name: string; message: string};
type Traveler = {first_name: string; last_name: string; traveler_type: string; date_of_birth: string};
const emptyTraveler = (): Traveler => ({first_name: '', last_name: '', traveler_type: 'unknown', date_of_birth: ''});

export function BookingRequest({slug}: {slug: string}) {
  const [tour, setTour] = useState<Tour | null>(null);
  const [loadError, setLoadError] = useState('');
  const [attempt, setAttempt] = useState(0);
  const [travelers, setTravelers] = useState<Traveler[]>([emptyTraveler()]);
  const [partySize, setPartySize] = useState(1);
  const [busy, setBusy] = useState(false);
  const [uncertain, setUncertain] = useState(false);
  const [error, setError] = useState('');
  const [receipt, setReceipt] = useState<Receipt | null>(null);
  const sending = useRef(false);
  const lastBody = useRef('');
  const successHeading = useRef<HTMLHeadingElement>(null);
  const today = new Date().toISOString().slice(0, 10);
  useEffect(() => {
    if (!slug) return;
    let active = true;
    setLoadError('');
    Promise.resolve().then(() => fetch(`${requireApiUrl()}/public/tours/${encodeURIComponent(slug)}`, {cache: 'no-store', credentials: apiCredentials, signal: AbortSignal.timeout(10000)}))
      .then(async response => { if (!response.ok) throw new Error('This experience is unavailable for requests right now.'); return response.json(); })
      .then(data => { if (active) setTour(data); }).catch(error => { if (active) setLoadError(error.message || 'Unable to load this experience.'); });
    return () => { active = false; };
  }, [slug, attempt]);
  useEffect(() => { if (receipt) successHeading.current?.focus(); }, [receipt]);
  function changeTraveler(index: number, key: keyof Traveler, value: string) {
    setTravelers(current => current.map((traveler, i) => i === index ? {...traveler, [key]: value} : traveler));
  }
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (sending.current || receipt) return;
    sending.current = true; setBusy(true); setError('');
    try {
      if (!uncertain) {
        const data = new FormData(event.currentTarget);
        const value = (key: string) => String(data.get(key) || '').trim();
        const payload = {tour_slug: slug, requested_date: value('requested_date'), requested_time: value('requested_time') || null,
          customer: {first_name: value('first_name'), last_name: value('last_name'), email: value('email').toLowerCase(), phone: value('phone') || null, preferred_contact_method: value('preferred_contact_method') || null},
          start_date: value('start_date') || null, end_date: value('end_date') || null, party_size: partySize,
          travelers: travelers.map(traveler => ({...traveler, first_name: traveler.first_name.trim(), last_name: traveler.last_name.trim(), date_of_birth: traveler.date_of_birth || null})),
          customer_notes: value('customer_notes') || null};
        const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(JSON.stringify(payload))))).map(byte => byte.toString(16).padStart(2, '0')).join('');
        let key = crypto.randomUUID();
        // Store no names, emails, DOBs, or notes in browser storage. Retain only
        // a digest and random key so an identical retry can recover its receipt.
        try {
          const saved = JSON.parse(sessionStorage.getItem('vv-booking-submission') || 'null');
          if (saved?.hash === hash && typeof saved.key === 'string') key = saved.key;
          sessionStorage.setItem('vv-booking-submission', JSON.stringify({hash, key}));
        } catch { /* Memory-only duplicate protection still works if storage is unavailable. */ }
        lastBody.current = JSON.stringify({...payload, idempotency_key: key});
      }
      const response = await fetch(`${requireApiUrl()}/public/booking-requests`, {method: 'POST', credentials: apiCredentials, headers: {'Content-Type': 'application/json'}, body: lastBody.current, signal: AbortSignal.timeout(20000)});
      const data = await response.json();
      if (!response.ok) {
        setUncertain(response.status >= 500);
        const detail = data.detail;
        setError(typeof detail === 'string' ? detail : Array.isArray(detail) ? detail.map((item: {loc: string[]; msg: string}) => `${item.loc.slice(1).join('.')}: ${item.msg}`).join('; ') : 'Unable to submit. Please try again.');
        return;
      }
      setReceipt(data); setUncertain(false);
    } catch {
      setUncertain(!!lastBody.current);
      setError('We could not verify receipt. Please retry this same request. Retrying will not create a second request.');
    } finally { sending.current = false; setBusy(false); }
  }
  if (!slug) return <div className="request-message"><h2>Choose your experience</h2><p>Start with a tour and we’ll bring its details into your request.</p><Link className="button button--primary" href="/tours">Explore tours</Link></div>;
  if (!tour) return <div role={loadError ? 'alert' : 'status'}><p>{loadError || 'Loading your selected experience…'}</p>{loadError && <><button className="button button--secondary" onClick={() => setAttempt(value => value + 1)}>Try again</button> <Link href="/tours">Browse tours</Link></>}</div>;
  if (receipt) return <section className="request-success" aria-labelledby="request-received"><p className="eyebrow">Your Costa Rica plans</p><h2 id="request-received" ref={successHeading} tabIndex={-1}>Request Received</h2><p>Reference: <strong data-testid="request-reference">{receipt.reference}</strong></p><dl><dt>Selected tour</dt><dd>{receipt.tour_name}</dd><dt>Requested date</dt><dd>{receipt.requested_date}</dd><dt>Party size</dt><dd>{receipt.party_size}</dd></dl><p>{receipt.message}</p><p>We’ll follow up using the contact details you supplied. This screen acknowledges your request; it does not guarantee a spot. No email has been sent automatically.</p><Link className="button button--primary" href="/tours">Explore more experiences</Link></section>;
  return <div className="request-layout"><aside className="request-selected"><div className="request-photo"><TourPhoto image={tour.primary_image} /></div><p className="eyebrow">Selected experience</p><h2>{tour.name}</h2><p>{tour.short_description}</p><dl><dt>From</dt><dd>${tour.retail_price} USD per person</dd><dt>Duration</dt><dd>{tour.duration}</dd><dt>Location</dt><dd>{tour.location || 'Costa Rica'}</dd></dl><p>We’ll confirm availability and final details before you commit. No payment is collected here.</p></aside>
    <form className="planning-form request-form" onSubmit={submit}>
      <fieldset disabled={busy || uncertain}><legend>Let’s plan your experience</legend>
        <section><h3>Your preferred date</h3><div className="field-grid"><label>Requested date<input name="requested_date" type="date" required min={today} /></label><label>Preferred time <small>(optional, Costa Rica local time)</small><input name="requested_time" type="time" /></label></div></section>
        <section><h3>How can we reach you?</h3><div className="field-grid"><label>First name<input name="first_name" required maxLength={120} autoComplete="given-name" /></label><label>Last name<input name="last_name" required maxLength={120} autoComplete="family-name" /></label><label>Email<input name="email" type="email" required maxLength={180} autoComplete="email" /></label><label>Phone <small>(optional, include country code)</small><input name="phone" type="tel" maxLength={50} autoComplete="tel" /></label><label>Preferred contact method<select name="preferred_contact_method" defaultValue="email"><option value="email">Email</option><option value="phone">Phone</option><option value="whatsapp">WhatsApp</option></select></label></div></section>
        <section><h3>Who’s traveling?</h3><label>Party size<input name="party_size" type="number" required min={travelers.length} max={50} value={partySize} onChange={event => setPartySize(Number(event.target.value))} /></label><p>List at least the primary traveler. Additional names can be confirmed during follow-up. Birth dates are optional.</p>
          {travelers.map((traveler, index) => <fieldset key={index} className="request-traveler"><legend>{index === 0 ? 'Primary traveler' : `Traveler ${index + 1}`}</legend><div className="field-grid"><label>Traveler first name<input name={`traveler_${index}_first_name`} required maxLength={120} value={traveler.first_name} onChange={event => changeTraveler(index, 'first_name', event.target.value)} /></label><label>Traveler last name<input name={`traveler_${index}_last_name`} required maxLength={120} value={traveler.last_name} onChange={event => changeTraveler(index, 'last_name', event.target.value)} /></label><label>Traveler type<select name={`traveler_${index}_type`} value={traveler.traveler_type} onChange={event => changeTraveler(index, 'traveler_type', event.target.value)}>{['unknown', 'adult', 'child', 'infant'].map(type => <option key={type} value={type}>{type}</option>)}</select></label><label>Date of birth <small>(optional)</small><input name={`traveler_${index}_dob`} type="date" max={today} value={traveler.date_of_birth} onChange={event => changeTraveler(index, 'date_of_birth', event.target.value)} /></label></div>{index > 0 && <button type="button" className="request-secondary" onClick={() => setTravelers(current => current.filter((_, i) => i !== index))}>Remove traveler {index + 1}</button>}</fieldset>)}
          <button type="button" className="request-secondary" disabled={travelers.length >= partySize || travelers.length >= 50} onClick={() => setTravelers(current => [...current, emptyTraveler()])}>Add traveler</button>
        </section>
        <section><h3>Your Costa Rica dates <small>(optional)</small></h3><div className="field-grid"><label>Arrival date<input name="start_date" type="date" /></label><label>Departure date<input name="end_date" type="date" /></label></div></section>
        <section><label>Special requests or questions<textarea name="customer_notes" rows={4} maxLength={4000} placeholder="Anything we should know about accessibility or your plans? Please do not include passport or payment details." /></label></section>
      </fieldset>
      <p>This is a request only. We’ll confirm availability before payment is collected.</p>
      {error && <p className="request-error" role="alert">{error}</p>}
      {uncertain && <p>Your details are held while we recover the result. Retry to safely check the same submission.</p>}
      <button className="button button--primary" type="submit" disabled={busy}>{busy ? 'Sending request…' : uncertain ? 'Retry request' : 'Send booking request'}</button>
    </form>
  </div>;
}
