import type { Metadata } from 'next';
import Link from 'next/link';
import { ArrowIcon, CalendarIcon, CompassIcon, CupIcon, HeartIcon, LeafIcon, MountainIcon, PalmIcon, RequestIcon, SparkIcon } from '../components/icons';
import { TourInventory } from '../components/tour-inventory';
import { Container, Eyebrow, LinkButton } from '../components/ui';
import { ScenicImage } from '../components/scenic-image';
import './home.css';

export const metadata: Metadata = {
  title: 'Costa Rica Experiences, Thoughtfully Planned',
  description: 'Explore curated tours and get personal trip-planning help for La Fortuna, Arenal, and Costa Rica.',
};

const benefits = [
  { icon: LeafIcon, title: 'Local connections', text: 'Authentic experiences with trusted local guides.' },
  { icon: MountainIcon, title: 'Carefully selected tours', text: 'Handpicked for quality, safety, and memorable experiences.' },
  { icon: CompassIcon, title: 'Simple trip planning', text: 'Easy planning and personalized support.' },
  { icon: HeartIcon, title: 'Personal support', text: 'We’re here before, during, and after your trip.' },
];

const categories = [
  { title: 'Adventure', text: 'Get your heart racing', image: 'rafting', icon: MountainIcon },
  { title: 'Nature & Wildlife', text: 'Discover the extraordinary', image: 'rainforest', icon: LeafIcon },
  { title: 'Relaxation', text: 'Slow down and recharge', image: 'springs', icon: SparkIcon },
  { title: 'Culture', text: 'Experience local life', image: 'coffee', icon: CupIcon },
];

const steps = [
  { title: 'Explore', text: 'Browse tours and tell us what you love.', icon: CompassIcon },
  { title: 'Request', text: 'Submit a request for your preferred dates.', icon: RequestIcon },
  { title: 'We Confirm', text: 'We check availability with our local partners.', icon: CalendarIcon },
  { title: 'Enjoy', text: 'Receive confirmation and get ready for Costa Rica.', icon: PalmIcon },
];

export default function Home() {
  return (
    <main id="main-content" className="home-page">
      <section className="home-hero" aria-labelledby="hero-title">
        <ScenicImage priority />
        <Container className="home-hero__grid">
          <div className="home-hero__copy">
            <Eyebrow>Costa Rica</Eyebrow>
            <h1 id="hero-title">Adventure<br />Awaits <em>Your Way</em></h1>
            <p className="hero-categories">Tours • Nature • Relaxation • Authentic experiences</p>
            <p>Discover remarkable tours, trusted local experiences, and a simpler way to shape your time around Arenal.</p>
            <div className="button-row"><LinkButton href="/tours" arrow>Explore Tours</LinkButton><LinkButton href="/plan-your-trip" variant="secondary">Plan My Trip</LinkButton></div>
            <div className="hero-note"><LeafIcon width={17} height={17} />Thoughtful planning for every pace of travel</div>
          </div>
          <div className="pura-vida"><span className="script-accent">Pura Vida</span><p>More than a trip<br />A different<br />perspective</p></div>
        </Container>
      </section>

      <section className="home-featured" aria-labelledby="featured-title">
        <Container>
          <div className="home-section-heading"><h2 id="featured-title">A little wild. A lot unforgettable.</h2><LinkButton href="/tours" variant="text" arrow>View all tours</LinkButton></div>
          <TourInventory featured />
          <p className="pricing-note">Development preview: seeded experiences, imagery, and prices are demo content, not current supplier offers. Confirm details before booking.</p>
        </Container>
      </section>

      <section className="benefits-section" aria-label="The Volcan Vacations difference">
        <Container><div className="benefit-grid">{benefits.map(({ icon: Icon, title, text }) => <article className="benefit-card" key={title}><div className="benefit-card__icon"><Icon /></div><h3>{title}</h3><p>{text}</p></article>)}</div></Container>
      </section>

      {/* One continuous image spans both stories; only its outer edges fade. */}
      <div className="home-journey">
        <div className="home-journey__scenery"><picture><source media="(max-width: 600px)" srcSet="/images/toucan-waterfall-mobile-v2.webp" /><ScenicImage src="/images/toucan-waterfall.webp" /></picture></div>
        <Container className="home-journey__content">
          <section className="home-planning" aria-labelledby="planning-title">
            <div className="home-planning__copy">
              <Eyebrow>Costa Rica is calling</Eyebrow>
              <h2 id="planning-title">Plan Your<br />Unforgettable Experience</h2>
              <p>Tell us what you love. We’ll help put it together.</p>
              <LinkButton href="/plan-your-trip" arrow>Plan My Trip</LinkButton>
            </div>
            <p className="script-accent journey-script">Good People<br />Wilder Places</p>
          </section>
          <section className="home-destination" aria-labelledby="destination-title">
            <Eyebrow>Explore</Eyebrow>
            <h2 id="destination-title">Arenal &amp; La Fortuna</h2>
            <p>Lush rainforests, stunning waterfalls, natural hot springs, and the iconic Arenal Volcano — a destination where nature, adventure, and relaxation come together.</p>
            <LinkButton href="/about" variant="secondary" arrow>Learn More</LinkButton>
          </section>
        </Container>
      </div>

      <section className="home-categories" aria-labelledby="categories-title">
        <Container>
          <div className="home-section-heading"><div><h2 id="categories-title">Find Your Kind of Adventure</h2><p>From adrenaline to relaxation, there’s a Costa Rica experience for everyone.</p></div><LinkButton href="/tours" variant="text" arrow>Explore all experiences</LinkButton></div>
          <div className="experience-grid">{categories.map(({ title, text, image, icon: Icon }) => <Link href="/tours" className="experience-card" key={title}><ScenicImage src={`/images/${image}.webp`} sizes="(max-width: 600px) 100vw, (max-width: 1100px) 50vw, 25vw" /><div className="experience-card__copy"><Icon /><div><h3>{title}</h3><p>{text}</p></div><ArrowIcon className="experience-card__arrow" /></div></Link>)}</div>
        </Container>
      </section>

      <section className="home-process" aria-labelledby="process-title">
        <Container>
          <div className="home-section-heading"><div><h2 id="process-title">How It Works</h2><p>A simple way to plan your Costa Rica adventure.</p></div></div>
          <ol className="process-grid">{steps.map(({ title, text, icon: Icon }, index) => <li key={title}><Icon className="process-icon" /><div><h3>{index + 1}. {title}</h3><p>{text}</p></div>{index < steps.length - 1 && <ArrowIcon className="process-arrow" />}</li>)}</ol>
        </Container>
      </section>

      <section className="home-final-cta" aria-labelledby="final-title">
        <ScenicImage />
        <Container><h2 id="final-title">Costa Rica Is Calling</h2><p>Let’s Plan Your Trip</p><LinkButton href="/plan-your-trip" arrow>Plan My Trip</LinkButton></Container>
      </section>
    </main>
  );
}
