# VV public visual editor — Part 2

Part 2 extends the public foundation in [public-vv-integration.md](public-vv-integration.md). It reuses `PageEditor`, its history/movement helpers, renderer and Page → Section → Column → Widget schema. No competing editor, layout table or new migration was introduced.

## Owner workflow

Sign into Operations as an active Owner. Open Website → Pages, choose a page and select Edit. The existing single-use handoff opens that page's private editor in the public web application. Partner and Staff cannot issue handoffs, read the management catalog or save layouts. Changing dashboard profile does not grant editing permissions.

The top bar offers Desktop, Tablet, Mobile, Undo, Redo, Preview, Save Draft and Exit. The left panel contains Widgets, Structure, Settings and Media. Export/Import remains available from the reusable editor. Publish and revision actions are not exposed by this consumer's draft-only adapter. Exit warns about unsaved changes; a saved draft exits directly to Website Pages. Browser navigation also warns while changes remain unsaved.

The canvas includes the real public header/logo, footer, fonts, photography and public inventory widgets. It is a same-origin blank iframe populated through a React portal, not a separately addressable draft page. Styles are copied from the public document (including CSSOM rules used in development). The frame waits for styles/fonts before becoming visible. Its CSS viewport is 1440px, 900px or 390px, scaled to fit the available canvas area. The public site's actual media queries run at those widths. Operations appearance is never applied to the canvas. Scaled drag/select controls compensate for zoom to remain at least 44px physically.

Preview hides authoring controls and shows the current private draft. Public forms, links and inventory actions remain inert in the editor/preview; layout editing cannot submit bookings or payment actions. Use the normal public site to exercise business flows.

## Structure and text

Structure is a nested keyboard-accessible list of sections, columns and widgets. Homepage sections use recognizable widget/chapter names. Select an item in Structure or its canvas bar to open Settings. Drag only from handles; Escape cancels dragging. Move Up/Down reorders sections or widgets, Move Left/Right reorders columns or transfers widgets to adjacent columns, and Move to column selects an explicit destination. Cross-frame pointer coordinates account for the frame's scale during edge scrolling.

Sections can be added, reordered, removed and duplicated when all contained widgets allow duplication. The same protection applies to columns. Business widgets remain nonduplicable; generic content can be duplicated. A section always retains 1–12 columns. Width is a bounded 12-column span; adding a column redistributes spans for the selected device. Visibility, width, order, alignment, spacing, density, surfaces, borders and containment use validated settings. White is an additive surface option in the existing version-1 schema; Black/Charcoal/Warm Ivory map to the core's base/panel/accent tokens. Raw CSS and free-pixel positioning remain unavailable.

Desktop/Tablet/Mobile use one layout with per-device overrides. Moving a widget between columns changes shared structure; order and width can vary by device. Clear device overrides restores inheritance. Undo/Redo includes structural, text, image, crop and responsive changes.

Public text controls include eyebrow, headline, subheadline, body and supported CTA fields. Input remains plain text; raw HTML is rejected. Link edits validate on blur so intermediate typing is possible. Supported targets are internal routes/anchors, HTTPS, mailto and tel. Protocol-relative URLs, executable schemes, credentials, control characters and encoded header-injection characters are rejected by both API and browser validators. Existing public contact content retains `info@volcanvacations.com`.

Some existing sections contain multiple pieces of copy or media. Their editorial controls target the primary headline/body/image and supported CTA; the preserved source block keeps its remaining content. This does not claim arbitrary inline editing of every word or every photograph inside a composite business widget. Generic widgets and separate columns provide additional editable content.

## Pages and inventory

Home starts with Hero → Arenal → Featured Experiences → Why VV → Trip Planning → Pacific Coast → Coastal Destinations → Kinds of Adventure → How It Works → Final CTA. No automatic rearrangement occurs. Public defaults retain the rainforest/coast separation.

Tours, the shared Tour Detail Template, Plan Your Trip, About and Contact each expose only their compatible widget registry. Tour detail receives an active public Tour object; there are no independent per-tour layout copies. Prices, suppliers, availability, inventory visibility and booking state cannot be configured in JSON. Featured Experiences/Tour Grid/Related Tours allow a bounded 1–12 item limit. Existing forms and request/availability logic remain authoritative. Planning and Contact retain their existing preview/disabled submission behavior.

Image + Text supports image-left/image-right arrangements, mobile stacking, heading/body/CTA and media. Full Width Media supports small/medium/large height presets, optional text and CTA, focal points and overlays. Tour Hero and Gallery can use a presentation media override without changing ProductImage records.

## Media

Media is a searchable thumbnail catalog with category filters, known dimensions, MIME type, source, provenance and rights metadata. Image-backed public widgets use a nested media binding; the generic Image/Media widget uses its existing direct configuration. Change Image opens this same library.

Select an approved asset, review its alt text, choose cover/contain and an overlay, then set the focal point by clicking/touching the image or using the labeled keyboard-operable X/Y sliders. Coordinates are normalized percentages from 0–100, preserving the core contract. Fit, alt/decorative status and overlay are shared; Tablet and Mobile optionally override the asset and focal point. No separate image is required. Use default image/crop clears a device override. Reset media removes the public widget override and restores the source image; Remove image stores an explicit empty selection.

Meaningful alt text may use reviewed catalog alt text when no override is supplied. Filenames are never synthesized as final alt text. Decorative status is explicit. `NEEDS_RIGHTS_REVIEW` entries remain visible with a warning and unavailable selection; no rights inference or promotion is performed. Approved assets are resolved by stable catalog ID and validated source. No arbitrary external URL entry or bulk ingestion is added.

The existing safe video contract remains available for future approved local MP4/WebM catalog entries: poster, muted playback, loop, controls and muted autoplay. Controls remain available, autoplay cannot enable audio, and reduced motion suppresses autoplay. The current catalog contains images; no new video, transcoding, upload or production storage infrastructure was added. Final publishing/media-rights acceptance remains Part 3.

## Private save architecture

The Part 1 handoff still expires after 60 seconds; the page-scoped canvas credential expires 15 minutes after issuance and is stored in an HttpOnly, SameSite=Strict cookie (Secure on HTTPS). It remains tied to the original internal login session. Every media read and draft write rechecks parent-session validity, account activity, Owner role and password-change state.

The Next.js `PUT /api/website-editor/pages/{key}/draft` proxy requires same-origin JSON, enforces a bounded payload, and forwards the HttpOnly credential server-to-server. FastAPI `PUT /website-editor/pages/{key}/draft` verifies the scope, validates presentation/media, reuses the existing version check and layout lock, and writes the draft plus the authenticated Owner audit actor. The scoped media endpoint is `GET /website-editor/pages/{key}/media`. No scoped publish endpoint exists.

Saving never updates published content or creates a published revision. API/network/session failures leave the in-memory draft available with an error message. On expiry, export the unsaved layout if needed, reopen Edit through Operations and import it. No credential is returned to browser JavaScript. Full publish, revision-restore, stale-publish and concurrency acceptance are deferred to Part 3.

## Validation

Validated with production builds and Chromium browser emulation. iPad checks use 1024px and 768px browser viewports; they are not a claim of physical Safari/iPad hardware testing.

| Check | Result |
| --- | --- |
| Backend regressions, including PostgreSQL tests | 304 passed |
| Reusable builder and public registry/media/link tests | 36 passed |
| Public TypeScript / ESLint / production build | PASS |
| Operations TypeScript / ESLint / production build | PASS |
| Docker Compose config, build/start, four healthy services | PASS |
| Alembic upgrade head | PASS; remains 0011_website_edit_sessions; no new migration |
| Editor at 1440 / 1024 / 768 | PASS |
| Home at 1440 / 1024 / 900 / 768 / 430 / 390 | PASS |
| Tours, Tour Detail, Plan, About, Contact at 1440 / 768 / 390 each | PASS |
| Public horizontal overflow / browser errors | None in the 21 page/device checks |
| Automated WCAG A/AA audit of sampled public/editor states | No reported violations |

Rendered screenshots were inspected for all public page/device combinations and desktop/iPad editor states. Black/gold, warm ivory, logo, public typography and rainforest/coast chapter separation remain intact. Six Featured Experiences and seven existing public tours rendered from the real API. The contact address is explicitly `info@volcanvacations.com` in both the default section and standalone contact-information widget.

The controlled Home workflow exercised section reorder, headline editing, adding/moving/duplicating/removing safe content, image replacement, alt text, cover/contain, overlay, visual and keyboard focal points, Tablet/Mobile media overrides, Undo/Redo, Save Draft and Preview. Actual pointer drags covered sections, columns, widget ordering and moving widgets between columns. Non-drag movement, column resizing and physical touch-target sizing were checked at 1024/768. All six page editors saved text/media drafts. Image + Text placement/mobile stacking and Full Width Media height/overlay were checked in the rendered canvas. Unreviewed media displayed a warning and disabled selection. The video safety contract was covered by reusable tests; no real video asset was added or playback acceptance claimed.

Production editor checks repeated handoff, Save Draft, private Preview and Exit at all three editor widths. A new handoff is redeemed before mounting editable state, preventing delayed reloads from discarding early edits. The draft proxy rejected a request without the required Origin. Public pages remained on defaults/published content after draft saves, with no editor controls or draft text. Owner scope, revoked/expired sessions and role denial are also covered by backend tests.

Keyboard navigation, labeled controls, focus, mobile navigation and reduced-motion behavior were checked alongside automated accessibility analysis. This is bounded validation, not an accessibility certification. `/request` and `/pay` rendered successfully; existing booking, availability and payment regressions passed in the backend suite. No PayPal transaction was initiated. Planning/Contact retain their existing disabled delivery state.

Browser authoring used isolated review accounts and a separate temporary SQLite database, with PayPal credentials explicitly blank. PostgreSQL persistence was tested by the backend regression suite. Public-origin checks preserved the configured Codespaces origins while forwarding browser transport to local services; API responses were real, not fixture substitutions. No customer or business records in the normal PostgreSQL database were edited by browser authoring. Temporary review servers were stopped after validation.

Part 3 publish, revision restore, stale-publish and full concurrency acceptance were not performed. No bulk ingestion, hotel/package inventory, public transportation booking, email, AI, Live PayPal or production media storage was added.
