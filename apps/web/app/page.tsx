import type {Metadata} from 'next';
import {WebsitePage} from '../components/website/website-page';
import './home.css';
export const metadata: Metadata = {
  title: 'Costa Rica Experiences, Thoughtfully Planned',
  description: 'Discover Costa Rica, from Arenal’s rainforest to the Pacific Coast, with remarkable tours and thoughtful trip planning.',
};
export default function Page(){return <WebsitePage pageKey="home"/>;}
