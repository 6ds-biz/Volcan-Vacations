import Link from 'next/link';
import {TourAvailability} from './tour-availability';
import {ConfiguredMedia} from './public-media';
import type {Tour} from '../../lib/inventory';
import {TourPhoto} from '../tour-photo';
import {TourInventory} from '../tour-inventory';
import {Container,LinkButton} from '../ui';
import type {Editorial} from '../../lib/website/registry';
export function TourBlock({kind,tour,config}:{kind:string;tour:Tour;config:Editorial}){
 const request=`/request?tour=${encodeURIComponent(tour.slug)}`;
 if(kind==='tour-hero')return <section className="website-tour-hero"><div className="website-tour-photo">{config.media?<ConfiguredMedia config={config.media} scenic/>:<TourPhoto image={tour.primary_image}/>}</div><Container><p className="eyebrow">{config.eyebrow||tour.location||'Costa Rica'}</p><h1>{config.heading||tour.name}</h1>{config.subheadline&&<p className="website-subheadline">{config.subheadline}</p>}{config.copy&&<p>{config.copy}</p>}</Container></section>;
 const content:Record<string,React.ReactNode>={
 'tour-overview':<><h2>{config.heading||'Your experience'}</h2><p>{tour.short_description}</p></>,
 description:tour.description&&<><h2>{config.heading||'About this tour'}</h2><p className="website-tour-description">{tour.description}</p></>,
 'price-request':<><h2>{config.heading||'Plan your experience'}</h2><p>From ${tour.retail_price} USD per person</p><LinkButton href={request} arrow>Request This Tour</LinkButton><p>Availability and final details are confirmed before payment.</p></>,
 'duration-details':<><h2>{config.heading||'Tour details'}</h2><dl><dt>Duration</dt><dd>{tour.duration}</dd><dt>Category</dt><dd>{tour.category}</dd>{tour.difficulty&&<><dt>Activity level</dt><dd>{tour.difficulty}</dd></>}{tour.minimum_age!==null&&<><dt>Minimum age</dt><dd>{tour.minimum_age}</dd></>}</dl></>,
 included:<><h2>{config.heading||"What's included"}</h2><p>We confirm the inclusions for your selected experience when reviewing your request.</p></>,
 bring:<><h2>{config.heading||'What to bring'}</h2><p>Ask us about preparation and what to bring when requesting this experience.</p></>,
 gallery:(config.media||tour.images.length>0)&&<><h2>{config.heading||'Gallery'}</h2><div className="website-tour-gallery">{config.media?<ConfiguredMedia config={config.media}/>:tour.images.map(image=><div key={image.id}><TourPhoto image={image}/></div>)}</div></>,
 availability:<><h2>{config.heading||'Availability'}</h2><TourAvailability slug={tour.slug}/><Link href={request}>Request a date →</Link></>,
 destination:<><h2>{config.heading||'Destination'}</h2><p>{tour.location||'Costa Rica'}</p></>,
 'related-tours':<><h2>{config.heading||'More experiences'}</h2><TourInventory limit={config.limit||3}/></>,
 };
 return content[kind]?<section className="section"><Container>{config.eyebrow&&<p className="eyebrow">{config.eyebrow}</p>}{content[kind]}{config.subheadline&&<p className="website-subheadline">{config.subheadline}</p>}{config.copy&&<p>{config.copy}</p>}</Container></section>:null;
}
