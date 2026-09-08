# Schema V1

Authoritative TypeScript contract: `packages/page-builder/src/core.ts`. VV independently validates the same contract on the server in `app/page_layout_schema.py`.

```ts
Page = { schema_version: 1, page_id: string, sections: Section[] }
Section = ElementBase & { columns: Column[] }
Column = ElementBase & { widgets: Widget[] }
Widget = ElementBase & { type: string, config: Record<string, unknown> }
ElementBase = { id: string, presentation: Presentation, responsive: Responsive }
Responsive = Partial<Record<'desktop' | 'tablet' | 'mobile', Partial<Presentation>>>
```

Every element has a unique stable ID. The complete base presentation contains order (0–1000), width (1–12 grid columns), visible, spacing (`none/small/normal/large`), align (`start/center/end/stretch`), density (`normal/compact`), surface (`transparent/base/panel/accent`), container (`full/contained`) and border (`none/subtle`). Overrides may contain only these fields.

A page permits up to 30 sections, 1–12 columns per section, 50 widgets per column and 250 total elements. An empty page is valid; a section must have a column. Unknown fields, versions, nesting, IDs, widget types, incompatible page/widget pairs, forbidden duplicates and invalid configs are rejected. Plain text is escaped by React and disallows HTML angle brackets. No styles, functions, raw URLs or business data fields exist in this contract.

Widget configuration is registry-specific. Media configuration holds asset IDs, alt/decorative status, fit, x/y focal percentages, ratio, radius, overlay, tablet/mobile asset/crop overrides and safe video flags/poster ID. It contains no image bytes or source URLs.

`exportPage` validates then sorts object keys recursively for deterministic JSON. Array order and stable IDs remain intact. `importPage` caps input at 100 KB and validates before changing the draft. `migratePage` rejects unsupported versions unless the consumer supplies an explicit migration; it does not silently reinterpret future schemas.
