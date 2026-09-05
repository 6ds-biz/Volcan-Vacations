import Link from 'next/link';
import type { Tour } from '../data/tours';
import { ArrowIcon, ClockIcon } from './icons';

export function TourCard({ tour }: { tour: Tour }) {
  return <article className="tour-card"><div className={`tour-card__visual tour-card__visual--${tour.visual}`} aria-hidden="true"><span className="tour-card__land land--back" /><span className="tour-card__land land--front" /><span className="tour-card__sun" /></div><div className="tour-card__body"><p className="tour-card__category">{tour.category}</p><h3>{tour.title}</h3><p className="tour-card__description">{tour.description}</p><div className="tour-card__meta"><span><ClockIcon width={18} height={18} />{tour.duration}</span><span><small>From</small> ${tour.priceFrom} <small>USD</small></span></div><Link className="tour-card__link" href={`/contact?experience=${tour.slug}`} aria-label={`Ask about ${tour.title}`}>Ask about this tour <ArrowIcon width={18} height={18} /></Link></div></article>;
}
export function TourGrid({ items }: { items: Tour[] }) { return <div className="tour-grid">{items.map((tour) => <TourCard key={tour.slug} tour={tour} />)}</div>; }
