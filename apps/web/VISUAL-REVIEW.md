# Public visual redesign review

Reviewed 2026-09-05 against the production Compose web service on local port 3000.

## Validation

- PASS: `npm exec -- tsc --noEmit --incremental false` (no typecheck script exists).
- PASS: `npm run lint` (no warnings/errors; existing Next lint command emits a deprecation notice).
- PASS: public `npm run build`.
- PASS: Operations `npm run build`.
- PASS: `docker compose config --quiet` and `docker compose up --build -d`.
- PASS: postgres, api, web, and ops all healthy.
- PASS: `/`, `/tours`, `/plan-your-trip`, `/about`, `/contact` return HTTP 200.
- PASS: Chromium review of all five pages at 1440px, 900px, and 390px. No horizontal overflow, broken images, or JavaScript page errors; one H1 and preserved page title per route.
- PASS: mobile menu opens, skip link receives keyboard focus, questionnaire radio/checkbox selections work, name input accepts text. Preview submission remains disabled.

Screenshots were inspected for hero text, image crops, navigation, card layouts, form labels and selected controls. The final pass uses the production server. Screenshots are in `/tmp/vv-visual-review/screenshots/` for this Codespace session.

The authenticated forwarded URL returned HTTP 401 to the automated browser environment. Review used local port 3000 serving the same Compose application; forwarding permissions were not changed.

Compose's pre-existing anonymous `.next` volume retains old build output after an image rebuild. The public service was refreshed with `docker compose up -d --force-recreate --renew-anon-volumes web`. No database volume was removed or altered.

## Approved logo completion

The header and footer now use the approved `public/branding/volcan-vacations-logo.png` through the same CSS alpha mask. The PNG is unchanged (SHA-256 verified before and after). Its full 11944 × 1154 geometry, spacing, volcano/cloud mark, and transparency supply the mask, filled with exactly `#D7A84B`. `contain`, no-repeat, and the original aspect ratio prevent cropping or distortion. The separate existing header tagline remains in `#E8C675`. No other design elements were changed in this branding pass.

All build/configuration checks above were rerun successfully after the logo replacement. Only the public web image/container was rebuilt/refreshed; all four services are healthy. All five public routes again returned HTTP 200 at 1440px, 900px, and 390px, with no horizontal overflow, broken images, or page errors. Form-control selections, keyboard skip-link focus, and mobile navigation passed again.

Additional logo assertions passed at 320, 390, 600, 768, 900, 1000, 1001, 1200, 1440, and 1920px: both logos use the exact source mask and gold fill, retain aspect ratio within browser subpixel rounding, remain inside their containers, and do not overlap navigation. Desktop/mobile header and footer screenshots were visually inspected for crisp edges and an unclipped volcano/cloud mark on dark backgrounds. The home links retain their accessible name and minimum 44px height.

Focused checks: `/tmp/vv-visual-review/logo-review.cjs`; screenshots: `/tmp/vv-visual-review/screenshots/logo-{header,footer}-{320,390,1440}.png` (2× device pixel ratio). Initial repeated-navigation browser checks timed out; the successful final pass uses a fresh page for each viewport. See `VISUAL-ASSETS.md` for source and treatment details.

## Scope

Only `apps/web` source/assets/documentation changed. Tour inventory data, form fields, metadata, API environment configuration, Operations source, FastAPI, PostgreSQL/Alembic, and deployment configuration remain unchanged. No payments, authentication, bookings, data persistence, or messaging were added. Changes remain uncommitted and unpushed.
