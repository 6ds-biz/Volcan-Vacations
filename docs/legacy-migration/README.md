# VV legacy migration audit

Start with [migration-plan.md](migration-plan.md), the [catalog](legacy-tour-inventory.md), and the [partner checklist](partner-verification-list.md).

The package contains **13 legacy product records (12 tours + one shuttle)** and an audit of **371 media source URLs**. Product staging is **0 SAFE_TO_STAGE / 11 NEEDS_VERIFICATION / 2 DO_NOT_IMPORT**. Every proposed product is inactive and blocked; no database import was performed.

`VERIFIED_FROM_LEGACY` means a value was present on the old public site. It does not establish that the offer, price, operator, schedule or media rights are current. Missing values remain MISSING in source inventory and null in typed financial/import drafts.

- [Tour data with field provenance](legacy-tour-inventory.json)
- [Staged import review envelope — not executable](staged-import.json)
- [Media register](legacy-media-inventory.md) and [complete media data](legacy-media-inventory.json)
- [Copy/contact audit](legacy-copy-audit.md)
- [Supplier audit](legacy-supplier-audit.md)
- [Current inventory comparison](current-inventory-comparison.json)
- [Proposed redirects](legacy-url-redirect-map.md)
- [Source coverage and request manifest](source-manifest.json)
- [Platform/database validation](validation.md)

Canonical public contact: **info@volcanvacations.com**. A separate payments alias must not replace it. No contact, payment, booking, inventory, availability, schema, public UI or DNS changes were made.

Validate the package without network/database access:

```bash
python3 docs/legacy-migration/validate-package.py
```

The validator reads package files only. It contains no import or application-mutation operation.
