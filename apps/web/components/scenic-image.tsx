import Image from 'next/image';
import type { Tour } from '../data/tours';

// Presentation assets are separate from inventory. Replace these local files
// with approved VV photography without changing the tour model or API contract.
export const tourImages: Record<Tour['visual'], { src: string; alt: string }> = {
  river: { src: '/images/rafting.webp', alt: 'Illustrative rainforest rafting adventure' },
  volcano: { src: '/images/arenal.webp', alt: 'Illustrative Arenal volcano and rainforest landscape' },
  springs: { src: '/images/springs.webp', alt: 'Illustrative thermal pools surrounded by tropical gardens' },
  bridges: { src: '/images/bridges.webp', alt: 'Illustrative hanging bridge through rainforest canopy' },
  waterfall: { src: '/images/waterfall.webp', alt: 'Illustrative waterfall flowing into a turquoise forest pool' },
  coffee: { src: '/images/coffee.webp', alt: 'Illustrative Costa Rican coffee and cacao still life' },
};

export function ScenicImage({ src = '/images/arenal.webp', alt = '', priority = false, sizes = '100vw' }: { src?: string; alt?: string; priority?: boolean; sizes?: string }) {
  return <Image className="scenic-image" src={src} alt={alt} fill sizes={sizes} priority={priority} />;
}
