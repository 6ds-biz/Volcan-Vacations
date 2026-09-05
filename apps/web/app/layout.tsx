import './globals.css';
import type { Metadata } from 'next';
import { SiteFooter } from '../components/site-footer';
import { SiteHeader } from '../components/site-header';

export const metadata: Metadata = {
  metadataBase: new URL('https://volcanvacations.com'),
  title: {
    default: 'Volcan Vacations | Costa Rica Experiences',
    template: '%s | Volcan Vacations',
  },
  description:
    'Thoughtfully selected tours and personal trip planning for La Fortuna, Arenal, and Costa Rica.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <a className="skip-link" href="#main-content">
          Skip to content
        </a>
        <SiteHeader />
        {children}
        <SiteFooter />
      </body>
    </html>
  );
}
