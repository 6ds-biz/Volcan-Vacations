import {publicRegistry, publicTokens, isPageKey} from '../../../../web/lib/website/registry';
import {defaultLayout} from '../../../../web/lib/website/defaults';
import {publicMediaProvider} from '../../../../web/lib/website/media';
import type {MediaAsset} from '@6ds/page-builder/core';
import type {ProjectDefinition} from '../../project';

// Same reviewed IDs and provenance as services/api/app/website/media.py.
export const assets: MediaAsset[] = [
  ['pacific', 'pacific-sunset', 'Illustrative Pacific sunset over golden sand and a wooded coastal headland.'],
  ['papagayo', 'papagayo', 'Illustrative blue Pacific cove framed by wooded headlands.'],
  ['nosara', 'nosara', 'Illustrative surfers walking along a Pacific beach beside coastal forest.'],
  ['las-catalinas', 'las-catalinas', 'Illustrative coastal village beside the Pacific.'],
  ['tamarindo', 'tamarindo', 'Illustrative Pacific bay at sunset.'],
].map(([id, file, alt]) => ({id: 'vv-' + id, type: 'image', source: `/images/coast/${file}-temporary.webp`, filename: `${file}-temporary.webp`, mime_type: 'image/webp', width: 1536, height: 1024, alt, rights_status: 'APPROVED', provenance: 'Existing generated VV illustration: docs/public-homepage/coastal-media.md.', tags: ['Destinations']}));
function key(value: string) { if (!isPageKey(value)) throw Error('Unknown VV page.'); return value; }
export const vvDefinition: ProjectDefinition = {
  id: 'volcan-vacations', name: 'Volcan Vacations', defaultLabel: 'New from VV Default', publicEmail: 'info@volcanvacations.com',
  pages: [
    {id: 'home', label: 'Home', filename: 'vv-home-layout.json'},
    {id: 'tours', label: 'Tours', filename: 'vv-tours-layout.json'},
    {id: 'tour-detail', label: 'Tour Detail Template', filename: 'vv-tour-detail-layout.json'},
    {id: 'plan-your-trip', label: 'Plan Your Trip', filename: 'vv-plan-layout.json'},
    {id: 'about', label: 'About', filename: 'vv-about-layout.json'},
    {id: 'contact', label: 'Contact', filename: 'vv-contact-layout.json'},
  ],
  tokens: publicTokens,
  surfaceLabels: {base: 'Black', panel: 'Charcoal', accent: 'Warm Ivory', white: 'White', transparent: 'Transparent'},
  media: publicMediaProvider(assets),
  defaults: pageType => defaultLayout(key(pageType)),
  registry: pageType => {
    const registry = publicRegistry(key(pageType));
    for (const definition of Object.values(registry)) {
      // Business widgets remain unique; presentation sections may be duplicated safely.
      definition.duplicate = !['tour-grid', 'planning-form', 'contact-form', 'contact-content', 'availability', 'price-request'].includes(definition.type);
      if (definition.category.startsWith('Public') || ['image-text', 'full-width-media'].includes(definition.type)) {
        definition.fields = [...definition.fields, ...Object.entries(publicTokens).map(([field, options]) => ({key: field, label: field === 'space' ? 'Section spacing' : field === 'accent' ? 'Accent' : field === 'surface' ? 'Surface token' : 'Typography', kind: 'choice' as const, options}))];
      }
    }
    return registry;
  },
};
