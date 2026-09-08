import type {Metadata} from 'next';
import {WebsitePage} from '../../components/website/website-page';
export const metadata: Metadata = { title: 'Tours & Experiences', description: 'Browse adventure, nature, relaxation, culture, and family experiences around La Fortuna and Arenal.' };
export default function Page(){return <WebsitePage pageKey="tours"/>;}
