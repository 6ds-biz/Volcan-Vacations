# Portable layout format v1

The standalone tool wraps the existing core schema in an explicit project/page envelope:

```json
{
  "schema_version": 1,
  "project": "volcan-vacations",
  "page_type": "home",
  "sections": []
}
```

`sections` contains the existing core Section → Column → Widget hierarchy, stable IDs, complete presentation objects, responsive overrides, registered widget types and strictly validated configuration. Each section needs 1–12 columns; pages have at most 30 sections and 250 total elements. The core registry restricts widget compatibility and singleton application widgets.

The wire format intentionally omits core `page_id`: the selected project's default maps `page_type` to that identifier (for example `home` → `public-home`). The core remains version 1 and unchanged. **Standalone portable JSON is not the existing VV API draft payload.** A later explicit integration must validate this envelope, map page identity and convert coordinates before writing any draft. No such endpoint is added here. Raw legacy core JSON is rejected because it lacks project/page metadata.

## Media and responsive values

Media are stable IDs in `config.media.asset` (or `config.asset` for generic Media), with optional poster/tablet/mobile references. Source URLs, binary files, base64 and media metadata are not embedded. Null clears a reference. If an editorial media override is absent, the source-controlled widget supplies its original image. Unknown or unapproved references are rejected before export and after import.

Wire focal coordinates `x` and `y` are normalized **0 through 1**, including tablet/mobile overrides. The existing core and editor use percentages 0–100. The portable adapter converts in both directions; this distinction is part of the v1 contract. Device presentation uses the core `desktop`, `tablet`, `mobile` overrides: width 1–12, order, visibility, bounded spacing, alignment, density, surface, container and border. Missing override values inherit base presentation; structural edits are shared across devices.

## Validation and determinism

`src/portable.ts` performs:

1. A 100 KB UTF-8 limit, JSON syntax and exact envelope-key checks.
2. Schema version, configured project and selected page-type checks.
3. Core validation of nesting, IDs, widget/page compatibility, complete and responsive presentation, bounded text, links and media settings.
4. Normalized-coordinate conversion on import, followed by full core validation again.
5. Project media approval/source checks and canonical public-contact checks.

Export repeats full validation, converts media coordinates, recursively sorts object keys, preserves array order/stable IDs, and writes two-space JSON with a final newline. It adds no timestamps or random metadata. IDs are generated only when creating or duplicating elements. A valid export → import → export is byte-for-byte stable; edited defaults round trip to the same core layout.

Unknown configuration keys prevent fields such as customer records, supplier costs, prices, credentials, raw HTML or scripts from entering the layout structure. Inventory samples and application context are never serialized. Public-facing text fields are for public design content only; validation cannot infer every kind of private information someone might type in prose.

Schema changes require an explicit future migration. Do not reinterpret a version-1 export or silently import another project's layout.
