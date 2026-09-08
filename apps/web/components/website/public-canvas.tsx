'use client';
import {useMemo} from 'react';
import {PageRenderer,genericRuntime,useDevice,type RuntimeRegistry} from '@6ds/page-builder/runtime';
import type {MediaAsset} from '@6ds/page-builder/core';
import type {Tour} from '../../lib/inventory';
import {publicRegistry,type PublicPageKey,type Editorial} from '../../lib/website/registry';
import {defaultLayout,resolvedLayout} from '../../lib/website/defaults';
import {publicMediaProvider} from '../../lib/website/media';
import {WebsiteContext,ConfiguredMedia} from './public-media';
import * as Home from './default-blocks/home';
import * as Tours from './default-blocks/tours';
import * as About from './default-blocks/about';
import * as Planning from './default-blocks/planning';
import * as Contact from './default-blocks/contact';
import {TourBlock} from './tour-blocks';
import {Container,LinkButton} from '../ui';
import {CTASection} from '../cta-section';
import './website.css';
const blocks:Record<string,(config:Editorial)=>React.ReactNode>={hero:Home.HomeHero,'arenal-feature':Home.ArenalFeature,'featured-experiences':Home.FeaturedExperiences,benefits:Home.HomeBenefits,'trip-planning':Home.TripPlanning,'pacific-coast':Home.PacificCoast,'coastal-destinations':Home.CoastalDestinations,'kinds-of-adventure':Home.KindsOfAdventure,'how-it-works':Home.HowItWorks,'final-cta':Home.FinalCTA,'tours-hero':Tours.ToursHero,'tour-grid':Tours.ToursCatalog,'page-hero':Planning.PlanningHero,'planning-form':Planning.PlanningContent,intro:Planning.PlanningIntro,'about-hero':About.AboutHero,'about-story':About.AboutStory,values:About.AboutValues,'local-expertise':About.AboutStory,'contact-hero':Contact.ContactHero,'contact-content':Contact.ContactContent,'contact-information':Contact.ContactInformation,'contact-form':Contact.ContactForm};
export function PublicCanvas({pageKey,layout,assets,tour}:{pageKey:PublicPageKey;layout:unknown;assets:MediaAsset[];tour?:Tour}){
 const device=useDevice(),media=useMemo(()=>publicMediaProvider(assets),[assets]);const defaults=defaultLayout(pageKey),page=resolvedLayout(layout,pageKey);const generic=genericRuntime();const registry:RuntimeRegistry={};
 for(const [type,definition]of Object.entries(publicRegistry(pageKey))){registry[type]={...definition,render:(raw,context)=>{
  const config=raw as Editorial;
  if(generic[type])return generic[type].render(raw,context);
  if(type==='cta')return <CTASection {...config}/>;
  if(type==='button')return <Container><LinkButton href={config.href||'/plan-your-trip'} arrow>{config.label||'Plan My Trip'}</LinkButton></Container>;
  if(type==='full-width-media')return config.media?<ConfiguredMedia config={config.media}/>:null;
  if(type==='image-text')return <section className="section"><Container>{config.media&&<ConfiguredMedia config={config.media}/>}<h2>{config.heading}</h2>{config.copy&&<p>{config.copy}</p>}</Container></section>;
  if(pageKey==='tour-detail')return tour?<TourBlock kind={type} tour={tour} config={config}/>:null;
  if(blocks[type])return blocks[type](config);
  return <section className="section"><Container>{config.heading&&<h2>{config.heading}</h2>}{config.copy&&<p>{config.copy}</p>}</Container></section>;
 }};}
 const context={device,permissions:{role:'public',permissions:[]},data:tour?{tour}:{},media};
 // A one-column, zero-spacing source template uses display:contents to preserve
 // the approved page's visual boxes. Customized layouts use the core grid.
 const source=JSON.stringify(page)===JSON.stringify(defaults);
 return <WebsiteContext.Provider value={context}><div className={`website-runtime${source?' website-source-layout':''}`}><PageRenderer page={page} fallback={defaults} registry={registry} context={context}/></div></WebsiteContext.Provider>;
}
