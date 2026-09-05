import Link from 'next/link';
import { Container } from './ui';

export function SiteFooter() {
  return <footer className="site-footer"><Container><div className="site-footer__grid"><div className="footer-intro"><Link className="footer-brand" href="/">Volcan Vacations</Link><p>Thoughtful Costa Rica experiences, with roots in La Fortuna and Arenal.</p></div><div><h2>Explore</h2><nav aria-label="Footer navigation"><Link href="/tours">Tours</Link><Link href="/plan-your-trip">Plan Your Trip</Link><Link href="/about">About</Link><Link href="/contact">Contact</Link></nav></div><div><h2>Start here</h2><p>Not sure which experience fits? Tell us how you like to travel.</p><Link className="footer-link" href="/plan-your-trip">Plan my trip <span aria-hidden="true">→</span></Link></div></div><div className="site-footer__bottom"><p>© {new Date().getFullYear()} Volcan Vacations. Costa Rica.</p><p>Terms & privacy information coming soon.</p></div></Container></footer>;
}
