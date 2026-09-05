'use client';
import { useEffect, useState } from 'react';
import { apiRequest, imagePreviewUrl } from '../lib/api';
import type { ProductImage } from '../lib/inventory';

export function useInventory<T>(path: string) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState('');
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    let active = true;
    setError(''); setData(null);
    apiRequest<T>(path).then(result => { if (active) setData(result); }).catch(error => { if (active) setError(error.message || 'API unavailable'); });
    return () => { active = false; };
  }, [path, attempt]);
  return {data, error, retry: () => setAttempt(value => value + 1)};
}
export function LoadState({error, retry}: {error: string; retry: () => void}) {
  return error ? <div role="alert"><p>{error}</p><button onClick={retry}>Try again</button></div> : <p role="status">Loading inventory…</p>;
}
export function Thumbnail({image}: {image: ProductImage | null}) {
  const [failed, setFailed] = useState('');
  const src = image ? imagePreviewUrl(image.image_url) : undefined;
  if (!image || !src || failed === src) return <span className="ops-no-photo">No preview</span>;
  // Browser-direct URLs avoid server-side proxy fetching of untrusted addresses.
  // eslint-disable-next-line @next/next/no-img-element
  return <img className="ops-thumbnail" src={src} alt={image.alt_text} onError={() => setFailed(src)} referrerPolicy="no-referrer" />;
}
