import {publicRuntime, sourceFlow} from '../../../../web/components/website/public-canvas';
import {WebsiteContext} from '../../../../web/components/website/public-media';
import {CanvasFrame} from '../../../../web/components/website/editor/canvas-frame';
import {Container} from '../../../../web/components/ui';
import {editorial} from '../../../../web/components/website/editorial';
import {isPageKey, type Editorial} from '../../../../web/lib/website/registry';
import type {Tour} from '../../../../web/lib/inventory';
import type {DesignProject} from '../../project';
import {vvDefinition} from './definition';

// Runtime context only; never placed in a layout, browser storage or export.
const sampleTour: Tour = {
  name: 'Arenal rainforest discovery', slug: 'sample-experience', short_description: 'An illustrative experience among forest trails and volcanic landscapes.',
  description: 'Preview copy for the shared tour template. Each public tour supplies its own description.', category: 'Nature · Sample', duration: 'Provided by the public tour',
  retail_price: '', featured: false, location: 'Arenal · Sample tour', difficulty: null, minimum_age: null,
  primary_image: {id: 0, image_url: '/images/arenal.webp', alt_text: 'Arenal landscape illustration', sort_order: 0, is_primary: true},
  images: [{id: 0, image_url: '/images/rainforest.webp', alt_text: 'Rainforest illustration', sort_order: 0, is_primary: true}],
};
const context = {device: 'desktop' as const, permissions: {role: 'designer', permissions: []}, data: {tour: sampleTour}, media: vvDefinition.media};
export const vvProject: DesignProject = {
  ...vvDefinition, context,
  runtime: pageType => {
    if (!isPageKey(pageType)) throw Error('Unknown VV page.');
    const registry = publicRuntime(pageType, sampleTour), definitions = vvDefinition.registry(pageType);
    for (const [type, definition] of Object.entries(definitions)) registry[type] = {...registry[type], ...definition};
    if (registry['price-request']) registry['price-request'].render = raw => {
      const c = raw as Editorial;
      return editorial(<section className="section"><Container><h2>{c.heading || 'Plan your experience'}</h2><p>Request CTA · application widget</p><p>Price and request details are supplied by the public tour.</p><span className="button button--primary">Request This Tour →</span></Container></section>, c);
    };
    return registry;
  },
  Canvas: function VVCanvas({children, device, page, preview}) {
    return <CanvasFrame device={device}><WebsiteContext.Provider value={{...context, device}}><main id="main-content" className={`${page.page_id === 'public-home' ? 'home-page ' : ''}website-runtime${preview && sourceFlow(page) ? ' website-source-layout' : ''}`}>{page.page_id === 'public-tour-detail' && <p className="builder-sample-note">Sample tour · template preview only</p>}{children}</main></WebsiteContext.Provider></CanvasFrame>;
  },
};
