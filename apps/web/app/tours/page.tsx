import type { Metadata } from 'next';
import { CTASection } from '../../components/cta-section';
import { TourGrid } from '../../components/tour-card';
import { Container, PageHero } from '../../components/ui';
import { tourCategories, tours } from '../../data/tours';

export const metadata: Metadata = { title: 'Tours & Experiences', description: 'Browse adventure, nature, relaxation, culture, and family experiences around La Fortuna and Arenal.' };

export default function ToursPage() {
  return <main id="main-content"><PageHero eyebrow="Explore Arenal" title="Experiences worth traveling for." intro="Find a thoughtful mix of adventure, nature, culture, and time to slow down—all in the remarkable landscape around La Fortuna." /><section className="section section--cream tours-catalog"><Container><div className="category-filter" aria-label="Tour categories"><span className="category-filter__label">Browse by</span><span className="filter-pill filter-pill--active">All experiences</span>{tourCategories.map((category) => <span className="filter-pill" key={category}>{category}</span>)}</div><TourGrid items={tours} /><p className="pricing-note">Categories are a preview of the future browsing experience. Tour details and prices shown are placeholders until live inventory is connected.</p></Container></section><CTASection /></main>;
}
