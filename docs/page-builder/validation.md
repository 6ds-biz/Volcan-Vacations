# Validation — 2026-09-08

## Automated suites

- Full backend: **243 passed**, including existing inventory, booking, availability, supplier, authentication, task, transportation and payment tests. Existing datetime deprecation warnings remain.
- New backend builder coverage: 30 schema/API/security/persistence tests plus one PostgreSQL integration test. Concurrent first publication returns one success and one stale-version rejection; the actual migrated immutable-revision trigger rejects raw UPDATE/DELETE in an isolated schema.
- Reusable core: **22 passed**. VV frontend registry/default/permission integration: **6 passed**. Total **28**.
- Invalid schema/imports, unknown widgets/fields, business data injection, page compatibility, responsive settings, movement, undo/redo, source fallback, permission/context/device restrictions and safe media/video configuration covered.
- Backend checks include Owner-only writes, forged actors/profiles, draft privacy, rights/alt/source checks, immutable revisions, restore-as-new, stale versions, CSRF and unchanged business tables.

## Browser validation

Chromium with touch emulation and reduced motion; not physical iPad hardware certification.

| Review | Coverage | Result |
| --- | --- | --- |
| Runtime | Five enabled page types × 1440/1024/768/430/390 × Light/Dark = 50 views | PASS |
| Editor | Five page types × 1440/1024/768 × Light/Dark = 30 views | PASS |
| Media panel | 1440/1024/768 × Light/Dark = 6 views | PASS |
| Partner/Staff | 36 additional role/device/theme views | PASS |
| System | OS Light/Dark changes; persisted template unchanged | PASS |

Final 86-view runtime/editor/media matrix: zero horizontal overflow, zero JavaScript errors and zero axe WCAG 2 A/AA / 2.1 AA violations. Rendered screenshots were inspected for readable headings, spacing, module grouping, image rendering, tablet controls and phone navigation. Automated accessibility checks are not an exhaustive certification.

Actual editor interactions passed: add/duplicate, responsive width/visibility, sibling reorder, cross-column movement, undo/redo, invalid import rejection, valid import/export, image replacement, crop/focal range keyboard control, fit/overlay, responsive image selection, private draft save, publish on all five page types, refresh persistence, immutable revision restore and stale-session rejection. Rights-unreviewed publication was rejected. No business mutation requests occurred during editor/preview operations.

Mouse and CDP touch dragging passed at 1024 and 768, including Escape cancellation, 44px handles and keyboard panel tabs. Live forms are inert during editing/preview. Tests caught and corrected inherited picker flex styling, picker label contrast and canvas presentation class application.

The editor JavaScript chunk was absent from normal runtime requests and loaded only after Owner entry. Exit removed editor UI. Simulated layout-service failure rendered the source default and disabled editing; recovery returned to the published layout. The old Studio UI and browser key were absent after Owner entry.

## Business workflow regression

Seven actual browser role/device scenarios passed: Owner 768/1024; Partner 390/430; Staff 390/768/1024. Across these scenarios, 66 recorded workflow groups covered:

- UI login/logout and role-appropriate dashboards.
- Booking notes/status, supplier confirmation, readiness and availability checks.
- Task creation/assignment/reassignment, notes, start/wait/complete, refresh persistence and another authenticated device seeing the assignment.
- Supplier contact links (no messages/calls sent), notes and relationship changes.
- Transportation origin/destination lookup, schedules, dated rates and rate revision; Staff financial/admin access denied.
- Payment summaries/exceptions and secure payment-link generation/revocation, without checkout.
- Owner user creation, role/profile/activity management; availability, inventory, agreements, customers and trips.

All writes occurred in a separate `vv_builder_review_*` PostgreSQL database. Provider credentials were blank. Illustrative paid/failed records were manual test fixtures, not PayPal results. No PayPal transaction occurred.

Public browser regression passed for `/`, `/tours`, `/plan-your-trip`, `/about`, `/contact`, `/request`, and `/pay#token=invalid-review-token`. The existing Codespaces public origin was mapped to local services for review, preserving its configured Origin/CORS behavior. API-backed request links rendered and the invalid payment-link message remained accurate. Public tour API returned seven existing records; no inventory was hardcoded into the builder.

## Build, migration and service checks

PASS: public TypeScript, public ESLint, public production build; Operations TypeScript, Operations ESLint, Operations production build; Docker Compose configuration and rebuild/start; PostgreSQL/API/web/Ops healthy; Alembic upgrade and current head `0010_page_builder`.

Only disposable Ops dependency/build caches were refreshed with `--renew-anon-volumes ops`. PostgreSQL's named volume was preserved. No prior migration changed. Temporary screenshots and command results were reviewed during execution; this document is the durable validation summary.

The isolated review database and processes were removed. Read-only fingerprints before and after cleanup confirmed **all records in the configured development database remained unchanged**. Test users/customer records and published test layouts existed only in the removed review database. No test template was published into the real Operations database.

Scope remained builder presentation and its layout persistence: no public redesign/builder, Hotels, Packages, public Transportation booking, email, AI, customer accounts, live PayPal, payment changes, paid storage or arbitrary-code widgets.
