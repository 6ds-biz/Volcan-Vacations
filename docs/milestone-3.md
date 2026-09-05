# Milestone 3 — booking requests and follow-up

## Lifecycle and relationships

`/request?tour={slug}` loads the selected active tour. The visitor supplies a requested date, optional local Costa Rica time, contact details, party size (1–50), at least one named traveler, optional additional travelers/DOBs, optional trip dates, and customer notes. Traveler count cannot exceed party size. Remaining names can be obtained in follow-up. This is a request for availability, never an automatic reservation confirmation. No payment is collected or email sent.

One transaction creates/reuses Customer, creates Trip (`inquiry`), creates/reuses Travelers, associates them via TripTraveler, and creates Reservation (`new`). Prices and the tour name are snapshotted. A failure rolls back every new record/link. A unique `VV-YYMMDD-{12 random hex characters}` trip reference is generated; database uniqueness plus bounded whole-transaction retries handle collisions. References are not public lookup credentials.

Customer emails are stripped/lowercased. The migration stops for manual review if pre-existing normalized emails collide, rather than merging/deleting customers. Public email matching is **not proof of identity**: reuse does not overwrite existing customer names, phone, preferred contact, or internal notes. Reservation `contact_snapshot` preserves exactly the new request's contact for follow-up. Public receipts use only the submitted name, not previously stored customer data. Operations displays both submitted contact and the linked record.

Exact traveler matches (customer, case-insensitive names, DOB including null, type) are reused without overwriting any prior traveler data. Ambiguous existing matches create a separate traveler; no destructive merges. A trip association preserves participant order. DOBs are optional; duplicate names/DOBs within one submission need clarification rather than silently collapsing participants. No passport/document fields were added.

## Migration and historical data

`0003_booking_requests` follows the unchanged `0001_initial_schema` and `0002_tour_inventory`. It adds customer contact preference/notes, traveler type/notes, nullable trip names/dates, trip reference/party size/notes, TripTraveler, and reservation time/notes/contact and receipt snapshots/idempotency fields. Existing statuses and financial values are retained; only new defaults change to inquiry/new. Legacy trips receive `VV-LEGACY-{id}` references. No database recreation is performed. Automatic downgrade intentionally refuses because new nullable dates cannot safely be converted back to required dates without a reviewed data migration.

```bash
docker compose exec api alembic upgrade head
docker compose exec api alembic check
```

Reservation `unit_price` and `supplier_unit_cost` copy Product's Decimal/NUMERIC values inside the intake transaction. Later product edits do not affect historical booking economics. Retail total = unit price × quantity. Gross margin shown in Operations is **the entire request**: `(unit_price - supplier_unit_cost) × quantity`; no redundant margin is stored. USD per-person and total labels distinguish these values. Supplier confirmations and final price renegotiation are not implemented.

## APIs and duplicate protection

- `POST /public/booking-requests`: only the strict intake schema is accepted. No public internal notes, price overrides, or arbitrary customer IDs. Requires a UUID `idempotency_key`.
- Returns reference, initial request status, snapshotted tour name, requested date, party size, submitted customer name, and next-step message. No sequential IDs, costs, contact details, or internal data.
- `GET /ops/bookings?status=...`: newest actionable requests first, then other statuses, newest first within each group.
- `GET /ops/bookings/{id}`: customer/submitted contact, trip, associated travelers, snapshot prices/margin, and notes.
- `PUT /ops/bookings/{id}`: status, expected current status, internal notes, optional explicit trip status. Does not edit historical economics or participant identities.
- No public booking lookup, customer list, or public booking history endpoint.

The unique submission key and canonical payload SHA-256 are stored with the reservation. An exact retry returns the original safe receipt, even if Operations status or Product pricing changed. A reused key with changed details returns 409. Concurrent uniqueness races retry the entire transaction. A different key means a distinct request; this is accidental-duplicate protection, not abuse prevention or authentication.

The public submit button and synchronous in-flight guard prevent double clicks. Only a payload digest and random key are kept in sessionStorage, never contact/DOB/note fields. A lost/uncertain response keeps the in-memory payload frozen for an identical retry. A blocked browser-storage policy still permits in-memory retries. The success screen displays the reference with clear “Request Received” language and no payment button. No receipt with personal details is persisted in browser storage.

## Operations workflow

Bookings navigation opens `/bookings`; `/bookings/{id}` provides the detail/editor. Customer and traveler views are intentionally scoped to each booking rather than expanding this milestone into a CRM. Inactive inventory and existing Milestone 2 screens remain intact.

Allowed reservation transitions:

| Current | Next |
| --- | --- |
| new | contacted, pending_supplier, confirmed, cancelled |
| contacted | pending_supplier, confirmed, cancelled |
| pending_supplier | contacted, confirmed, cancelled |
| confirmed | completed, cancelled |
| cancelled / completed | terminal; internal notes still editable |

Saving unchanged status is allowed for note updates. Status changes lock the reservation and verify `expected_status`; stale clients receive 409. `pending_supplier` is a placeholder for later coordination, not a message trigger. Manually choosing confirmed records the operator's decision; it does not run an availability check. Opening a record never changes status. Trip status (inquiry/planning/confirmed/completed/cancelled) stays separate and changes only through an explicit Operations selection. No automatic whole-trip confirmation.

## Security, availability, and future email

**Operations UI and `/ops/*` APIs are unauthenticated and NOT production-safe. Protect both before production launch.** Hidden URLs, CORS, and noindex are not security. Keep Codespaces ports private; private-port GitHub cookies are infrastructure access, not application authentication. Customer/DOB/contact data makes this boundary especially important. No rushed auth was added.

Public output uses an explicit allowlist and never returns other bookings/customers, supplier cost/margin, supplier contact information, or internal notes. Do not add public lookup without verified ownership. Before public production launch, also add an appropriate intake abuse/rate-limit boundary and data retention/privacy review; idempotency is not rate limiting.

No availability checks, supplier confirmations, payments, or transactional email are implemented. Future trigger: **booking request committed → transactional outbox/queue → acknowledgement email**. Add durable delivery and retry handling at that post-commit boundary; do not send before commit or on idempotent replay. No delivery is claimed today.

## Explicit demo seed

```bash
docker compose exec api python -m app.seed_bookings --confirm-demo
```

Development-only; requires the Milestone 2 active whitewater-rafting demo. Creates labeled examples in new/contacted/confirmed/cancelled states with `.invalid` emails. A stable per-example UUID makes subsequent runs skip existing records without changing notes or statuses. No startup seed and no real confirmations/emails. Demo data is not a supplier offer.

## Validation

```bash
cd services/api
# Use a virtual environment with requirements-dev.txt installed.
python -m pytest -q
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

If Compose's pre-existing anonymous frontend build volumes retain an old build, refresh only those: `docker compose up -d --no-deps --force-recreate --renew-anon-volumes web ops`. Never remove the named Postgres volume.

`scripts/milestone3-e2e.cjs` uses Playwright installed separately from the app runtime. Set `VV_E2E_CONFIRM_DEMO=yes`, optionally `VV_E2E_WEB_URL`, `VV_E2E_OPS_URL`, `VV_E2E_API_URL`. It creates test-owned demo inventory, submits through the public UI, verifies graph/snapshots/privacy and Operations follow-up, then cancels the test booking/trip and deactivates only its own inventory (audit records retained). Optional `VV_E2E_LOCAL_TRANSPORT=1` keeps configured Codespaces origins while routing to real local containers; it does not mock booking data or change forwarding visibility. Default screenshots: `/tmp/vv-m3-review`.

Next narrow milestone: availability requests and supplier confirmation workflow. Do not begin it as part of this milestone. Payments, auth, email/SMS, hotels, transportation, packages, accounting, AI, and production media storage remain deferred.
