> Part 1 foundation record. The current editing workflow is documented in [Public visual editor — Part 2](public-vv-editor.md). The Part 1 read-only canvas described below has been extended using the same secure handoff.

# VV public Page Builder — Part 1 foundation

The primary VV consumer is now **apps/web**. Operations is the authenticated management entry, not a layout-editing canvas. This corrects the first consumer integration; it does not rebuild the reusable package.

## Scope and entry

An active `owner_admin` opens **Website → Pages** or **Website → Media** in Operations. Pages shows published/source-default state, draft state, last publication and actor. Edit opens the public-site canvas; Preview opens the customer route; Revisions shows private revision metadata. The Part 1 canvas is an inert, authenticated preview of the draft or fallback. Full visual editing/media UX is Part 2. Publish/restore controls and their final acceptance are Part 3.

Operations Edit Page buttons, operational canvas adapters, widgets and their copied imagery are retired. The approved pre-builder operational components remain in use. Legacy `/ops/page-layouts/*` endpoints are not registered in the application. Historical layout/revision records are retained, never rolled back or deleted. Legacy persistence tests use a test-only route harness.

The core package remains unchanged: Page → Section → Column → Widget, responsive presentation, accessible controls, drag/drop, schema, registry, runtime, editor, history, import/export, media abstraction and safe video support remain available for Part 2 and other 6DS consumers.

## Pages and source defaults

| Key | Customer route | Default composition |
| --- | --- | --- |
| home | `/` | Costa Rica Hero, Arenal, Featured Experiences, Why VV, Trip Planning, Pacific Coast, Coastal Destinations, Kinds of Adventure, How It Works, Final CTA |
| tours | `/tours` | Hero, API-backed tour grid, CTA |
| tour-detail | `/tours/[slug]` | Shared template populated by the requested active public tour |
| plan-your-trip | `/plan-your-trip` | Existing hero and planning content/form preview |
| about | `/about` | Existing hero, story, values, CTA |
| contact | `/contact` | Existing hero, contact content/form preview |

The repository did not previously have a tour-detail route. The new shared template consumes the existing public detail and availability APIs. It does not create per-product layouts or change the request workflow.

The original JSX was extracted into source-controlled blocks, preserving photography, typography, black/gold/ivory styling, navigation and global footer. Default renderer wrappers use `display: contents` so their boxes do not alter the existing layout. Arenal and Pacific photography remain separated by Featured Experiences, benefits and planning. Customized layouts use the existing section/column responsive grid.

No publication, unavailable API, invalid schema or invalid published media resolves to the known-valid default. Inventory loading/error behavior remains owned by the inventory component. Only active public records populate detail pages. Page metadata is preserved; tour detail adds a canonical route and metadata from public inventory. Content is server-rendered; editor pages are noindex with a no-referrer policy.

## Widget registry and boundaries

The registry lives in `apps/web/lib/website/registry.ts`; the independent API validator is `services/api/app/website/schema.py`. Both restrict widgets by page type and reject unknown configuration.

Basic widgets: Heading, Text, Divider, Spacer, Image/Media, Image + Text, Full Width Media, Button. Homepage widgets cover each chapter above. Tours supports Hero, Grid, Category Intro, Destination Intro and CTA. Tour Detail supports Hero, Overview, Description, Price/Request, Duration/Details, Included, Bring, Gallery, Availability, Destination, Related Tours and CTA. Planning, About and Contact register their existing content/form composites plus the requested standalone building blocks.

Layouts contain presentation only. A tour slug selects the existing public API record; the runtime injects that allowlisted record into `tour` context. Required context is checked before rendering tour widgets. Layout JSON cannot contain prices, supplier IDs/costs, availability truth, customer data, form actions, scripts, arbitrary CSS or custom font uploads. Inventory widgets may set editorial copy and an integer item limit of 1–12. Business widgets cannot be duplicated. Existing planning/contact forms remain disabled previews; this foundation does not activate delivery. Availability wraps the existing read endpoint, and Request CTA uses the existing request route.

Approved public tokens: black, charcoal, warm ivory, white, transparent; gold/light gold; display, heading, subheading, body, small and script; none, small, medium, large and XL spacing. The core's structural `base/panel/accent` surfaces map to black/charcoal/ivory. Editorial widgets expose the named public tokens without changing core schema.

## Owner handoff and authorization

Owner authorization is enforced by FastAPI, not dashboard profile or hidden links. Partner, Staff and visitors cannot read management data or save/publish/restore layouts. Writes retain existing session, Origin and CSRF checks.

1. Owner POSTs `/ops/website/pages/{key}/edit-session` using the existing Ops session and CSRF token.
2. API creates a cryptographically random, single-use ticket. Only its SHA-256 digest is stored; it expires in 60 seconds and is scoped to one page and the originating internal login session.
3. Operations navigates to `${PUBLIC_WEB_URL}/website-editor/{key}#ticket=…`. The fragment is not sent in HTTP requests. The browser immediately clears it, including when an earlier canvas cookie already exists.
4. The same-origin Next.js `/api/website-editor/session` route checks Origin, exchanges the ticket server-to-server, and sets an HttpOnly, SameSite=Strict cookie. Secure is set on HTTPS. The browser never receives the replacement canvas secret in JSON.
5. The canvas credential expires 15 minutes after issuance, is limited to reading that page, and cannot authenticate to Operations. Every backend canvas request rechecks the parent session, account activity, exact Owner role and password-change state. Logout/session revocation invalidates the handoff and canvas.

No query flag authorizes editing. No internal session credential is shared between applications. Keep `PUBLIC_WEB_URL` and `OPS_WEB_URL` set to the exact deployment origins. `WEBSITE_API_URL` is a server-only API address (`http://api:8000` inside Compose), never a public credential. Production relies on HTTPS and the existing authenticated Operations deployment.

## Persistence

Migration `0010_page_builder` and its tables are unchanged. Generic keys `public-home`, `public-tours`, etc. keep public layouts separate from historical operational templates. Drafts, immutable revisions, optimistic versions, row locks, authenticated audit actors and restore-as-new semantics are reused.

New forward migration **0011_website_edit_sessions** creates only scoped handoff/session state. It references the originating user/session, stores digests and expiry timestamps, and adds no business-data fields.

Management routes: `/ops/website/pages`, `/media`, `/pages/{key}`, `/pages/{key}/draft`, `/publish`, `/revisions`, `/restore`, `/edit-session`. Draft writes and existing publication services are wired for later parts; there is no Part 1 publishing UI. Public `/public/website/pages/{key}` returns only validated published presentation or `page: null`; no drafts, revisions, actor IDs or internal timestamps. These validators cannot infer whether an Owner typed sensitive information into ordinary editorial prose; Owners must use public copy only.

## Media foundation

`services/api/app/website/media.py` adapts the existing catalog; `apps/web/lib/website/media.ts` implements the reusable MediaProvider contract. Approved local generated coastal illustrations retain their existing paths and provenance (`docs/public-homepage/coastal-media.md`). No external assets were imported. Existing Arenal and active ProductImage entries without asset-level rights evidence remain `NEEDS_RIGHTS_REVIEW`; their existing source-default use is not treated as a new rights approval.

Management metadata includes reference, filename, type, known dimensions, alt, source, provenance, rights and tags, with extension fields for destination, tour, orientation, duplicate hash, recommended use and photographer. Public responses contain only approved media and the renderer's required safe metadata. Publishing checks every media reference, including responsive overrides and posters; it rejects unreviewed assets. Missing or disallowed media produces the existing safe placeholder.

Image configuration preserves stable references, alt/decorative state, cover/contain, focal points, overlays and responsive overrides. The core video contract requires muted autoplay and retains controls. No video storage/transcoding or autoplay audio is introduced. Real-media ingestion will feed reviewed metadata and stable references into this provider; bulk ingestion and production storage are deferred.

## Runtime separation and future reuse

Normal visitors load the core/runtime, public widgets and validated published layout. They do not import editor panels, drag/drop UI, undo/redo, media management or revision controls. Owner canvas code lives on its separate route. Full production-bundle acceptance is Part 3.

Future destination, Transportation, Hotels and Packages pages can register new page keys/defaults and public context adapters. None are implemented here. Other 6DS applications can supply their own registries, source defaults, authorization and media/persistence adapters while retaining the core.

## Validation

Validated on 2026-09-08. Implementation/build/backend checks completed before the Codespace interruption; final rendered/public-origin and isolated workflow checks resumed from the existing changes afterward. No implementation was restarted.

| Check | Result |
| --- | --- |
| Backend regressions, including real PostgreSQL locking/immutable-revision tests | 283 passed |
| Unchanged reusable core tests | 22 passed |
| Public consumer tests | 11 passed |
| Operations canvas-retirement/navigation test | 1 passed |
| Public TypeScript / ESLint / production build | PASS / PASS / PASS |
| Operations TypeScript / ESLint / production build | PASS / PASS / PASS |
| Compose config and `up --build -d` | PASS |
| API, PostgreSQL, public web, Operations | All healthy, rechecked after interruption |
| Alembic upgrade/current | PASS, `0011_website_edit_sessions` head |
| Public homepage at 1440 / 900 / 390 | Visually inspected, no horizontal overflow |
| Homepage WCAG A/AA automated scan at all three widths | No violations |
| Public routes `/`, `/tours`, `/plan-your-trip`, `/about`, `/contact`, `/request`, `/pay` | PASS |
| Active shared tour detail, existing availability API, unknown-tour 404 | PASS |
| API-backed tours | Six featured cards; seven active public tours |
| Operations role/device/appearance/task matrix | 66 passing checks; no page errors |
| Website Media automated WCAG A/AA scan | No violations |
| Owner handoff, repeat entry, HttpOnly/Strict cookie, revision metadata | PASS |
| Partner/Staff Website denial | PASS |
| Public request → supplier contact → availability → confirmation | PASS, isolated data |
| Ready payment page and snapshot amount | PASS, $85.00 isolated reservation; no checkout initiated |
| Invalid payment token | Expected invalid/expired message |
| Private About draft in Owner canvas, unchanged public fallback | PASS |
| PayPal/provider calls during workflow review | Zero |
| Core package and migrations 0001–0010 unchanged | Confirmed |
| Git whitespace check | PASS |

The browser visited the configured Codespaces public/API origins with local transport routing to the running services. API response bodies and CORS headers were preserved; no inventory responses or CORS approval were mocked. Six featured experiences rendered at each reviewed width. The direct localhost check separately exercised the existing inventory error state caused by its different origin. This is a local rendered/public-origin validation, not a claim that external GitHub private-port authentication was tested.

Owner, Partner and Staff routes were reviewed at 1440, 900 and 390 pixels. Permitted dashboard, bookings, tasks, suppliers, availability, payments, Transportation and Users routes rendered without overflow or former Edit Page controls. Light, Dark and System preferences were exercised for all three roles; System followed both simulated color schemes. Each role created and completed a task. Management writes used a separate temporary SQLite database, generated test accounts and explicitly blank PayPal credentials; normal PostgreSQL business records were not modified by those reviews. Existing PostgreSQL-specific behavior was covered by the backend regression suite.

The final browser workflow submitted the existing public request form, recorded supplier events through the existing authenticated API, verified persistent confirmed readiness in Operations, generated a local secure payment link, and viewed the customer page without creating an order. A draft-only About layout was saved through the Owner API, rendered in the scoped canvas, and remained absent from the public route. No publish, restore or stale-publish acceptance sequence was performed.

Browser sizes are emulation, not physical hardware. Automated accessibility results supplement the visual review; they are not a complete accessibility certification. The intentional unknown-tour 404 generated its expected browser resource warning. No application JavaScript errors were observed in the successful checks.

Reproduce the code checks from the repository root:

```sh
docker compose exec api sh -c 'pip install -r requirements-dev.txt && VV_TEST_POSTGRES=1 python -m pytest -q'
docker compose exec web sh -c 'npm run typecheck && npm run lint && npm run build'
docker compose exec web sh -c 'NODE_PATH=/repo/apps/web/node_modules node --test tests/*.cjs /repo/packages/page-builder/tests/*.cjs'
docker compose exec ops sh -c 'npm run typecheck && npm run lint && npm run build'
docker compose exec ops node --test tests/website-management.test.cjs
docker compose config --quiet
docker compose up --build -d
docker compose ps
docker compose exec api alembic upgrade head
```

Web now builds from the repository root and runs in `/repo/apps/web`; Operations again builds from `apps/ops` and runs in `/app`. Only disposable web/ops dependencies and build output may need refreshing after package changes (`docker compose up -d --no-deps --renew-anon-volumes web ops`). Never remove the PostgreSQL named volume.

Part 2 full editor/media UX and Part 3 publication/revision acceptance remain deferred. No live payment, Hotels, Packages, public Transportation, email, AI or production media storage was added.
