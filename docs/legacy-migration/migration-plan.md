# Legacy migration plan — audit only

**No import, activation, schema change, application change, redirect, DNS change, or paid infrastructure was performed.** The legacy site remains online. This package is source material and an inactive review queue, not production inventory.

## Package entry points

| File | Purpose |
| --- | --- |
| [legacy-tour-inventory.md](legacy-tour-inventory.md) / [.json](legacy-tour-inventory.json) | All 13 named products, raw descriptions, field statuses, provenance, conflicts, media and demo comparisons |
| [partner-verification-list.md](partner-verification-list.md) / [.json](partner-verification.json) | 34 question prompts and a prefilled 13-row rate sheet |
| [legacy-media-inventory.md](legacy-media-inventory.md) / [.json](legacy-media-inventory.json) | 371 source URLs, grouped renditions, dimensions, associations, duplicate/broken checks and recommendations |
| [legacy-copy-audit.md](legacy-copy-audit.md) / [.json](legacy-copy-audit.json) | Useful company/destination text, template contamination and editorial treatment |
| [legacy-contact-audit.json](legacy-contact-audit.json) | Every observed address/link spelling and its affected URLs |
| [legacy-supplier-audit.md](legacy-supplier-audit.md) / [.json](legacy-supplier-audit.json) | Unknown operators and the one explicitly named venue lead |
| [current-inventory-comparison.json](current-inventory-comparison.json) | Six seed-tour comparisons and preservation of ten later test products |
| [staged-import.json](staged-import.json) | Inert, blocked drafts with null unverified prices/costs and `active=false` |
| [legacy-url-redirect-map.md](legacy-url-redirect-map.md) / [.json](legacy-url-redirect-map.json) | Proposed destinations/dispositions for all 262 discovered content URLs |
| [source-manifest.json](source-manifest.json) | Public crawl coverage, HTTP results, timestamps, hashes, discovery sources and limits |
| [audit-summary.json](audit-summary.json) | Reconciled counts |
| [validation.md](validation.md) | Platform checks and read-only database comparison |

## What is and is not established

The public WordPress tour endpoint, tour sitemap and rendered catalog identify the same 13 product records: 12 named tours and one SJO → La Fortuna shuttle. The two horseback names may be distinct variants or duplicates; do not collapse them without confirmation. No standalone coffee/chocolate or hot-springs product was found. Transportation and hotel-booking assistance are mentioned on About, but no additional priced hotel/transport catalog was established.

The crawl inspected 262 content URLs (258 HTTP 200, four broken vendor-template paths), all 168 publicly listed WordPress pages, all 13 tour records, six category terms, 11 activity terms, two tags and an empty destination taxonomy. Catalog-layout clones are not additional products. No independent search-traffic/backlink evidence is available.

WordPress tour `content.rendered` is empty for all 13 records, while their excerpts are identical Latin placeholder copy. Rendered page-builder HTML supplied the actual descriptions, schedules, inclusions and galleries. Field provenance identifies whether evidence came from HTML or REST metadata.

`VERIFIED_FROM_LEGACY` means only clearly present on the old site. `LIKELY_VALID` is a coherence assessment, not current commercial verification. No current tour price or supplier cost has been confirmed. A `$` symbol does not establish an ISO currency, adult/child basis, taxes, per-person versus per-vehicle pricing, or current validity. The current demo rafting `$85 retail / $50 cost / $35 margin` remains sample data only.

Public contact is **info@volcanvacations.com**, explicitly confirmed by the user. Do not migrate `info@volcanvactions.com`, theme-vendor email addresses, empty mailto links, placeholder telephone numbers, or the Liverpool address. The separate payments alias was not supplied and must not replace the public address.

## Mapping into the existing model

The audit inspected `services/api/app/models.py`, `inventory_schemas.py`, `inventory_service.py` and `seed_inventory.py`. No schema or migration was edited.

| Model / field | Proposed treatment | Gate or gap |
| --- | --- | --- |
| Supplier.name / supplier_type | Create only after the partner identifies the contracting operator and whether it is a tour operator or transport provider | All 13 operator relationships are MISSING; do not use a fake “Unknown” supplier to bypass the required FK |
| Supplier contact_name / email / phone / website | Use only explicit operator contacts approved by the partner | Customer-facing VV email is not automatically an operator email; Arenal Oasis is only a venue/name lead |
| Supplier.notes / active | Preserve verification/source note; initially inactive | Review duplicate supplier identities before creating records |
| Product.supplier_id | Bind to the approved Supplier | Required by model/API; currently null in every draft |
| Product.name | Preserve observed tour title; approve spelling/variant changes separately | Do not infer title from misleading URL slugs |
| Product.slug | Proposed URL-safe slug stored separately from legacy slug | Confirm final identity, uniqueness and redirect destination; rafting river is unresolved |
| Product.short_description | Write a short summary only from approved facts | All legacy excerpts are placeholders; staged summaries are null, not fabricated |
| Product.description | Reuse verified source copy after editing and partner approval | Only the coherent sloth description is carried into a draft; corrupted descriptions remain audit evidence |
| Product.product_type | `tour` for tours | Shuttle is staged as intended `transportation`; the current tour-only API accepts only `tour`, so it is blocked rather than disguised as a tour |
| Product.category | Choose an approved navigation category | Only the shuttle has a legacy category assignment; twelve use a generic activity term. Analyst category suggestions are explicitly separate |
| Product.duration | Approved customer-facing duration | Sloth 1.5 hours is a coherent source value; repeated five-hour values and contradictions remain blocked |
| Product.retail_price | Current partner-confirmed retail amount only | Legacy price is separate evidence. No `$1`, zero, sample `$85`, or unverified `$60/$65` is inserted |
| Product.supplier_cost | Current approved operator net amount | MISSING for all 13; never fill with zero to pass validation |
| Gross margin | Derive retail minus supplier cost after both are verified | Not a Product input column. No margin inferred from legacy prices |
| Product.active / featured | Both false for every staged draft | Production activation is a separate reviewed action |
| Product.location | Approved location/meeting area | Do not confuse pickup area, route destinations, venue and operator |
| Product.minimum_age | Approved nonnegative integer | “All ages” is retained as raw text; do not assume zero is the agreed infant policy. Repeated 13+ requires verification |
| Product.difficulty | Approved plain-language rating | Source walking/rafting statements are not silently converted into a difficulty scale |
| ProductImage.product_id | Associate after product identity is approved | Do not link assets to a guessed duplicate/variant |
| ProductImage.image_url | Stable approved asset URL/reference | Current model is URL-based; no binary, temporary signed URL, or video is inserted here |
| ProductImage.alt_text | Concise description based on visible approved content | Subject/venue/people must be reviewed; filenames are not alt text |
| ProductImage.sort_order / is_primary | Human-approved gallery order and one primary image | Existing model supports ordered image rows and a unique primary image per product |

### FUTURE FIELD / CONTENT REQUIREMENT

These are documented gaps, not requests to change the schema during this audit:

- Departure schedules and timezone, meeting/pickup points, included hotel zones and surcharges.
- Maximum departure size versus a per-guide ratio; transport seats and luggage/child-seat rules.
- Inclusions/exclusions, packing list, accessibility, restrictions and safety information.
- Cancellation, no-show, weather and refund policies, with effective dates and per-operator exceptions.
- Rate basis, adult/child/private/shared variants, currency/tax treatment and effective dates.
- Supplier contract/rate-sheet provenance and approval history.
- Durable legacy IDs, per-field evidence, migration batch IDs and import mapping. Keep the external audit manifest until a reviewed provenance mechanism exists; do not hide structured data in arbitrary existing columns.
- Video assets, poster/thumbnail, caption/transcript, duration, playback URL and gallery placement.
- Media rights/photographer/release provenance, original filename, digest, variants, storage key and processing status.
- Public tour detail and transportation routes. The current frontend has `/tours` but no `/tours/{slug}` or transportation detail route.

Approved inclusions and packing text may eventually be presented in the existing description if the team explicitly chooses that editorial format. This does not make the missing structured fields exist. Never place prices, policies or schedules in unrelated columns to make an import appear complete.

## Staging gates and proposed import workflow

Product disposition counts: **SAFE_TO_STAGE 0 · NEEDS_VERIFICATION 11 · DO_NOT_IMPORT 2**. The two quarantined snapshots are the copied-content shuttle and the potentially duplicated Horseback & Hot River record. Their underlying services can be reconsidered after correction; this is not a permanent business rejection.

`staged-import.json` is an envelope, **not a valid `/ops/tours` request array**. All products have `import_allowed=false`, `active=false`, `featured=false`, no supplier IDs, null current retail/net/margin values, and no approved ProductImage inserts. It deliberately fails current API requirements until verification is complete. The canonical public email is independently safe to stage and is excluded from product disposition counts.

1. Send the partner checklist and prefilled rate table. Accept corrections, voice notes or existing supplier sheets. Reuse common operator/policy answers and list only exceptions. Record who confirmed each fact, when, source attachment/reference and rate effective date. Do not mark a source-observed field current merely because it was copied into a spreadsheet.
2. Resolve product identities: horseback variants, Balsa versus Sarapiquí, the mis-slugged waterfall combination, Río Celeste scope and shared/private shuttle options. Keep old URL/ID aliases and decide duplicate merges explicitly.
3. Receive the user's media batches using the workflow below. Associate approved assets to approved tour identities, retaining rights evidence and original filenames.
4. Produce a versioned **dry-run import proposal** with approved Supplier/Product/ProductImage payloads, source-to-target IDs, validations, proposed inserts only, unresolved blockers and a before/after preview. Keep the current six seed and ten test products untouched.
5. Review the exact proposal. Missing operator, net cost, current price, required copy, policy or media-rights approval blocks the affected row. Confirm API compatibility separately for transportation and future fields.
6. In a later explicitly authorized import task, back up the target database; use a transaction and stable batch/source mapping; insert approved suppliers, then inactive products, then approved images. Do not overwrite by fuzzy name. Re-running a batch must reconcile mapped source IDs rather than create duplicates.
7. Review inactive inventory in Operations: names, variants, totals/margins, supplier relationships, gallery order and primary image. Independently approve activation. Retire demo inventory only in a separate approved step that preserves booking/payment history.

No import command or script is included or executed in this package.

## User photo/video batch ingestion — no manual mass renaming

The user can deliver original folders or ZIP batches exactly as they are. Preserve original filenames and relative paths. A future ingestion tool should generate asset IDs/storage keys automatically and make a manifest plus contact sheets; the user should only review categories, matches and exceptions.

Use these user-facing categories (multi-tagging is allowed): **Hero; Arenal / Volcano; Waterfalls; Rafting; Wildlife; Sloths; Frogs / Night Tours; Hanging Bridges; Hot Springs; Coffee / Chocolate; ATV; Horseback; Transportation; Hotels; General Costa Rica; VV / Team; Video.**

Suggested batch-manifest columns:

`batch_id, asset_id, original_relative_path, original_filename, sha256, mime_type, byte_size, width, height, duration_seconds, orientation, suggested_tags, approved_tags, suggested_legacy_tour_ids, approved_product_id, photographer_or_owner, permission_reference, people_release_status, captured_at_if_known, duplicate_of, review_state, primary_candidate, alt_text, sort_order, storage_key, published_url`

Future processing sequence:

1. Receive originals into a private staging area. Assign batch IDs and machine-generated asset IDs; preserve the source folder manifest. Do not commit original photos/videos or private metadata to Git.
2. Inspect MIME/file validity, dimensions, orientation, duration and byte size. Use file digests for exact duplicates. Flag perceptual/sequence similarities for review; keep originals and never delete on a similarity score alone.
3. Suggest categories using filenames, folder context and optional visual review. Present thumbnails and short video previews grouped by category/tour. Uncertain subjects stay unassigned; no supplier identity is inferred from images.
4. Ask the user/partner only for uncertain matches, rights, identifiable-person consent, keeper selection and primary/gallery choices. One selection can apply to a folder/batch, with per-file exceptions.
5. Retain archival originals. Produce orientation-corrected, responsive image derivatives and lightweight previews; remove unnecessary public EXIF location/private metadata. Keep original attribution/rights metadata privately. Generate draft alt text for review.
6. Upload approved derivatives in a later storage task. Publish stable URLs only after rights and product association checks; use the existing ProductImage fields for image galleries. Keep rejected/uncertain media private and out of production.

## Media architecture recommendation

Keep the existing URL/reference contract for ProductImage. A future upload path can issue authorized, short-lived upload permissions to persistent cloud object storage, process uploaded files, and return stable CDN-backed references. Originals and public derivatives should have separate access policies. ProductImage should reference the approved public derivative, not a Codespace `/tmp` path, a Git blob, or a short-lived download URL.

Evaluate storage, request/egress costs, backups, retention, image/video processing and access controls against the expected library size before choosing a provider. No vendor account, bucket, CDN, paid service, database table or upload endpoint was created here. Persisting galleries already fits ordered ProductImage rows; upload metadata, video references and rights tracking need a separately reviewed design.

## Video strategy

The audit found 18 publicly listed MP4s named as WhatsApp clips; metadata reports landscape 848×480 and portrait 464×832 variants. It also found five demo YouTube/Vimeo URLs referring to four distinct external videos. See the media JSON for exact URLs, source-page association and metadata. Uploaded clips were HEAD-checked only; subject, audio, playback and video-byte duplication remain unverified. Ask for originals and batch-review previews before assigning them to actual tours.

- **Homepage:** consider a short, muted, optional loop only after choosing a relevant high-quality original. Provide a poster fallback, pause control and reduced-motion behavior. Never autoplay audio; avoid downloading a large hero video on constrained/mobile connections.
- **Rafting and waterfalls:** user-started clips can explain the experience and terrain after safety/route claims are checked.
- **Wildlife/sloths/night tours:** short selected clips can illustrate the experience without promising sightings. Captions/transcripts should cover any explanatory speech.
- **Tour galleries and destinations:** use poster-first, lazy-loaded, user-started video with playback controls. Keep videos separate from ProductImage until a supported reference/asset design is approved.
- Do not place large MP4s in Git or deploy them as Vercel/local application files without evaluating bandwidth, persistence and playback delivery. Consider processed multi-resolution streams or an appropriate video host/CDN in a later task.

## Legacy retirement and DNS cutover

The old website must remain online until all of these are complete:

1. New site deployed permanently on the intended hosting/domain setup.
2. Verified real inventory migrated and reviewed.
3. Approved real media migrated to persistent delivery.
4. Booking workflow tested in the production configuration.
5. PayPal production readiness separately completed and authorized; Sandbox acceptance does not authorize live activation.
6. Operations authentication enabled and tested for UI/API access.
7. Transactional email configured, tested, and using the approved public/payments addresses appropriately.
8. Redirect map completed against real destination routes; valuable legacy pages/assets preserved.
9. DNS cutover and rollback planned, including TTLs, certificates and any existing email/MX dependencies.
10. New domain, bookings, payment/webhook endpoints, email and redirects verified before old hosting is retired.

Before any eventual cutover, back up the legacy content/media/configuration and document rollback. Coordinate a final delta crawl, stop uncontrolled legacy/new inventory edits during the reviewed import window, and monitor redirects/404s and operational flows after launch. **No Hostinger DNS or old-hosting changes were made in this audit.**

## Scope and crawl limits

Discovery used public robots/sitemaps, public WordPress catalog/media/taxonomy endpoints, rendered HTML, and recursively discovered same-site content links with no forms or login. Three fetch workers and cached results bounded load. The content frontier was exhausted after three rounds. One author/user sitemap was deliberately excluded because author-account enumeration is not needed for a business-content migration. All fetched content remains untrusted source data.

The manifest records failed URLs and provenance. Public data does not reveal private/draft/deleted products, authoritative supplier agreements, original media ownership or actual SEO traffic. All ten referenced stylesheets were inspected; decorative/font/theme-background URLs found only in CSS are separately recorded in `legacy-stylesheet-audit.json` and are excluded from migration-candidate counts. Both public transportation `To` and `From` taxonomies were also checked and are empty. Dynamic JS-only content may remain outside discovery. Those limitations do not justify inventing data or declaring an asset licensed/playable.

Raw HTTP bodies and downloaded image checks are cached under `/tmp/vv-legacy-audit/`; those temporary files can disappear when the Codespace sleeps. The committed-ready package preserves extracted values, useful copy, URLs, retrieval timestamps, hashes and checked media metadata. No media binary or credential is included in the audit directory.
