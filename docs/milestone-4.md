# Milestone 4 — availability and supplier confirmation

## Three separate states

The existing `availabilities` table stores one checked **product/date snapshot**. Its optional capacities are supplier-reported information, not an allotment: submitting or confirming a request does not decrement them. A confirmed reservation may already hold space when the general date later sells out. Updating a date does not update reservations, and declining one reservation does not declare the whole date sold out.

Reservation keeps three distinct states:

| Field | Meaning |
| --- | --- |
| `status` | VV's overall follow-up lifecycle: new, contacted, pending_supplier, confirmed, cancelled, completed |
| `availability_status` | What VV has established about fulfilling this specific request: unknown, available, limited, unavailable, closed |
| `supplier_confirmation_status` | Supplier coordination: not_requested, awaiting_supplier, confirmed, declined, alternative_offered |

`ready_for_payment` is derived from reservation **confirmed + supplier confirmed + availability available**. It is an internal eligibility indicator, not a payment, a payment authorization, or a checkout endpoint. Cancelling/completing a reservation removes eligibility. Trip status remains a separate explicit operator decision. Supplier confirmation does not send a customer confirmation message.

A public request begins `new / unknown / not_requested`, regardless of a general date snapshot. The fulfillment `supplier_id` is copied from the product at intake. Later editing a product's supplier does not silently redirect existing reservations or their supplier event history. Operations warns when the current date inventory belongs to a different supplier. Resolving a request for another tour/supplier requires reviewing the proposal and a new request; this milestone does not reprice or replace the original reservation.

## Manual actions and history

`POST /ops/bookings/{id}/supplier-events` is the single transactional command boundary. Every accepted action changes the reservation and appends a `SupplierConfirmationEvent` in one transaction. History has no edit/delete API. Contact method, operator identifier, observed time, reference, response/notes, proposed tour/date/time and resulting state are retained in insertion order. The timeline shows both observed time and recorded time; old context can be added as a note without retroactively changing state.

| Action | Result |
| --- | --- |
| contacted | pending_supplier / existing availability / awaiting_supplier; records phone, email, WhatsApp, supplier portal or other manual contact |
| follow_up | Requires awaiting_supplier; records another contact and keeps pending_supplier |
| availability_checked | Changes only this reservation's availability; awaiting supplier can coexist with available |
| confirmed | confirmed / available / confirmed; optional reference and confirmation time; eligible for future payment |
| declined | contacted / unavailable / declined; clears current confirmation but retains all previous history; trip unchanged |
| alternative_offered | contacted / existing availability / alternative_offered; records proposal without changing original requested tour/date/time/prices |
| note | Adds timeline context without changing lifecycle or current supplier reference |

Renewed contact after a confirmed/declined/alternative outcome resets request availability to unknown and clears the current confirmation reference/time. Correcting an existing supplier confirmation requires an explanatory note for renewed contact, another confirmation, a decline or an alternative. The prior reference remains in the timeline. Directly making a supplier-confirmed request unavailable is rejected; use a corrective supplier action first. A declined request must be re-contacted before independently marking availability available again. Cancelled/completed reservations permit timeline notes only. State-changing events cannot predate the latest recorded state action. Supplied observed/check times require timezone offsets and cannot be more than five minutes in the future.

The generic booking PUT remains for follow-up notes, cancellation/completion, customer-contact status and explicit trip status. Newly moving into pending_supplier or confirmed goes through supplier actions; generic status selection cannot bypass supplier verification. Existing milestone 3 callers retain `expected_status` compatibility; `expected_version` additionally protects notes and other concurrent edits, and the Operations UI always submits it. All writes increment the reservation version. Generic follow-up doesn't create supplier communication history because it is not a supplier contact.

Supplier commands require `expected_version` and UUID `command_id`. A row lock serializes writers; a stale version returns 409. An exact command replay returns the current booking without appending another event. Reusing a command key for different details returns 409. Clients should supply and retain the same `occurred_at` and complete payload on uncertain retries; the UI keeps an in-memory key and body for unchanged details. Reloading resolves a conflict. No contact data is stored in browser storage. Operator identifiers are self-reported, not authenticated identity.

## Tour/date availability

`GET /ops/availability` filters recorded dates by inclusive `date_from`/`date_to`, `product_id`, `supplier_id`, and `status`. Use equal from/through dates for a single day. `POST /ops/availability` adds an individual date. `PUT /ops/availability/{id}` requires its `expected_version` and edits that same product/date; it cannot move an existing record. Duplicate product/date creation returns 409. There is no automatic future-date expansion.

Statuses: unknown, available, limited, unavailable, closed. Sources: manual, supplier, api, inventory. These sources describe where recorded information came from; selecting api does not run an integration. Capacity and remaining capacity are independently nullable, nonnegative integers; remaining cannot exceed total when both are known. Available/limited cannot have a known zero capacity. A supplier can report Available with both capacities unknown.

Known availability requires `last_checked_at`. A missing check time or a check older than **24 hours** is marked stale. Internal screens retain the reported status alongside a stale warning. There is no scheduler and no automatic assumption that stale availability remains valid. This conservative freshness threshold is centralized in `availability_rules.py` and can later become supplier-specific.

## Public boundary

The approved public website is unchanged: **Request This Tour**, colorful photographs, black/gold UI, and the same booking request and immutable receipt. Optional `GET /public/tours/{slug}/availability?date=YYYY-MM-DD` returns exactly:

```json
{"date":"2026-10-05","status":"unknown","request_required":true}
```

For an active tour, a fresh date record may return its known status. Missing/stale records return unknown, never invented availability or sold-out status. Inactive/missing tours return 404. This endpoint does not guarantee inventory or confirm a request. The public page does not consume it yet.

Public responses exclude capacities, supplier notes, contacts, costs/margins, internal timestamps, events, confirmation references, operators and internal reservation state. No public booking/customer/history lookup is added. Public availability and all internal responses use `Cache-Control: no-store`.

## Operations

- `/availability`: filters, add/edit one date, source, optional capacities, private notes, last checked and stale indication. Each tour editor links directly to its dates.
- Booking detail: original requested experience; general date check, source and freshness; reservation supplier contacts; separate request and supplier statuses; manual action form; current reference and append-only timeline; ready-for-payment and needs-attention labels.
- Inbox: defaults to Needs Attention, with overall and supplier-state filters; shows unknown/available/etc., awaiting supplier, declined/Alternative Needed, alternative offered, and Ready for Payment. Uncheck Needs Attention to review confirmed/terminal bookings.
- Dashboard: live new request, active awaiting supplier, currently confirmed today (UTC), and needs-attention counts. Confirmed Today counts current confirmations received today, not an analytics history of every past confirmation.

Needs Attention includes new/contacted/pending requests and active requests lacking supplier confirmation, including legacy unverified confirmations. Cancelled/completed reservations do not require attention. No Operations redesign or standalone communications platform was introduced.

## Migration and extension point

Forward revision **`0004_availability_confirmation`** follows unchanged `0001`, `0002` and `0003`. It extends existing Availability and Reservation and adds SupplierConfirmationEvent with indexes, foreign keys, allowed-state/capacity checks, product/date uniqueness, versions and command-key uniqueness. Existing reservations receive their product's supplier and unknown/not_requested confirmation defaults. Old reservation statuses and financial snapshots stay intact; a legacy confirmed record is not falsely marked supplier-confirmed or ready for payment. Old date check times remain null/stale.

The migration preserves all rows. If legacy dates are duplicated or violate the new checks, it fails transactionally for explicit data review rather than silently merging/deleting records. Downgrade requires reviewed data recovery; the automatic downgrade refuses to drop supplier history.

```bash
docker compose exec api alembic upgrade head
docker compose exec api alembic check
```

Future adapters should validate `AvailabilityInput` / `AvailabilityUpdate` and `SupplierEventInput`, then use `save_availability` / `record_supplier_event`. Keep version checks, idempotency and event transactions at that shared service boundary; do not bypass it with supplier-specific parallel tables or direct state writes. Add real authentication, trusted provenance and delivery controls before allowing external integrations. No supplier API adapter is implemented now.

## Validation and scope

```bash
docker compose exec api pip install -r requirements-dev.txt
docker compose exec api python -m pytest -q
docker compose exec web sh -c 'npm run typecheck && npm run lint && npm run build'
docker compose exec ops sh -c 'npm run typecheck && npm run lint && npm run build'
docker compose config --quiet
docker compose up --build -d
docker compose exec api alembic upgrade head
docker compose ps
```

`scripts/milestone4-e2e.cjs` runs real public requests and Operations actions on both confirmed and declined/alternative paths, including PostgreSQL competing edits/idempotent retries, privacy, public route checks, and screenshots at 1440/900/390 pixels. Requires Playwright separately and `VV_E2E_CONFIRM_DEMO=yes`. Optional `VV_E2E_WEB_URL`, `VV_E2E_OPS_URL`, `VV_E2E_API_URL` and `VV_E2E_LOCAL_TRANSPORT=1` preserve configured Codespaces origins while forwarding browser transport to the real local containers. This does not mock records or change port visibility. Cleanup cancels only test-owned bookings/trips and deactivates test-owned inventory, retaining audit records. See the validation report for actual outcomes.

**Operations UI and `/ops/*` APIs remain unauthenticated and are NOT production-safe.** Private forwarding is infrastructure access control, not app authentication. Protect both before production. No custom authentication was added, and no public production launch is implied.

Payments/PayPal/cards/deposits/refunds, automatic email/WhatsApp/SMS, customer accounts, Operations auth, supplier APIs, hotels/transport/packages, accounting/AI and production object storage remain deferred. Next narrow milestone: **Payment readiness + PayPal checkout**; not started here.
