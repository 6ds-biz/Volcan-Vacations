import type {Metadata} from 'next';
import {WebsitePage} from '../../components/website/website-page';
export const metadata: Metadata = { title: 'About Us', description: 'Learn about Volcan Vacations and our focused approach to travel planning in Costa Rica.' };
export default function Page(){return <WebsitePage pageKey="about"/>;}
