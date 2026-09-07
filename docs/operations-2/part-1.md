# Operations 2.0 — Part 1

Internal users and customer identities are separate. Migration `0007_internal_users_tasks` adds users, hashed opaque sessions, persistent login throttles, tasks and append-only audit history, plus nullable booking assignees and supplier-event actors. Migrations 0001–0006 and historical rows are unchanged.

## Authentication and deployment

Passwords use Argon2id through `argon2-cffi`, with rehash on successful login. New passwords require 15–128 characters. No default account or password is seeded. Owner-created users must change their temporary password before accessing business APIs. Password change requires the current password and revokes every session.

Sessions use 256-bit random opaque tokens; only SHA-256 token hashes are persisted. Cookies are HttpOnly, SameSite=Strict, host-only and Secure outside local development. Sessions expire absolutely after `OPS_SESSION_HOURS` (default 8, range 1–24). Each request reloads the active user and current permissions. Logout deletes the server session. Changing a user's role, profile, or active state revokes their sessions.

Operations browser requests go through `/api/ops/*` on the same Next.js origin. Its fixed server-only `OPS_API_URL` points to FastAPI; it cannot proxy arbitrary destinations. The public website does not use this proxy. Protected page layouts validate sessions with FastAPI before rendering. All internal API routes enforce authentication and centralized capabilities independently of the UI.

Every write, including login, validates the exact Operations Origin. Authenticated writes additionally require a session-bound synchronizer CSRF token from `/ops/auth/me`. Cross-site forms are rejected; the proxy accepts JSON writes only. Validation responses do not echo credentials. Responses use `Cache-Control: no-store`. Login limits are persisted across workers: 8 failures per account and 80 attempts per proxy peer in 15 minutes. The peer limit intentionally applies across the BFF; adjust only after measuring legitimate internal use. No untrusted forwarded IP is used for security decisions.

Development allows localhost:3001 and explicitly configured Codespaces Operations origins. Hosted environments keep `/ops/*` disabled unless `OPS_ENABLED=true`, with an exact HTTPS `OPS_WEB_URL`. This task does not authorize a public deployment. Configure the Ops server's `OPS_API_URL`, `OPS_ENVIRONMENT` and the API's environment explicitly; HTTPS, private infrastructure/network controls and managed host secrets still require deployment verification. Never use development environment settings on a hosted installation.

## First owner

On the trusted host with API database access, run:

```bash
docker compose exec api python -m app.bootstrap_owner
```

Enter the email, display name and password at the prompts. Password input is hidden and is not passed as a command-line argument or environment variable. The command refuses if an active owner already exists. Store the credential in your password manager. It does not print a password or create a customer. Existing owners create users through the authenticated owner-only API, sharing temporary credentials through an approved secure channel. Email invitations and password recovery email are deferred; an operator with trusted database access must handle emergency recovery through a controlled, audited process.

## Roles and profiles

`app/permissions.py` defines capabilities and route policies; unknown routes fail closed. Owner has business, finance, approval, user and security access. Operations Partner has business, inventory, supplier follow-up and payment operations access, but cannot administer users or approve commercial agreements. Staff only see assigned tasks and explicitly assigned/relevant bookings through `/ops/work/*` safe projections, and may record follow-up notes or availability checks. A booking task in an active status grants relevant-booking access; completing/cancelling that task ends that relevance unless there is another active assignment. Staff cannot confirm suppliers, access company-wide payments/pricing, or administer users.

Owner, Operations and Staff **dashboard profiles affect emphasis only**. Authorization always derives from role. An Owner profile on a staff account grants no extra access. Only an owner can assign profiles. Last-active-owner removal/demotion is rejected, including concurrent updates under a PostgreSQL table lock.

## Tasks

`/ops/tasks` supports list/detail/create/update. Update takes `expected_version`, preventing silent overwrites; assignee, status, due date and other editable fields use the same command. Filters: mine, shared, assigned user, status, priority, overdue, UTC due date, relationship and search. Open work is `open`, `in_progress` or `waiting`; `completed` records completion time and actor; `cancelled` retains history without implying booking cancellation. Reopening clears completion fields while audit history remains.

Sources are manual or system_generated. Priorities are low, normal, high and urgent. Related entities are validated. Owner exception tasks live in an owner-only queue; other shared work is visible to Operations managers. Staff can manage their own tasks, cannot delegate or relink them, and cannot retrieve owner-queue work. Assigning a booking task explicitly grants relevant-booking visibility, so managers should include only appropriate details.

Four reliable transaction-bound system rules:

- New booking → Review booking and check availability.
- Supplier decline → Contact customer with alternative.
- Failed payment → Review payment issue (owner queue).
- Agreement enters in_review → Review vendor rates (owner queue).

Unique event keys and conflict-safe insertion prevent duplicates, including retries and completed-task replays. Operational tasks prefer active Operations Partners; owner exceptions prefer active owners. Among eligible users, choose the fewest open tasks then ID; missing eligible users leave shared work in the appropriate queue. This is a best-effort load balance, not a scheduling guarantee under simultaneous unrelated events. There is no historical backfill or automatic cancellation. Time-driven agreement expiration and supplier follow-up tasks are deferred until a scheduler and business intervals are agreed.

## Audit and boundaries

Authenticated booking changes, supplier confirmation, tasks, users, suppliers, availability and agreements append sanitized actor-linked history. Existing supplier events gain nullable actor IDs; old anonymous/operator labels remain valid. Audit stores event summaries, not credentials, full provider payloads or copied internal notes. Business history is not rewritten. No delete/update audit API is exposed. Database administrators remain trusted.

Public tours, booking intake, safe availability, secure payment sessions and verified PayPal webhooks remain publicly accessible as designed. All existing server-side PayPal eligibility, snapshots and idempotency protections remain. No new PayPal order/capture is needed to validate Operations authentication.

## References

[Argon2-cffi API](https://argon2-cffi.readthedocs.io/en/stable/api.html), [OWASP session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [OWASP CSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html).
