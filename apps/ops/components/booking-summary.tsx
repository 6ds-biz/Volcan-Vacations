'use client';
import {LoadState, useInventory} from './inventory-ui';
export function BookingSummary() {
  const {data, error, retry} = useInventory<Record<string, number>>('/ops/booking-summary');
  return <section aria-label="Booking counts"><h2>Booking overview</h2>{!data ? <LoadState error={error} retry={retry} /> : <dl className="ops-metrics">{[['new_requests', 'New Requests'], ['awaiting_supplier', 'Awaiting Supplier'], ['confirmed_today', 'Confirmed Today (UTC)'], ['needs_attention', 'Needs Attention']].map(([key, label]) => <div key={key}><dt>{label}</dt><dd>{data[key]}</dd></div>)}</dl>}</section>;
}
