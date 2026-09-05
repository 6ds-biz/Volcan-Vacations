import { ScenicImage } from './scenic-image';
import { Container, LinkButton } from './ui';

export function CTASection() {
  return <section className="cta-band"><ScenicImage src="/images/rainforest.webp" /><Container><div className="cta-band__inner"><p className="script-accent">Your Costa Rica<br />Adventure Starts Here</p><div><h2>Let’s Plan Your Costa Rica Experience</h2><p>Tell us a bit about your trip, and we’ll help you find the perfect experiences.</p></div><LinkButton href="/plan-your-trip" variant="light" arrow>Plan My Trip</LinkButton></div></Container></section>;
}
