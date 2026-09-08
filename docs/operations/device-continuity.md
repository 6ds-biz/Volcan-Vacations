# Operations device continuity

## One authenticated workspace

Phone is for execution, tablet for management, desktop for deep work. This refinement changes `apps/ops` presentation and interactions only. All mutations still use the existing same-origin proxy, authenticated API, CSRF token, role permissions, audit actors and optimistic versions. Appearance remains an account preference. Business records remain server-side; a second signed-in device sees saved changes on its next load. Unsaved form drafts do not synchronize.

The previous owner-bootstrap work remains complete and unchanged. No public site, backend, schema, payment-provider or deployment configuration changes belong to this refinement.

## Navigation and presentation

- **Phone, up to 600px:** Home, Tasks, Bookings, Vendors and More. Items use existing capabilities; Staff receives assigned Bookings and no Vendors shortcut. Tasks opens My Tasks. More contains the permitted full navigation and Profile/appearance. The drawer has an explicit close button, backdrop, Escape dismissal, focus containment/return and an inert background.
- **Tablet:** Compact brand/header and a dismissible full navigation drawer, leaving the workspace width available for management. No phone bottom bar. Owner Business Health, Needs Attention, My Tasks, Vendor Pipeline, Inventory and Recent Payments retain an adaptive two-column workspace at 768–1024px.
- **Desktop:** Existing dark sidebar and light top navigation remain at 1440px, with full tables and the established dashboard layouts.
- **Phone dashboard:** Needs Attention and My Tasks precede summary counts and vendor/inventory work. DOM order matches visual order, including keyboard and screen-reader order.
- **Filters:** Selected execution and management lists have expandable phone search/filters. Tablet and desktop filters remain visible; existing filter logic and API queries are retained.

Selected table rows become labelled, compact two-column operational records on phones: bookings, tasks, suppliers, assigned work, availability, payments and transport routes/schedules. Booking rows omit the desktop amount column and keep reference, customer, experience/date, status and attention. Desktop remains a table. Tablet uses compact tables and scoped horizontal scrolling for dense route/rate information; route service-type duplication is omitted from the tablet overview. Rate histories and administrative sheets retain table scrolling rather than becoming oversized phone cards. Semantic table roles, headers and captions remain available to assistive technology.

## Daily work

- **Tasks:** Start, Wait, Complete and Notes/Edit are visible without hovering or opening action menus. The same versioned task update endpoint handles changes and reports conflicts. Full editors retain assignment, reassignment, priority, due date, related entity, completion and cancellation. Editors opened from long lists scroll into view and focus their first editable control.
- **Bookings:** Summary/attention and section links lead to customer, availability/supplier, payment, tasks, notes/status and history. Existing contact/traveler/trip content remains. Supplier communication history is a disclosure so past events do not dominate the next action. Customer follow-up, availability and supplier confirmation remain distinct operations.
- **Suppliers:** Contact links and note anchors work in both lists and detail. The list includes an open permitted follow-up task when available; task loading/failure is distinguished from no task. Existing relationship controls support outreach stages. Agreements and rate links remain internal.
- **Communication:** `ContactActions` validates supplied email/phone syntax before constructing `mailto:` and `tel:` links. It does not invent country codes, auto-send messages or call any messaging API. WhatsApp remains deferred; a future action can extend this shared component after phone normalization requirements are agreed.
- **Transportation:** Phone filters support origin, destination, vendor and service lookup. Rows show departures, verification and review state. Route detail retains schedule/source context. Tablet editors support routes, services, schedules, verification and dated rate revisions using existing APIs.
- **Availability:** Phone operational rows and touch controls retain all five states: unknown, available, limited, unavailable and closed. Staff uses the existing assigned-booking availability workflow; broader availability remains permission controlled.
- **Payments:** Tablet can review eligibility, snapshot amounts, exceptions and paid time; generate/revoke permitted payment links and open the booking. No provider behavior changed. The existing Operations Partner role already has payment-link and commercial/transport-management permissions; this task neither expands nor removes them. Staff remains denied finance and commercial administration.
- **Users:** Owner tablet controls retain create, role, dashboard profile, active/inactive and last-login review. Last-owner protection remains on the backend.

## Touch, accessibility and tradeoffs

Important touch controls target at least 44px height; inputs use 16px text at touch widths. Checkboxes have larger controls inside touch-sized labels. Bottom navigation has safe-area padding and content clearance. Long-form actions stay in document flow rather than floating over fields or the keyboard. Section anchors have sticky-header clearance. All critical actions are visible or opened by a button/summary; hover changes appearance only.

Warm light, dark and account-level System appearance use the existing tokens and persistence. No device-specific account state, authentication shortcut, new offline cache or realtime system was added.

Dense rate histories may require controlled **table** scrolling on smaller tablets. Ordinary editing is in responsive forms and does not require a 1400px canvas. Desktop remains faster for bulk review. Unsaved edits remain local to their current tab. Validation uses real browsers with emulated viewports/touch capability, not physical iPad/iPhone hardware; physical Safari keyboard behavior is a separate device acceptance check.

## PWA review — recommendation only

A lightweight online-only Add to Home Screen experience is appropriate as a future narrow task: production HTTPS, a scoped web manifest, VV icons and a standalone launch path can improve repeated access. A service worker/offline system is not required for the basic installability direction; browser installation behavior varies. See [MDN's installability guide](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable).

Before shipping that work, verify standalone login/logout/session expiry, CSRF origin handling, deep links, theme initialization, safe areas and lost connectivity on real iOS/Android devices. Keep private API responses and authenticated HTML network-only/no-store. Do not cache customers, tasks, booking details, payment data or credentials offline. No manifest, service worker, install prompt or offline persistence was implemented here.

## Validation

Local screenshots and command logs are in `/tmp/vv-device-review/`; review credentials are temporary and excluded from the repository.

- Full backend suite: **212 passed** with 1970 existing deprecation warnings, including explicitly enabled PostgreSQL integration tests.
- Public `typecheck`, `lint`, `build`: **PASS**. Public source unchanged.
- Operations `typecheck`, `lint`, `build`: **PASS**.
- Visual/accessibility matrix: **210 rendered page/form checks passed**, with no horizontal document overflow, nonempty application error alerts or axe WCAG 2 A/AA / 2.1 AA violations. Owner: 768/1024/1440, Partner: 390/430/768/1024, Staff: 390/768/1024, each in Light and Dark. This includes 16 Owner tablet editor checks. Empty Next.js route-announcer nodes are not application errors.
- System appearance followed browser color-scheme changes, survived reload and remained persisted after logout/login for all three roles. Drawer focus containment, return, Escape dismissal, permission-filtered menus and orientation widths passed.
- Seven real authenticated UI workflow paths passed in a uniquely named disposable PostgreSQL database: Owner at 768/1024, Partner at 390/430, Staff at 390/768/1024. Existing development accounts and business records were not used for mutations.
- Owner paths saved booking notes/status, supplier confirmation, generated/revoked a payment link, created/assigned/reassigned a task, set priority/date, edited vendor notes/relationship, edited transport schedules and dated rates, created/changed/disabled a temporary review user, updated availability and reviewed inventory, agreements and payment exceptions. A second authenticated Staff browser saw the iPad-assigned task through persisted API state.
- Partner paths edited task notes, started/waited/completed tasks, followed related bookings, reviewed contact controls, saved booking notes/status, recorded availability, changed vendor outreach status and reviewed transport schedules. Staff paths saved assigned follow-up and availability checks, completed tasks and were denied finance/user/vendor administration. Logout passed on all seven paths.
- Payment status fixtures were explicitly synthetic manual records in the disposable database. No successful PayPal payment is claimed. Provider credentials were disabled in the review API, provider checkout endpoints were not invoked, and no external message was sent.
- Authenticated actors were present on all 107 audit events checked after the primary workflow runs. Existing auth/CSRF/role/payment tests remain passing.


Task query navigation is reactive: moving between All/My Tasks/shared queues on the same page updates the view without requiring a page reload. Closing an editor removes its task deep link while preserving the queue query.

### Final checks

- **20 additional task-page checks passed** after the same-page query fix across every role/width/theme combination. My Tasks navigation updated without reload; desktop/tablet query changes also updated the selected queue.
- Touch-only menu navigation, supplier note saving at **390 × 450**, contact-control activation (external dialing/mail handling intercepted), 390→768 orientation with draft retention, and a rejected bad-CSRF mutation all passed.
- Final `docker compose config --quiet` and `docker compose up --build -d`: **PASS**. All four normal services healthy after the rebuild.
- `docker compose exec -T api alembic upgrade head`: **PASS**, still `0009_ops_appearance`. No new migration or historical migration edit.
- Post-rebuild public routes `/`, `/tours`, `/plan-your-trip`, `/about`, `/contact`, `/request`, `/pay`: HTTP 200. API health and six featured tours passed. Anonymous Operations `/`, `/tasks`, `/users` returned to the login boundary.
- The isolated review database was removed. Fingerprints of every existing application table matched the pre-review baseline: **development database unchanged**, no changed tables. Generated review credentials were removed from the API container and host review directory. Recreating the normal services stopped the temporary review processes.
- Source changes are limited to Operations UI components/styles and this documentation. No Hotels, Packages, public Transportation, public redesign, email, AI, production media storage, Live PayPal or broad offline caching were implemented. No commit or push was performed.
