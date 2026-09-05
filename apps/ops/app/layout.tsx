import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Volcan Vacations Operations',
  description: 'Internal operations dashboard placeholder for Volcan Vacations.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
