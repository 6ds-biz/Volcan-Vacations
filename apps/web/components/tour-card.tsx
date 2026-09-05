import Link from 'next/link';
import type { Tour } from '../data/tours';
import { ArrowIcon, ClockIcon, LeafIcon, CompassIcon } from './icons';
import { ScenicImage, tourImages } from './scenic-image';

export function TourCard({ tour }: { tour: Tour }) {
  const photo = tourImages[tour.visual];
  const CategoryIcon = tour.category === 'Adventure' ? CompassIcon : LeafIcon;
  return (
    <article className="tour-card">
      <div className="tour-card__visual"><ScenicImage {...photo} sizes="(max-width: 600px) 100vw, (max-width: 1000px) 50vw, 33vw" /></div>
      <div className="tour-card__body">
        <div className="tour-card__heading">
          <h3>{tour.title}</h3>
          <Link className="tour-card__link" href={`/contact?experience=${tour.slug}`} aria-label={`Ask about ${tour.title}`}><ArrowIcon width={19} height={19} /></Link>
        </div>
        <p className="tour-card__category"><CategoryIcon width={19} height={19} />{tour.category}</p>
        <p className="tour-card__description">{tour.description}</p>
        <div className="tour-card__meta"><span><ClockIcon width={18} height={18} />{tour.duration}</span><span><small>From</small> ${tour.priceFrom} <small>USD</small></span></div>
      </div>
    </article>
  );
}
export function TourGrid({ items }: { items: Tour[] }) { return <div className="tour-grid">{items.map((tour) => <TourCard key={tour.slug} tour={tour} />)}</div>; }
