import type { Metadata } from 'next';
import { CTASection } from '../components/cta-section';
import { CompassIcon, HeartIcon, LeafIcon, SparkIcon } from '../components/icons';
import { TourInventory } from '../components/tour-inventory';
import { Container, Eyebrow, LinkButton, SectionHeading } from '../components/ui';
import { ScenicImage } from '../components/scenic-image';

export const metadata: Metadata = {
  title: 'Costa Rica Experiences, Thoughtfully Planned',
  description: 'Explore curated tours and get personal trip-planning help for La Fortuna, Arenal, and Costa Rica.',
};

const benefits = [
  { icon: LeafIcon, title: 'Local connections', text: 'Real relationships. Better experiences.' },
  { icon: SparkIcon, title: 'Carefully selected tours', text: 'Quality over quantity.' },
  { icon: CompassIcon, title: 'Simple trip planning', text: 'Less stress. More adventure.' },
  { icon: HeartIcon, title: 'Personal support', text: 'We’re here to help.' },
];

export default function Home() {
  return (
    <main id="main-content" className="home-page">
      <section className="home-hero">
        <ScenicImage priority />
        <Container className="home-hero__grid">
          <div className="home-hero__copy">
            <Eyebrow>Costa Rica</Eyebrow>
            <h1>Adventure<br />Awaits <em>Your Way</em></h1>
            <p className="hero-categories">Tours • Nature • Relaxation • Authentic experiences</p>
            <p>Discover remarkable tours, trusted local experiences, and a simpler way to shape your time around Arenal.</p>
            <div className="button-row"><LinkButton href="/tours" arrow>Explore Tours</LinkButton><LinkButton href="/plan-your-trip" variant="secondary">Plan My Trip</LinkButton></div>
            <div className="hero-note"><span aria-hidden="true">✦</span> Thoughtful planning for every pace of travel</div>
          </div>
          <div className="pura-vida"><span className="script-accent">Pura Vida</span><p>More than a trip<br />A different<br />perspective</p></div>
        </Container>
      </section>

      <section className="section section--cream"><Container><div className="heading-with-action"><SectionHeading eyebrow="Find your experience" title="A little wild. A lot unforgettable." intro="From river rapids to quiet thermal waters, discover different sides of La Fortuna and Arenal." /><LinkButton href="/tours" variant="text" arrow>View all tours</LinkButton></div><TourInventory featured /><p className="pricing-note">Development preview: seeded experiences, imagery, and prices are demo content, not current supplier offers. Confirm details before booking.</p></Container></section>

      <section className="section benefits-section"><Container><SectionHeading eyebrow="Travel well" title="A more considered way to explore" intro="Clear choices, local perspective, and room for your own travel style." align="center" /><div className="benefit-grid">{benefits.map(({ icon: Icon, title, text }) => <article className="benefit-card" key={title}><div className="benefit-card__icon"><Icon /></div><h3>{title}</h3><p>{text}</p></article>)}</div></Container></section>
      <section className="intro-section section"><Container className="intro-grid"><Eyebrow>Why Volcan Vacations</Eyebrow><h2>Local knowledge. Carefully chosen experiences. One simple place to plan.</h2><p>We help travelers organize memorable Costa Rica experiences without the work of coordinating every provider separately. Start with Arenal, then build a trip that moves at your pace.</p></Container></section>
      <CTASection />
    </main>
  );
}
