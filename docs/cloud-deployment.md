# Cloud deployment

## Intended workflow

```text
Developer
   |
GitHub Codespace
   |
Private GitHub repository
   |
   +-- Vercel / apps/web
   +-- Vercel / apps/ops
   +-- Render / services/api
                     |
                     v
               Render PostgreSQL
```

Hostinger remains the registrar and DNS provider for `volcanvacations.com`. No domain transfer is required.

## 1. Publish the private GitHub repository

Create an empty private GitHub repository without generated starter files. From the reviewed local repository:

```powershell
git add .
git status --short
git commit -m "Establish Volcan Vacations platform foundation"
git branch -M main
git remote add origin <PRIVATE_GITHUB_REPOSITORY_URL>
git push -u origin main
```

Before committing, confirm that `.env`, `.env.local`, virtual environments, build directories, and `node_modules` are not staged. Package lockfiles should be staged.

## 2. Open a Codespace

On GitHub, select **Code > Codespaces > Create codespace on main**. The configuration in `.devcontainer/devcontainer.json` installs Node.js 20, npm, Python 3.12, Git, Docker, and Docker Compose and forwards ports `3000`, `3001`, and `8000`.

The post-create script creates the ignored `.env` if needed. In Codespaces it also derives the HTTPS forwarded-port URLs for `NEXT_PUBLIC_API_URL` and `ALLOWED_ORIGINS`. Start all components with:

```bash
docker compose up --build
```

Use the Codespaces **Ports** panel to open the public web, operations app, and API. The ports are private by default and are not production deployments.

## 3. Create the Render preview

The root `render.yaml` is an optional Blueprint for a free preview API and free preview PostgreSQL database. Nothing is created until a user explicitly connects the repository and applies the Blueprint in Render.

Blueprint service settings:

| Setting | Value |
| --- | --- |
| Service type | Web service |
| Runtime | Python |
| Root directory | `services/api` |
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health check | `/health` |
| Database | `DATABASE_URL` from Render PostgreSQL |
| CORS | `ALLOWED_ORIGINS` entered during Blueprint creation |

For the first preview, set `ALLOWED_ORIGINS` to the two Vercel preview origins after Vercel assigns them. Add the production domains later as a comma-separated list:

```text
https://volcanvacations.com,https://www.volcanvacations.com,https://ops.volcanvacations.com
```

The Blueprint intentionally does not include a pre-deploy command because Render pre-deploy commands require a paid web-service plan. Before the first API deploy, set the Render database's external connection URL only for the current Codespace shell and run:

```bash
cd services/api
read -rsp "Render DATABASE_URL: " DATABASE_URL && export DATABASE_URL
echo
alembic upgrade head
unset DATABASE_URL
```

Do not save that URL in the repository or shell history. A Codespaces secret is another safe option. On a paid Render service, configure `alembic upgrade head` as the pre-deploy command so a failed migration stops the deploy.

Free Render PostgreSQL is suitable only for an initial preview: it currently expires after 30 days and has no backups. Select a durable plan before storing production or customer data.

## 4. Create two Vercel projects

Import the same private GitHub repository twice. Vercel does not need a `vercel.json` for this layout.

| Project | Public web | Operations |
| --- | --- | --- |
| Root Directory | `apps/web` | `apps/ops` |
| Framework Preset | Next.js | Next.js |
| Install Command | default (`npm install`) | default (`npm install`) |
| Build Command | default (`npm run build`) | default (`npm run build`) |
| Output Directory | default (`.next`) | default (`.next`) |
| Environment Variable | `NEXT_PUBLIC_API_URL=https://<render-api-host>` | `NEXT_PUBLIC_API_URL=https://<render-api-host>` |

Set `NEXT_PUBLIC_API_URL` for Preview and Production. It is inlined at build time, so redeploy after changing it. It is public configuration, never a secret.

After both preview deployments exist, update Render's `ALLOWED_ORIGINS` with their exact `https://...vercel.app` origins and redeploy the API. Verify `/health` before testing either frontend.

## 5. Keep DNS at Hostinger

The future routing is:

```text
volcanvacations.com     -> Vercel public web project
www.volcanvacations.com -> Vercel public web project
ops.volcanvacations.com -> Vercel operations project
api.volcanvacations.com -> Render FastAPI service
```

Add each domain to its Vercel or Render project first. Then copy the exact DNS records displayed by that provider into Hostinger's DNS editor. Do not guess A, CNAME, or verification records; providers can issue account- and project-specific values.

After DNS and certificates are active:

1. Set both Vercel projects' `NEXT_PUBLIC_API_URL` to `https://api.volcanvacations.com` and redeploy.
2. Set Render `ALLOWED_ORIGINS` to the three exact website origins shown above and redeploy.
3. Verify the apex, `www`, `ops`, API root, and `/health` over HTTPS.

## 6. First online preview checklist

1. Review and commit the repository, rename the branch to `main`, and push to an empty private GitHub repository.
2. Create a Codespace and verify `docker compose up --build`.
3. Import `render.yaml` in Render, review the free-resource limitations, and enter `ALLOWED_ORIGINS` when prompted.
4. Run `alembic upgrade head` against the Render database without storing its external URL in Git.
5. Create the two Vercel projects with root directories `apps/web` and `apps/ops`.
6. Set each Vercel project's `NEXT_PUBLIC_API_URL` to the Render API URL and deploy.
7. Add the two Vercel preview origins to Render CORS and verify all three services.

DNS changes can wait until previews are healthy.
