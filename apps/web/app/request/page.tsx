import type { Metadata } from 'next';
import { Container, PageHero } from '../../components/ui';
import { BookingRequest } from '../../components/booking-request';

export const metadata: Metadata = {title: 'Request This Tour', description: 'Start your Costa Rica tour request. We will confirm availability before any payment.', robots: {index: false, follow: true}};

export default async function RequestPage({searchParams}: {searchParams: Promise<{tour?: string | string[]}>}) {
  const query = await searchParams;
  const slug = typeof query.tour === 'string' ? query.tour : '';
  return <main id="main-content"><PageHero eyebrow="Your Costa Rica experience" title="A great adventure starts here." intro="Tell us who’s coming and when you’d like to explore. This is a request—not a confirmed booking. We’ll check availability with you before any payment." /><section className="section planner-section"><Container><BookingRequest key={slug} slug={slug} /></Container></section></main>;
}
