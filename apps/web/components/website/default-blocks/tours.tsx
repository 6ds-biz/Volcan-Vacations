import { CTASection } from '../../cta-section';
import { TourInventory } from '../../tour-inventory';
import { Container, PageHero } from '../../ui';
import {editorial,type Editorial} from "../editorial";

export function ToursHero(config:Editorial={}){return editorial((<PageHero eyebrow="Explore Arenal" title="Experiences worth traveling for." intro="Find a thoughtful mix of adventure, nature, culture, and time to slow down—all in the remarkable landscape around La Fortuna." />),config);}
export function ToursCatalog(config:Editorial={}){return editorial((<section className="section section--cream tours-catalog"><Container><TourInventory filters limit={config.limit} /><p className="pricing-note">Development preview: seeded experiences, imagery, and prices are demo content, not current supplier offers. Confirm details before booking.</p></Container></section>),config);}
export function ToursCTA(config:Editorial={}){return editorial((<CTASection />),config);}