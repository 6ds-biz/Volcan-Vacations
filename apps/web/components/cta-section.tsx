import { SparkIcon } from './icons';
import { Container, LinkButton } from './ui';

export function CTASection() {
  return <section className="cta-band"><Container><div className="cta-band__inner"><div className="cta-band__icon"><SparkIcon /></div><div><p className="eyebrow eyebrow--light">Your trip, made simpler</p><h2>Let’s shape a Costa Rica escape that feels like yours.</h2><p>Share your travel style and interests. We’ll help you find a thoughtful starting point.</p></div><LinkButton href="/plan-your-trip" variant="light" arrow>Plan My Trip</LinkButton></div></Container></section>;
}
