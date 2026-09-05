import type { Metadata } from 'next';
import { CTASection } from '../../components/cta-section';
import { TourInventory } from '../../components/tour-inventory';
import { Container, PageHero } from '../../components/ui';

export const metadata: Metadata = { title: 'Tours & Experiences', description: 'Browse adventure, nature, relaxation, culture, and family experiences around La Fortuna and Arenal.' };

export default function ToursPage() {
  return <main id="main-content"><PageHero eyebrow="Explore Arenal" title="Experiences worth traveling for." intro="Find a thoughtful mix of adventure, nature, culture, and time to slow down—all in the remarkable landscape around La Fortuna." /><section className="section section--cream tours-catalog"><Container><TourInventory filters /><p className="pricing-note">Development preview: seeded experiences, imagery, and prices are demo content, not current supplier offers. Confirm details before booking.</p></Container></section><CTASection /></main>;
}
