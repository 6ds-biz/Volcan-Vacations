# Volcan Vacations project

Project ID: `volcan-vacations`. Configuration is in `apps/page-builder/src/projects/vv/definition.ts`; rendering and safe runtime context are in `index.tsx`. The generic workspace only consumes `DesignProject`, defined in `src/project.ts`.

| Page type | Source default | Export filename |
| --- | --- | --- |
| `home` | Hero, Arenal, Featured Experiences, Why VV, Trip Planning, Pacific Coast, Coastal Destinations, Kinds of Adventure, How It Works, Final CTA | `vv-home-layout.json` |
| `tours` | Current tours introduction, catalog and CTA | `vv-tours-layout.json` |
| `tour-detail` | Current shared tour template | `vv-tour-detail-layout.json` |
| `plan-your-trip` | Current introduction and planning form | `vv-plan-layout.json` |
| `about` | Current hero, story, values and CTA | `vv-about-layout.json` |
| `contact` | Current hero, public contact details and form | `vv-contact-layout.json` |

The defaults come directly from `apps/web/lib/website/defaults.ts`; VV's existing public components, typography, theme CSS, header, footer and canvas frame are reused. The homepage is not redesigned. Tour Detail also registers Included and What to Bring for insertion through Widgets alongside the existing default blocks.

Approved choices expose black, charcoal, warm ivory, white and transparent surfaces; gold/light-gold accents; none/small/medium/large/XL section spacing; and display/heading/subheading/body/small/script typography. Element presentation uses the core's none/small/normal/large spacing vocabulary; `normal` is the medium element preset. Script typography uses the existing local Allura font. Changes are bounded tokens, never arbitrary CSS.

The reviewed selectable catalog preserves the existing API media IDs `vv-pacific`, `vv-papagayo`, `vv-nosara`, `vv-las-catalinas` and `vv-tamarindo`, sources and generated-illustration provenance. Legacy images remain in the source-controlled page defaults. They are not newly approved for the selectable catalog. Replacing an image chooses a reviewed asset; reset removes the override and restores the original source presentation.

Media settings include alt text, decorative status, cover/contain, overlays, aspect ratio, radius, visual focal-point selection and separate tablet/mobile asset/crop overrides. The portable adapter converts core percentage crops into normalized 0–1 coordinates. No upload endpoint or binary data is implemented.

`next.config.mjs` substitutes the two public presentation imports named `tour-inventory` and `tour-availability` with `sample-inventory.tsx`. This boundary applies only to the standalone build. Samples are clearly labeled, perform no API calls and show no price snapshots. The project replaces the tour request/price block with a presentation placeholder, while a runtime-only sample tour supplies safe example description/gallery content. Forms are registered application widgets, rendered inert inside the editor/preview; form values and backend definitions never enter layout JSON.

Business widgets remain unique. Safe presentation sections/widgets may be duplicated; attempting to duplicate a section containing a unique application widget is unavailable. Page layout controls may move or remove business widget placements, but cannot redefine their data or backend behavior.

The combined Contact Content source block remains available to preserve the current page. Contact Information and Contact Form are also available separately when rearranging the page. Canonical public contact is always `info@volcanvacations.com`.
