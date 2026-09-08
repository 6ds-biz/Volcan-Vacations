import type {Metadata} from 'next';
import {notFound} from 'next/navigation';
import {getPublicTour} from '../../../lib/website/server';
import {WebsitePage} from '../../../components/website/website-page';
export async function generateMetadata({params}:{params:Promise<{slug:string}>}):Promise<Metadata>{const {slug}=await params;const tour=await getPublicTour(slug);return {title:tour?.name||'Tour not found',description:tour?.short_description,alternates:{canonical:'/tours/'+encodeURIComponent(slug)}};}
export default async function Page({params}:{params:Promise<{slug:string}>}){const {slug}=await params;const tour=await getPublicTour(slug);if(!tour)notFound();return <WebsitePage pageKey="tour-detail" tour={tour}/>;}
