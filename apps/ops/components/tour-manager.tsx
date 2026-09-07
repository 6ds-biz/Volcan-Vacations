'use client';
import Link from 'next/link';
import {PageHeader} from './ops-ui';
import {TourDestinations} from './foundation-editors';
import { useRouter } from 'next/navigation';
import { useEffect, useState, type FormEvent } from 'react';
import { apiRequest } from '../lib/api';
import { margin, type Supplier, type Tour } from '../lib/inventory';
import { LoadState, Thumbnail, useInventory } from './inventory-ui';
import { ImageManager } from './image-manager';

export function TourList() {
  const {data, error, retry} = useInventory<Tour[]>('/ops/tours');
  return <><div className="ops-heading"><h1>Tours</h1><Link className="ops-button" href="/tours/new">New tour</Link></div>
    {!data ? <LoadState error={error} retry={retry} /> : data.length === 0 ? <p>No tours yet. Create a supplier, then add your first tour.</p> :
      <div className="ops-table-wrap" tabIndex={0} role="region" aria-label="Tour inventory table"><table className="ops-tour-table"><caption>Tour inventory · USD · internal pricing</caption><thead><tr>{['Image', 'Name', 'Supplier', 'Category', 'Retail', 'Cost', 'Gross margin', 'Featured', 'Status'].map(label => <th key={label}>{label}</th>)}</tr></thead><tbody>{data.map(tour => <tr key={tour.id}><td><Thumbnail image={tour.primary_image} /></td><td><Link href={`/tours/${tour.id}`}>{tour.name}</Link></td><td>{tour.supplier.name}</td><td>{tour.category}</td><td>${tour.retail_price}</td><td>${tour.supplier_cost}</td><td>${tour.gross_margin}</td><td>{tour.featured ? 'Yes' : 'No'}</td><td>{tour.active ? 'Active' : 'Inactive'}</td></tr>)}</tbody></table></div>}</>;
}

export function TourEditor({id}: {id?: string}) {
  const router = useRouter();
  const [tour, setTour] = useState<Tour | null>(null);
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [saved, setSaved] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [retail, setRetail] = useState('0.00');
  const [cost, setCost] = useState('0.00');
  useEffect(() => {
    let active = true;
    setLoading(true); setError('');
    Promise.all([apiRequest<Supplier[]>('/ops/suppliers'), id ? apiRequest<Tour>(`/ops/tours/${id}`) : Promise.resolve(null)])
      .then(([suppliers, tour]) => { if (active) { setSuppliers(suppliers); setTour(tour); setRetail(tour?.retail_price || '0.00'); setCost(tour?.supplier_cost || '0.00'); } })
      .catch(error => { if (active) setError(error.message); }).finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [id, attempt]);
  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const optional = (key: string) => String(form.get(key) || '').trim() || null;
    const payload = {
      name: form.get('name'), slug: form.get('slug'), supplier_id: Number(form.get('supplier_id')),
      category: form.get('category'), location: optional('location'), duration: form.get('duration'),
      short_description: form.get('short_description'), description: optional('description'), difficulty: optional('difficulty'),
      minimum_age: optional('minimum_age') === null ? null : Number(form.get('minimum_age')),
      retail_price: retail, supplier_cost: cost, active: form.has('active'), featured: form.has('featured'), product_type: 'tour',
    };
    setBusy(true); setError(''); setSaved(false);
    try {
      const result = await apiRequest<Tour>(`/ops/tours${id ? `/${id}` : ''}`, {method: id ? 'PUT' : 'POST', body: JSON.stringify(payload)});
      setTour(result); setSaved(true);
      if (!id) router.push(`/tours/${result.id}`);
    } catch (error) { setError(error instanceof Error ? error.message : 'Unable to save tour'); }
    finally { setBusy(false); }
  }
  if (loading || (id && !tour) || (error && !suppliers.length)) return <><PageHeader title={id ? 'Edit tour' : 'New tour'} description="Maintain experience details, imagery and internal pricing" icon="tours"/><LoadState error={error} retry={() => setAttempt(value => value + 1)} /></>;
  return <><Link href="/tours">← Tours</Link><PageHeader title={id ? 'Edit tour' : 'New tour'} description="Maintain experience details, imagery and internal pricing" icon="tours"/>{id && <Link href={`/availability?product_id=${id}`}>Manage tour availability</Link>}
    {!suppliers.length && <p role="alert">A supplier is required. <Link href="/suppliers/new">Create a supplier</Link> first. {error}</p>}
    <form className="ops-editor" onSubmit={save}>
      <fieldset disabled={busy}><legend>Basics</legend><div className="ops-fields">
        <label>Name<input name="name" required maxLength={220} defaultValue={tour?.name} /></label>
        <label>Slug<input name="slug" required maxLength={240} pattern="[a-z0-9]+(-[a-z0-9]+)*" title="Lowercase letters and numbers separated by hyphens" defaultValue={tour?.slug} /><small>Unique URL identifier; e.g. arenal-rafting</small></label>
        <label>Supplier<select name="supplier_id" required defaultValue={tour?.supplier_id || ''}><option value="" disabled>Select a supplier</option>{suppliers.map(supplier => <option value={supplier.id} key={supplier.id}>{supplier.name}{supplier.active ? '' : ' (inactive)'}</option>)}</select></label>
        <label>Category<input name="category" required maxLength={80} list="categories" defaultValue={tour?.category} /><datalist id="categories">{['Adventure', 'Nature', 'Relaxation', 'Culture', 'Family'].map(value => <option key={value}>{value}</option>)}</datalist></label>
        <label>Location<input name="location" maxLength={220} defaultValue={tour?.location || ''} /></label>
        <label>Duration<input name="duration" required maxLength={120} defaultValue={tour?.duration} /></label>
      </div></fieldset>
      <fieldset disabled={busy}><legend>Customer content</legend>
        <label>Short description<textarea name="short_description" required maxLength={500} rows={2} defaultValue={tour?.short_description} /></label>
        <label>Description<textarea name="description" maxLength={30000} rows={6} defaultValue={tour?.description || ''} /></label>
        <div className="ops-fields"><label>Difficulty<input name="difficulty" maxLength={80} defaultValue={tour?.difficulty || ''} /></label><label>Minimum age<input name="minimum_age" type="number" min="0" max="120" step="1" defaultValue={tour?.minimum_age ?? ''} /></label></div>
      </fieldset>
      <fieldset disabled={busy}><legend>Pricing · USD</legend><div className="ops-fields">
        <label>Retail price<input name="retail_price" inputMode="decimal" required pattern="[0-9]+([.][0-9]{1,2})?" value={retail} onChange={event => setRetail(event.target.value)} /></label>
        <label>Supplier cost<input name="supplier_cost" inputMode="decimal" required pattern="[0-9]+([.][0-9]{1,2})?" value={cost} onChange={event => setCost(event.target.value)} /></label>
      </div><p>Gross margin: <output aria-label="Gross margin">${margin(retail, cost)}</output> USD</p><small>Retail minus supplier cost; excludes other expenses.</small></fieldset>
      <fieldset disabled={busy}><legend>Publishing</legend><label className="ops-check"><input name="active" type="checkbox" defaultChecked={tour?.active ?? false} />Active — visible publicly</label><label className="ops-check"><input name="featured" type="checkbox" defaultChecked={tour?.featured ?? false} />Featured — show on homepage when active</label><button type="submit" disabled={!suppliers.length}>{busy ? 'Saving…' : 'Save tour'}</button></fieldset>
      {error && <p role="alert">{error}</p>}{saved && <p role="status">Tour saved. Server gross margin: ${tour?.gross_margin} USD.</p>}
    </form>
    {id && <TourDestinations id={id}/>}
    {id ? <ImageManager tourId={id} /> : <p>Save this tour to manage its primary image and gallery.</p>}
  </>;
}
