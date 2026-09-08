import type {Metadata} from 'next';
import {WebsitePage} from '../../components/website/website-page';
export const metadata: Metadata = { title: 'Plan Your Costa Rica Trip', description: 'Share your travel style and interests to start planning a personalized Costa Rica experience.' };
export default function Page(){return <WebsitePage pageKey="plan-your-trip"/>;}
