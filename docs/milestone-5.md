# Milestone 5 — Payment readiness and PayPal Sandbox

This milestone pays **one confirmed reservation per checkout**, in USD, using the existing Payment model. No trip-wide balance allocation, deposits, split payments, customer accounts, communications, or live payment activation is implemented. The public homepage and its approved black/gold design are preserved.

**`apps/ops` and `/ops/*` are NOT production-safe until authentication is implemented.** Keep both private to the development environment. A non-guessable public payment link does not secure the unauthenticated Operations API that issues it. Do not expose Operations or its APIs publicly to make a sandbox webhook reachable.

## Configuration

Set these only in the backend's ignored development `.env` or host secrets, using a PayPal **sandbox business app**:

```dotenv
PAYPAL_ENVIRONMENT=sandbox
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=
PAYPAL_CURRENCY=USD
PAYPAL_WEBHOOK_ID=
```

The old unused `PAYPAL_SECRET` placeholder is replaced by `PAYPAL_CLIENT_SECRET`. Do not prefix secrets with `NEXT_PUBLIC_`, add them to Next.js configuration, include them in screenshots, or commit them. The public session may return the client-safe app ID only when checkout is available. The secret and webhook ID never appear in public response schemas or frontend code.

Compose already passes the backend `.env`; after changing configuration, recreate the development API with `docker compose up -d --force-recreate api`. Do not print the resolved Compose environment to shared logs; `docker compose config --quiet` validates it without printing secret values.

The provider adapter defines both base URLs, but deliberately refuses all live requests in this milestone. Unsupported environment/currency and missing sandbox app credentials disable checkout with a safe 503. Database constraints also restrict PayPal records to positive USD sandbox payments. Changing an environment variable alone cannot enable live checkout. The webhook ID is additionally required for notification verification; Operations displays a separate warning if it is missing.

PayPal's browser SDK receives only the safe client ID and creates/captures through FastAPI. Its native gold PayPal controls are used without custom restyling. The surrounding page uses the existing black/charcoal/gold variables. See [PayPal's standard integration](https://developer.paypal.com/studio/checkout/standard/integrate).

## Eligibility and historical money

The server requires all of the following before creating or capturing an unpaid order:

- Reservation status `confirmed`.
- Supplier confirmation `confirmed` and reservation availability `available`; these are the existing `ready_for_payment` prerequisites. General tour/date availability is a separate record and does not itself confirm a reservation.
- Parent trip is neither cancelled nor completed.
- A positive snapshot total within the existing `NUMERIC(12,2)` range.
- No received payment for the reservation, and any payment deadline is still in the future.
- A valid, unexpired payment token for public calls; provider configuration and a safe retry state for provider mutations.

New, contacted, pending-supplier, cancelled, completed, declined, unavailable, or alternative-offered reservations cannot pay. An alternative must first become a supplier-confirmed reservation through the existing fulfillment process. Merely setting a generic status or hiding a frontend button is insufficient.

`Reservation.unit_price × Reservation.quantity` is authoritative. A snapshot of $85 for two guests charges $170 even when Product now costs $95. All backend arithmetic uses Python Decimal; persisted money uses PostgreSQL NUMERIC; JSON money is represented as strings. The order schema accepts an idempotency UUID only: browser-supplied amounts are rejected with 422. The Payment amount is copied once from that reservation snapshot and retained.

## Database

Apply forward revision `0005_paypal_payments` after `0004_availability_confirmation`:

```bash
docker compose exec api alembic upgrade head
docker compose exec api alembic check
```

The existing Payment retains its ID, trip, amount, method, status, external reference, and timestamps. It gains nullable unique reservation linkage, currency, provider/environment, unique provider order/capture IDs, unique create/capture request IDs, attempt start times, sanitized failure fields, paid time, refunded amount, and a reconciliation flag. One immutable intent per reservation is deliberate; legacy trip-only records retain nullable reservation linkage and `manual` provider.

Reservation gains a unique token hash, token expiry, and payment deadline. `payment_webhook_events` retains unique notification IDs and processing outcomes, without raw payloads. `payment_refunds` retains unique verified refund IDs and Decimal amounts to prevent double-counting different notifications for the same refund. Database constraints protect allowed states, amounts, scope, and uniqueness. Prior migrations are unchanged; automatic downgrade refuses to discard payment audit data.

## Exact payment states

| State | Meaning |
| --- | --- |
| `pending` | Local intent exists, provider outcome is uncertain, or a capture is still pending. No confirmed receipt yet. |
| `created` | Provider order exists; no completed capture. Customer approval may still be required. |
| `approved` | PayPal has approved the order; approval alone is not payment. |
| `captured` | Authenticated provider order reports a matching completed capture; `paid_at` is set. |
| `failed` | A definite provider rejection or a condition requiring manual review prevented completion. Safe funding retries reuse the same order. |
| `cancelled` | Customer dismissed checkout before capture started. The confirmed reservation remains unchanged and can retry the same intent. |
| `refunded` | The full captured amount has been refunded. The reservation cannot start another payment automatically. |
| `partially_refunded` | A verified partial refund was reported. Refund amounts are reconciled individually; missing detail is flagged for review. |

`ready` and `not_ready` are public display states when no Payment exists, not persisted payment statuses. Reservation fulfillment status is kept separate from payment status. A pending or failed checkout does not cancel supplier confirmation. Received/refunded states cannot be downgraded by a delayed approval/failure event. Operations also displays the independent eligibility and review flags.

## Secure customer entry point

In Operations booking detail, confirm the supplier, then choose **Generate payment link**. The server generates 32 cryptographically random bytes, keeps only a SHA-256 hash, and returns `/pay#token=<random-value>`. The fragment is not part of HTTP request URLs; the page sends the token in an Authorization bearer header. It uses no local/session storage, has `noindex,nofollow` metadata and a no-referrer policy, and payment responses are `no-store`.

Treat the URL as a bearer credential. Anyone holding it can view this booking's limited payment summary. Operations cannot retrieve a previously generated raw token; generating another replaces it. Revoking it or cancelling the reservation makes it unusable. Terminal parent trips also fail token checks. Supplier corrections that remove readiness invalidate the link. Do not put tokens in analytics or HTTP header logging.

Links expire at the earlier of seven days or the selected deadline. The default deadline is seven days; an operator may choose a future deadline within 30 days. Overdue bookings are visible in Operations and cannot pay until an operator reviews and renews the deadline/link. No automatic cancellation, capacity release, or supplier message occurs. A renewed link does not replace a provider order or clear payment review flags.

The customer sees booking reference, stored tour name/date, party size, snapshot amount and PayPal status. Before checkout: “Your tour has been confirmed and is ready for payment.” After a completed capture: **Payment Received**, amount paid, reference, tour, date and party size. Popup cancellation says “Payment was not completed. Your confirmed reservation is still awaiting payment.” Errors and loading states are actionable without provider stack traces. Refresh reconciles an uncertain provider outcome. Refunds display a payment update, not a claim that the trip is complete.

## HTTP flow

All public payment calls use `Authorization: Bearer <token>`. No sequential reservation ID or predictable booking reference authorizes public access.

| Endpoint | Purpose |
| --- | --- |
| `GET /public/payments/session` | Safe summary, eligibility, configuration availability, and safe SDK client ID when available. |
| `POST /public/payments/paypal/order` | Body `{"idempotency_key":"<UUID>"}`; validate, commit local intent, create/reuse provider order, return safe checkout state/order ID. |
| `POST /public/payments/paypal/{order_id}/capture` | Verify token/order ownership and current eligibility; capture the existing approved order or return its already-received state. |
| `POST /public/payments/paypal/{order_id}/cancel` | Record checkout dismissal when no capture has started; preserve reservation and order. |
| `POST /public/payments/reconcile` | Read authenticated provider state and merge it locally; never initiates a capture. |
| `POST /webhooks/paypal` | Verify and reconcile provider notifications; no payment-token authentication. |

The adapter in `app/services/paypal.py` handles OAuth, order/capture reads and writes, refunds/capture reads, bounded timeouts, safe error normalization, and signature verification. POST responses may be minimal: the domain service reads the full authenticated order before validating its binding, amount, currency and capture. Orders include an opaque UUID binding to the Payment; no supplier cost, customer notes, or payer details are sent as order context.

## Duplicate-charge protection and recovery

Trip, reservation and Payment row locks serialize supplier/booking changes, order creation, captures and webhook updates in PostgreSQL. Unique reservation linkage ensures different browser keys still resolve to the same intent. Provider create/capture request IDs are committed before network mutations, so a lost response or rolled-back result can retry the same provider request. No second chargeable order is automatically created for a reservation.

PayPal request IDs are API-specific and have finite retention; the Orders API documents a six-hour default. This implementation bounds uncertain mutation retries to five hours and requires manual review afterward. It continues to read a known provider order for reconciliation. See [PayPal idempotency](https://developer.paypal.com/api/rest/reference/idempotency/) and [Orders create](https://developer.paypal.com/sdk/orders/v2/orders-create/).

An ordinary funding rejection can retry the same approved order. A declined capture resource, amount/binding mismatch, voided/missing/expired order, or uncertain mutation outside the safe window blocks further automatic charge attempts. **Automatic replacement orders are deliberately not supported.** Operations must reconcile with PayPal and review the provider outcome; do not delete records, reset request IDs, or issue a new reservation to bypass a possible charge. A future controlled recovery workflow is needed for an irrecoverably expired order.

Repeated capture returns the received state without a second capture. Frontend capture and webhook processing use the same validation/merge function, and a unique event receipt makes repeated webhooks harmless. A completed capture can recover local state even if the frontend lost its response. A late received capture on a changed/cancelled booking remains recorded as received and is flagged for review rather than erased.

## Webhooks and refunds

Register the sandbox app's webhook against an HTTPS endpoint that can reach **only the required API route** without exposing Operations. Set its webhook ID in backend secrets. Register order approved/completed and capture completed/pending/denied/refunded/reversed events as available in PayPal. Relevant failed/declined capture notifications are also handled; unrelated verified events are recorded as ignored.

The endpoint forwards PayPal transmission headers, the original parsed event, and the configured webhook ID to PayPal's signature verification API. Only `SUCCESS` is trusted. Missing/invalid signatures fail with 400 when configured; missing configuration or temporarily unverifiable/reconcilable outcomes return 503 for retry. Body size is bounded. Incoming certificate URLs are never fetched locally. See [PayPal webhook signature verification](https://developer.paypal.com/api/webhooks/v1/verify-webhook-signature-post).

Notification payloads alone do not mark paid: the server fetches the merchant's authenticated order, validates reference/currency/amount/capture ID, and merges it transactionally. Refund notifications fetch and validate refund and capture details; unique refund IDs prevent duplicate totals. Full and partial refunds are representable; delayed partial-refund details and reversals flag review. There is **no refund button or outgoing refund API**, and disputed/reversed payments require operator review.

## Operations

Booking detail shows Not Ready, Ready for Payment, Payment Pending, Paid, Payment Failed, Refunded/Partially Refunded; amount due, deadline/overdue, provider, order/capture, paid time, sanitized failure reason and review flag. It provides link generation/revocation and read-only provider reconciliation. `/payments` lists booking/customer/tour/amount/provider/created/paid/status with All, Pending, Paid, Failed and Refunded filters. Cancelled intents remain visible under All.

Public schemas exclude supplier costs, margins, contacts, internal notes, other customers, capture IDs, provider debug payloads, secret, and webhook ID. Operations contains private booking data and remains development-only; authentication is intentionally deferred, not implied by these payment protections.

## Tests and local acceptance

```bash
docker compose exec -T api pip install -r requirements-dev.txt
docker compose exec -T api python -m pytest -q
docker compose exec -T -e VV_TEST_POSTGRES=1 api python -m pytest -q
```

The optional PostgreSQL test creates a randomly named isolated test schema, exercises real row locks with simultaneous order/capture/webhook requests, and drops only that schema afterward. Provider calls in backend tests are **mocked**, including httpx adapter tests. They are not evidence of real sandbox checkout.

`scripts/milestone5-local-e2e.cjs` uses Playwright and real local UI/API/PostgreSQL, with `VV_E2E_CONFIRM_DEMO=yes` and `VV_E2E_WEB_URL`, `VV_E2E_OPS_URL`, `VV_E2E_API_URL`. Install Playwright outside the repository if needed and supply it through `NODE_PATH`. In this Codespace, `VV_E2E_LOCAL_TRANSPORT=1` retains configured origins but forwards browser transport to local ports, bypassing only Codespaces' GitHub login page. It does not mock application responses or change port visibility.

This local script verifies a real booking request, confirmation, secure link, snapshot amount, responsive pages, privacy, revocation and missing-configuration behavior. It never fakes or performs a provider capture. It cancels/deactivates only its own DEMO records, retaining audit history. The existing Milestone 4 script checks request, availability and supplier regressions.

## Required real sandbox acceptance

Use a separate PayPal sandbox buyer account, never real funds. Configure the sandbox business app and registered webhook first. On a development test booking:

1. Submit a public request; confirm its supplier in Operations; verify Ready for Payment.
2. Generate and open its private URL. Verify snapshot price × party size, including a test where current Product price changed.
3. Use the native PayPal button to create an actual sandbox order. Approve with the sandbox buyer and let FastAPI capture it.
4. Verify **Payment Received** and the correct amount/details publicly; verify **Paid**, order/capture and paid time internally.
5. Refresh both pages. Repeat the same capture request and confirm PayPal has exactly one capture.
6. Verify an actual signed capture webhook, including repeated delivery, produces one receipt and no duplicate charge. Test a lost frontend response followed by webhook/reconcile recovery.
7. On a second confirmed booking, begin then cancel the PayPal popup. Confirm it remains supplier-confirmed, unpaid, and retryable with the exact cancellation wording.

Record real order/capture evidence privately and only masked evidence in shared reports. Do not call mocked tests or webhook simulator payloads a successful actual checkout. The current workspace has no sandbox app credentials/webhook ID; see the validation report for blocked acceptance items.

## Before any future live activation

Live mode requires a separately reviewed code/database change after this checklist, not just an environment toggle:

1. Production domain deployed.
2. HTTPS verified.
3. Operations authentication enabled for both UI and APIs.
4. Production database backed up.
5. PayPal live app created.
6. Live credentials stored only in host secrets.
7. Live webhook URL registered.
8. Webhook verification tested.
9. Sandbox end-to-end acceptance passed.
10. Test a small controlled live payment before broad launch, with explicit authorization.

Live activation, refunds UI, customer accounts, Operations authentication, email/SMS, hotels, transportation, packages, accounting and AI remain deferred. The next narrow milestone is **transactional email plus customer confirmation/receipt delivery**; it is not started here.
