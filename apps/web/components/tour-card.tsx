import Link from 'next/link';
import type { Tour } from '../lib/inventory';
import { ArrowIcon, ClockIcon, LeafIcon, CompassIcon } from './icons';
import { TourPhoto } from './tour-photo';

export function TourCard({ tour, compact = false }: { tour: Tour; compact?: boolean }) {
  const CategoryIcon = tour.category === 'Adventure' ? CompassIcon : LeafIcon;
  if (compact) return <article className="tour-card tour-card--compact">
    <div className="tour-card__visual"><TourPhoto image={tour.primary_image} /></div>
    <div className="tour-card__body">
      <h3>{tour.name}</h3>
      <div className="featured-tour-meta"><span><ClockIcon width={16} height={16} />{tour.duration}</span><span><CategoryIcon width={16} height={16} />{tour.difficulty || tour.category}</span></div>
      <p className="tour-card__description">{tour.short_description}</p>
      <div className="featured-tour-action"><span className="featured-tour-price">${tour.retail_price.replace(/\.00$/, '')}<small> USD</small></span><Link className="tour-request-link" href={`/request?tour=${encodeURIComponent(tour.slug)}`} aria-label={`Request This Tour: ${tour.name}`}>Request tour <ArrowIcon width={15} height={15} /></Link></div>
    </div>
  </article>;
  return (
    <article className="tour-card">
      <div className="tour-card__visual"><TourPhoto image={tour.primary_image} /></div>
      <div className="tour-card__body">
        <div className="tour-card__heading">
          <h3>{tour.name}</h3>
          <Link className="tour-card__link" href={`/request?tour=${encodeURIComponent(tour.slug)}`} aria-label={`Request This Tour: ${tour.name}`}><ArrowIcon width={19} height={19} /></Link>
        </div>
        <p className="tour-card__category"><CategoryIcon width={19} height={19} />{tour.category}</p>
        <p className="tour-card__description">{tour.short_description}</p>
        <div className="tour-card__meta"><span><ClockIcon width={18} height={18} />{tour.duration}</span><span><small>From</small> ${tour.retail_price.replace(/\.00$/, '')} <small>USD</small></span></div>
        <Link className="tour-request-link" href={`/request?tour=${encodeURIComponent(tour.slug)}`}>Request This Tour</Link>
      </div>
    </article>
  );
}
export function TourGrid({ items, compact = false }: { items: Tour[]; compact?: boolean }) { return <div className="tour-grid">{items.map((tour) => <TourCard key={tour.slug} tour={tour} compact={compact} />)}</div>; }
