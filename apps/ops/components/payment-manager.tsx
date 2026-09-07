'use client';
import Link from 'next/link';
import {useState, type FormEvent} from 'react';
import {apiRequest, publicPageUrl} from '../lib/api';
import {type Booking, statusLabel} from '../lib/bookings';
import {timeLabel} from '../lib/availability';
import type {BookingPayment, Payment} from '../lib/payments';
import {LoadState, useInventory} from './inventory-ui';

export function PaymentPanel({booking, onBookingChange}: {booking: Booking; onBookingChange: (value: Booking) => void}) {
  const state = useInventory<BookingPayment>(`/ops/bookings/${booking.id}/payment`, booking.version);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [url, setUrl] = useState('');
  const [copied, setCopied] = useState(false);
  async function updateBooking() {
    onBookingChange(await apiRequest<Booking>(`/ops/bookings/${booking.id}`)); state.retry();
  }
  async function issue(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError(''); setCopied(false);
    const date = new FormData(event.currentTarget).get('payment_due_at');
    try {
      const link = await apiRequest<{path: string; expires_at: string}>(`/ops/bookings/${booking.id}/payment-link`, {method: 'POST', body: JSON.stringify({expected_version: booking.version, payment_due_at: date ? new Date(String(date)).toISOString() : null})});
      setUrl(publicPageUrl(link.path) || link.path);
      await updateBooking();
    } catch (error) {setError(error instanceof Error ? error.message : 'Unable to create link');}
    finally {setBusy(false);}
  }
  async function action(kind: 'revoke' | 'reconcile' | 'refresh') {
    setBusy(true); setError('');
    try {
      if (kind === 'revoke') {
        await apiRequest(`/ops/bookings/${booking.id}/payment-link/revoke`, {method: 'POST', body: JSON.stringify({expected_version: booking.version})});
        setUrl('');
      } else if (kind === 'reconcile') {
        await apiRequest(`/ops/bookings/${booking.id}/payment/reconcile`, {method: 'POST', signal: AbortSignal.timeout(45000)});
      }
      await updateBooking();
    } catch (error) {setError(error instanceof Error ? error.message : 'Unable to update payment');}
    finally {setBusy(false);}
  }
  const data = state.data;
  return <section className="ops-confirmation" aria-labelledby="payment-title"><h2 id="payment-title">Payment</h2>
    {!data ? <LoadState error={state.error} retry={state.retry} /> : <><div className="ops-booking-grid"><section><h3>{data.label}</h3><dl><dt>Eligibility</dt><dd>{data.eligible ? 'Supplier-confirmed and unpaid' : 'Not payable'}</dd><dt>Amount due — reservation snapshot</dt><dd>${data.amount_due} {data.currency}</dd><dt>Payment due</dt><dd>{data.payment_due_at ? timeLabel(data.payment_due_at) : 'Set when issuing payment link'}</dd></dl>{data.overdue && <p className="ops-attention">Overdue — review and issue a renewed link/deadline. No supplier booking has been released.</p>}<p>PayPal Sandbox only. One reservation per checkout.</p>
    {!data.sandbox_configured && <p className="ops-attention">Sandbox credentials are missing or configuration is unsupported. Checkout is unavailable.</p>}{!data.webhook_configured && <p className="ops-attention">PayPal webhook ID is not configured. Real webhook verification cannot run yet.</p>}</section>
    <section><h3>Payment record</h3>{!data.payment ? <p>No payment initiated.</p> : <><dl><dt>Status</dt><dd>{statusLabel(data.payment.status)}</dd><dt>Provider</dt><dd>{data.payment.provider} · {data.payment.provider_environment}</dd><dt>Amount</dt><dd>${data.payment.amount} {data.payment.currency}</dd><dt>PayPal order</dt><dd>{data.payment.provider_order_id || 'Not assigned'}</dd><dt>Capture / reference</dt><dd>{data.payment.provider_capture_id || 'Not captured'}</dd><dt>Paid at</dt><dd>{data.payment.paid_at ? timeLabel(data.payment.paid_at) : 'Unpaid'}</dd><dt>Refunded amount</dt><dd>${data.payment.refunded_amount} {data.payment.currency}</dd></dl>{data.payment.reconciliation_required && <p className="ops-attention">Reconciliation / review required</p>}{data.payment.failure_code && <p className="ops-preserve-text">{data.payment.failure_code}: {data.payment.failure_message}</p>}</>}</section></div>
      <form className="ops-editor" onSubmit={issue}><fieldset disabled={busy || !booking.ready_for_payment || booking.payment_received}><legend>Customer payment link</legend><p>Generate a private link for this customer. It replaces the previous link and expires within seven days. No message is sent.</p><label>Payment due (your local time, optional)<input name="payment_due_at" type="datetime-local" /><small>Defaults to seven days from now. A renewed deadline does not alter supplier confirmation.</small></label><button type="submit">Generate payment link</button></fieldset></form>
      {url && <div className="ops-payment-link"><label>Private customer payment URL<input readOnly value={url} onFocus={e => e.target.select()} /></label><p>Anyone with this link can view this reservation’s payment summary. Share only with its customer.</p><div className="ops-actions"><a className="ops-button" href={url} target="_blank" rel="noopener noreferrer">Open customer payment page</a><button disabled={busy} onClick={async () => {try {await navigator.clipboard.writeText(url); setCopied(true);} catch {setError('Copy was unavailable. Select and copy the link manually.');}}}>{copied ? 'Copied' : 'Copy payment link'}</button></div></div>}
      <div className="ops-actions"><button disabled={busy} onClick={() => action('refresh')}>Refresh payment</button>{data.link_active && <button disabled={busy} onClick={() => action('revoke')}>Revoke payment link</button>}{data.payment?.provider_order_id && <button disabled={busy || !data.sandbox_configured} onClick={() => action('reconcile')}>Reconcile with PayPal</button>}<Link href="/payments">All payments</Link></div>
    </>}{error && <p role="alert">{error} <button disabled={busy} onClick={() => action('refresh')}>Reload booking state</button></p>}
  </section>;
}

export function PaymentList() {
  const [status, setStatus] = useState('');
  const state = useInventory<Payment[]>(`/ops/payments${status ? `?status=${status}` : ''}`);
  return <><h1>Payments</h1><p>One reservation per checkout. PayPal Sandbox only. Refunds are reconciled from verified notifications; no refund action is available here.</p><label className="ops-status-filter">Payment filter<select value={status} onChange={e => setStatus(e.target.value)}>{['', 'pending', 'paid', 'failed', 'refunded'].map(s => <option key={s} value={s}>{s ? statusLabel(s) : 'All'}</option>)}</select></label>
    {!state.data ? <LoadState error={state.error} retry={state.retry} /> : !state.data.length ? <p role="status">No payments match this filter.</p> : <div className="ops-table-wrap" tabIndex={0} role="region" aria-label="Payment list"><table className="ops-payment-table"><caption>Internal payment records</caption><thead><tr>{['Booking', 'Customer / tour', 'Amount', 'Status', 'Provider', 'Created / paid', 'Review'].map(s => <th key={s}>{s}</th>)}</tr></thead><tbody>{state.data.map(p => <tr key={p.id}><td>{p.reservation_id ? <Link href={`/bookings/${p.reservation_id}`}>{p.booking_reference}</Link> : p.booking_reference}</td><td>{p.customer}<br />{p.tour}</td><td>${p.amount} {p.currency}</td><td><span className="ops-badge">{statusLabel(p.status)}</span></td><td>{p.provider}<br />{p.provider_environment}</td><td>{timeLabel(p.created_at)}<br />{p.paid_at ? timeLabel(p.paid_at) : 'Unpaid'}</td><td>{p.reconciliation_required ? 'Review required' : p.failure_code || '—'}</td></tr>)}</tbody></table></div>}
  </>;
}
