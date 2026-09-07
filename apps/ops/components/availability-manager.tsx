'use client';
import Link from 'next/link';
import {PageHeader,Modules} from './ops-ui';
import {useEffect, useState, type FormEvent} from 'react';
import {apiRequest} from '../lib/api';
import {availabilityStatuses, localDateTime, timeLabel, type Availability} from '../lib/availability';
import {statusLabel} from '../lib/bookings';
import type {Tour, Supplier} from '../lib/inventory';
import {LoadState, useInventory} from './inventory-ui';

export function AvailabilityManager() {
  const [filters, setFilters] = useState({date_from: '', date_to: '', product_id: '', supplier_id: '', status: ''});
  const [editing, setEditing] = useState<Availability | 'new' | null>(null);
  const tours = useInventory<Tour[]>('/ops/tours');
  const suppliers = useInventory<Supplier[]>('/ops/suppliers');
  useEffect(() => { const id = new URLSearchParams(window.location.search).get('product_id'); if (id && /^\d+$/.test(id)) setFilters(current => ({...current, product_id: id})); }, []);
  const query = new URLSearchParams(Object.entries(filters).filter(([, value]) => value)).toString();
  const records = useInventory<Availability[]>(`/ops/availability?${query}`);
  const filter = (key: keyof typeof filters, value: string) => setFilters(current => ({...current, [key]: value}));
  return <><PageHeader title="Availability" description="Current supplier and tour availability" icon="bookings"><button onClick={() => setEditing('new')}>Add date</button></PageHeader>
    {records.data && <Modules items={[{label:"Recorded dates",value:records.data.length},{label:"Available",value:records.data.filter(r=>r.status==='available'&&!r.stale).length},{label:"Limited",value:records.data.filter(r=>r.status==='limited'&&!r.stale).length},{label:"Stale / unchecked",value:records.data.filter(r=>r.stale).length}]}/>}
    <p className="muted">Counts reflect current filters. Record information for one tour and date. Missing information means Unknown, never sold out. These checks do not reserve capacity or confirm customer bookings.</p>
    <div className="ops-filters"><label>From date<input type="date" value={filters.date_from} onChange={e => filter('date_from', e.target.value)} /></label><label>Through date<input type="date" min={filters.date_from} value={filters.date_to} onChange={e => filter('date_to', e.target.value)} /></label>
    <label>Filter by tour<select value={filters.product_id} onChange={e => filter('product_id', e.target.value)}><option value="">All tours</option>{tours.data?.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}</select></label>
    <label>Filter by supplier<select value={filters.supplier_id} onChange={e => filter('supplier_id', e.target.value)}><option value="">All suppliers</option>{suppliers.data?.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}</select></label>
    <label>Availability status<select value={filters.status} onChange={e => filter('status', e.target.value)}><option value="">All statuses</option>{availabilityStatuses.map(s => <option key={s} value={s}>{statusLabel(s)}</option>)}</select></label><button onClick={() => setFilters({date_from: '', date_to: '', product_id: '', supplier_id: '', status: ''})}>Clear filters</button></div>
    {(!tours.data || !suppliers.data) && <LoadState error={tours.error || suppliers.error} retry={() => {tours.retry(); suppliers.retry();}} />}
    {editing && tours.data && <AvailabilityEditor key={editing === 'new' ? 'new' : `${editing.id}-${editing.version}`} record={editing === 'new' ? null : editing} tours={tours.data} selectedTour={filters.product_id} done={() => {setEditing(null); records.retry();}} />}
    {!records.data ? <LoadState error={records.error} retry={records.retry} /> : !records.data.length ? <p role="status">No recorded dates match these filters. Availability is unknown for dates without a record.</p> : <div className="ops-table-wrap" tabIndex={0} role="region" aria-label="Tour date availability"><table className="ops-availability-table"><caption>Checked availability · information older than 24 hours may be stale</caption><thead><tr>{['Date', 'Tour / supplier', 'Status', 'Capacity / remaining', 'Source / checked', 'Action'].map(s => <th key={s}>{s}</th>)}</tr></thead><tbody>{records.data.map(row => <tr key={row.id}><td>{row.date}</td><td><Link href={`/tours/${row.product_id}`}>{row.tour_name}</Link><br />{row.supplier_name}</td><td><span className="ops-badge">{statusLabel(row.status)}</span>{row.stale && <p className="ops-attention">Availability may be stale</p>}</td><td>{row.capacity ?? 'Unknown'} / {row.remaining_capacity ?? 'Unknown'}</td><td>{statusLabel(row.source)}<br />{timeLabel(row.last_checked_at)}</td><td><button onClick={() => setEditing(row)} aria-label={`Edit ${row.tour_name} ${row.date}`}>Edit date</button></td></tr>)}</tbody></table></div>}
  </>;
}

function AvailabilityEditor({record, tours, selectedTour, done}: {record: Availability | null; tours: Tour[]; selectedTour: string; done: () => void}) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError('');
    const form = new FormData(event.currentTarget);
    const value = (key: string) => String(form.get(key) || '');
    const capacity = (key: string) => value(key) === '' ? null : Number(value(key));
    try {
      const payload = {product_id: record?.product_id ?? Number(value('product_id')), date: record?.date ?? value('date'), status: value('status'), source: value('source'), capacity: capacity('capacity'), remaining_capacity: capacity('remaining_capacity'), notes: value('notes') || null, last_checked_at: value('last_checked_at') ? new Date(value('last_checked_at')).toISOString() : null, ...(record ? {expected_version: record.version} : {})};
      await apiRequest(`/ops/availability${record ? `/${record.id}` : ''}`, {method: record ? 'PUT' : 'POST', body: JSON.stringify(payload)});
      done();
    } catch (error) {setError(error instanceof Error ? error.message : 'Unable to save availability');}
    finally {setBusy(false);}
  }
  return <form className="ops-editor" onSubmit={save}><fieldset disabled={busy}><legend>{record ? 'Edit date' : 'Add date'}</legend><div className="ops-fields">
    <label>Tour<select name="product_id" required disabled={!!record} defaultValue={record?.product_id ?? selectedTour}><option value="">Choose tour</option>{tours.map(t => <option key={t.id} value={t.id}>{t.name}{!t.active ? ' (inactive)' : ''}</option>)}</select></label>
    <label>Date<input name="date" type="date" required disabled={!!record} defaultValue={record?.date} /></label>
    <label>Status<select name="status" defaultValue={record?.status || 'unknown'}>{availabilityStatuses.map(s => <option key={s} value={s}>{statusLabel(s)}</option>)}</select></label>
    <label>Source<select name="source" defaultValue={record?.source || 'manual'}>{['manual', 'supplier', 'api', 'inventory'].map(s => <option key={s} value={s}>{statusLabel(s)}</option>)}</select><small>Source describes the information you are recording. No integration runs automatically.</small></label>
    <label>Capacity (optional)<input name="capacity" type="number" min="0" max="2147483647" step="1" defaultValue={record?.capacity ?? ''} /></label>
    <label>Remaining capacity (optional)<input name="remaining_capacity" type="number" min="0" max="2147483647" step="1" defaultValue={record?.remaining_capacity ?? ''} /></label>
    <label>Last checked (your local time)<input name="last_checked_at" type="datetime-local" defaultValue={record?.last_checked_at ? localDateTime(record.last_checked_at) : record ? '' : localDateTime()} /><small>Required for known availability. Leave capacities blank when the supplier does not provide them.</small></label></div>
    <label>Internal availability notes<textarea name="notes" rows={3} maxLength={10000} defaultValue={record?.notes ?? ''} /></label><div className="ops-actions"><button type="submit">{busy ? 'Saving…' : 'Save availability'}</button><button type="button" onClick={done}>Close editor / reload</button></div></fieldset>{error && <p role="alert">{error} Close and reopen the editor to load the latest version.</p>}</form>;
}
