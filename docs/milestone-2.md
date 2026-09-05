# Milestone 2: database-backed tour inventory

## Data and migration

`0002_tour_inventory` extends `0001_initial_schema` without modifying the original migration. Supplier gains website and private notes. Product remains the inventory entity (`product_type = "tour"`); it gains a unique slug, customer content, category, duration, publishing flags, location, difficulty, and minimum age. Existing product rows receive `legacy-product-{id}` slugs and safe defaults. Money remains `NUMERIC(12,2)` / Python Decimal. Gross margin is calculated, not stored. JSON money fields are decimal strings; send `"85.00"`, not a floating-point number. The Operations margin preview uses integer cents.

ProductImage stores URL, alt text, order, primary flag, and timestamps. A partial unique index allows at most one primary per product. Gallery mutations lock the parent product row; a nonempty gallery always retains one primary. First image becomes primary automatically. Selecting a new primary clears the old one atomically. Removing the primary promotes the first remaining image. Ordering is `(sort_order, id)`; duplicate order numbers are deterministic. Images are always checked against the owning tour.

```bash
docker compose exec api alembic upgrade head
```

No database drop, reset, or startup seed is required. A migration constraint failure on invalid pre-existing prices must be investigated, not solved by deleting records.

## APIs

- Public: `GET /public/tours` (`category` and `featured` optional), `GET /public/tours/{slug}`. Only active Products of type tour. No supplier object/contact information, supplier cost, or margin. Explicit response models allowlist public fields; they do not serialize arbitrary ORM dictionaries. See [FastAPI response-model filtering](https://fastapi.tiangolo.com/tutorial/response-model/).
- Internal suppliers: `GET/POST /ops/suppliers`, `GET/PUT /ops/suppliers/{id}`.
- Internal tours: `GET/POST /ops/tours`, `GET/PUT /ops/tours/{id}`. Includes supplier, cost and calculated gross margin.
- Internal galleries: `GET/POST /ops/tours/{id}/images`, `PUT/DELETE /ops/tours/{id}/images/{image_id}`.
- `GET /` and `GET /health` are preserved.

PUT replaces editable fields; clients should send the complete editor payload. Slug conflicts return 409; missing entities/foreign image ownership return 404; invalid input returns 422. Supplier/tour removal is active/inactive, not hard delete. Supplier inactive is an internal status, not an implicit bulk unpublish operation: deactivate its individual tours when required. Responses use `Cache-Control: no-store`.

## Operations and public integration

Operations includes `/suppliers`, `/suppliers/new`, `/suppliers/{id}`, `/tours`, `/tours/new`, and `/tours/{id}`. Forms manage the specified fields, Decimal pricing, publishing, alt text, URL references, ordering, and primary selection. Save tour basics first, then manage its gallery. No full CMS, file upload pipeline, or booking features were added.

Both applications use `NEXT_PUBLIC_API_URL`. Public inventory is loaded in the browser with no-store fetches: homepage requests active featured tours; `/tours` requests active tours and derives category buttons from that inventory. Reload/revisit a public page after saving in Operations to see current data; no rebuild is needed. Existing card styling, scenic hero art, logo, navigation, and contact inquiry links are preserved. API failure and empty inventory show helpful messages; no hardcoded fallback tours are presented as live data. This milestone does not add server-rendered tour SEO/detail pages.

## Development images and production storage

Use HTTPS URLs to approved externally hosted raster photos, or existing public-site paths such as `/images/rafting.webp`. HTTP is permitted for development. The API validates URL schemes and never downloads supplied URLs. Browsers load content images directly, not through an unrestricted server-side image proxy. Missing/broken photos have a neutral placeholder.

The seed references the existing generated, illustrative WebP files shipped with the public website. Operations resolves these demo paths to port 3000 in local/Codespaces development. For another public hostname, configure `NEXT_PUBLIC_WEB_URL` in Operations at build time, or use absolute HTTPS image URLs. Keep image origins trustworthy; remote hosts see image requests. Use persistent object storage/CDN URLs and an authenticated upload/validation pipeline before introducing production uploads. Do not use Vercel/Render ephemeral local files as uploaded-image storage. No paid storage resources were created. Removing an image deletes only its database reference, not the source file.

## Explicit demo seed

```bash
docker compose exec api python -m app.seed_inventory --confirm-demo
```

Refuses environments other than `development`. Insert-only by tour slug and demo supplier name; rerunning skips existing tours and does not overwrite Operations edits. Never runs automatically. Creates DEMO Arenal Adventures and DEMO Costa Rica Experiences, plus Whitewater Rafting, Arenal Volcano Hike, Hot Springs Experience, Wildlife & Hanging Bridges, Waterfall Adventure, and Coffee & Chocolate Tour. All six are active/featured development samples. Rafting uses $85 retail / $50 cost / $35 gross margin; these are not current production quotes. Public preview notes and tour descriptions disclose demo status. Retire/review demo data before a production launch.

## Security boundary — NOT production-secure

Authentication is intentionally deferred. `/ops/*` APIs and Operations expose private supplier contacts, costs, and write actions to anyone who can reach them. CORS and `noindex` are not access controls. Keep the Codespace/API ports private and put both the Operations frontend **and the `/ops` API routes** behind a trusted access boundary before public production use. Protecting only the frontend is insufficient. Do not make the entire API port public to work around Codespaces login/CORS problems. No custom authentication, customer login, payments, reservations, availability, or production object storage was implemented.

Codespaces API fetches include GitHub's private-port session cookies for `.app.github.dev` origins only. Open the forwarded API URL and sign into GitHub if it redirects to login; keep all three forwarded origins in `ALLOWED_ORIGINS`. This is existing infrastructure access, not Operations authentication. Other origins omit credentials.

## Tests and validation commands

```bash
cd services/api
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
cd ../../apps/web
npm run typecheck && npm run lint && npm run build
cd ../ops
npm run typecheck && npm run lint && npm run build
cd ../..
docker compose config --quiet
docker compose up --build -d
docker compose exec api alembic upgrade head
docker compose ps
```

Backend tests override the DB dependency with isolated SQLite memory databases; the real forward migration and acceptance test must also run against Compose PostgreSQL. Test-only dependencies are not added to the production image. Existing dependency datetime/TestClient deprecation warnings do not indicate failing assertions.

Compose's existing anonymous `.next` volumes can retain previous frontend builds. Refresh only disposable frontend build/dependency volumes after rebuilding if needed:

```bash
docker compose up -d --no-deps --force-recreate --renew-anon-volumes web ops
```

Do not remove the named Postgres volume.

`scripts/milestone2-e2e.cjs` is an explicit development browser acceptance test using Playwright (install test tooling separately; not an app runtime dependency). Set `VV_E2E_CONFIRM_DEMO=yes`; optional `VV_E2E_WEB_URL`, `VV_E2E_OPS_URL`, `VV_E2E_API_URL` default to localhost ports. It creates labeled DEMO records through Operations, verifies publication/privacy, and deactivates only those test records afterward. It retains recoverable test audit data and does not delete suppliers/tours. `VV_E2E_OUTPUT` selects a screenshot folder (default `/tmp/vv-m2-review`).

In a Codespace whose forwarded origins require GitHub login, `VV_E2E_LOCAL_TRANSPORT=1` routes those exact configured origins to the corresponding local running containers in Playwright. It uses real HTML/API/database responses, not mocked inventory, and does not alter forwarding permissions. Empty/unavailable state tests are separately and explicitly simulated. This validates the application stack, not GitHub's forwarding authentication.
