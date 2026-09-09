# Future roadmap

## Phase 2 — backups (deferred)

Phase 1 stores working pages and bounded undo/redo only in memory and saves through deliberate JSON export. No autosave or backup implementation is included.

A later storage adapter may add autosave, named snapshots, history, restore, cloud backup and retention. Keep these separate from rendering and the portable schema. Define project/page identity, version/conflict handling, recovery behavior and retention before adding storage. Persist validated design data only; never credentials, customer/payment data or private business records. The existing core history and optional revision adapter do not imply that cloud backup exists.

## Reusing the engine for another project

Add a project module implementing `DesignProject` with:

- A stable ID, display name, public contact policy and page types/filenames.
- Approved tokens and human-readable surface labels.
- Widget validators/field definitions and runtime renderers.
- Versioned source/default layouts.
- A media provider with synchronous reference lookup and source approval checks.
- A theme/canvas component and safe preview context.

Pass that configuration to `Builder`. The workspace, core grid, history, movement, media controls and portable validation remain shared. A later project picker can choose among registered definitions; only VV is implemented in Phase 1. Project-specific live-data boundaries belong inside the project adapter, like VV's standalone sample inventory substitution. A future extraction of VV presentation into a shared package can replace current source imports without forking the builder engine.

## VV draft import/publish (deferred)

Later VV integration will import portable JSON as a draft, validate permissions/schema/media/project, preview against real public context and publish through VV's controlled workflow. Production publishing does not belong in this standalone design app. Only after the standalone tool is proven should a separate cleanup remove obsolete live-editor handoff code.

## Customer “Request a Change” (concept only)

A future customer website could let a customer select a visible page element and describe a requested change. AI could capture page URL, project/page identity, stable element ID, component context and a visual reference, then create a support ticket for review. Selection should capture only the minimum public context and respect authentication/privacy boundaries.

This milestone implements no customer selection overlay, AI endpoint, ticket integration, automatic change execution or messaging. A later specification must define consent, ticket routing, access control, review and feedback before implementation.
