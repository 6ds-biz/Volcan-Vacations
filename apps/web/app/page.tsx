import type { Metadata } from 'next';
import { CTASection } from '../components/cta-section';
import { CompassIcon, HeartIcon, LeafIcon, SparkIcon } from '../components/icons';
import { TourGrid } from '../components/tour-card';
import { Container, Eyebrow, LinkButton, SectionHeading } from '../components/ui';
import { tours } from '../data/tours';

export const metadata: Metadata = {
  title: 'Costa Rica Experiences, Thoughtfully Planned',
  description: 'Explore curated tours and get personal trip-planning help for La Fortuna, Arenal, and Costa Rica.',
};

const benefits = [
  { icon: LeafIcon, title: 'Local connections', text: 'A grounded perspective on La Fortuna, Arenal, and the experiences that make this region special.' },
  { icon: SparkIcon, title: 'Carefully selected', text: 'A focused collection designed to make choosing quality experiences feel less overwhelming.' },
  { icon: CompassIcon, title: 'Simpler planning', text: 'Bring your ideas together in one place instead of coordinating every detail on your own.' },
  { icon: HeartIcon, title: 'Personal support', text: 'Helpful, human guidance for couples, families, friends, and solo travelers.' },
];

export default function Home() {
  return (
    <main id="main-content">
      <section className="home-hero">
        <Container className="home-hero__grid">
          <div className="home-hero__copy">
            <Eyebrow>La Fortuna · Arenal · Costa Rica</Eyebrow>
            <h1>Experience Costa Rica <em>your way.</em></h1>
            <p>Discover remarkable tours, trusted local experiences, and a simpler way to shape your time around Arenal.</p>
            <div className="button-row"><LinkButton href="/tours" arrow>Explore Tours</LinkButton><LinkButton href="/plan-your-trip" variant="secondary">Plan My Trip</LinkButton></div>
            <div className="hero-note"><span aria-hidden="true">✦</span> Thoughtful planning for every pace of travel</div>
          </div>
          <div className="hero-art" role="img" aria-label="Layered rainforest and Arenal Volcano landscape illustration">
            <div className="hero-art__sun" /><div className="hero-art__cloud hero-art__cloud--one" /><div className="hero-art__cloud hero-art__cloud--two" /><div className="hero-art__volcano" /><div className="hero-art__ridge" /><div className="hero-art__forest" />
            <div className="hero-art__caption"><span>01</span><p><strong>Arenal, Costa Rica</strong>Where rainforest meets adventure</p></div>
          </div>
        </Container>
        <div className="hero-curve" />
      </section>

      <section className="intro-section section"><Container className="intro-grid"><Eyebrow>Why Volcan Vacations</Eyebrow><h2>Local knowledge. Carefully chosen experiences. One simple place to plan.</h2><p>We help travelers organize memorable Costa Rica experiences without the work of coordinating every provider separately. Start with Arenal, then build a trip that moves at your pace.</p></Container></section>

      <section className="section section--cream"><Container><div className="heading-with-action"><SectionHeading eyebrow="Find your experience" title="A little wild. A lot unforgettable." intro="From river rapids to quiet thermal waters, discover different sides of La Fortuna and Arenal." /><LinkButton href="/tours" variant="text" arrow>View all tours</LinkButton></div><TourGrid items={tours} /><p className="pricing-note">Tour details and “from” prices are planning estimates for this website preview and will be confirmed before booking.</p></Container></section>

      <section className="section benefits-section"><Container><SectionHeading eyebrow="Travel well" title="A more considered way to explore" intro="Clear choices, local perspective, and room for your own travel style." align="center" /><div className="benefit-grid">{benefits.map(({ icon: Icon, title, text }) => <article className="benefit-card" key={title}><div className="benefit-card__icon"><Icon /></div><h3>{title}</h3><p>{text}</p></article>)}</div></Container></section>
      <CTASection />
    </main>
  );
}
