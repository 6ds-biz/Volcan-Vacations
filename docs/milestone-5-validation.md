# Milestone 5 validation — 2026-09-05

Implementation and local validation are complete. **Real PayPal sandbox acceptance is blocked** by missing sandbox client ID, client secret and webhook ID. No real provider order, buyer approval, capture, popup cancellation, or signed webhook delivery is claimed. Live calls are disabled and no money was collected.

## Database and preservation — PASS

Forward revision `0005_paypal_payments` was applied to the existing PostgreSQL database with `docker compose exec -T api alembic upgrade head`. Repeating the command on the final rebuilt stack succeeded as a no-op. `alembic check` reports **No new upgrade operations detected**.

The existing Payment model now supports reservation-scoped immutable intents, provider IDs and environment, currency, stable create/capture request IDs, attempt timestamps, sanitized failure state, paid time, refunded amount and reconciliation flags. Reservation gains hashed payment-token/expiry and deadline fields. New webhook receipts and refund records provide notification/refund deduplication. Money remains Decimal and NUMERIC. Details and exact statuses are in [the implementation guide](milestone-5.md).

The initial working tree was clean at `fb13cd7` (`Complete VV Milestone 4 availability and supplier confirmation`). Required preflight `git status --short` and `git log --oneline -5` were run. Hash checks passed for migrations 0001–0004, homepage source/CSS, all photographs/fonts and the real VV logo. No database recreation, history rewrite, Git reset, unrelated discard, prior migration edit, or deployment configuration change occurred. Existing test/demo history is retained.

## Eligibility and payment behavior — PASS with mocked provider

Server-side create/capture require confirmed reservation, confirmed supplier, reservation availability `available` (the existing readiness predicate), nonterminal trip, positive valid snapshot amount, unpaid status, unexpired deadline and a valid public token. Provider configuration and a safe retry state are additionally required. One reservation is paid per checkout; a Product price edit never changes its reservation snapshot or Payment amount. Browser amount input is rejected.

Created/approved orders are unpaid. Only a validated completed capture sets paid time and the booking's derived payment-received state. Popup cancellation preserves the confirmed reservation and existing provider order. Safe funding failures remain retryable on the same intent. Uncertain/expired/voided/terminal orders require reconciliation or manual review; there is no automatic replacement order that could double-charge. Refunds and late/duplicate events preserve received state, with partial refund totals deduplicated by provider refund ID.

## Backend suite — PASS, 104 tests

Final backend command, after installing `requirements-dev.txt` in the development API container:

```bash
docker compose exec -T -e VV_TEST_POSTGRES=1 api python -m pytest -q
```

**104 passed**: all 66 existing Milestone 2/3/4 tests, 25 payment-domain cases, 12 adapter cases, and one actual PostgreSQL concurrency test. Existing httpx TestClient and datetime.utcnow deprecation warnings remain; no failures. Without the explicit PostgreSQL opt-in, that one test is skipped.

Coverage includes ineligible/terminal reservations, confirmed checkout, snapshot economics after Product price changes, rejected browser pricing, duplicate orders/captures, received state, cancellation, safe failure retry, lost create/capture responses, expired retry windows, provider binding/amount mismatch, invalid/expired/revoked/rotated tokens, supplier correction, public privacy, missing configuration, due-date expiry without supplier release, minimal provider POST representations, and recovery after a database write fails following provider capture.

Webhook tests cover invalid authentication, duplicate notification receipts, capture updates, frontend-first/webhook-first convergence, and full/partial refund deduplication. Adapter tests exercise OAuth/request payloads through httpx MockTransport, safe timeout/error handling, server-side signature-verification inputs, and refusal to call live or unsupported configurations.

The PostgreSQL test uses an isolated, randomly named test schema and **a mocked PayPal adapter**. Eight simultaneous order requests with different client keys produce one Payment and one provider order; four captures plus four webhook requests produce one capture and one notification receipt. Only its own test schema is dropped afterward. This verifies real database locking, not real PayPal network behavior.

## Builds and services — PASS

| Check | Result |
| --- | --- |
| Public `npm run typecheck` | PASS |
| Public `npm run lint` | PASS; no ESLint warnings/errors |
| Public `npm run build` | PASS, including `/pay` |
| Operations `npm run typecheck` | PASS |
| Operations `npm run lint` | PASS; no ESLint warnings/errors |
| Operations `npm run build` | PASS, including `/payments` |
| `docker compose config --quiet` | PASS; resolved secrets were not printed |
| `docker compose up --build -d` | PASS; final API/web/ops images rebuilt |
| PostgreSQL health | PASS |
| API health | PASS |
| Public web health | PASS |
| Operations health | PASS |
| Alembic upgrade and model drift check | PASS |
| Existing public routes/request/availability/supplier flows | PASS against running UI/API/PostgreSQL |
| `git diff --check` | PASS |

Frontend checks ran inside their matching Compose containers against the shared source. `next lint` emits its existing command-deprecation notice; lint itself passes.

## Browser acceptance — PASS for local application

The final `scripts/milestone5-local-e2e.cjs` run used actual public/Operations pages, FastAPI and PostgreSQL. **No provider responses or payment success states were mocked in this browser run.** Final test reference: `VV-260905-7FF79AC206D1`, booking 10.

Verified sequence: submit a public request for two guests at $85; reject payment-link creation while unconfirmed; show Not Ready; record manual supplier confirmation; generate an unguessable payment link; change current Product price to $95; open the payment page and still show **$170.00 USD**; verify safe public fields and token-in-header rather than request-URL transport; inspect noindex/no-referrer metadata; verify missing configuration blocks order creation with 503 and loads no SDK; refresh Operations; revoke the link and receive 404; cancel the test booking through Operations and observe the payment summary update to Not Ready without a page reload.

The final `scripts/milestone4-e2e.cjs` regression also passed against the rebuilt stack. References: `VV-260905-798CAA54155D` (booking 11, supplier confirmed) and `VV-260905-E209F7C62552` (booking 12, declined/alternative). Public mobile request submission, supplier contact timeline, date availability editing, stale checks, independent reservation availability, retained supplier reference, confirmation readiness, competing/duplicate PostgreSQL supplier actions, decline/alternative history and original price integrity all pass. Operations bookings and dashboard still work.

The existing six public routes pass at 1440/900/390px; `/pay` also returns 200 with invalid-link handling. Homepage and payment-page screenshots at all three widths were visually inspected: structural UI remains black/charcoal with gold actions and colorful unchanged photographs. Operations payment panels were inspected on desktop and mobile. Page-error and horizontal-overflow checks pass. An Operations payment-summary refresh issue found during review was fixed and verified by the cancellation test.

Two initial browser selector ambiguities were corrected: Next.js also supplies a route-announcement alert, and booking detail now contains both Payment and Supplier Confirmation panels. Acceptance selectors now target the intended region. A screenshot wait was tightened to capture the loaded payment panel. Final runs pass.

Artifacts: `/tmp/vv-m5-review/local-e2e-results.json`, payment-page/Operations screenshots, and `/tmp/vv-m5-review/m4-regression/` results/screenshots. Operations screenshots contain only test-owned data and subsequently revoked demo links. These are local review artifacts, not production customer records.

Codespaces forwarding requires GitHub authentication. `VV_E2E_LOCAL_TRANSPORT=1` retains configured browser origins while fetching real local services; it does not mock API data, change port visibility, or test GitHub login. Chromium ran with the approved process-sandbox escalation. Scripts create explicit DEMO inventory and `.invalid` contacts, then cancel/deactivate only their own records. Audit history is retained; no existing inventory is repurposed or deleted.

## Real sandbox and end-to-end acceptance — BLOCKED

Credential presence was checked without printing values in the workspace/environment and API container. Sandbox client ID, client secret and webhook ID are absent. The runtime safely displays unavailable checkout; no Payment row is created when configuration is absent.

| Acceptance path | Result |
| --- | --- |
| Public request → supplier confirmation → secure payment page → snapshot amount | PASS, actual local browser/API/database |
| PayPal order → actual sandbox buyer approval → capture → Payment Received → Operations Paid | BLOCKED; missing sandbox credentials |
| Refresh customer/Operations after actual capture | BLOCKED; no actual capture exists |
| Actual PayPal popup cancellation, confirmed/unpaid reservation retained | BLOCKED; missing sandbox credentials |
| Cancellation state and same-intent retry | PASS with mocked provider backend tests only |
| Duplicate-charge protection and frontend/webhook convergence | PASS with mocked provider tests and real PostgreSQL locks; actual provider retry still unverified |
| Actual signed PayPal webhook and repeated delivery | BLOCKED; missing sandbox app/webhook configuration and registered reachable endpoint |

The guide contains the exact remaining sandbox acceptance steps and the future live-readiness checklist. No live credentials were enabled and no successful sandbox capture is fabricated.

## Security, deferred scope and Git

The PayPal secret remains backend-only; public schemas exclude cost/margin, supplier contacts, internal notes, other customer data, capture IDs, provider debug bodies and webhook configuration. Payment URLs use 256-bit random bearer tokens stored as hashes and can expire, rotate or be revoked. Operations failures show only sanitized provider codes/messages.

**`apps/ops` and `/ops/*` are NOT production-safe until authentication is implemented.** No rushed authentication, public Operations exposure or automatic messages were added.

Live PayPal activation, refunds UI, customer accounts, Operations authentication, email/SMS, hotels, transportation, packages, accounting and AI remain deferred. Payment expiry is manual-review/deadline enforcement only; no automatic supplier release. Terminal provider-order replacement requires a future controlled recovery workflow.

Changes are **uncommitted and unpushed**. Final `git status --short`, `git diff --stat` and whitespace checks were run; new files remain intentionally untracked pending review. Next recommended narrow milestone: **transactional email plus customer confirmation/receipt delivery**. It has not been started.

**VV MILESTONE 5: NOT COMPLETE** — real sandbox acceptance remains blocked by missing configuration.
