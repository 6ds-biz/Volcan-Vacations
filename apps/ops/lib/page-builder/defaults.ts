import {base,type Page,type Widget} from '@6ds/page-builder/core';
import type {RuntimeRegistry} from '@6ds/page-builder/runtime';
/** Defaults reproduce the approved grouping; mobile order can prioritize execution. */
export function defaultPage(pageType:string,rows:[number,string[]][][],registry:RuntimeRegistry):Page{
 return {schema_version:1,page_id:pageType,sections:rows.map((columns,si)=>({...base(`${pageType}-s${si}`,si),presentation:{...base().presentation,order:si,spacing:'none'},responsive:pageType==='operations-dashboard'&&si<2?{mobile:{order:1-si}}:{},columns:columns.map(([width,types],ci)=>({...base(`${pageType}-s${si}-c${ci}`,ci),presentation:{...base().presentation,order:ci,width,spacing:'none'},responsive:{mobile:{width:12}},widgets:types.map((type,wi):Widget=>({...base(`${pageType}-s${si}-c${ci}-w${wi}`,wi),presentation:{...base().presentation,order:wi,spacing:'none'},type,config:structuredClone(registry[type].defaultConfig)}))}))}))};
}
