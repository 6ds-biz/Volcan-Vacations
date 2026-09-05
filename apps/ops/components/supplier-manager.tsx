'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useState, type FormEvent } from 'react';
import { apiRequest } from '../lib/api';
import type { Supplier } from '../lib/inventory';
import { LoadState, useInventory } from './inventory-ui';

export function SupplierList() {
  const {data, error, retry} = useInventory<Supplier[]>('/ops/suppliers');
  return <><div className="ops-heading"><h1>Suppliers</h1><Link className="ops-button" href="/suppliers/new">New supplier</Link></div>
    {!data ? <LoadState error={error} retry={retry} /> : data.length === 0 ? <p>No suppliers yet. Create one to start adding tours.</p> :
      <div className="ops-table-wrap" tabIndex={0} role="region" aria-label="Supplier directory table"><table><caption>Internal supplier directory</caption><thead><tr><th>Name</th><th>Type</th><th>Contact</th><th>Status</th></tr></thead><tbody>{data.map(supplier => <tr key={supplier.id}><td><Link href={`/suppliers/${supplier.id}`}>{supplier.name}</Link></td><td>{supplier.supplier_type.replace(/_/g, ' ')}</td><td>{supplier.contact_name || '—'}<br />{supplier.email}<br />{supplier.phone}</td><td>{supplier.active ? 'Active' : 'Inactive'}</td></tr>)}</tbody></table></div>}</>;
}

export function SupplierEditor({id}: {id?: string}) {
  const router = useRouter();
  const [supplier, setSupplier] = useState<Supplier | null>(null);
  const [loading, setLoading] = useState(!!id);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [saved, setSaved] = useState(false);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    if (!id) return;
    let active = true;
    setLoading(true); setError('');
    apiRequest<Supplier>(`/ops/suppliers/${id}`).then(data => { if (active) setSupplier(data); }).catch(error => { if (active) setError(error.message); }).finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [id, attempt]);
  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const optional = (name: string) => String(form.get(name) || '').trim() || null;
    const payload = {name: form.get('name'), supplier_type: form.get('supplier_type'), contact_name: optional('contact_name'), email: optional('email'), phone: optional('phone'), website: optional('website'), notes: optional('notes'), active: form.has('active')};
    setBusy(true); setError(''); setSaved(false);
    try {
      const result = await apiRequest<Supplier>(`/ops/suppliers${id ? `/${id}` : ''}`, {method: id ? 'PUT' : 'POST', body: JSON.stringify(payload)});
      setSaved(true);
      if (!id) router.push(`/suppliers/${result.id}`);
    } catch (error) { setError(error instanceof Error ? error.message : 'Unable to save supplier'); }
    finally { setBusy(false); }
  }
  return <><Link href="/suppliers">← Suppliers</Link><h1>{id ? 'Edit supplier' : 'New supplier'}</h1>
    {loading || (id && !supplier) ? <LoadState error={error} retry={() => setAttempt(value => value + 1)} /> :
      <form className="ops-editor" onSubmit={save}>
        <fieldset disabled={busy}><legend>Supplier details · internal only</legend><div className="ops-fields">
          <label>Name<input name="name" required maxLength={200} defaultValue={supplier?.name} /></label>
          <label>Supplier type<select name="supplier_type" defaultValue={supplier?.supplier_type || 'tour_operator'}>{['tour_operator', 'transportation', 'hotel', 'other'].map(type => <option key={type} value={type}>{type.replace(/_/g, ' ')}</option>)}</select></label>
          <label>Contact name<input name="contact_name" maxLength={140} defaultValue={supplier?.contact_name || ''} /></label>
          <label>Email<input name="email" type="email" maxLength={180} defaultValue={supplier?.email || ''} /></label>
          <label>Phone<input name="phone" type="tel" maxLength={60} defaultValue={supplier?.phone || ''} /></label>
          <label>Website<input name="website" type="url" maxLength={2048} defaultValue={supplier?.website || ''} /></label>
        </div><label>Private notes<textarea name="notes" maxLength={10000} rows={4} defaultValue={supplier?.notes || ''} /></label>
        <label className="ops-check"><input name="active" type="checkbox" defaultChecked={supplier?.active ?? true} />Active</label>
        <button type="submit">{busy ? 'Saving…' : 'Save supplier'}</button></fieldset>
        {error && <p role="alert">{error}</p>}{saved && <p role="status">Supplier saved.</p>}
      </form>}</>;
}
