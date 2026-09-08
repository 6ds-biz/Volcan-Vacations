'use client';
import type {ReactNode} from 'react';
import {devices,keys,mediaDefaults,validateMedia,type MediaConfig} from '@6ds/page-builder/core';
import {genericRuntime,MediaView,type RuntimeRegistry} from '@6ds/page-builder/runtime';
export const pageWidgets:Record<string,Record<string,string>>={
 'owner-dashboard':{'business-health':'Business Health','needs-attention':'Needs Attention','my-tasks':'My Tasks','vendor-pipeline':'Vendor Pipeline',inventory:'Inventory','recent-payments':'Recent Payments','visual-feature':'Visual Feature'},
 'operations-dashboard':{'my-tasks':'My Tasks','needs-attention':'Needs Attention','new-bookings':'New Bookings','supplier-followup':'Supplier Follow-up',availability:'Availability','vendor-work':'Vendor Work','transportation-lookup':'Transportation Lookup'},
 'booking-detail':{'booking-summary':'Booking Summary',customer:'Customer',travelers:'Travelers',trip:'Trip',availability:'Availability','supplier-confirmation':'Supplier Confirmation',payment:'Payment','related-tasks':'Related Tasks',notes:'Notes',history:'History'},
 'supplier-detail':{'supplier-overview':'Supplier Overview','contact-information':'Contact Information','relationship-status':'Relationship Status',capabilities:'Capabilities',agreements:'Agreements',rates:'Rates','open-tasks':'Open Tasks',notes:'Notes',history:'History'},
 'transportation-detail':{'route-summary':'Route Summary','origin-destination':'Origin / Destination','vendor-services':'Vendor Services',schedules:'Schedules',rates:'Rates',freshness:'Verification / Freshness','related-tasks':'Related Tasks',notes:'Notes',history:'History'},
};
export type PageType=keyof typeof pageWidgets;
const pageCapability:Record<string,string>={'owner-dashboard':'users.manage','operations-dashboard':'bookings.read','booking-detail':'bookings.read','supplier-detail':'suppliers.read','transportation-detail':'transport.read'};
const contextKey:Record<string,string>={'owner-dashboard':'dashboard_profile','operations-dashboard':'dashboard_profile','booking-detail':'booking_id','supplier-detail':'supplier_id','transportation-detail':'route_id'};
export function vvRegistry(pageType:string,slots:Record<string,ReactNode>):RuntimeRegistry{
 const result=genericRuntime();for(const [type,label] of Object.entries(pageWidgets[pageType]||{})){
  const permission=type==='rates'?(pageType==='transportation-detail'?'transport.rates':'commercial.read'):type==='history'?'audit.read':type==='payment'?'payments.read':type==='recent-payments'?'users.manage':pageCapability[pageType];
  result[type]={type,label,category:type==='visual-feature'?'Media':'VV '+pageType,icon:type,defaultConfig:type==='visual-feature'?{...structuredClone(mediaDefaults),asset:'vv-arenal',alt:'Arenal volcano and surrounding rainforest.',overlay:'dark'}:{},validate:type==='visual-feature'?validateMedia:c=>keys(c,[]),fields:[],devices,duplicate:false,context:[contextKey[pageType]],pages:[pageType],allowed:p=>p.permissions.includes(permission),render:type==='visual-feature'?(config,context)=><section className="vv-personality vv-builder-feature"><MediaView config={config as unknown as MediaConfig} context={context}/><div><span>Pura vida</span><h2>Extraordinary Experiences</h2><p>Start with great operations.</p></div></section>:()=>slots[type]??<p>This section is unavailable for the current record.</p>};
 }
 return result;
}
