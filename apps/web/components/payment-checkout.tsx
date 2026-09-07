'use client';
import Link from 'next/link';
import {useCallback, useEffect, useRef, useState} from 'react';
import {apiCredentials, requireApiUrl} from '../lib/api';

type Payment = {
  booking_reference: string; tour: string; date: string; party_size: number;
  amount: string; amount_due: string; amount_paid: string; currency: string;
  provider: 'PayPal'; status: string; eligible: boolean; checkout_available: boolean;
  retryable: boolean; message: string; client_id: string | null; environment: 'sandbox'; order_id: string | null;
};
type PayPalButtons = {render: (element: HTMLElement) => Promise<void>; close: () => Promise<void>};
type PayPalSDK = {Buttons: (options: {
  style: {layout: string; color: string; label: string};
  createOrder: () => Promise<string>;
  onApprove: (data: {orderID: string}) => Promise<void>;
  onCancel: (data: {orderID?: string}) => Promise<void>;
  onError: () => void;
}) => PayPalButtons};

declare global { interface Window { vvPayPal?: PayPalSDK; } }
let sdkPromise: Promise<PayPalSDK> | null = null;
let sdkClient: string | null = null;
function loadSDK(clientId: string): Promise<PayPalSDK> {
  if (sdkPromise && sdkClient === clientId) return sdkPromise;
  sdkClient = clientId;
  sdkPromise = new Promise<PayPalSDK>((resolve, reject) => {
    document.getElementById('vv-paypal-sdk')?.remove();
    const script = document.createElement('script');
    script.id = 'vv-paypal-sdk';
    script.src = `https://www.paypal.com/sdk/js?${new URLSearchParams({'client-id': clientId, currency: 'USD', intent: 'capture', components: 'buttons', 'disable-funding': 'card,credit,paylater,venmo'})}`;
    script.dataset.namespace = 'vvPayPal';
    script.referrerPolicy = 'no-referrer';
    script.onload = () => window.vvPayPal ? resolve(window.vvPayPal) : reject(new Error('PayPal checkout could not load.'));
    script.onerror = () => reject(new Error('PayPal checkout could not load. Please retry.'));
    document.head.appendChild(script);
  }).catch(error => {sdkPromise = null; throw error;});
  return sdkPromise;
}

export function PaymentCheckout() {
  const [token, setToken] = useState('');
  const [payment, setPayment] = useState<Payment | null>(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [sdkAttempt, setSdkAttempt] = useState(0);
  const [sdkLoading, setSdkLoading] = useState(false);
  const buttonsHost = useRef<HTMLDivElement>(null);
  const requestKey = useRef('');
  const order = useRef<string | null>(null);
  const inFlight = useRef<Promise<string> | null>(null);
  useEffect(() => {
    const update = () => {
      const value = new URLSearchParams(window.location.hash.slice(1)).get('token') || '';
      setToken(value); setPayment(null); setError(''); requestKey.current = ''; order.current = null;
      if (!/^[A-Za-z0-9_-]{43}$/.test(value)) setError('This payment link is invalid or expired. Please contact Volcan Vacations for a new link.');
    };
    update(); window.addEventListener('hashchange', update);
    return () => window.removeEventListener('hashchange', update);
  }, []);
  const call = useCallback(async (path: string, method = 'GET', body?: unknown): Promise<Payment> => {
    const response = await fetch(requireApiUrl() + path, {method, cache: 'no-store', credentials: apiCredentials,
      referrerPolicy: 'no-referrer', signal: AbortSignal.timeout(45000),
      headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`}, ...(body ? {body: JSON.stringify(body)} : {})});
    if (!response.ok) {
      const data = await response.json().catch(() => null);
      throw new Error(typeof data?.detail === 'string' ? data.detail : 'Payment could not be completed. Refresh payment status before retrying.');
    }
    return response.json();
  }, [token]);
  useEffect(() => {
    if (!/^[A-Za-z0-9_-]{43}$/.test(token)) return;
    let active = true;
    call('/public/payments/session').then(data => {if (active) {setPayment(data); order.current = data.order_id;}}).catch(error => {if (active) setError(error.message);});
    return () => {active = false;};
  }, [token, call]);
  const clientId = payment?.client_id;
  const available = payment?.checkout_available;
  useEffect(() => {
    if (!available || !clientId || !buttonsHost.current) return;
    let active = true;
    let buttons: PayPalButtons | undefined;
    setSdkLoading(true);
    loadSDK(clientId).then(async sdk => {
      if (!active || !buttonsHost.current) return;
      buttons = sdk.Buttons({style: {layout: 'vertical', color: 'gold', label: 'paypal'},
        createOrder: () => {
          if (inFlight.current) return inFlight.current;
          if (!requestKey.current) requestKey.current = crypto.randomUUID();
          setError('');
          inFlight.current = call('/public/payments/paypal/order', 'POST', {idempotency_key: requestKey.current}).then(data => {
            setPayment(data); order.current = data.order_id;
            if (!data.order_id || !data.checkout_available) throw new Error(data.message);
            return data.order_id;
          }).catch(error => {setError(error.message); throw error;}).finally(() => {inFlight.current = null;});
          return inFlight.current;
        },
        onApprove: async ({orderID}) => {
          setBusy(true); setError('');
          try {setPayment(await call(`/public/payments/paypal/${encodeURIComponent(orderID)}/capture`, 'POST'));}
          catch (error) {setError(error instanceof Error ? error.message : 'Payment response was lost. Refresh payment status before retrying.');}
          finally {setBusy(false);}
        },
        onCancel: async data => {
          const orderId = data.orderID || order.current;
          if (!orderId) return;
          try {setPayment(await call(`/public/payments/paypal/${encodeURIComponent(orderId)}/cancel`, 'POST'));}
          catch {setError('Payment was not completed. Refresh payment status before trying again.');}
        },
        onError: () => setError('PayPal checkout could not complete. Refresh payment status before retrying.'),
      });
      await buttons.render(buttonsHost.current);
      if (active) setSdkLoading(false);
    }).catch(error => {if (active) {setError(error.message); setSdkLoading(false);}});
    return () => {active = false; void buttons?.close().catch(() => {});};
  }, [available, clientId, call, sdkAttempt]);
  async function refresh() {
    setBusy(true); setError('');
    try {setPayment(await call('/public/payments/reconcile', 'POST')); setSdkAttempt(value => value + 1);}
    catch (error) {setError(error instanceof Error ? error.message : 'Unable to refresh payment status.');}
    finally {setBusy(false);}
  }
  const received = payment && ['captured', 'refunded', 'partially_refunded'].includes(payment.status);
  return <section className="vv-payment" aria-label="Tour payment"><p className="eyebrow">Your Costa Rica experience</p><h1>{payment?.status === 'captured' ? 'Payment Received' : received ? 'Payment Update' : 'Your Tour Payment'}</h1>
    {!payment && !error && <p role="status">Loading your confirmed tour…</p>}
    {payment && <><p role="status">{payment.message}</p><dl><dt>Booking reference</dt><dd>{payment.booking_reference}</dd><dt>Tour</dt><dd>{payment.tour}</dd><dt>Date</dt><dd>{payment.date}</dd><dt>Party size</dt><dd>{payment.party_size}</dd><dt>Provider</dt><dd>PayPal</dd><dt className="vv-payment-total">{received ? 'Amount paid' : 'Total due'}</dt><dd className="vv-payment-total">${received ? payment.amount_paid : payment.amount_due} {payment.currency}</dd></dl>
      <div className="vv-payment-notice"><strong>PayPal Sandbox</strong><p>Development checkout uses test funds only.</p></div>
      {!received && payment.eligible && !payment.client_id && !payment.checkout_available && <p>Online checkout is currently unavailable. Please contact Volcan Vacations for help.</p>}
      {sdkLoading && <p role="status">Loading PayPal checkout…</p>}
      <div className="vv-paypal-buttons" ref={buttonsHost} hidden={!payment.checkout_available} />
      <div className="vv-payment-actions"><button type="button" className="button button--secondary" onClick={refresh} disabled={busy}>{busy ? 'Checking payment…' : 'Refresh payment status'}</button><Link className="button button--text" href="/contact">Contact VV</Link></div>
    </>}
    {error && !received && <p role="alert">{error}</p>}
    {!payment && error && <Link className="button button--secondary" href="/contact">Contact Volcan Vacations</Link>}
  </section>;
}
