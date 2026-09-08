import Link from 'next/link';
import { ArrowIcon, CalendarIcon, CompassIcon, CupIcon, HeartIcon, LeafIcon, MountainIcon, PalmIcon, RequestIcon, SparkIcon } from '../../icons';
import { TourInventory } from '../../tour-inventory';
import { Container, Eyebrow, LinkButton } from '../../ui';
import { ScenicImage } from '../../scenic-image';
import { coastalDestinations, pacificChapterMedia } from '../../../lib/home-media';
import {editorial,type Editorial} from "../editorial";
const benefits = [
  { icon: LeafIcon, title: 'Local connections', text: 'Authentic experiences with trusted local guides.' },
  { icon: MountainIcon, title: 'Carefully selected experiences', text: 'Handpicked for quality, safety, and memorable experiences.' },
  { icon: CompassIcon, title: 'Simple trip planning', text: 'Easy planning and personalized support.' },
  { icon: HeartIcon, title: 'Personal support', text: 'We’re here before, during, and after your trip.' },
];
const categories = [
  { title: 'Adventure', text: 'From river rapids to ocean waves', image: 'rafting', icon: MountainIcon },
  { title: 'Nature & Wildlife', text: 'Discover the extraordinary', image: 'rainforest', icon: LeafIcon },
  { title: 'Relaxation', text: 'Hot springs to barefoot beach days', image: 'springs', icon: SparkIcon },
  { title: 'Culture', text: 'Coffee, chocolate & local life', image: 'coffee', icon: CupIcon },
];
const steps = [
  { title: 'Explore', text: 'Browse tours and tell us what you love.', icon: CompassIcon },
  { title: 'Request', text: 'Submit a request for your preferred dates.', icon: RequestIcon },
  { title: 'We Confirm', text: 'We check availability with our local partners.', icon: CalendarIcon },
  { title: 'Enjoy', text: 'Receive confirmation and get ready for Costa Rica.', icon: PalmIcon },
];
export function HomeHero(config:Editorial={}){return editorial((<section className="home-hero" aria-labelledby="hero-title">
        <ScenicImage priority alt="Arenal Volcano rising above the rainforest at sunset." />
        <Container className="home-hero__grid">
          <div className="home-hero__copy">
            <Eyebrow>Costa Rica</Eyebrow>
            <h1 id="hero-title">Adventure<br />Awaits <em>Your Way</em></h1>
            <p className="hero-categories">Tours • Nature • Relaxation • Authentic experiences</p>
            <p>Discover remarkable experiences, trusted local connections, and a simpler way to explore Costa Rica.</p>
            <div className="button-row"><LinkButton href="/tours" arrow>Explore Tours</LinkButton><LinkButton href="/plan-your-trip" variant="secondary">Plan My Trip</LinkButton></div>
            <div className="hero-note"><LeafIcon width={17} height={17} />Thoughtful planning for every pace of travel</div>
          </div>
          <div className="pura-vida"><span className="script-accent">Pura Vida</span><p>More than a trip<br />A different<br />perspective</p></div>
        </Container>
      </section>),config);}
export function ArenalFeature(config:Editorial={}){return editorial((<section className="home-journey" aria-labelledby="arenal-title">
        <div className="home-journey__scenery"><picture><source media="(max-width: 600px)" srcSet="/images/toucan-waterfall-mobile-v2.webp" /><ScenicImage src="/images/toucan-waterfall.webp" alt="A toucan above lush rainforest and a waterfall tumbling into a turquoise pool." /></picture></div>
        <Container className="home-journey__content">
          <div className="home-planning">
            <div className="home-planning__copy">
              <Eyebrow>Into the rainforest</Eyebrow>
              <h2 id="arenal-title">Arenal &amp;<br />La Fortuna</h2>
              <p>Volcano trails, wildlife encounters, and a little wonder around every bend.</p>
              <LinkButton href="/tours" arrow>Explore Tours</LinkButton>
            </div>
            <p className="script-accent journey-script">Good People<br />Wilder Places</p>
          </div>
          <section className="home-destination" aria-labelledby="destination-title">
            <Eyebrow>A little closer to nature</Eyebrow>
            <h3 id="destination-title">Wild by nature</h3>
            <p>Lush rainforests, stunning waterfalls, natural hot springs, and the iconic Arenal Volcano — a destination where nature, adventure, and relaxation come together.</p>
            <LinkButton href="/about" variant="secondary" arrow>Learn More</LinkButton>
          </section>
        </Container>
      </section>),config);}
export function FeaturedExperiences(config:Editorial={}){return editorial((<section className="home-featured home-ivory" aria-labelledby="featured-title">
        <Container>
          <div className="home-section-heading"><div><Eyebrow>Featured experiences</Eyebrow><h2 id="featured-title">A little wild. A lot unforgettable.</h2></div><LinkButton href="/tours" variant="text" arrow>View all tours</LinkButton></div>
          <TourInventory featured limit={config.limit} />
          <p className="pricing-note">Development preview: seeded experiences, imagery, and prices are demo content, not current supplier offers. Confirm details before booking.</p>
        </Container>
      </section>),config);}
export function HomeBenefits(config:Editorial={}){return editorial((<section className="benefits-section home-ivory" aria-label="The Volcan Vacations difference">
        <Container><Eyebrow>Why Volcan Vacations</Eyebrow><div className="benefit-grid">{benefits.map(({ icon: Icon, title, text }) => <article className="benefit-card" key={title}><div className="benefit-card__icon"><Icon /></div><h3>{title}</h3><p>{text}</p></article>)}</div></Container>
      </section>),config);}
export function TripPlanning(config:Editorial={}){return editorial((<section className="home-trip-planning home-ivory" aria-labelledby="planning-title">
        <Container className="trip-planning-grid">
          <div><Eyebrow>Your Costa Rica, thoughtfully planned</Eyebrow><h2 id="planning-title">More possibilities.<br />One personal approach.</h2></div>
          <div><p>Follow your curiosity. Make room for adventure, slow mornings, and the places that stay with you. Start with what you love, and imagine a Costa Rica trip at your own pace.</p><LinkButton href="/plan-your-trip" arrow>Plan My Trip</LinkButton></div>
        </Container>
      </section>),config);}
export function PacificCoast(config:Editorial={}){return editorial((<section className="home-pacific" aria-labelledby="pacific-title">
        {/* Dedicated media layer: a future muted video can replace the image without moving copy or CTA. */}
        <div className="home-pacific__media"><ScenicImage {...pacificChapterMedia} /></div>
        <Container><div className="home-pacific__copy"><Eyebrow>Beyond the volcano</Eyebrow><h2 id="pacific-title"><span>Discover Costa Rica’s</span><br />Pacific Coast</h2><p>Warm Pacific water. Golden beaches. Unforgettable sunsets. From surf towns to quiet coastal escapes, discover a different rhythm of relaxation and adventure.</p><LinkButton href="#coastal-destinations" arrow>Explore the Coast</LinkButton></div></Container>
      </section>),config);}
export function CoastalDestinations(config:Editorial={}){return editorial((<section id="coastal-destinations" className="home-coastal-destinations home-ivory" aria-labelledby="coastal-title">
        <Container>
          <div className="home-section-heading"><div><Eyebrow>Find your coastal rhythm</Eyebrow><h2 id="coastal-title">Four places. So many ways to unwind.</h2><p>A little inspiration for the Pacific chapter of your journey.</p></div></div>
          <div className="coastal-destination-grid">{coastalDestinations.map(destination => <article className="coastal-destination-card" id={`coast-${destination.slug}`} key={destination.slug}>
            <div className="coastal-destination-card__image"><ScenicImage src={destination.image} alt={destination.alt} sizes="(max-width: 600px) 110vw, (max-width: 1000px) 55vw, 40vw" /></div>
            <div className="coastal-destination-card__copy"><h3>{destination.name}</h3><p>{destination.description}</p></div>
          </article>)}</div>
          <div className="coastal-next"><p>Where would you like your Costa Rica story to take you?</p><LinkButton href="/plan-your-trip" variant="text" arrow>Start imagining your trip</LinkButton></div>
          <p className="coastal-media-note">Coastal images are illustrative destination inspiration.</p>
        </Container>
      </section>),config);}
export function KindsOfAdventure(config:Editorial={}){return editorial((<section className="home-categories" aria-labelledby="categories-title">
        <Container>
          <div className="home-section-heading"><div><h2 id="categories-title">Find Your Kind of Adventure</h2><p>From adrenaline to relaxation, there’s a Costa Rica experience for everyone.</p></div><LinkButton href="/tours" variant="text" arrow>Explore all experiences</LinkButton></div>
          <div className="experience-grid">{categories.map(({ title, text, image, icon: Icon }) => <Link href="/tours" className="experience-card" key={title}><ScenicImage src={`/images/${image}.webp`} sizes="(max-width: 600px) 100vw, (max-width: 1100px) 50vw, 25vw" /><div className="experience-card__copy"><Icon /><div><h3>{title}</h3><p>{text}</p></div><ArrowIcon className="experience-card__arrow" /></div></Link>)}</div>
        </Container>
      </section>),config);}
export function HowItWorks(config:Editorial={}){return editorial((<section className="home-process" aria-labelledby="process-title">
        <Container>
          <div className="home-section-heading"><div><h2 id="process-title">How It Works</h2><p>A simple way to plan your Costa Rica adventure.</p></div></div>
          <ol className="process-grid">{steps.map(({ title, text, icon: Icon }, index) => <li key={title}><Icon className="process-icon" /><div><h3>{index + 1}. {title}</h3><p>{text}</p></div>{index < steps.length - 1 && <ArrowIcon className="process-arrow" />}</li>)}</ol>
        </Container>
      </section>),config);}
export function FinalCTA(config:Editorial={}){return editorial((<section className="home-final-cta" aria-labelledby="final-title">
        <ScenicImage />
        <Container><h2 id="final-title">Costa Rica Is Calling</h2><p>Let’s Plan Your Trip</p><LinkButton href="/plan-your-trip" arrow>Plan My Trip</LinkButton></Container>
      </section>),config);}