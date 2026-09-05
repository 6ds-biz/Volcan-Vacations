import Link from 'next/link';
import { Container } from './ui';
import { Brand } from './brand';

export function SiteFooter() {
  return <footer className="site-footer"><Container>
    <div className="site-footer__grid">
      <Brand />
      <nav aria-label="Footer navigation"><Link href="/tours">Tours</Link><Link href="/plan-your-trip">Plan Your Trip</Link><Link href="/about">About</Link><Link href="/contact">Contact</Link></nav>
      <span className="script-accent footer-script">Pura Vida</span>
    </div>
    <div className="site-footer__bottom"><p>© {new Date().getFullYear()} Volcan Vacations. All rights reserved.</p><p>Terms &amp; privacy information coming soon.</p></div>
  </Container></footer>;
}
