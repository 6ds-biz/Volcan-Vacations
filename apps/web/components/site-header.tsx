import Link from 'next/link';
import { LinkButton, Container } from './ui';
import { Brand } from './brand';

const navigation = [
  { href: '/tours', label: 'Tours' },
  { href: '/plan-your-trip', label: 'Plan Your Trip' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'Contact' },
];


export function SiteHeader() {
  return <header className="site-header"><Container className="site-header__inner"><Brand /><nav className="desktop-nav" aria-label="Main navigation">{navigation.map((item) => <Link href={item.href} key={item.href}>{item.label}</Link>)}</nav><div className="desktop-cta"><LinkButton href="/plan-your-trip" arrow>Plan My Trip</LinkButton></div><details className="mobile-menu"><summary aria-label="Open main navigation"><span /><span /><span /></summary><nav aria-label="Mobile navigation">{navigation.map((item) => <Link href={item.href} key={item.href}>{item.label}</Link>)}<Link className="button button--primary" href="/plan-your-trip">Plan My Trip</Link></nav></details></Container></header>;
}
