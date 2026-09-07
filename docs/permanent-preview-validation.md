# Permanent preview preparation — validation

Date: 2026-09-07 UTC. Starting repository: clean working tree at `7a62a95` (`Audit legacy Volcan Vacations inventory and media`). The prior Sandbox acceptance and legacy audit were already committed and were preserved.

**Repository preparation is complete. Permanent provider acceptance is BLOCKED.** No Render/Vercel account connection or assigned provider URLs were available, no resources were created, and no Git commit/push was performed. Follow [cloud-deployment.md](cloud-deployment.md) for the provider handoff.

## Results

| Check | Status | Evidence / limits |
| --- | --- | --- |
| Public typecheck, lint, production build | PASS | Next.js 15.5.24; existing Node 20.20.2 container and isolated Node 22.23.2 container |
| Vercel-style build | PASS locally | `VERCEL=1`, HTTPS fixture API origin; no actual provider deployment |
| Invalid API build configuration | PASS | Missing, localhost and Codespaces API origins refused in Vercel mode |
| Browser bundle | PASS | Configured HTTPS API origin present; private configuration identifiers absent |
| Public assets/routes | PASS locally | Homepage, tours, booking request, `/pay`, real logo, local photography/font, homepage script assets respond |
| Backend tests | PASS | 121 passed, 1 skipped; final targeted deployment suite 18 passed |
| Sequential clean PostgreSQL migrations | PASS locally | All five actual revision IDs plus `head`; PostgreSQL 15; schema created only by Alembic |
| Empty-preview seed | PASS locally | 2 suppliers, 6 visibly labeled demo tours, 6 images; every other application table empty immediately after seed |
| Nonempty-preview seed refusal | PASS | Second seed run rejected; counts unchanged |
| Hosted API smoke | PASS locally | Health, inventory, CORS, booking, availability, payment session, restart persistence and booking idempotency |
| Operations API boundary | PASS | Preview and production app configurations omit every `/ops/*` route and exclude them from OpenAPI |
| Hosted payment-link origin | PASS | Absolute configured public HTTPS origin, fragment token; missing base URL refuses issuance before mutation |
| Render Blueprint | PASS locally | Checked against current official Render JSON schema; no resources created |
| Compose configuration | PASS | `docker compose config --quiet` to avoid resolving secrets into output |
| Four Codespace services | PASS | API, PostgreSQL, public web, Operations healthy |
| Development database preserved | PASS | Row-content fingerprints across all 13 application tables match before/after disposable validation |
| Vercel deployment | BLOCKED | Provider authorization/project creation and reviewed GitHub push needed |
| Render API deployment | BLOCKED | Provider authorization/service creation needed |
| Render PostgreSQL deployment | BLOCKED | Provider authorization and user-selected durable plan needed |
| Permanent API-backed tours | BLOCKED | Actual Vercel → Render → Render PostgreSQL URLs do not yet exist here |
| Booking on permanent preview | BLOCKED | Local smoke passed; provider acceptance not performed |
| Permanent Sandbox webhook/capture | BLOCKED | Actual API endpoint and registration required; current webhook unchanged |
| Codespace independence | BLOCKED for live proof | Configuration uses provider URLs, but no deployed permanent topology exists to verify |

Next.js reports its existing `next lint` deprecation notice. Backend warnings concern existing httpx TestClient and `datetime.utcnow()` deprecations. The skipped test is the explicit opt-in PostgreSQL capture/webhook concurrency test; providers in the ordinary suite are mocked. None of those tests proves real Sandbox checkout on the permanent preview.

The isolated Node 22 build did not change Codespaces' Node version or project dependencies. The initial Vercel-style test used the existing frontend build directory; a normal environment build restored the Codespaces API configuration afterward, and public script/static asset checks passed. Later compatibility builds used temporary directories. No app redesign, image substitution, or Operations frontend change occurred.

## Clean database evidence

The local validator used the complete repository revision names:

```text
0001_initial_schema
→ 0002_tour_inventory
→ 0003_booking_requests
→ 0004_availability_confirmation
→ 0005_paypal_payments
→ head
```

The validation tool was corrected during development to sort fingerprint rows by each table's actual primary key (including composite keys) and compare the full Alembic revision ID. Final results above reflect the corrected validator; historical migration files were never edited.

It created a uniquely named temporary database on local PostgreSQL, verified all 13 application tables were initially empty after migration, and ran only the controlled preview inventory seed. It then created one new synthetic validation customer/trip/reservation through HTTP, recorded synthetic availability and supplier confirmation through private domain services, issued a temporary payment link, restarted the temporary API, and verified the same request/reference and availability persisted. The payment session was Sandbox and checkout was disabled because provider credentials were cleared.

**Provider calls: 0. Payments created: 0. Webhook records created: 0.** The validation database was removed, and existing development data fingerprints remained identical. No Codespaces customers, Sandbox buyer data, completed payments, old bookings, or internal history were copied into a new database. No Render database has been provisioned or migrated yet.

## Security review

- `.env`, application `.env.local`, and API `.env` are ignored. No environment file was edited or staged.
- Current configured Sandbox client ID, client secret, and webhook ID values were checked against repository files and Git history; no matches. The local development database URL matches the intentionally documented example configuration, not a Render credential.
- Generated browser chunks were checked for `DATABASE_URL`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_WEBHOOK_ID`, and the live PayPal API host; none were present. The HTTPS fixture API origin was correctly inlined. The client-safe Sandbox app ID is obtained from the scoped backend session when enabled.
- Hosted routes do not expose Operations inventory, customers, costs, payment management, or booking management. Local development Operations remains available through the existing private Codespaces workflow. Authentication is still a launch blocker.
- Hosted CORS is an exact origin list, not `*` or a regex; credentialed Codespaces behavior remains development-only.
- `PAYPAL_ENVIRONMENT=sandbox` is explicit in the Blueprint, and hosted settings refuse live mode. Capture/signature-verification logic is unchanged.
- Tokens are generated by the existing payment-link service, retained in the URL fragment, and are not included in this report. The payment URL change only supplies the configured website origin.
- `EMAIL_FROM=info@volcanvacations.com` corrects the example/preview sender configuration; no email sending or DNS change was implemented.
- No Operations hosting, public custom domain, Hostinger DNS/email change, production-site change, paid infrastructure, or real inventory import occurred.

## Git and remaining work

Changed deployment/configuration/source files:

- `.env.example`, `README.md`
- `apps/web/next.config.mjs`
- `render.yaml`
- `services/api/alembic/env.py` (runner configuration, not historical migrations)
- `services/api/app/config.py`, `main.py`, `payment_service.py`, `seed_inventory.py`
- `docs/cloud-deployment.md`

New files:

- `services/api/tests/test_deployment.py`
- `services/api/scripts/validate_preview.py`
- `docs/permanent-preview-validation.md`

All changes remain uncommitted/unpushed. No lockfile, Docker configuration, historical migration, existing legacy-audit file, payment acceptance record, or public visual asset changed. `git diff --check` passed.

Next actions are provider account setup and a reviewed push, durable Render database selection, schema/seed execution, one Vercel project rooted at `apps/web`, actual origin configuration, and permanent acceptance including the Sandbox webhook. After that is healthy, proceed to real media batches and partner-verified inventory import under the existing migration plan.

**VV PERMANENT PREVIEW: NOT READY**
