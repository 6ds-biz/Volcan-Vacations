> **Historical integration — retired.** The operational canvas described below is no longer active. Use [Public VV integration](public-vv-integration.md) for current architecture, routes, startup paths and scope. Historical records and the reusable core are preserved.

# VV Operations — 6DS Page Builder V1

Owner-authored page templates now use the reusable package in `packages/page-builder`. The existing public website and business services remain outside the builder. Templates are shared by **page type**, not individual booking/supplier/route records; the same template resolves each record's live data. The Operations Partner template is a shared role dashboard layout. Staff retains its existing dashboard and can render permitted detail templates.

## Start and use

```sh
docker compose up --build -d
# Refresh only disposable Ops dependencies/build output when updating the package:
docker compose up -d --no-deps --renew-anon-volumes ops
docker compose exec api alembic upgrade head
```

The Ops build context is the repository root because it installs the local package. Inside its container, Ops is at `/repo/apps/ops` and the package at `/repo/packages/page-builder`. Other services retain their existing paths. Use `docker compose exec ops ...` without assuming the former `/app` path.

Sign in as an active Owner and choose **Edit Page** on a supported page. The Owner dashboard links to **Operations Partner layout** for editing that role's template using the Owner's own permitted live work, without impersonating another user. Choose Structure or a canvas element, then Settings. Add generic widgets from Widgets. Choose Image / Media or Visual Feature and open Media to replace imagery.

Use Desktop/Tablet/Mobile to edit presentation overrides. Adding/removing elements and moving a widget between columns changes shared structure. Preview is read-only. Undo/Redo affects the in-memory draft. **Save Draft** persists privately without changing runtime. **Publish** validates and creates a revision. **Revisions → Restore** creates another published revision. **Reset page to default** loads the source default into the draft; it still needs explicit publication. Exit discards unsaved in-memory edits; save first when they should survive reload. Export/import contains presentation only and cannot bypass server validation.

## Pages and widgets

| Page type | Registered business widgets |
| --- | --- |
| Owner dashboard | Business Health, Needs Attention, My Tasks, Vendor Pipeline, Inventory, Recent Payments, Visual Feature |
| Operations Partner dashboard | My Tasks, Needs Attention, New Bookings, Supplier Follow-up, Availability, Vendor Work, Transportation Lookup |
| Booking detail | Booking Summary, Customer, Travelers, Trip, Availability, Supplier Confirmation, Payment, Related Tasks, Notes, History |
| Supplier detail | Supplier Overview, Contact Information, Relationship Status, Capabilities, Agreements, Rates, Open Tasks, Notes, History |
| Transportation route detail | Route Summary, Origin / Destination, Vendor Services, Schedules, Rates, Verification / Freshness, Related Tasks, Notes, History |

All five also support the seven generic widgets, including Image / Media for a reviewed supplier image/logo or route/destination illustration. The registry rejects business widgets belonging to other pages. Business widgets cannot be duplicated. Existing forms, handlers, workflow rules and protected API queries remain authoritative.

Default Owner composition retains health metrics above the attention/vendor/inventory column and tasks/payments/visual feature column. Partner defaults prioritize Needs Attention and My Tasks on phones, with new bookings, vendor work, availability, supplier follow-up and transportation lookup. Booking defaults retain its summary/contact/travelers/trip, supplier confirmation, payment, tasks, follow-up and history sections. Supplier defaults retain the complete original overview form and foundation/relationship form. Transportation defaults retain route summary/editor, original vendor service cards and history.

Some default widgets intentionally preserve an existing composite form: Supplier Overview includes its original editable contact and notes fields; Relationship Status includes the existing foundation fields. Vendor Services retains its original schedules, rates and editing actions. Optional standalone widgets reuse the same live data/handlers for alternate arrangements. Adding both composite and standalone widgets can repeat displayed information; it does not create a second business system. Supplier rates link to the existing Agreements workflow for editing.

Live context (`booking_id`, `supplier_id`, `route_id`, `dashboard_profile`) is injected at render time. Layouts store no customer details, supplier prices, tasks, payment values or query results. Generic text is presentation copy; authors should not paste private record data into a shared template.

## Media

The authenticated VV adapter resolves stable catalog IDs. Three existing generated, illustrative coastal assets were copied from the public site's established local media library into Ops `public/images/builder`: `pacific-sunset-temporary.webp`, `papagayo-temporary.webp`, `nosara-temporary.webp`. Each is 1536×1024. Provenance: `docs/public-homepage/coastal-media.md`. They are temporary illustrations, not claims of documentary destination photography. No external imagery was downloaded and no new generation was required.

The existing Arenal personality image and active ProductImage references are discoverable but marked **NEEDS_RIGHTS_REVIEW** because they lack asset-level rights metadata. Their existing application use is not converted into an approval. In particular, publishing the Owner source default requires replacing its Visual Feature with approved media, removing it, or completing a genuine rights review in the catalog. Hidden, mobile/tablet and poster references are checked too. There is no user-facing bypass that marks an asset approved.

The picker exposes thumbnails, filename, dimensions when known, MIME type, provenance, rights warning, alt/decorative settings, cover/contain, focal point, ratio, radius, overlay and responsive asset/crop. It accepts no arbitrary image URL. ProductImage dimensions remain unknown rather than invented. A missing asset produces a safe placeholder.

Replace temporary images through reviewed catalog IDs when real VV media arrives. Record provenance, rights, meaningful alt text and dimensions; preserve stable IDs only when the replacement is semantically equivalent. Text/overlays remain separate. The reusable video type supports safe controls, poster, loop and muted autoplay, but VV currently registers images only. Upload, object storage and video hosting are deferred.

## Persistence and migration

Forward revision **`0010_page_builder`**, after `0009`, adds `page_layouts` and `page_layout_revisions`. Prior migrations are unchanged. `page_layouts` stores unique page type, schema version, draft, published layout, optimistic version, authenticated updater and timestamps. Revisions store immutable content, sequential revision number per layout, schema version, actor, timestamp, action and optional restored-from reference.

`GET /ops/page-layouts/{page_type}` returns published layout and version; only Owner receives draft. Owner-only endpoints are `PUT .../draft`, `POST .../publish`, `GET .../revisions`, `POST .../restore`. Media is `GET /ops/page-layouts/media`. Writes require `expected_version`; stale writes return 409 with reload guidance. Publication locks the layout row, validates schema/page/media, writes a new immutable revision and updates the active publication in one transaction. Concurrent first publication is protected by the unique page type and insert-on-conflict before locking. Restore validates the old revision against current rules and publishes a new revision.

Authenticated audit actions are `draft_saved`, `published`, `restored` on `page_layout`. Clients cannot choose the actor. Both ORM guards and a PostgreSQL trigger prevent revision updates/deletes. No booking, supplier, reservation, money or authentication schema was altered. An absent, unavailable or invalid published layout falls back to source-controlled defaults; editor entry is disabled while the layout service is unavailable.

## Security and normal runtime

Owner authorization is enforced server-side in addition to the UI. Partner and Staff have no draft, publish, restore or revision access. A changed dashboard profile or forged actor field grants no rights. Existing session/CSRF/Origin protection remains in force. Widget permissions are checked before mounting and APIs still enforce their existing access rules. Staff cannot acquire transportation rates or history by receiving a layout containing those widgets.

Normal pages import only the renderer/core/runtime CSS. The editor module and editor CSS are dynamically loaded on explicit Owner entry. No handles, inspector, draft history, preview controls or picker are mounted in normal runtime. All business content in editor/preview is inert, including embedded forms. Layout changes write only layout tables and authenticated audit records.

Light/Dark/System remain the existing account preference. The builder uses the same tokens; the established Owner personality image is Light-only. Phone layouts preserve execution workflows and compact navigation. Tablet authoring offers touch handles plus non-drag alternatives; desktop offers more canvas space.

## Temporary Studio retirement

The temporary Owner-only Layout Studio is replaced after the new editor's validation. Its UI, renderer and schema helpers are retired; the old local key `vv-layout-studio-owner-v1` is removed on Owner page entry. Old local drafts are not automatically interpreted as published layouts. Source defaults preserve the real dashboard modules, and normal runtime uses the reusable renderer.

## Validation and next steps

See [validation](validation.md) for the recorded build, backend, browser and workflow results. Browser device sizes are emulation, not a claim of physical iPad testing. Review data and publishing tests use a separate disposable database with PayPal credentials disabled. Source business records are fingerprinted before and after review.

Next: use the new editor to approve final VV layouts, then ingest real photos with rights metadata. Future Nova reuse should supply its own registry, media and persistence adapters. Public redesign, Hotels, Packages, public Transportation, AI, email, customer accounts, payment functionality and live PayPal remain outside this task.
