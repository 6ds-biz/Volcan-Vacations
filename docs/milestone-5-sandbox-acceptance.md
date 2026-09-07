# Milestone 5 real PayPal Sandbox acceptance — 2026-09-07

## Post-payment verification — latest status

**COMPLETE: real Sandbox capture, persisted Paid/Payment Received state, actual signed webhook verification, and duplicate protection are confirmed.** The user supplied the existing current customer URL after waking the Codespace. No new payment, charge, or manual payment-state change was made during post-payment verification.

### Captured transaction and preserved snapshots

Booking `VV-260907-CD7A3D01E30E` has exactly one Payment, amount **USD 170.00**, provider `paypal`, and local status `captured`. `paid_at` is **2026-09-07 05:10:41.240942 UTC**. The internal provider order and capture IDs both exist and match authenticated Sandbox API reads. PayPal reports the order and its one capture as `COMPLETED`, with the correct USD 170.00 amount and immutable local reference context.

The reservation remains `confirmed`, supplier-confirmed, with availability `available`. Snapshot values are unchanged: quantity 2, unit retail USD 85.00, unit supplier cost USD 50.00, total retail USD 170.00, historical gross margin USD 70.00. The Payment points to the correct reservation and trip. Trip workflow status remains `inquiry`, as before payment; the implementation tracks supplier fulfillment on the reservation and derives received/Paid state from the Payment without automatically advancing the independent trip workflow.

### Actual signed webhook and redelivery — PASS

The API received `CHECKOUT.ORDER.APPROVED` and `PAYMENT.CAPTURE.COMPLETED`, returned HTTP 200 for each, and stored both receipts as `applied` against this Payment. Authenticated provider event reads match the stored event and resource IDs. The unchanged webhook implementation requires PayPal's verification response to be `SUCCESS` before processing or recording even duplicate events; these accepted real receipts therefore establish successful signature verification.

Using PayPal's [documented event-resend endpoint](https://developer.paypal.com/api/webhooks/v1/webhooks-events-resend), both existing events were redelivered to only the configured Sandbox webhook. Both redeliveries reached `/webhooks/paypal` and returned HTTP 200: four accepted deliveries in total. PostgreSQL still has exactly two unique event receipts and one Payment. Status, amount, original paid timestamp, and capture ID remain unchanged. PayPal still reports one completed capture. The late duplicate approval did not regress captured state. No webhook simulator or forged signature was used.

### Operations — PASS

A fresh browser verified **Paid**, USD 170.00, PayPal, a paid timestamp, and matching internal order/capture references on booking 13. Payment eligibility is false, amount due is zero, and Generate payment link is disabled. Reload preserved Paid. The Payments list contains the captured row, its paid timestamp and amount; the Paid filter and list reload passed.

### Customer persistence and capture retries — PASS

After the Codespace woke, the user's existing secure link loaded **Payment Received** in a fresh browser with the correct booking, party size, PayPal, and USD 170.00 paid. Reload preserved this state from the real token-scoped API. Browser request monitoring found no order or capture POST during navigation/reload. The paid page did not load the PayPal SDK, and the session exposed no private payment/supplier fields. Clicking Refresh payment status made only the existing `/reconcile` request and retained Payment Received.

Three concurrent POST retries to the existing FastAPI capture endpoint for this already-captured order all returned captured, USD 170.00 paid, and zero due. The existing `paid_at` early-return branch handles these requests before any provider call. Before/after Operations responses matched on payment ID, amount, currency, status, order ID, capture ID, original paid timestamp, and updated timestamp. A subsequent authenticated Sandbox GET independently confirmed exactly one completed provider capture with the same ID. PostgreSQL still held one Payment and two unique webhook receipts. No order-creation endpoint was called during this post-payment verification.

### Cancellation preserved — PASS

Booking `VV-260907-9B14CA9E7C7B` retains one locally `cancelled` payment, supplier-confirmed reservation, payment eligibility, and no paid timestamp or capture ID. PayPal still reports `PAYER_ACTION_REQUIRED` and zero captures. Operations shows Ready for Payment rather than Paid. The earlier real popup cancellation and same-order frontend retry evidence below remains valid; no additional cancellation checkout was started in this verification.

### Regression, builds, and wake persistence — PASS

The complete backend suite passed again after the real payment: **104 passed**, including the isolated PostgreSQL concurrency test. Public and Operations TypeScript, ESLint, and production builds all passed. Compose configuration validation (`--quiet` to avoid printing resolved secrets), Alembic upgrade, and all four service health checks passed. Existing deprecation warnings remain.

After the Codespace subsequently slept and woke, all four services were healthy. A new database/provider read again found one captured USD 170.00 payment, the original paid timestamp, two applied webhook receipts, and exactly one completed provider capture with the same ID.

### Security and outstanding verification

Sandbox configuration remains enabled. No live credentials, real funds, secret output, or manual payment/reservation state changes were used. Scans of the served public HTML/scripts (8 assets) and Operations HTML/scripts (10 assets) found no configured Client Secret. Public payment schemas exclude OAuth tokens, Client Secret, and webhook credentials. `.env` is ignored and untracked. Signature verification remains enabled.

No application code fix was needed. All existing Milestone 5 work remains uncommitted/unpushed; only this report was updated in the repository during post-payment verification. Sleep cleared the earlier temporary browser files. The final customer harness was restored under `/tmp/vv-sandbox-browser/`, and the final screenshot, sanitized result JSON, and mode-0600 current-link state are under `/tmp/vv-sandbox-acceptance/`. These are temporary local artifacts; this report preserves the verification evidence in the repository. The customer screenshot was visually inspected.

All requested Sandbox acceptance checks are complete. The replaced original link correctly returned 404; verification used the current link supplied by the user. No token hash or paid-state override was used. No live activation, Milestone 6 work, commit, or push was performed.

## Historical pre-approval acceptance

The following sections record the earlier run before buyer approval. Their pending status statements are superseded by the latest verification above.

## Sandbox configuration and integration fix

The running API was checked before testing and after rebuilding: sandbox environment; client ID present; client secret present; webhook ID present; USD currency. Real sandbox OAuth authentication succeeded.

Reading the existing webhook registration through the authenticated Sandbox API discovered that it pointed to the Codespace root `/`, which returned HTTP 405 for POST. The registration was corrected in place to:

`https://opulent-memory-p77vqgjpw7w6f64jr-8000.app.github.dev/webhooks/paypal`

Readback confirmed the configured webhook ID still matches the registration and its subscribed events were preserved. An unauthenticated HTTPS POST to the corrected URL reached FastAPI and returned HTTP 400, `Invalid PayPal webhook signature`. This proves public ingress and rejection of an unsigned request; it does **not** establish successful verification of a genuine signed payment notification. The `gh` CLI was unavailable, so port reachability was verified directly over public HTTPS.

No application source changes were needed. The initial PayPal browser selector matched both the real and prerender iframes; the temporary test harness was corrected to select the real iframe.

## Real payment preparation and order

| Evidence | Payment booking | Cancellation booking |
| --- | --- | --- |
| Booking reference | `VV-260907-CD7A3D01E30E` | `VV-260907-9B14CA9E7C7B` |
| Reservation ID | 13 | 14 |
| Tour | DEMO M5 Sandbox Tour 1788756270006 | Same dedicated DEMO tour |
| Quantity / snapshot unit price | 2 × USD 85.00 | 2 × USD 85.00 |
| Snapshot total / provider amount | USD 170.00 | USD 170.00 |
| Real sandbox order | PASS | PASS |
| PayPal status at final read | `PAYER_ACTION_REQUIRED` | `PAYER_ACTION_REQUIRED` |
| Local payment status | `created` | `cancelled` |
| Local payment rows | 1 | 1 |
| Provider captures | 0 | 0 |
| `paid_at` / capture ID | Absent / absent | Absent / absent |

Both bookings used dedicated DEMO inventory and `.invalid` customer addresses. Public browser forms submitted actual booking requests. Existing Operations API commands recorded reservation availability checked, supplier contacted, and supplier confirmed, in that order. These were DEMO workflow records; no supplier communication was sent. The real readiness predicate was verified before proceeding.

The Operations UI generated each secure payment link. Tokens use the existing 256-bit random generation, 43-character URL-safe encoding, and hashed database storage. Token-scoped session responses verified the correct booking reference, tour, quantity, and reservation snapshot total. No amount override was sent. Existing request schemas reject browser pricing fields.

Clicking each native PayPal button created an actual order through FastAPI and opened `www.sandbox.paypal.com` at the buyer email/login form. No provider calls or application responses were mocked. Authenticated provider GETs independently verified USD 170.00, zero captures, and `reference_id`, `custom_id`, and `invoice_id` matching the immutable local payment reference associated with each reservation.

## Cancellation, retries, and persistence

The cancellation booking's real PayPal popup was closed at login. The PayPal SDK invoked the existing cancellation endpoint, which returned HTTP 200. The customer page displayed:

> Payment was not completed. Your confirmed reservation is still awaiting payment.

The reservation remained `confirmed`, supplier confirmation remained `confirmed`, eligibility and retryability remained true, and Operations showed **Ready for Payment**, **Cancelled**, and **Unpaid** in the appropriate views. No capture or paid timestamp existed. The reservation itself was never cancelled.

Two concurrent repeated order requests using different client request keys for each reservation returned its same provider order. After the requested stack rebuild, a fresh browser reloaded the cancellation page, reopened checkout through the native PayPal button, and again received the same order. Closing that popup again successfully invoked cancellation. Customer page reload, Operations booking detail reload, and Operations payments reload all retained the expected unpaid cancellation state from PostgreSQL.

Final database/provider reads confirmed exactly one Payment per reservation and zero provider captures. Repeated successful capture and real signed-webhook redelivery tests remain pending; mocked coverage is not presented as real acceptance.

## Webhook and Paid-state checks pending buyer approval

There were zero payment-linked webhook receipts for these bookings at the final read. Actual delivery, successful signature verification, event-to-payment association, state convergence, and duplicate delivery remain unverified. Signature verification remains enabled.

The payment booking showed **Payment Pending** in Operations and local `created` status. Approval alone will not count as payment. Successful FastAPI capture must establish `captured`, `paid_at`, the internal provider capture ID, the derived booking payment-received state, **Payment Received** on the customer page, and **Paid** in Operations. These displays must then be reloaded and checked against PostgreSQL.

To continue, open the payment booking's secure customer link, click PayPal, log in using a **Personal Sandbox buyer account**, and approve **USD 170.00**. The existing frontend calls FastAPI capture in `onApprove`. Do not supply real PayPal credentials. After approval, inspect application/provider state before any retry; use the existing same-order capture endpoint if capture is still needed.

## Automated tests and builds

The full backend suite ran after installing the declared development dependencies in the API container:

`docker compose exec -T -e VV_TEST_POSTGRES=1 api python -m pytest -q`

**104 passed**, including the isolated PostgreSQL concurrency test. Existing deprecation warnings remain. Provider calls in the automated suite are mocked; real-provider evidence is recorded separately above. The suite was run while buyer authentication remained pending, so it does not replace post-capture acceptance.

| Requested check | Result |
| --- | --- |
| Public TypeScript | PASS |
| Public ESLint | PASS |
| Public production build | PASS |
| Operations TypeScript | PASS |
| Operations ESLint | PASS |
| Operations production build | PASS |
| Docker Compose configuration | PASS (`config --quiet`, avoiding resolved secret output) |
| `docker compose up --build -d` | PASS |
| Four healthy services | PASS: API, PostgreSQL, public web, Operations |
| `docker compose exec -T api alembic upgrade head` | PASS |
| `git diff --check` | PASS |

Frontend checks ran inside the corresponding containers against shared repository source. Both lint commands passed with the existing Next.js command-deprecation notice. The subsequent Compose rebuild reused valid cached image build steps and recreated the application containers, preserving the PostgreSQL volume.

## Security, artifacts, and Git

Sandbox only; no live credentials added; no real money; no approval or capture fabricated; webhook verification remained enabled. Client secrets, OAuth access tokens, and webhook credentials were not printed. `.env` remained ignored and was not committed. No Git reset, unrelated discard, database reset, or architecture rewrite occurred. Milestone 6 was not started.

Only dedicated DEMO records were created. They remain available for continuation. Private payment-link/order state is stored in `/tmp/vv-sandbox-acceptance/private-state.json` with mode 0600 under a mode-0700 directory. Browser evidence is in that directory; temporary Playwright harnesses are in `/tmp/vv-sandbox-browser/`. These temporary files are not committed. Browser transport forwards the private frontend hosts to their actual local services; FastAPI and PayPal use their real public HTTPS endpoints.

The pre-existing Milestone 5 work remains uncommitted/unpushed. This acceptance report is newly untracked. The actual fix was to the existing remote Sandbox webhook registration; no code fix awaits commit. No commits or pushes were performed.

**VV MILESTONE 5: COMPLETE**
