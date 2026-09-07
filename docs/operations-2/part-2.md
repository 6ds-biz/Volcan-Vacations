# Operations 2.0 — Part 2

Part 2 began only after the [Part 1 validation gate](part-1-validation.md) passed. The implementation uses the requested compact operational concepts; it imports no Nova source code or dependencies.

## Workspace

The sidebar groups Work, Inventory, Vendors, Finance and Admin. Navigation derives from the same capabilities returned by the authenticated API. Unsupported areas are hidden. A compact topbar provides the current user, profile/password, owner settings and logout. Below 850px, a labeled navigation toggle opens the sidebar; selecting a destination closes it.

The interface uses the approved near-black/charcoal, gold and ivory values. The real VV logo asset uses the same gold alpha-mask treatment as the public site. Headers use a 32px tile, 17px icon and 8px radius. Shared status modules, filter toolbars, tables, empty states and form sections replace the previous large white panels. There are no decorative UI gradients, green surfaces or new public-site changes.

Tables preserve meaningful columns and use contained horizontal scrolling when necessary. Booking links and task edit controls appear in the first column. Amounts and date fields do not break across lines. Tables have captions and column headers; navigation and scroll regions have labels. Native forms, details/summary menus, focus rings, textual statuses and reduced-motion rules support keyboard and assistive technology use. Operations also sends frame-embedding, MIME-sniffing and referrer-policy protections.

## Dashboards and count definitions

Profiles select emphasis, while capabilities continue to limit both server data and visible controls.

- Owner: business health, attention queues, active vendor pipeline, inventory, six personal tasks and recent captured/refunded payment activity. No unsupported revenue/margin aggregates.
- Operations Partner: daily bookings, supplier responses, availability, vendor work, personal/shared tasks; no user or security administration.
- Staff: own tasks, scoped booking follow-up and reservation availability checks. Assigning the Owner profile to staff cannot reveal company-wide financial or administrative data.

`GET /ops/dashboard` computes values from persisted application records. No counts are placeholders. Empty data produces zero/empty states.

- New requests: reservation status `new`.
- Awaiting supplier: active reservations whose supplier state is `awaiting_supplier`.
- Ready for payment: supplier-confirmed, payable bookings with no captured payment and no cancelled/completed trip.
- Paid bookings: bookings with recorded capture time; refund status remains visible in the booking and payment details.
- Tour review: active tours missing a primary image or summary. Featured and active/inactive counts use their stored flags.
- Supplier relationship modules: persisted relationship states. Follow-up means active suppliers in `contacted` or `rates_requested`; it is not an invented overdue deadline. Dashboard vendor counts explicitly cover active suppliers. Destination filters use mapped product destinations.
- Payment pending: pending/created/approved. Paid payment records: captured. Exceptions: failed or flagged for reconciliation. Ready lists confirmed unpaid bookings, including those with no Payment row. Refund states remain separate.
- Availability modules describe the current filtered result set. Upcoming stale checks use the existing 24-hour freshness rule. A check never constitutes supplier confirmation.
- Task open states: open/in_progress/waiting. Due-day filtering uses UTC; displayed timestamps use the browser's local time. My Tasks orders urgent, overdue, due today and upcoming work, limited to six entries.

Needs Attention displays separate named queues, without a combined total that would double-count related work. Booking reasons are mutually exclusive. A task and its underlying business exception can both appear in their distinct queues. No supplier-response deadline or automated expiration scheduler was invented.

## Connected pages

Bookings have search, status, supplier/date filters and real status modules. Detail retains customer, travelers, trip, snapshot pricing, availability, supplier confirmation, payment and internal notes, and adds assignment, related tasks and authenticated booking history. Existing supplier history shows the authenticated actor; historical operator/system labels remain valid.

Tasks support creating, editing, assigning, starting, waiting, completing, reopening and cancelling, with version conflicts surfaced. Owner exceptions stay in the owner queue. Staff can only manage their own permitted work. Related links connect to bookings, suppliers, tours and permitted record lists.

Suppliers show service capabilities, relationship, contact, agreement count and status. Supplier detail edits the existing commercial relationship/capability foundation. Tours show mapped destination, supplier, retail, cost and margin; these remain internal. Tour detail retains image management and allows editing destination mappings. Availability retains its original editor, stale indicators and confirmation distinctions.

Payments expose current activity and exceptions without secrets or new charge controls. Customers and trips are simple internal read views linking existing records. Agreements are a read view of the existing append-only commercial references and rates; this does not implement a pricing engine or new approval workflow.

Owner-only Users manages names, roles, profiles and active status; owner-created accounts require a temporary-password change. Changing the selected role defaults the profile appropriately, while explicit profile selection remains possible. Profile/password is available to every user; deployment configuration remains managed on the host.

## Boundaries

The public website, public data allowlists, historical prices, supplier confirmation, sandbox payment rules and existing audit records are preserved. No new PayPal order or capture is required for this review. Live activation, Transportation/Hotels/Packages pages, customer accounts, email/SMS, AI and production media storage remain deferred. Supplier service classifications are existing reference fields, not new booking products.

Hosted Operations is still an explicit deployment opt-in. This work does not deploy it publicly. Create the real first owner with the secure CLI documented in Part 1; validation accounts use random temporary credentials and are retired after review.

## Validation

See `part-2-validation.md` for final results. `scripts/operations2-review.cjs` reads private temporary test-user/fixture files, checks the three roles at 1440/1024/768, exercises actual forms and runs axe WCAG A/AA checks. Its browser transport rejects non-localhost destinations. The adapted Milestone 4 regression similarly uses localhost credentials and maps configured public origins to local transport. These scripts never establish PayPal sandbox success from mocks or initiate another charge.
