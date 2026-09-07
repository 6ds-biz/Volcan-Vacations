# Part 1 validation gate — 2026-09-07

Part 1 was implemented and validated before starting the Part 2 presentation work.

- Authentication: Argon2id, opaque hashed sessions, real login/logout, absolute expiry, active-user checks, session revocation, exact-origin plus synchronizer CSRF checks, same-origin Ops proxy and server-validated protected page layout.
- Users: owner-only administration, temporary-password change requirement, first-owner CLI and serialized last-active-owner protection.
- Permissions: centralized role capabilities; profiles cannot grant authority; staff assigned-booking/task scope and safe projections.
- Tasks: manual CRUD, assignment/status transitions, optimistic concurrency, filters, related-record validation and protected owner/shared queues.
- System rules: transactional/idempotent booking review, supplier-decline alternative, payment-failure owner review and agreement review. Balanced eligible assignees; shared fallback.
- Audit: authenticated actors on new operational history; historical records untouched.
- Migration: `0007_internal_users_tasks` applied to the retained database; repeated `alembic upgrade head` succeeds.
- Backend: **158 passed**, including PostgreSQL regression tests and **14 authentication/authorization tests**. Existing deprecation warnings remain.
- Public: TypeScript PASS; ESLint PASS; production build PASS.
- Operations: TypeScript PASS; ESLint PASS; production build PASS.
- Compose: configuration PASS; `up --build -d` PASS; postgres, api, web and ops healthy.
- Actual Chromium: anonymous protected-page redirect, anonymous proxy denial, login form, authenticated business data, HttpOnly cookie and logout revocation PASS.
- Authenticated Milestone 4 browser regression: public mobile request, availability editor/stale-data handling, supplier contact/confirmation/decline/alternative, concurrent command rejection/idempotency and public privacy allowlists PASS. Six public routes checked at 1440, 900 and 390 pixels.
- Isolated PostgreSQL hosted regression: sequential migrations, demo seed controls, public requests/availability/payment session, API restart persistence and booking idempotency PASS. Validation database removed; retained database unchanged. **Zero provider calls**.
- Preservation: all **205 original business rows**, using every original column, match pre-change SHA-256 fingerprints. All **80 protected files** (public application, migrations 0001–0006 and legacy audit) match their baseline. Legacy migration package validator PASS.
- Browser tests used newly created, clearly marked development data. Test bookings were cancelled and inventory deactivated; history retained. Random-credential internal validation users are temporary and will be retired after Part 2 review.
- Git: changes uncommitted; no push, reset, history rewrite or unrelated deletion.

Evidence logs and screenshots: `/tmp/vv-ops2-review/` (temporary environment artifacts). An initial browser command was rejected by automatic approval review for apparent external credential transmission. The accepted test helper now refuses credential submission to non-loopback hosts; local browser transport maps configured origins to localhost and aborts other network destinations. The completed regression ran locally.

VV OPERATIONS 2.0 PART 1: COMPLETE
