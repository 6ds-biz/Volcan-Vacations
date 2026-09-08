import type {Editorial} from '../lib/website/registry';
import {ConfiguredMedia} from './website/public-media';
import { ScenicImage } from './scenic-image';
import { Container, LinkButton } from './ui';

export function CTASection(config:Editorial={}) {
  return <section className="cta-band">{config.media?<ConfiguredMedia config={config.media} scenic/>:<ScenicImage src="/images/rainforest.webp" />}<Container><div className="cta-band__inner"><p className="script-accent">Your Costa Rica<br />Adventure Starts Here</p><div>{config.eyebrow&&<p className="eyebrow">{config.eyebrow}</p>}<h2>{config.heading||'Let’s Plan Your Costa Rica Experience'}</h2>{config.subheadline&&<p className="website-subheadline">{config.subheadline}</p>}<p>{config.copy||'Tell us a bit about your trip, and we’ll help you find the perfect experiences.'}</p></div><LinkButton href={config.href||"/plan-your-trip"} variant="light" arrow>{config.label||"Plan My Trip"}</LinkButton></div></Container></section>;
}
