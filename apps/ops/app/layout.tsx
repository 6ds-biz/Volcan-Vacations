import './globals.css';
import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Volcan Vacations Operations',
  description: 'Internal Volcan Vacations inventory management.',
  robots: {index: false, follow: false},
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body><a className="ops-skip" href="#ops-content">Skip to content</a><header className="ops-header"><Link href="/">Volcan Operations</Link><nav aria-label="Operations navigation"><Link href="/">Dashboard</Link><Link href="/bookings">Bookings</Link><Link href="/tours">Tours</Link><Link href="/availability">Availability</Link><Link href="/payments">Payments</Link><Link href="/suppliers">Suppliers</Link></nav></header><div className="ops-warning">Internal development only · Authentication is not implemented. Protect Operations and /ops APIs before production use.</div><main id="ops-content" className="ops-main">{children}</main></body>
    </html>
  );
}
