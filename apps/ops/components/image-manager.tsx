'use client';
import { useEffect, useState, type FormEvent } from 'react';
import { apiRequest } from '../lib/api';
import type { ProductImage } from '../lib/inventory';
import { Thumbnail } from './inventory-ui';

function imagePayload(form: FormData) {
  return {image_url: String(form.get('image_url')), alt_text: String(form.get('alt_text')), sort_order: Number(form.get('sort_order')), is_primary: form.has('is_primary')};
}
function ImageFields({image}: {image?: ProductImage}) {
  return <><label>Image URL<input name="image_url" required maxLength={2048} placeholder="https://… or /images/rafting.webp" defaultValue={image?.image_url} /></label><label>Alt text<input name="alt_text" required maxLength={300} defaultValue={image?.alt_text} /></label><label>Sort order<input name="sort_order" type="number" required min="0" max="2147483647" step="1" defaultValue={image?.sort_order ?? 0} /></label><label className="ops-check"><input name="is_primary" type="checkbox" defaultChecked={image?.is_primary ?? false} />Primary image</label></>;
}
export function ImageManager({tourId}: {tourId: string}) {
  const [images, setImages] = useState<ProductImage[]>([]);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [version, setVersion] = useState(0);
  const base = `/ops/tours/${tourId}/images`;
  useEffect(() => {
    let active = true;
    apiRequest<ProductImage[]>(base).then(data => { if (active) { setImages(data); setLoaded(true); } }).catch(error => { if (active) setError(error.message); });
    return () => { active = false; };
  }, [base, version]);
  async function save(event: FormEvent<HTMLFormElement>, image?: ProductImage) {
    event.preventDefault();
    const form = event.currentTarget;
    const success = await mutate(image ? `/${image.id}` : '', image ? 'PUT' : 'POST', imagePayload(new FormData(form)));
    if (!image && success) form.reset();
  }
  async function mutate(suffix: string, method: string, payload?: ReturnType<typeof imagePayload>) {
    setBusy(true); setError(''); setMessage('');
    try {
      await apiRequest(`${base}${suffix}`, {method, body: payload ? JSON.stringify(payload) : undefined});
      const updated = await apiRequest<ProductImage[]>(base);
      setImages(updated); setVersion(value => value + 1); setMessage('Gallery saved.');
      return true;
    } catch (error) { setError(error instanceof Error ? error.message : 'Unable to update gallery'); return false; }
    finally { setBusy(false); }
  }
  return <section className="ops-gallery"><h2>Images</h2><p>Use a hosted HTTP(S) image URL or an existing public-site /images/ asset. No files are uploaded here. Lower sort numbers appear first; ties use image ID. Selecting a primary replaces the previous selection.</p><p>Removing a primary promotes the first remaining image. To switch primary, select another image; a nonempty gallery always retains one.</p>
    {error && <p role="alert">{error} <button onClick={() => { setError(''); setVersion(value => value + 1); }}>Reload gallery</button></p>}{message && <p role="status">{message}</p>}
    {!loaded && !error && <p role="status">Loading gallery…</p>}{loaded && images.length === 0 && <p>No images yet.</p>}
    <div className="ops-image-grid">{images.map(image => <form key={`${image.id}-${version}`} className="ops-image-editor" aria-label={`Edit image ${image.id}`} onSubmit={event => save(event, image)}><fieldset disabled={busy}><legend>Image {image.id}{image.is_primary ? ' · Primary' : ''}</legend><Thumbnail image={image} /><ImageFields image={image} /><div className="ops-actions"><button type="submit">Save image</button><button type="button" className="ops-danger" onClick={() => { if (window.confirm('Remove this image reference? The source file will not be deleted.')) void mutate(`/${image.id}`, 'DELETE'); }}>Remove image</button></div></fieldset></form>)}</div>
    <form className="ops-editor" aria-label="Add image" onSubmit={event => save(event)}><fieldset disabled={busy || !loaded}><legend>Add image</legend><ImageFields /><button type="submit">Add image</button></fieldset></form>
  </section>;
}
