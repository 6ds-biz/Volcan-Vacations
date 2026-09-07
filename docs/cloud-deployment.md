# Permanent provider preview: Vercel + Render

The repository is prepared for this topology. **Provider deployment and permanent acceptance are still blocked on account access, a reviewed GitHub push, and database plan selection. No provider URLs have been created by this task.** See [validation results](permanent-preview-validation.md).

```text
GitHub: 6ds-biz/Volcan-Vacations
  ├── Vercel: apps/web → HTTPS *.vercel.app
  └── Render: services/api → HTTPS *.onrender.com
                └── separate Render PostgreSQL
```

**Operations deployment blocked pending authentication.** Do not create a Vercel/Render project for `apps/ops`. With `ENVIRONMENT=preview` or `production`, the API does not mount any `/ops/*` routes, including suppliers, costs, bookings, availability mutations, or payment-link issuance. CORS is not authentication. Do not set the hosted API to `development` to restore those routes.

The existing `volcanvacations.com` website remains production. Do not add its domain to either provider, change Hostinger DNS/email records, deploy redirects, or retire the old hosting. Keep Docker and private Codespaces ports for development. Preview bookings must use synthetic identities; current prices are demo data, not approved offers. No transactional email is enabled; `info@volcanvacations.com` remains the canonical customer email.

## Provider choices and account handoff

No authenticated Render/Vercel integration, CLI session, project link, or provider token was available during preparation. Connect the existing GitHub repository through the providers' dashboards; do not paste secrets into chat. Do not create another GitHub repository or rewrite/rename branches as part of setup.

The optional root `render.yaml` describes a **free bootstrap**, not a durable database commitment. Render's free PostgreSQL expires after 30 days and has no backups. Its free API service sleeps after 15 minutes of inactivity and may take about a minute to wake. A lasting preview requires a user-approved paid PostgreSQL plan; choose paid API compute too if cold starts are unacceptable. No paid resources have been created. Review the current provider estimate before confirming a paid plan. [Render free limitations](https://render.com/docs/free)

The ordered manual setup below supports choosing plans in the dashboard. Alternatively, use **Render → New → Blueprint → connect this repository → review `render.yaml`**. Select/approve a durable database plan before treating it as permanent. The Blueprint disables automatic API deploys for deliberate migration review. It contains no Operations service and no secret values. Keep database and API in the same Render region. PostgreSQL major version **15** matches the validated development version.

## Required configuration

### Vercel — public project only

| Setting | Value |
| --- | --- |
| Repository | Existing `6ds-biz/Volcan-Vacations`, reviewed deployment branch |
| Root Directory | `apps/web` |
| Framework Preset | Next.js |
| Node.js | `22.x`; select explicitly in Build and Deployment settings. Existing Node 20 Docker/Codespaces support is preserved. |
| Install Command | `npm ci` using the committed `apps/web/package-lock.json` |
| Build Command | `npm run build` |
| Output Directory | Framework default; do not override or set `out` |
| Required environment variable | `NEXT_PUBLIC_API_URL=https://<actual-render-api-host>` |

Set `NEXT_PUBLIC_API_URL` in **both Preview and Production** environment scopes. Here Vercel's “Production” scope means the project's stable `*.vercel.app` alias; it does not authorize a VV domain cutover. Changing this variable requires a new build/deploy. The Vercel build refuses missing, non-HTTPS, localhost, or Codespaces API origins. Normal root-directory settings suffice; no `vercel.json` is needed. [Vercel monorepos](https://vercel.com/docs/monorepos), [Node versions](https://vercel.com/docs/functions/runtimes/node-js/node-js-versions), [Next.js public environment variables](https://nextjs.org/docs/app/guides/environment-variables)

**No separate PayPal environment variable is required on Vercel.** The token-scoped API session returns the public Sandbox client ID when checkout is available. Never put `PAYPAL_CLIENT_SECRET`, `PAYPAL_WEBHOOK_ID`, or `DATABASE_URL` in Vercel settings or browser code. No Vercel-to-database connection exists.

The real logo is `public/branding/volcan-vacations-logo.png`; current imagery and the local font are also committed inside `apps/web/public`. Next.js handles local scenic images; database tour photos use ordinary `<img>` elements and existing fallback behavior. Seed `/images/*.webp` paths resolve against the **Vercel website**, not the API. No remote-image allowlist or filesystem upload directory is required for current inventory. Any future remote image must be HTTPS and independently reachable.

### Render — API configuration

| Variable | Setting / scope |
| --- | --- |
| `ENVIRONMENT` | `preview`; disables every unauthenticated Operations route |
| `DATABASE_URL` | Render database **Internal Database URL** for the API, secret; Blueprint uses `fromDatabase.connectionString` |
| `ALLOWED_ORIGINS` | Initially empty; then exact Vercel HTTPS origin(s), comma-separated, without paths/trailing slashes |
| `ALLOWED_ORIGIN_REGEX` | Empty; hosted configurations reject regex origins |
| `PUBLIC_WEB_URL` | Initially empty; then the stable Vercel HTTPS origin, without a path |
| `PAYPAL_ENVIRONMENT` | `sandbox` only |
| `PAYPAL_CLIENT_ID` | Existing Sandbox app client ID, supplied in Render configuration |
| `PAYPAL_CLIENT_SECRET` | Existing Sandbox app secret, supplied through Render secret configuration |
| `PAYPAL_CURRENCY` | `USD` |
| `PAYPAL_WEBHOOK_ID` | The ID registered for the actual permanent endpoint; leave unset until registered |
| `EMAIL_FROM` | `info@volcanvacations.com`; no delivery is enabled |
| `PYTHON_VERSION` | Blueprint's Python 3.12 pin |
| `PORT` | Assigned by Render; consumed by the start command |

`API_PORT` is retained for local Docker support; Render uses `PORT`. No `.env` file is necessary on Render. `postgres://` connection strings normalize to `postgresql://`; Alembic preserves percent-encoded password characters. The API reads/writes PostgreSQL only; it does not depend on a Codespaces mount, local SQLite database, media directory, or startup seed.

The Blueprint deliberately omits `PAYPAL_WEBHOOK_ID` during bootstrap because the endpoint cannot be registered until Render assigns the API URL. Add that secret in the API's Render Environment settings after registration; no placeholder ID is needed to start the service.

Empty CORS origins allow bootstrap health checks while denying browser cross-origin access. Hosted settings reject wildcard origins, regexes, non-HTTPS website URLs, Codespaces URLs, non-PostgreSQL databases, and live PayPal mode. Configure the stable Vercel alias rather than granting `*.vercel.app`. If you intentionally test a branch deployment, add that **exact** deployment origin explicitly and remove it when finished.

`PUBLIC_WEB_URL` controls newly issued customer links: `https://<actual-vercel-host>/pay#token=...`. The existing response field is named `path`; it contains the absolute URL when configured. Development keeps its relative-link behavior when unset. Hosted issuance fails before changing the booking if the base URL is absent. Tokens stay in the fragment and are sent to the API in the Authorization header. Do not put secure customer links in logs, screenshots, or committed acceptance reports.

## Exact deployment sequence

1. **Publish reviewed work to the existing GitHub repository.** Inspect `git status --short` and `git diff`; commit only reviewed deployment changes, then push the current intended branch. Nothing was automatically committed or pushed by this task. Confirm no `.env` file is staged.
2. **Render → New → Postgres.** Choose a new database for the preview, PostgreSQL 15, and the intended region. Choose and approve a durable plan. Do not restore a Codespaces dump. Keep external access disabled unless using the restricted external migration procedure below.
3. **Render → New → Web Service → connect the existing GitHub repo.** Select Python, Root Directory `services/api`, Build Command `pip install -r requirements.txt`, Start Command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, Health Check Path `/health`. Set the API environment above and the database's internal URL. Leave CORS and public website URL empty until Vercel assigns an origin. Deploy; record the actual assigned `https://…onrender.com` URL privately in deployment notes. `/health` can pass before migrations; inventory acceptance cannot.
4. **Run `alembic upgrade head` against the new Render database** using one of the private methods below. Run `alembic current`; expect `0006_platform_foundation (head)`. Never use `create_all()`, modify old migrations, or run a downgrade. On a paid API service, use `alembic upgrade head` as the reviewed pre-deploy command for future schema changes. [Render deploy commands](https://render.com/docs/deploys)
5. **Seed safe inventory once:** `python -m app.seed_inventory --confirm-demo --preview`, with `ENVIRONMENT=preview`. This requires every application table to be empty and inserts only **two demo suppliers, six visibly labeled demo tours, and six image references**. It creates no customers, travelers, trips, reservations, availability, payments, or webhook history. A second preview run refuses instead of overwriting records. Do not run `seed_bookings`, copy development data, or import the unverified legacy catalog.
6. **Verify Render directly.** `/health` must return `{"status":"ok","service":"volcan-vacations-api"}`; `/public/tours` must return six labeled demo tours with image references and no supplier costs. `/ops/bookings`, `/ops/suppliers`, and `/ops/payments` must return 404. Restart the API and confirm the same inventory remains.
7. **Vercel → Add New → Project → import this GitHub repo.** Create **one** public project, Root Directory `apps/web`, Next.js preset, and the build settings above. Do not import Operations.
8. **Set `NEXT_PUBLIC_API_URL`** to the actual Render HTTPS API origin for both Preview and Production, then deploy. Record the stable assigned `*.vercel.app` URL; no custom domain is needed.
9. **Render → API → Environment.** Set `ALLOWED_ORIGINS` to that exact Vercel origin and `PUBLIC_WEB_URL` to the same stable origin. Keep `ALLOWED_ORIGIN_REGEX` empty. If using the Blueprint, manage these values consistently: its bootstrap empty defaults must not overwrite configured origins on a later Blueprint sync.
10. **Save/redeploy Render; redeploy Vercel whenever its build-time variable changes.** Confirm direct Render health, expected CORS headers from the actual Vercel origin, and a rejected unlisted origin. Keep auto-deploy off until the initial acceptance is reviewed.
11. **Verify the public website and persistence** using the acceptance checklist below. Booking acceptance requires synthetic preview identities, not previous Sandbox buyers. A healthy static homepage alone does not prove the database connection works.
12. **PayPal Developer Dashboard → Apps & Credentials → Sandbox → the existing Sandbox app → Webhooks.** Only after the actual Render URL exists, register/update the Sandbox endpoint to `https://<actual-render-api-host>/webhooks/paypal`. Configure that endpoint's Webhook ID in Render, save/redeploy, and retain signature verification. Do not guess an endpoint or reuse an ID for a different registration. Preserve the current development webhook until the new registration is verified where the dashboard supports separate registrations. No webhook was changed during this task.
13. **Retest Sandbox checkout on the permanent preview** with a newly reviewed synthetic preview booking after supplier confirmation and private link issuance. Use the Sandbox buyer approval flow; never live credentials. Verify capture persistence, actual signed webhook delivery, reload, and already-captured retry protection. This preparation task created no new PayPal order or charge. Record only masked evidence.

## Private migration and seed execution

Prefer **Render API → Shell** on a paid service. The shell inherits the internal `DATABASE_URL` and `ENVIRONMENT=preview`. From the API root run:

```bash
alembic upgrade head
alembic current
python -m app.seed_inventory --confirm-demo --preview
```

Render free services do not provide Shell or one-off jobs. For a free bootstrap API, use a temporary local shell with the database **External Database URL** and a narrowly scoped database IP allowlist entry. Render's default Blueprint blocks all external database connections. Temporarily add only the operator's current public IP `/32` in **Database → Networking**, then remove it when finished. Never allow `0.0.0.0/0` just to simplify migration. [Render free service capabilities](https://render.com/docs/free)

In a Codespace terminal (not a chat message), use this subshell. It prompts with hidden input, supplies secrets through process environment/stdin, uses the existing API container's installed dependencies, and leaves the running development API's environment unchanged:

```bash
(
  set +x
  read -rsp 'Render external DATABASE_URL (with sslmode=require): ' VV_RENDER_DATABASE_URL
  echo
  case "$VV_RENDER_DATABASE_URL" in
    *sslmode=require*) ;;
    *) echo 'Use the provider external URL with sslmode=require.'; exit 1 ;;
  esac
  export VV_RENDER_DATABASE_URL
  python3 - <<'PY' | docker compose exec -T api python -c '
import json, os, subprocess, sys
config = json.load(sys.stdin)
env = dict(os.environ, DATABASE_URL=config["database_url"], ENVIRONMENT="preview",
           ALLOWED_ORIGINS="", ALLOWED_ORIGIN_REGEX="", PUBLIC_WEB_URL="",
           PAYPAL_ENVIRONMENT="sandbox", PAYPAL_CLIENT_ID="", PAYPAL_CLIENT_SECRET="", PAYPAL_WEBHOOK_ID="")
for command in (["alembic", "upgrade", "head"], ["alembic", "current"],
                [sys.executable, "-m", "app.seed_inventory", "--confirm-demo", "--preview"]):
    result = subprocess.run(command, env=env, capture_output=True)
    if result.returncode:
        sys.exit("Deployment command failed; inspect privately without sharing credentials. Remaining commands were not run.")
    print("Completed: " + " ".join(command))
'
import json, os
print(json.dumps({"database_url": os.environ["VV_RENDER_DATABASE_URL"]}))
PY
)
```

This is an **initial empty-preview** procedure, not a recurring seed job. Review the target Render database before entering its URL. For future deployments, run reviewed migrations only; do not repeat the initial seed. The local disposable-database validator described below is separate and cannot target Render.

## Acceptance without public Operations

Record actual deployment URLs, Git revision, UTC time, expected result, and PASS/FAIL for each item. Provider HTTPS and account access must be checked on the real URLs; local tests do not substitute for them.

| Check | Required evidence |
| --- | --- |
| Homepage and static assets | Vercel `/`, About, Contact, and planning pages load; real logo, local font and photography render |
| Tours | `/tours` requests the actual Render `/public/tours`; six labeled demo tours and their photos appear |
| Booking | `/request?tour=whitewater-rafting` submits a synthetic request and displays a VV reference; use the app's generated link if the query contract changes |
| Persistence | Through private DB access, match that reference to exactly one trip/reservation/customer; restart Render and verify it remains; repeat an identical request key only if deliberately testing idempotency |
| Availability | Public `GET /public/tours/{slug}/availability?date=YYYY-MM-DD` works; a private operator can use existing `save_availability` service with the preview DB, then verify the public status changes |
| Payment page | `/pay` without a token displays its invalid-link state; an eligible synthetic booking's private link loads the correct Sandbox session on Vercel |
| Private API boundary | `/ops/*` absent from OpenAPI and returns 404; no supplier costs/private contacts in public tour responses |
| Webhook and capture | Real Sandbox buyer approval plus actual signed webhook on Render; one capture; reload/retry preserves received status |
| Codespace independence | Browser requests use only Vercel, Render, static/media and PayPal hosts; repeat from a separate browser after disconnecting from Codespaces; do not stop/destroy development services just for this check |

For synthetic preview supplier confirmation/link issuance, use an authenticated Render Shell or private administrative process with the preview DB environment and the existing domain services (`record_supplier_event`, `issue_link`), never a public `/ops` endpoint. Match the exact preview booking reference, confirm it is a synthetic demo, use its current `version`, and retain the returned secure link privately. Do not assume a booked request is supplier-confirmed. Normal Operations UI workflow remains blocked until authentication is implemented; the local Operations app is not authorized to bypass that boundary on Render.

The provider acceptance booking, availability change, and future Sandbox capture are intentional **new preview test records**. They are not copied from Codespaces and must not be represented as real reservations or approved retail inventory. This task's automated smoke test uses a disposable local database instead and performs no provider calls.

## Reproducible repository validation

```bash
docker compose exec -T web sh -c 'npm run typecheck && npm run lint && npm run build'
docker compose exec -T -e DATABASE_URL=sqlite:// -e ENVIRONMENT=development -e PUBLIC_WEB_URL= -e PAYPAL_CLIENT_ID= -e PAYPAL_CLIENT_SECRET= -e PAYPAL_WEBHOOK_ID= api python -m pytest -q
docker compose exec -T api python scripts/validate_preview.py --confirm-isolated
docker compose config --quiet
docker compose ps
```

The PostgreSQL validator allows only a local development database host, creates a cryptographically named separate database, runs `0001 → 0002 → 0003 → 0004 → 0005 → 0006 → head`, checks an empty schema, runs the preview-only seed, tests HTTP routing/CORS/bookings/availability/payment-session rendering data and restart persistence, then removes only its own database. Before/after fingerprints confirm the existing development application tables are unchanged. It neither invokes `create_all()` nor calls PayPal. It requires the development PostgreSQL role's database-creation permission.

The ordinary backend suite uses existing isolated test fixtures with mocked providers; its opt-in concurrency test is skipped unless requested separately. It is not real Sandbox acceptance.

## Next after a healthy permanent preview

Follow [the legacy migration plan](legacy-migration/migration-plan.md): obtain partner-approved suppliers, current retail/net prices, pickup/policies and disputed tour details; batch-ingest original user photos/videos using generated identifiers, duplicate checks, categories and rights review; review an inactive real-inventory import dry run; then execute an explicitly approved controlled import. No real catalog import, email setup, Operations deployment, live PayPal change, or domain cutover belongs to this preview task.
