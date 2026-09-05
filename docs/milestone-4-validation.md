# Milestone 4 validation — 2026-09-05

## Database and preservation — PASS

Forward revision `0004_availability_confirmation` applied successfully to the existing PostgreSQL database with `docker compose exec api alembic upgrade head`. Repeating the command succeeded as a no-op. `alembic check` reported no new upgrade operations/model drift.

The migration extends existing Availability and Reservation, and adds SupplierConfirmationEvent. Availability gained source, notes, last check, version, product/date uniqueness, status/capacity checks and an index. Reservation gained a fulfillment supplier snapshot, separate availability/supplier states, reference, contact/confirmation timestamps, response notes and version. Events retain supplier contact method/operator/time, response/reference, alternative details, resulting states, command deduplication and insertion time.

Preflight found 2 suppliers and 6 products, with no existing availability, customer/traveler/trip/reservation/payment rows and no duplicate or invalid availability records. The named PostgreSQL volume was retained. No database recreation, reset, historical migration edit, or deletion was performed. Backend tests separately verify that legacy generic confirmations do not become payment-ready without supplier verification.

The working tree started clean at `7c3b9f0` (`Finalize VV black and gold visual system`). Hash checks passed for migrations 0001–0003, homepage CSS/page, all photograph assets and the real VV logo. `git diff --quiet -- apps/web docker-compose.yml` passed: the public implementation and deployment configuration remain unchanged.

## Availability and supplier workflow — PASS

The backend suite validates unknown/available/limited/unavailable/closed; optional capacities and remaining-capacity constraints; date uniqueness; checked time/freshness; date/range/tour/supplier/status filters; and an explicit safe public availability response. Missing/stale dates return unknown publicly, with request_required true. Internal stale warnings use a 24-hour threshold.

Supplier contact records awaiting_supplier and pending_supplier while preserving independently known request availability. Confirmation records available/confirmed/confirmed and derives payment readiness. Decline records unavailable/declined/contacted and leaves the trip open. Alternatives preserve original dates/tour/pricing and remain in history. Correcting a supplier confirmation requires explanation; conflicting state edits are rejected. Terminal reservations allow history notes only.

Reservation and event changes commit atomically, including rollback on a simulated event insert failure. Version checks prevent stale actions. Commands use UUID/hash deduplication, including identical retries with server-assigned event times. Original confirmation references remain in history after a corrective action. No payments or supplier messages are sent.

## Backend tests — PASS

**66 passed**: 11 Milestone 2 inventory cases, 23 Milestone 3 booking cases, 32 Milestone 4 cases (including parameterized validations). The prior generic-confirmation test was deliberately updated to require the dedicated supplier-confirmation action; its existing booking, trip, note, and privacy assertions remain.

Command: `docker compose exec -T api python -m pytest -q` after installing the existing `requirements-dev.txt` in the development API container. Existing httpx TestClient and datetime.utcnow deprecation warnings remain; no test failures. A preliminary bare `pytest` invocation lacked the module path; the documented `python -m pytest` command passed.

## Builds and running services

| Check | Result |
| --- | --- |
| Public TypeScript | PASS |
| Public ESLint | PASS; no ESLint warnings/errors |
| Public production build | PASS |
| Operations TypeScript | PASS |
| Operations ESLint | PASS; no ESLint warnings/errors |
| Operations production build | PASS |
| Docker Compose configuration | PASS |
| `docker compose up --build -d` | PASS |
| PostgreSQL/API/web/ops health | PASS; all four healthy |
| Alembic upgrade and model drift check | PASS |
| Existing six public routes | PASS at 1440/900/390px |
| Existing public booking request flow | PASS through the browser |
| `git diff --check` | PASS |

## Browser acceptance

`scripts/milestone4-e2e.cjs` exercises real public requests and Operations against the running API/PostgreSQL. The script creates clearly named DEMO inventory and `.invalid` contacts, then cancels only its own bookings/trips and deactivates only its own tour/supplier. Supplier/availability audit records are retained. No existing tour is repurposed for test cleanup.

Final rebuilt-stack acceptance run: **PASS**. Confirmed path reference `VV-260905-1E5DC794283F` (booking 5); declined/alternative path `VV-260905-F476AB73351B` (booking 6). All browser page-error and horizontal-overflow assertions passed. Editing a date to a 48-hour-old check produced the stale warning and public Unknown; rechecking restored the fresh date status.

Both paths have passed:

1. Mobile visitor selects Request This Tour, submits a request and receives the original safe receipt. Operations inbox/detail show Unknown and Not Requested. Record WhatsApp supplier contact, then observe Awaiting Supplier and the timeline. Add general tour/date availability through the tour editor link; independently mark this reservation available. Record supplier confirmation with a reference. Refresh and verify Confirmed, retained reference/history, and Ready for Payment.
2. Submit another public request on another date. Record supplier contact and decline. Verify Unavailable, Needs Attention/Alternative Needed, and an inquiry trip. Offer another date/time/tour option. Refresh and verify history while original tour/date/time/prices/trip remain unchanged. Default Needs Attention inbox includes the alternative request and excludes the confirmed request.

Actual concurrent PostgreSQL requests verify that two different commands using one version produce one success and one 409; simultaneous identical commands produce one event and matching responses. Public receipt replays remain unchanged. Public tour/date/receipt output hides costs, supplier contacts/notes, internal timestamps, references and history. Public booking/customer lookup remains unavailable.

Codespaces forwarding requires GitHub sign-in. Browser validation retains configured forwarded origins but routes transport to the real local services (`VV_E2E_LOCAL_TRANSPORT=1`). API/data responses are not mocked, port visibility is unchanged, and this is not a GitHub login test. Chromium required the approved process-sandbox escalation. An initial acceptance selector used an exact match for a wrapping select label; fixing the selector allowed the run to pass.

Screenshots and machine-readable acceptance results are in `/tmp/vv-m4-review/`. Homepage captures at 1440, 900 and 390 pixels were visually inspected: black/gold structural UI and colorful photography are preserved. Operations availability/detail/inbox/dashboard captures were inspected. A narrow-cell wrapping issue in the new availability table was corrected with a wider scrollable table and nonwrapping compact table badges. The browser overflow check caught an overly broad no-wrap rule on the payment-readiness paragraph; that rule was scoped to table badges so mobile detail text wraps. Public CSS was untouched.

## Security, deferred scope and Git

**Operations UI and `/ops/*` APIs remain unauthenticated and are NOT production-safe.** Authentication must protect both before production. Operator identifiers are self-reported. No custom authentication, public production exposure, or automatic communication was added.

Payments/PayPal/cards/deposits/refunds, automatic email/WhatsApp/SMS, accounts/authentication, supplier integrations, hotels/transport/packages, accounting/AI and production object storage remain deferred. Changes are **uncommitted and unpushed**; no history rewrite or unrelated work was discarded.

Next recommended narrow milestone: **Payment readiness + PayPal checkout**. It has not been started.
