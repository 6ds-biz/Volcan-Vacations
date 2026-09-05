# Homepage refinement review

Reviewed against the approved black/gold Costa Rica reference on 2026-09-05.

## Homepage

Cinematic Arenal hero → up to six featured API tours → four compact benefits → continuous toucan/planning/waterfall/Arenal story → four photographic experience categories → four request-based planning steps → sunset CTA → restrained footer. The desktop homepage is intentionally longer and uses generous spacing between ideas. No articles, testimonials, fabricated reviews, hotels, transport, packages, or additional feature grids were added.

## Header

72px desktop/tablet header and 66px mobile header. Desktop Plan My Trip CTA is 150 × 42px. The exact original gold logo mask, source PNG, aspect ratio, and tagline are preserved. Source SHA-256 remains `8d094931f098a36b59836a6fad86b8a496e60b10df0873819c2456b1ab68cfad`. The existing native disclosure menu and keyboard focus treatment remain available.

## Toucan / waterfall transition

One image spans both planning and destination sections, with black/charcoal gradients only at the outer edges and behind text. Neither content section has a background panel, border, or horizontal divider. Native picture art direction selects a tall portrait version on mobile to keep wildlife and waterfall visible together. Local generated assets, provenance, and exact prompts are documented in `VISUAL-ASSETS.md`.

## API tours and environment

The initial `/public/tours?featured=true` request returned HTTP 500 because the fresh local PostgreSQL database had no `products` table. Applied the existing Alembic migrations through `0003_booking_requests`, then ran the existing insert-only development seed (`python -m app.seed_inventory --confirm-demo`). Six demo tours and two demo suppliers were initialized; no existing records were overwritten.

The configured, dynamically generated Codespaces API URL returned HTTP 200. No source/configuration URL changes were necessary. Featured cards still use the real public API response, including ProductImage URLs and retail prices. Difficulty is shown when present, otherwise the API category; no audience claims or supplier costs are invented. The professional error state and retry remain intact. The development-content disclosure is retained.

The forwarded web port redirects an unauthenticated browser to GitHub sign-in. Review therefore sends **web transport only** to the local Compose service using Playwright `route.fetch`, retaining the configured browser origin. API calls go directly to the real forwarded API, including actual browser CORS and credentials handling. No inventory responses are mocked, no temporary URL is hardcoded in application code, and port visibility is unchanged.

## Responsive and interaction review

Chromium screenshots and assertions at 1440px, 900px, and 390px cover header/logo, hero, live tour grids, seamless central scenery, categories, process, final CTA, and footer. Desktop uses six compact tour columns and four category columns; tablet uses three tour columns and two category columns; mobile preserves the narrative with readable full-width cards and vertically ordered steps.

Verified no horizontal overflow, decoded images, one H1, four categories, four process steps, keyboard skip link, native mobile navigation, visible focus styling, reduced-motion behavior, and no JavaScript page errors. All six API records match rendered names/prices and selected-tour request links. Clicking a featured CTA loads the matching live tour in `/request`. An intentionally aborted API call shows the professional error state; removing that failure and clicking Try again reloads real inventory.

Review script and screenshots for this Codespace session: `/tmp/vv-homepage-review/`.

## Validation

- PASS — Public TypeScript (`npm run typecheck`).
- PASS — Public ESLint (`npm run lint`, no warnings/errors).
- PASS — Public production build (`npm run build`).
- PASS — Operations TypeScript.
- PASS — Operations ESLint (no warnings/errors).
- PASS — Operations production build.
- PASS — Docker Compose configuration and `docker compose up --build -d`.
- PASS — postgres, api, web, and ops healthy.
- PASS — HTTP 200 for `/`, `/tours`, `/plan-your-trip`, `/about`, `/contact`, `/request`, and `/request?tour=whitewater-rafting`.
- PASS — Featured-tour API rendering, retail prices, imagery, selected-tour request navigation, error state, and retry.

The npm checks run from each app's working directory inside its Compose container because host `node_modules` directories are root-owned. No dependency versions or lockfiles were changed. Next's existing `next lint` command emits its deprecation notice. The final public image refresh renews only web's anonymous dependency/build volumes to avoid serving stale Next output; the named PostgreSQL volume is preserved.

## Scope and git

Only public frontend source, local imagery, and review documentation changed. API business logic, schema definitions/migration files, booking submission, customers, travelers, trips, reservations, Operations code/styling, supplier/tour management, and deployment configuration remain unchanged. No Milestone 4 features or external communications were added. Changes remain uncommitted and unpushed.
