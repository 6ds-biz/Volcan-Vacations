import type {Metadata} from 'next';
import {WebsitePage} from '../../components/website/website-page';
export const metadata: Metadata = { title: 'Contact', description: 'Get in touch with Volcan Vacations about your Costa Rica travel plans and questions.' };
export default function Page(){return <WebsitePage pageKey="contact"/>;}
