'use client';

import { useEffect, useState } from 'react';
import { apiCredentials, requireApiUrl } from '../lib/api';
import type { Tour } from '../lib/inventory';
import { TourGrid } from './tour-card';

export function TourInventory({ featured = false, filters = false, limit }: { featured?: boolean; filters?: boolean; limit?: number }) {
  const [tours, setTours] = useState<Tour[]>([]);
  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading');
  const [category, setCategory] = useState('');
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    let active = true;
    const timeout = setTimeout(() => controller.abort(), 10000);
    setStatus('loading');
    async function load() {
      try {
        const response = await fetch(`${requireApiUrl()}/public/tours${featured ? '?featured=true' : ''}`, {cache: 'no-store', credentials: apiCredentials, signal: controller.signal});
        if (!response.ok) throw new Error('Inventory unavailable');
        const data: Tour[] = await response.json();
        if (!Array.isArray(data)) throw new Error('Invalid inventory');
        if (active) { setTours(data); setStatus('ready'); }
      } catch {
        if (active) setStatus('error');
      } finally { clearTimeout(timeout); }
    }
    void load();
    return () => { active = false; clearTimeout(timeout); controller.abort(); };
  }, [featured, attempt]);
  if (status === 'loading') return <p role="status">Loading experiences…</p>;
  if (status === 'error') return <div role="status"><p>Experiences are temporarily unavailable. Please try again or contact us for help planning your trip.</p><button className="button button--secondary" onClick={() => setAttempt(value => value + 1)}>Try again</button></div>;
  const categories = [...new Set(tours.map(tour => tour.category))].sort();
  const visible = tours.filter(tour => !category || tour.category === category);
  return <>
    {filters && <div className="category-filter" aria-label="Tour categories"><span className="category-filter__label">Browse by</span>{['', ...categories].map(value => <button key={value} className={`filter-pill${category === value ? ' filter-pill--active' : ''}`} aria-pressed={category === value} onClick={() => setCategory(value)}>{value || 'All experiences'}</button>)}</div>}
    {visible.length ? <TourGrid items={visible.slice(0, limit ?? (featured ? 6 : visible.length))} compact={featured} /> : <p role="status">{featured ? 'Featured experiences are being prepared. Browse all tours or ask us to help plan your trip.' : 'No experiences are currently published for this selection. Please check back soon.'}</p>}
  </>;
}
