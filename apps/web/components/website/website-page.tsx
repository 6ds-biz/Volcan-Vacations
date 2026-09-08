import {PublicCanvas} from './public-canvas';
import {publicGet} from '../../lib/website/server';
import type {PublicPageKey} from '../../lib/website/registry';
import type {Tour} from '../../lib/inventory';
export async function WebsitePage({pageKey,tour}:{pageKey:PublicPageKey;tour?:Tour}){const [state,assets]=await Promise.all([publicGet('/public/website/pages/'+pageKey),publicGet('/public/website/media')]);return <main id="main-content" className={pageKey==='home'?'home-page':undefined}><PublicCanvas pageKey={pageKey} layout={state?.page} assets={Array.isArray(assets)?assets:[]} tour={tour}/></main>;}
