export type TourCategory = 'Adventure' | 'Nature' | 'Relaxation' | 'Culture' | 'Family';

export type Tour = {
  slug: string;
  title: string;
  category: TourCategory;
  description: string;
  duration: string;
  priceFrom: number;
  visual: 'river' | 'volcano' | 'springs' | 'bridges' | 'waterfall' | 'coffee';
  featured?: boolean;
};

export const tourCategories: TourCategory[] = [
  'Adventure',
  'Nature',
  'Relaxation',
  'Culture',
  'Family',
];

export const tours: Tour[] = [
  { slug: 'whitewater-rafting', title: 'Whitewater Rafting', category: 'Adventure', description: 'Paddle rainforest rapids with experienced local river guides.', duration: 'Half day', priceFrom: 85, visual: 'river', featured: true },
  { slug: 'arenal-volcano-hike', title: 'Arenal Volcano Hike', category: 'Nature', description: 'Follow forest trails to wide-open views of Arenal and its old lava fields.', duration: '4 hours', priceFrom: 72, visual: 'volcano', featured: true },
  { slug: 'hot-springs-experience', title: 'Hot Springs Experience', category: 'Relaxation', description: 'Unwind in naturally warm mineral pools surrounded by tropical gardens.', duration: 'Evening', priceFrom: 95, visual: 'springs', featured: true },
  { slug: 'wildlife-hanging-bridges', title: 'Wildlife & Hanging Bridges', category: 'Family', description: 'Walk through the canopy and look for monkeys, toucans, and sloths.', duration: '3 hours', priceFrom: 68, visual: 'bridges', featured: true },
  { slug: 'waterfall-adventure', title: 'Waterfall Adventure', category: 'Adventure', description: 'Descend into a lush canyon to one of La Fortuna’s iconic cascades.', duration: '3 hours', priceFrom: 55, visual: 'waterfall' },
  { slug: 'coffee-chocolate-tour', title: 'Coffee & Chocolate Tour', category: 'Culture', description: 'Taste two Costa Rican staples and meet the people behind the process.', duration: '2.5 hours', priceFrom: 48, visual: 'coffee' },
];
