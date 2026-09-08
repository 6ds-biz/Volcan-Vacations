# Widget registry

Each compiled `Definition` supplies type, label, category, icon identifier, default config, config validator, settings fields, supported devices, duplication policy, required context keys, a permission predicate and optional valid page IDs. `RuntimeDefinition` adds a trusted React render function. Never load widget implementations from layout JSON.

The generic registry includes Heading (h2/h3/h4), Text, Divider, Spacer, Metric, Generic List and Image / Media. Generic Metric is static display text, not an authoritative business metric. A consumer should register a live metric widget for real business counts. Settings fields support text, numeric, boolean and fixed choices; validation remains authoritative.

The renderer checks both permissions and required context before mounting a widget. The editor palette also filters by permission and page type. Hidden widgets do not grant access; backend APIs must enforce their own permissions. Required record IDs are supplied at render time and are not stored in layouts.

VV business widgets wrap existing live modules, reject config fields and disallow duplication. Generic presentation widgets can be duplicated. Duplicating a section containing a non-duplicable business widget is rejected, preserving the current draft. See the complete VV registry in `apps/ops/lib/page-builder/registry.tsx` and the [VV guide](vv-integration.md).
