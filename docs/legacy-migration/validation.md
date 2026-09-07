# Audit validation

## Platform — PASS

No application source, schema, migration, environment, inventory, booking, payment, availability, public copy, Operations behavior or DNS was changed. All generated repository files are under `docs/legacy-migration/`.

| Requested check | Result |
| --- | --- |
| Public `npm run typecheck` | PASS |
| Public `npm run lint` | PASS; no ESLint errors/warnings |
| Public `npm run build` | PASS |
| Operations `npm run typecheck` | PASS |
| Operations `npm run lint` | PASS; no ESLint errors/warnings |
| Operations `npm run build` | PASS |
| `docker compose config --quiet` | PASS; resolved credentials not printed |
| `docker compose ps` | PASS; API, PostgreSQL, web and Operations healthy |
| Package JSON/reference/staging validation | PASS |
| `git diff --check` | PASS |

Frontend checks ran inside their corresponding Compose containers against the shared repository source, using `npm run typecheck && npm run lint && npm run build`. Next.js emitted the existing `next lint` command-deprecation notice; the lint checks themselves passed. This documentation/data-only task did not require another payment flow, backend mutation or schema migration.

## Database — unchanged

The baseline and final database snapshots used PostgreSQL transactions explicitly set to **READ ONLY**. For every one of the 13 application tables, both the row count and an aggregate digest of all row content were compared. **All 13 matched.** The package retains only aggregate counts/digests, not private customer/payment rows.

| Table | Rows before and after |
| --- | --- |
| products | 16 |
| suppliers | 12 |
| product_images | 12 |
| reservations | 14 |
| trips | 14 |
| customers | 14 |
| travelers | 14 |
| trip_travelers | 14 |
| availabilities | 5 |
| supplier_confirmation_events | 38 |
| payments | 2 |
| payment_webhook_events | 2 |
| payment_refunds | 0 |

See [database-baseline.json](database-baseline.json) and [validation.json](validation.json). No inventory was imported, activated, overwritten, deactivated or deleted; no supplier cost or historical booking/payment value changed. No demo cleanup was performed.

## Extraction/package checks

`python3 docs/legacy-migration/validate-package.py` validates JSON parseability, unique source IDs, field status/provenance references, media associations, partner question counts, redirect coverage, canonical contact, and staging gates. It reads files only and performs no network or database operation.

- 13 tour/product records reconcile between the public REST catalog, sitemap and rendered page discovery.
- 12 named tours and one shuttle remain separate; the horseback duplicate/variant is flagged rather than silently merged.
- Every field has an allowed verification status; missing values stay MISSING, and all source-present fields retain a source URL/hash.
- All staged current prices, supplier costs and margins remain null. All product drafts are inactive, not featured, and blocked from import; no approved image or supplier inserts are staged.
- 371 library/page-media source rows reconcile with the media summary. Generated image renditions are grouped. Ten additional referenced stylesheets were inspected; decorative CSS-only URLs are recorded separately in [legacy-stylesheet-audit.json](legacy-stylesheet-audit.json), without counting them as migration candidates.
- Exact duplicate images were identified by fetched-byte SHA-256, not by filenames alone. Videos were HEAD-checked; playback and byte-duplicate checks were not claimed.
- 34 partner question prompts reconcile to five shared prompts plus 29 tour-specific prompts; the shared rate question covers a separate 13-row table.
- All 262 discovered content URLs have a proposed redirect/retirement disposition, with `implemented=false`. Planned product detail routes are correctly marked not yet implemented.
- The canonical email is `info@volcanvacations.com`; misspellings/vendor emails/empty links appear only as flagged legacy evidence.

## Discovery and operational limits

Public source observations are time-specific and do not prove current commercial accuracy or image rights. The media checks used bounded image downloads and video HEAD requests. External video HTTP 200 indicates reachability, not playable/owned VV content. No private WordPress access, analytics/backlink export, supplier contracts, or original user media collection was available or fabricated.

The read-only crawler initially reached its reviewed page bound because the site publishes many template/layout variants; the bound was extended and the frontier exhausted after three rounds. A preliminary database query referenced a nonexistent singular availability table; it failed in a read-only transaction, and the completed baseline used the exact existing SQLAlchemy table names. A package consistency review corrected the summary's WordPress video counting (`mime_type`, not its generic `media_type=file`) and retained the full partner rate-row array. Final results above reflect the corrected package.

## Git

Before the audit, `git status --short` was clean at **0f06ac2 — Complete VV Milestone 5 PayPal sandbox payments**. The requested before/after status, log and diff-stat checks were run. At completion, only `docs/legacy-migration/` is new/untracked; no tracked application file differs. Untracked audit files do not appear in ordinary `git diff --stat` until staged. Nothing was committed or pushed.

**VV LEGACY MIGRATION AUDIT: COMPLETE**
