# Coastal homepage expansion

## Story and scope

The homepage now follows: Costa Rica hero → Arenal / rainforest chapter → API-backed Featured Experiences → Why Volcan Vacations → trip planning → Pacific Coast → four coastal destinations → kinds of adventure → How It Works → Costa Rica Is Calling → existing footer.

The approved Arenal hero and continuous toucan/waterfall image remain. The rainforest chapter has its own heading and copy, with no Pacific content. Featured Experiences, benefits and planning form a substantial, continuous warm ivory interlude before the Pacific chapter. This separation remains in DOM order on mobile; there is no rainforest/beach split or blended image.

Featured cards still use `TourInventory` and API data, with the original request links. Cards receive a light treatment scoped to `.home-page`. No catalog, request, availability or payment behavior changes. Hero language now refers to exploring Costa Rica. The coast CTA targets the four discovery cards on the same page. The existing planning worksheet is still a preview; this task does not connect or replace it.

Coastal destinations are editorial discovery content, not Product inventory: Papagayo, Las Catalinas, Nosara and Tamarindo. Their slugs in `apps/web/lib/home-media.ts` represent geographical names conceptually; this task creates no Destination database records. No hotels or transportation appear in public navigation or as sellable inventory.

## Temporary imagery

All five images were generated with the built-in image_gen tool on 2026-09-08. They are conceptual Pacific Coast illustrations, **not verified documentary photographs of the named places or real VV properties**. No third-party hotel images are hotlinked. A short visible note identifies coastal imagery as illustrative; alt text also says illustrative. Full prompts are in `coastal-prompts.json`.

The original generated PNG files remain in `/home/node/.codex/generated_images/01a07302-8bc1-7682-bcbc-6fa99394746a/`. The project copies are WebP encodings, without compositing, recoloring or embedded typography. All generated originals are 1536 × 1024.

| Slot / project file under `apps/web/public/images/coast/` | Original PNG | Recommended real-media source | Crop guidance |
| --- | --- | --- | --- |
| `pacific-sunset-temporary.webp` | `exec-665513ee-2b2e-430e-83e7-f2526c80ae3e.png` | 2400 × 1500 or larger landscape; optional separate 1200 × 1000 mobile crop | Left copy area on desktop; mobile uses a clear 320px scenic opening above the copy, at 66% horizontal crop |
| `papagayo-temporary.webp` | `exec-9cda872d-b591-40f6-9de6-dbfdb6705a50.png` | At least 1200 × 1200 or generous 3:2 landscape | Central cove/headlands; desktop crops close to square |
| `las-catalinas-temporary.webp` | `exec-ade0b135-0834-4af7-b5ee-c8b1dcff9961.png` | At least 1200 × 1200 or generous 3:2 landscape | Central village/sea view, avoid clipping architectural subject |
| `nosara-temporary.webp` | `exec-40214800-dfa2-4312-b32b-8c0a236b836f.png` | At least 1200 × 1200 or generous 3:2 landscape | Beach/surf context; allow square and 1.3:1 crops |
| `tamarindo-temporary.webp` | `exec-184f8b28-29b7-428b-a8e4-b369c30cf2e6.png` | At least 1200 × 1200 or generous 3:2 landscape | Bay/sunset context, protect the horizon |

## Replace with real VV media

1. Select owned/licensed photos and record the real location, rights and any releases.
2. Export optimized WebP/AVIF assets, keeping sufficient crop room. Use new descriptive filenames and update the source/alt fields in `apps/web/lib/home-media.ts`; no component rewrite is required.
3. Replace illustrative alt text with accurate descriptions, and remove the illustrative note only after every coastal slot is real and verified.
4. Review 1440, 900 and 390px crops and text contrast. Keep critical subjects clear of the chapter's copy; do not put copy inside image files.

Images use Next Image responsive sizing and lazy loading below the fold. The existing hero retains priority. The Pacific chapter has independent `.home-pacific__media`, overlay, HTML copy and CTA layers. No video downloads or players are introduced. A future short muted, playsInline background video may replace the image in that media layer with a poster fallback, responsive object-fit, reduced-motion static fallback and accessible pause control. Audio must remain off; implement playback controls before enabling animation.

Future contracted hotel inventory could be inserted as a separate sibling section after coastal destinations and before adventure categories. No hotel placeholder or hotel functionality is implemented now.

## Validation — 2026-09-08

- Public and Operations: `npm run typecheck`, `npm run lint` and `npm run build` all passed. No Operations source changes.
- Docker: `docker compose config --quiet`, `docker compose up --build -d` passed. Postgres, API, web and Operations health checks passed after recreation; no database reset or schema change.
- Rendered Chromium review at **1440, 900 and 390px**: inspected every homepage chapter, final CTA and footer. No horizontal overflow or broken images. Four coastal cards render in four, two and one columns respectively. At 390px the coast has a visible scenic opening above the text. Arenal and Pacific are separated by about 1068, 1583 and 3693px of Featured Experiences, benefits and planning content respectively.
- Visual acceptance: brighter warm-light rhythm; black/gold interface with ivory contrast; distinct Arenal and Pacific chapters; Costa Rica-wide language; spacious cards and readable headings; six featured tours rendered from the actual API.
- Axe WCAG 2 A/AA and 2.1 AA checks found zero violations at all three widths. Keyboard checks passed for the skip link, mobile navigation and coast CTA. Ivory focus outlines and reduced-motion scrolling were checked. These automated checks complement visual review; they are not an exhaustive accessibility certification.
- Public routes `/`, `/tours`, `/plan-your-trip`, `/about`, `/contact`, `/request` and `/pay` returned HTTP 200 after the final rebuild. API health, six featured tours and Operations login also responded successfully.
- Browser regression: real featured-tour request links resolve to the matching tour and existing form; party size and traveler fields work. Featured empty/error states remain readable (simulated responses for those two states only). The invalid/expired payment-link page renders correctly. No browser booking submission or PayPal transaction was initiated.
- Existing focused backend suites for inventory, bookings, availability, payments, PostgreSQL payment concurrency and the PayPal adapter: **104 passed** (existing deprecation warnings). Provider calls in unit tests are mocked; this is not sandbox payment validation.
- `python scripts/validate_preview.py --confirm-isolated` passed: real API booking request, availability, public payment session, restart persistence and booking idempotency in a disposable validation database. Provider calls: **0**. The validation database was removed and the development database remained unchanged.

Review screenshots and command logs were written to `/tmp/vv-coastal-review/` in the development workspace, including `homepage-1440.png`, `homepage-900.png`, `homepage-390.png`, per-section captures and `visual-results.json`. These are local review artifacts, not deployed assets.
