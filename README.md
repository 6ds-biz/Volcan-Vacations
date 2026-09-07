# Volcan Vacations

Volcan Vacations is a Costa Rica travel platform foundation for tours, transportation, hotels, vacation packages, customers, trips, reservations, suppliers, and payments.

## Repository architecture

- `apps/web` - public customer-facing Next.js app
- `apps/ops` - internal operations Next.js app
- `services/api` - FastAPI, SQLAlchemy, and Alembic service
- `infrastructure` - infrastructure artifacts
- `docs` - architecture and deployment documentation

## Cloud-first development

GitHub is the source of truth and GitHub Codespaces is the development environment. The permanent preview target is Vercel for `apps/web` only, with FastAPI and PostgreSQL on Render. Operations deployment is blocked pending authentication; hosted APIs omit `/ops/*` routes. The existing `volcanvacations.com` site and Hostinger DNS remain untouched.

The Codespace includes Node.js 20, npm, Python 3.12, Git, Docker, and Docker Compose. On first creation it copies `.env.example` to the ignored `.env` file and configures Codespaces forwarded URLs.

1. On GitHub, open the private repository.
2. Select **Code**, then **Codespaces**, then **Create codespace on main**.
3. In the browser VS Code terminal, start the stack:

```bash
docker compose up --build
```

Open the forwarded ports from the **Ports** panel:

- `3000` - public web
- `3001` - operations
- `8000` - API
- `8000/health` - API health check

Stop the stack with `docker compose down`.

## Local development

Docker remains the preferred, cross-platform development path:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

The local URLs are:

- http://localhost:3000
- http://localhost:3001
- http://localhost:8000
- http://localhost:8000/health

Docker Compose overrides the API database host to `postgres` on the container network. The root `.env` uses `localhost` so Python and Alembic commands run from the host can connect through port `5432`.

## Environment configuration

`.env.example` is the safe template. Never commit `.env` or provider secrets.

- `NEXT_PUBLIC_API_URL` - browser-visible FastAPI base URL; use `http://localhost:8000` locally and the Render URL in Vercel
- `DATABASE_URL` - PostgreSQL connection URL used by FastAPI, SQLAlchemy, and Alembic
- `ALLOWED_ORIGINS` - comma-separated public and operations frontend origins
- `ALLOWED_ORIGIN_REGEX` - optional CORS regex, normally left blank in favor of explicit origins
- `ENVIRONMENT` - `development`, `preview`, or `production`
- `PAYPAL_ENVIRONMENT=sandbox`, `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_CURRENCY=USD`, `PAYPAL_WEBHOOK_ID` - backend sandbox checkout configuration; see [Milestone 5](docs/milestone-5.md)
- `EMAIL_FROM` - future transactional email placeholder only

Values prefixed with `NEXT_PUBLIC_` are exposed to the browser and must never contain secrets.

## Run components without Docker

Install and run each frontend independently:

```powershell
Set-Location apps/web
npm install
npm run dev

Set-Location ../ops
npm install
npm run dev
```

Install the API in a Python 3.12 virtual environment:

```powershell
Set-Location services/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Database migrations

Milestone 5 extends the existing Payment model with reservation-scoped sandbox PayPal checkout, private payment links, capture/webhook reconciliation, and Operations payment visibility. See [the payment guide](docs/milestone-5.md) and [validation report](docs/milestone-5-validation.md). Live payment calls are blocked. Real sandbox acceptance requires configured sandbox credentials and a verified webhook.

Milestone 4 adds manual tour/date availability, supplier contact/confirmation history, and derived payment readiness. See [the availability and supplier workflow guide](docs/milestone-4.md). Milestone 5 builds on those prerequisites; automated supplier communications remain deferred.

Milestone 3 connects public tour requests to customer/traveler/trip/reservation records and the Operations booking inbox. See [the booking workflow guide](docs/milestone-3.md) for lifecycle, financial snapshots, idempotency, demo seed, and security boundaries. Its original follow-up transitions are extended by Milestone 4.

Milestone 2 adds Operations-managed supplier/tour inventory and image galleries. See [the inventory guide](docs/milestone-2.md) for API contracts, the explicit demo seed, tests, and acceptance instructions. **Operations and `/ops/*` APIs are unauthenticated development-only interfaces; protect both before production use.**

Alembic owns schema creation; the application does not call `create_all()`.

```powershell
docker compose up -d postgres
Set-Location services/api
alembic upgrade head
```

`alembic/env.py` reads the same `DATABASE_URL` used by the API. For Render, run `alembic upgrade head` through a private Render Shell or the documented restricted external procedure before testing inventory. A paid Render service can use this as its reviewed pre-deploy command. The initial preview seed requires an empty database and `ENVIRONMENT=preview`; it does not copy development bookings or payments.

## Validation

```powershell
Set-Location apps/web
npm install
npm run build

Set-Location ../ops
npm install
npm run build

Set-Location ../../services/api
pip install -r requirements.txt
python -c "from app.main import app; print('FastAPI import OK')"

Set-Location ../..
docker compose config
```

## Git and private GitHub repository

This repository is already initialized locally. For a new copy without Git metadata, run `git init`, review `git status --short`, and confirm no secrets are staged. When the private GitHub repository URL is available:

```powershell
git add .
git status --short
git commit -m "Establish Volcan Vacations platform foundation"
git branch -M main
git remote add origin <PRIVATE_GITHUB_REPOSITORY_URL>
git push -u origin main
```

Do not replace the placeholder with a guessed URL. Create the GitHub repository as **Private** and do not initialize it with another README, `.gitignore`, or license.

## Deployment

```text
apps/web     -> Vercel project (Root Directory: apps/web)
apps/ops     -> Vercel project (Root Directory: apps/ops)
services/api -> Render web service
PostgreSQL   -> Render PostgreSQL
Hostinger    -> domain registration and DNS
```

See [docs/cloud-deployment.md](docs/cloud-deployment.md) for the exact preview deployment, environment, migration, and acceptance workflow. Provider deployment is separate from local repository validation; domain cutover is not part of this task.
