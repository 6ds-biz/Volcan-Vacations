# Operations appearance

Operations supports Light, Dark and System. Dark remains the default for existing and new accounts. Every role can change Appearance under **Profile & password**; owners also have it in Settings.

## Preference and rendering

The existing authenticated user record owns one `appearance` field, constrained to `light`, `dark`, or `system`. Forward migration `0009_ops_appearance` follows Transportation revision `0008_transportation_foundation`. Previous migrations are unchanged.

`PUT /ops/auth/appearance` changes only the current user's preference. It uses the existing session, Origin, CSRF and temporary-password requirements. It cannot select another user or alter permissions. `/ops/auth/me` supplies the saved preference to the server-rendered layout, including on subsequent sign-ins and other browsers.

The `vv_ops_appearance` cookie is a non-sensitive display hint for signed-out screens, not a separate authoritative preference store. An authenticated database preference takes precedence. There is no credential or bearer storage in JavaScript. System mode resolves the OS scheme before paint and subscribes to subsequent scheme changes. Failed preference saves leave the current setting intact and display an error.

## Visual system

The supplied `docs/design/vv-operations-light-reference.png` guides light mode: warm `#F7F4EE` workspace, white and `#FBFAF7` surfaces, `#101416` text, neutral borders, restrained `#D7A84B` gold, and compact `#071011` navigation. Gold text uses a darker `#815A13` for contrast on white. Semantic blue, amber, green and purple are confined to small metric tiles; attention rows have pale red. No large green UI surfaces.

At desktop widths, primary links run across the top; secondary, permission-filtered links live in More. Below 1300px a collapsible navigation keeps every permitted destination accessible. Dark mode retains the approved sidebar, compact header and near-black/charcoal/gold/ivory appearance.

Owner modules use the existing dashboard API, including real booking, supplier, inventory, task and payment counts. Existing urgent/overdue/today/upcoming task ordering is unchanged. One Owner-only visual uses an exact copy of the existing public Arenal asset; no public files are edited. Operations and Staff retain their distinct permitted work. Tables retain compact rows and keyboard-scrollable regions. Forms and Transportation editors inherit the same theme.

Intentional differences from the reference: the real VV logo and existing system typography are retained; the existing Arenal photograph replaces the mockup's coast; no nonexistent Reports destination is added; More preserves secondary destinations; dark navigation structure is unchanged.

## Verification

The backend suite includes account-isolated preference persistence, all three roles, valid value enforcement, rejection of other-user targeting, anonymous access, Origin and CSRF checks. The browser acceptance matrix covers the requested Owner / Operations Partner / Staff pages in both themes at 1440, 1024 and 768px, plus System changes and profile/navigation keyboard behavior. Test users are temporary and must be retired with sessions revoked after inspection.

No PayPal transaction is needed or permitted for appearance validation. Business data, public design, Transportation inventory and permissions remain unchanged. Hotels, packages, public Transportation, email, AI and live payments remain out of scope.

### Acceptance results — 2026-09-08

- Full backend regression: **212 passed**, including four new appearance test cases.
- Public TypeScript, ESLint and production build: **PASS**; `apps/web` unchanged.
- Operations TypeScript, ESLint and production build: **PASS**.
- Requested 72-view matrix: **PASS**, with zero axe WCAG 2 A/AA and 2.1 AA violations, page errors, or horizontal document overflow. Screenshots were reviewed against the reference.
- 33 additional page/form views and 13 final navigation/Transportation checks: **PASS**. Keyboard profile/More menus, table scrolling, actual temporary-user sign-in, persisted preferences and live System scheme changes were exercised. No screen-reader certification is implied by automated checks.
- Compose configuration/rebuild and all four service health checks: **PASS**. Migration `0009_ops_appearance` applied without recreating the database.
- 598 pre-existing records checked by non-secret fingerprints: **unchanged**, with none missing. Prior migrations and public source/assets unchanged.
- No PayPal transaction initiated. Existing payment regression coverage passed; no new real provider claim is made.

Detailed local logs, screenshots, and JSON results are in `/tmp/vv-light-review/`. Temporary validation accounts are retired after acceptance, their sessions revoked, and their credential file removed. No real user's credentials or preference are changed.
