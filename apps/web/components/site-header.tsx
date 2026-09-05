import Link from 'next/link';
import { LinkButton, Container } from './ui';

const navigation = [
  { href: '/tours', label: 'Tours' },
  { href: '/plan-your-trip', label: 'Plan Your Trip' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'Contact' },
];

function Brand() {
  return <Link className="brand" href="/" aria-label="Volcan Vacations home"><svg className="brand__mark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="currentColor" /><path d="M8 33.5 21.3 14l5.1 8.2 3.1-4.6L40 33.5H8Z" fill="#f8f2e6" /><path d="m17 33.5 7.2-10.7 3 4.7 2.3-3.5 6.4 9.5H17Z" fill="#91ab78" /><path d="M7.5 34h33" stroke="#e3b96f" strokeWidth="2" strokeLinecap="round" /></svg><span className="brand__text"><strong>Volcan</strong><span>Vacations</span></span></Link>;
}

export function SiteHeader() {
  return <header className="site-header"><Container className="site-header__inner"><Brand /><nav className="desktop-nav" aria-label="Main navigation">{navigation.map((item) => <Link href={item.href} key={item.href}>{item.label}</Link>)}</nav><div className="desktop-cta"><LinkButton href="/plan-your-trip">Plan My Trip</LinkButton></div><details className="mobile-menu"><summary aria-label="Open main navigation"><span /><span /><span /></summary><nav aria-label="Mobile navigation">{navigation.map((item) => <Link href={item.href} key={item.href}>{item.label}</Link>)}<Link className="button button--primary" href="/plan-your-trip">Plan My Trip</Link></nav></details></Container></header>;
}
