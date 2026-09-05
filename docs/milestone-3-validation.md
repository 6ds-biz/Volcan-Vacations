# Milestone 3 validation — 2026-09-05

## Scope and preservation

Implemented booking-request intake and Operations follow-up on top of the existing Milestone 2 worktree. Initial `git status --short` and `git log --oneline -5` were inspected before edits; HEAD was `fa5fa51`. Pre-existing uncommitted Milestone 2 changes were preserved. No reset, database recreation, commit, push, or deployment change was performed. The approved logo and imagery were retained. Migrations `0001_initial_schema` and `0002_tour_inventory` were not edited.

## Database and backend

- `0003_booking_requests` successfully applied to the existing PostgreSQL database with `docker compose exec api alembic upgrade head`. A subsequent upgrade was a successful no-op.
- `alembic check` reported no new upgrade operations/model drift.
- Existing Customer, Traveler, Trip, and Reservation models were extended; explicit TripTraveler associations were added. Price/cost remain Decimal/NUMERIC snapshots, not floating-point values.
- Backend suite: **34 passed** (11 inventory cases and 23 booking cases, including parametrized validations). Covers atomic rollback, customer reuse, participant relationships, active-tour restrictions, safe public receipts, historical pricing, idempotency, reference-collision retry, Operations reads/updates, and controlled/stale status changes.
- Existing dependency deprecation warnings remain (httpx TestClient integration and datetime.utcnow); no test failures.

## Builds and running services

| Check | Result |
| --- | --- |
| Public `npm run typecheck` | PASS |
| Public `npm run lint` | PASS; no ESLint warnings/errors |
| Public `npm run build` | PASS |
| Operations `npm run typecheck` | PASS |
| Operations `npm run lint` | PASS; no ESLint warnings/errors |
| Operations `npm run build` | PASS |
| `docker compose config --quiet` | PASS |
| `docker compose up --build -d` | PASS |
| postgres / api / web / ops | All four healthy |
| Alembic upgrade | PASS; head `0003_booking_requests` |
| Public route HTTP checks | All six HTTP 200 |
| `git diff --check` | PASS |

Public routes checked: `/`, `/tours`, `/plan-your-trip`, `/about`, `/contact`, and `/request?tour={test-slug}`. Desktop (1440px) and mobile (390px) checks found no horizontal document overflow. Screenshots of the request form/success and Operations detail/inbox were captured; request and detail layouts were visually inspected. An interrupted duplicate host public build was rerun successfully. Existing anonymous frontend build volumes were refreshed to serve the new builds; the named PostgreSQL volume was retained.

## Real browser acceptance

`scripts/milestone3-e2e.cjs` completed successfully twice against running web, ops, API, and PostgreSQL services. Final run reference: **VV-260905-24B1267A9B38** (booking/customer/trip ID 6).

Verified:

1. Open Tours and choose an active test-owned tour using “Request This Tour”; selected experience carries into the form.
2. Required-field validation blocks an incomplete submission without an API request.
3. Enter contact, requested date/time, two named travelers (one with DOB), optional trip dates, and customer notes on mobile.
4. Submit once, receive a VV reference and Request Received screen, with no payment action.
5. Read the persisted customer, both trip-associated travelers, inquiry trip, and new reservation through Operations.
6. Verify $85 retail / $50 supplier cost per person, quantity 2, $170 retail total, and $70 total gross margin.
7. Change the test tour's current prices to $99/$60 and confirm the reservation still retains $85/$50 and $70 margin.
8. Replay the identical submission, then issue four concurrent identical replays: every response returns the same receipt and only one booking exists for the reference.
9. Open Operations Bookings, locate/open the new request, verify its contact/travelers/trip/prices, change status to Contacted, and save an internal note.
10. Refresh and verify persisted status/note; verify mobile inbox filtering and detail layout.
11. Check public receipt/tour output excludes supplier cost, margin, internal notes, and private supplier contact data. Public booking/customer lookup endpoints return 404.
12. Check homepage CTA, all six public routes, and desktop/mobile document overflow.

Codespaces forwarding requires GitHub sign-in. The automated browser retained the configured Codespaces origins but used `VV_E2E_LOCAL_TRANSPORT=1` to route those requests to the real local containers. No API/data responses were mocked, forwarding visibility was not changed, and no GitHub-login acceptance claim is made.

Screenshots are in `/tmp/vv-m3-review/`. Test-owned bookings/trips were cancelled and test-owned suppliers/tours deactivated after validation; audit records were retained, not deleted. No existing inventory was repurposed for destructive test cleanup.

## Demo seed

`docker compose exec api python -m app.seed_bookings --confirm-demo` created four explicitly labeled development bookings in New, Contacted, Confirmed, and Cancelled states. A second run skipped all four without overwriting them. Seed is manual, development-only, and does not imply actual supplier confirmations or send email.

## Security and remaining scope

Public booking output is allowlisted and there is no public customer/history lookup. Normalized email reuse does not authorize overwriting an existing customer's private identity/contact record. The submitted contact is retained separately for Operations follow-up.

**Operations UI and `/ops/*` APIs are unauthenticated and NOT production-secure.** Protect them before production use. Public intake rate limiting/abuse protection and a privacy/retention review also remain production prerequisites. Idempotency is not authentication or abuse prevention.

Payments, real availability, supplier confirmation automation, customer/Operations authentication, email/SMS, hotels, transportation, packages, accounting, AI, and production media storage remain deferred. Customer/traveler visibility is provided within booking detail; a standalone CRM was not added. No outstanding Milestone 3 acceptance failures remain.

Final working tree contains both preserved Milestone 2 work and new Milestone 3 work, **uncommitted and unpushed**. Next recommended narrow milestone: **availability + supplier confirmation workflow**; it has not been started.
