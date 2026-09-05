import type { Metadata } from 'next';
import { ScenicImage } from '../../components/scenic-image';
import { CTASection } from '../../components/cta-section';
import { CompassIcon, LeafIcon, SparkIcon } from '../../components/icons';
import { Container, Eyebrow, PageHero } from '../../components/ui';

export const metadata: Metadata = { title: 'About Us', description: 'Learn about Volcan Vacations and our focused approach to travel planning in Costa Rica.' };

export default function AboutPage() {
  return <main id="main-content"><PageHero eyebrow="Our approach" title="Costa Rica, with more meaning and less guesswork." intro="Volcan Vacations is building a simpler way to discover and organize quality experiences, beginning in La Fortuna and Arenal." /><section className="section about-story"><Container className="about-grid"><div className="about-art"><ScenicImage src="/images/bridges.webp" alt="Illustrative view through the Costa Rica rainforest canopy" sizes="(max-width: 720px) 100vw, 50vw" /></div><div className="about-copy"><Eyebrow>Focused by design</Eyebrow><h2>A clear starting point for an extraordinary place.</h2><p>Costa Rica offers more possibilities than most travelers can fit into one trip. We begin with a place we know closely: the volcano, rivers, forests, wildlife, and warm hospitality of the La Fortuna and Arenal region.</p><p>Our goal is practical—to bring carefully considered experiences into one clear planning journey, with personal assistance when it matters. As Volcan Vacations grows, quality and a sense of place will remain at the center.</p></div></Container></section><section className="section section--cream values-section"><Container><div className="value-row"><div><LeafIcon /><h3>Rooted in Costa Rica</h3><p>A focused perspective on the landscapes and experiences that make this country distinct.</p></div><div><SparkIcon /><h3>Quality over quantity</h3><p>A considered collection that helps travelers choose with greater clarity and confidence.</p></div><div><CompassIcon /><h3>Personal by nature</h3><p>Planning that begins with how you actually want to spend your time.</p></div></div></Container></section><CTASection /></main>;
}
