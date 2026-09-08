> The current VV consumer is the public website. See [Public VV integration](public-vv-integration.md). Any Operations adapter examples below describe the retired first integration.

# 6DS Page Builder V1 architecture

`packages/page-builder` is a private, reusable React/TypeScript package. It contains no VV API endpoints, authentication implementation, database client, booking model, or payment logic.

- `core`: versioned presentation types, strict validation, registry contracts, immutable edit history, movement, canonical JSON import/export, media and persistence interfaces.
- `runtime`: validated page rendering, permission/context gates, responsive rendering and provider-resolved media. It imports no editor code.
- `editor`: separately loaded authoring UI, its own CSS, Structure/Widgets/Settings/Media panels, handles, accessible movement controls, preview, history and persistence controls.
- `styles.css`: runtime grid, presentation tokens and media styling. Consumers supply theme tokens.

A consumer compiles its own registry of trusted React widgets and supplies current, authenticated permissions and live record context. Layout JSON only chooses presentation and registered widget configuration. Business widgets continue to use the application's original data and action handlers.

The editor uses native Pointer Events rather than introducing a drag framework. Handles require an 8-pixel activation movement, capture the pointer, support edge scrolling and Escape/cancel, and leave ordinary content scrolling available. Structure controls provide keyboard/touch alternatives for moving elements and changing columns. Undo/redo holds up to 50 local snapshots. Save/publish are explicit; no localStorage autosave is part of the reusable engine.

V1 supports sections containing columns containing widgets. It deliberately excludes arbitrary nesting, HTML, JavaScript, CSS, arbitrary URLs, user-installed widgets and server-generated code. A future schema requires an explicit migration and validation. See [schema](schema-v1.md), [integration](integration-guide.md), and [VV implementation](vv-integration.md).
