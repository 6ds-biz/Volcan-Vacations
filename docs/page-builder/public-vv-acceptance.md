# VV public Page Builder — Part 3 acceptance

This completes the public consumer of the existing 6DS core. Parts 1 and 2 remain intact. Operations manages Website → Pages / Media; operational pages are not editable canvases.

## Owner workflow

1. Sign in to Operations as an active `owner_admin` and open Website → Pages → Edit.
2. Edit the public canvas, Save Draft, and use Preview at Desktop, Tablet or Mobile.
3. Select Publish and confirm the public change. Unsaved changes disable Publish.
4. Open Revisions to see number, timestamp, authenticated actor, action and Current status.
5. Restore an older revision and confirm. Restore publishes a **new** revision and replaces the current draft. Export unsaved work first if it must be retained.

There is no automatic publication. A source default has no historical database revision until explicitly saved and published. Reset page to default loads the source layout into the draft; it still requires Save Draft and Publish. The initial baseline in the isolated acceptance test was explicitly published before testing restore.

## Atomic publication and history

Both authenticated management and page-scoped editor publication lock the existing PageLayout using the expected version. The submitted layout must equal the saved draft. The server validates that persisted draft again: complete schema, page/widget compatibility, responsive settings, safe links, media references/rights, bounded presentation and public field allowlists.

One transaction inserts the immutable revision, updates draft and published pointers, increments the version and records the authenticated Owner audit actor. Success is returned after commit. Validation or persistence failure rolls back all these writes. There is no independent browser-authoritative publish payload. A lost response can be resolved by reloading; retrying the old version cannot create another revision.

PageLayoutRevision retains complete JSON, schema version, layout identity, number, timestamp, actor and action. Restore records `restored_from_id`; intermediate revisions remain. Current is the latest revision under this serialized publication contract. Existing ORM guards and the PostgreSQL immutable-history trigger from migration 0010 prevent revision updates/deletes. No historical migration was edited.

## Concurrency and errors

Draft saves, publication and restore all share the same version counter and row lock. Two Owner editors opening version X cannot silently overwrite each other. After B saves/publishes, A receives HTTP 409. The editor retains A's in-memory work and offers Reload latest saved layout. Export A's work before reloading if needed, then review/reapply it. Automatic merging is intentionally unavailable.

A failed save/publish displays a safe error rather than provider/server debug data. Rights and invalid-media errors identify the corrective action. Expired or revoked edit sessions require re-entry through Operations. A connection timeout instructs the Owner to check the latest persisted state before retrying.

## Security and privacy

The existing handoff is one-use, expires after 60 seconds and is removed from the URL fragment during exchange. The page-scoped credential lasts 15 minutes, uses an HttpOnly SameSite=Strict cookie (Secure on HTTPS), and stays tied to the original internal login session. Server checks enforce account activity, exact Owner role, password-change requirements, expiration, parent-session validity and page scope for every private operation.

The Next.js proxy permits only draft, publish, revisions and restore. Writes require same-origin JSON; credentials are forwarded server-to-server, never returned to browser JavaScript. Partner, Staff and public visitors cannot manage website layouts or obtain an Owner handoff. Normal role permissions and dashboards remain unchanged.

Public layout responses contain only validated published presentation or `page: null`. No draft/version/actor/session metadata is returned. Public media is an approved-only field allowlist; provenance and private management metadata remain in management. JSON cannot store supplier costs, margins, private contacts, customers, travelers, payment references, internal users or live inventory truth. Owner-authored plain text still requires editorial review; an allowlist cannot determine whether manually typed prose is confidential.

## Media and video

Every selected reference, Tablet/Mobile override and poster is rechecked on publication and public delivery. Missing/invalid references, unsupported public sources and `NEEDS_RIGHTS_REVIEW` block publication. No asset is promoted by inference. Existing source-default photography retains its established policy; publishing a new explicit override requires approved catalog media.

Meaningful media requires bounded alt text from the saved override or reviewed catalog; explicitly decorative media permits empty alt. Filenames are not synthesized as alt. Focal coordinates, fit, overlay and responsive asset IDs remain in presentation JSON. Reset removes the override and restores the source block. Management shows actual source/provenance and rights.

Approved local MP4/WebM references are supported by the existing provider contract. Posters must be images; controls remain available; autoplay requires muted audio and honors reduced motion. Unsupported references and autoplay with audio are rejected. No actual production video, storage, transcoding or bulk ingestion was added.

## Public runtime, fallback and SEO

Public routes load the lightweight renderer, validated presentation and public widgets. Editor code, Navigator, media controls, revisions UI and draft credentials remain on the private editor route. Approved catalog media can now resolve synchronously for server-rendered images and alt text; asynchronous providers remain compatible.

Missing, unavailable or invalid published layouts resolve to source-controlled defaults on all six page types. The renderer also validates and accepts its known-valid fallback. Business widgets keep live API context: the shared Tour Detail Template receives each active Tour; prices, availability and request links never come from layout JSON.

Existing page titles, descriptions, tour canonicals, public text and link semantics remain. Generic headings are H2–H4 and primary hero widgets cannot be duplicated, preventing uncontrolled extra H1s. Owners should retain the primary title when arranging a page. Canonical behavior outside tour detail remains unchanged; this release does not introduce a new SEO configuration system.

Public source imagery retains existing responsive/lazy-loading behavior. Builder media uses local catalog assets, bounded layouts and lazy image loading. This is a regression review, not a Lighthouse/Core Web Vitals certification. No speculative optimization or heavy media infrastructure was added.

## Validation record

The Codespace stopped after controlled publication acceptance. Those completed tests were preserved and were not restarted on resume:

- Full backend suite: **335 passed**, including rollback, immutable revisions, restore-as-new, stale publication, roles, links/media/privacy and business regressions.
- Controlled production-browser publish/restore at **1440, 1024 and 768px**: PASS. Draft remained private; public heading/image/order changed after Publish; restore created another revision and restored the baseline.
- Two separate Owner sessions: B published; A received **409**, reloaded and saw B's work.
- Deliberately unreviewed draft media: publication returned **422**, public state unchanged.
- Partner/Staff Website denial and sampled normal Operations access: PASS.
- Automated WCAG A/AA checks of revisions/editor states: no reported violations; no application browser errors.

Final checks after resume:

| Check | Result |
| --- | --- |
| Additional public-page PostgreSQL concurrent-first-publish/immutable-trigger case | 1 passed; 336 backend cases covered across the prior 335-test run and this added case |
| Builder/public frontend tests, including renderer fallback | 41 passed |
| Operations Website navigation regression | 1 passed |
| Public TypeScript / ESLint / build | PASS / PASS / PASS |
| Operations TypeScript / ESLint / build | PASS / PASS / PASS |
| Compose config / build / service startup | PASS |
| Four service health checks after cleanup | API, PostgreSQL, web and Operations all healthy |
| Alembic upgrade head | PASS; 0011_website_edit_sessions; no new migration |
| Home at 1440 / 1024 / 900 / 768 / 430 / 390 | PASS, rendered screenshots inspected |
| Tours / Tour Detail / Plan / About / Contact at 1440 / 768 / 390 | PASS, rendered screenshots inspected |
| Public runtime | 21 combinations, zero overflow/browser errors; six featured and seven API-backed tours |
| Public bundle inspection | 14 unique loaded JavaScript files; no editor-toolbar/publication code |
| Public SEO | Existing titles/descriptions retained; one H1 per reviewed page; crawlable server text; tour canonical retained |
| Two active tour contexts | Correct independent names, prices and request links |
| Public WCAG A/AA automated audit | No reported violations in sampled desktop/mobile states |
| Operations | 69 permitted route/device checks; Owner, Partner and Staff at 1440 / 900 / 390; no operational builder chrome |
| Appearance and tasks | Nine Light/Dark/System checks; System followed both simulated color schemes; all three roles completed a task |
| Operations task accessibility / browser errors | No reported violations / errors |
| Public request, supplier confirmation, availability, payment readiness | PASS in isolated data |
| Secure payment page | Correct persisted $170.00 snapshot total and confirmation wording; refreshed successfully; zero PayPal calls |

Production build reports approximately **129 kB First Load JS** on each of the six public page types, versus **139 kB** on the isolated editor route (editor route code approximately 10.7 kB). The common framework chunk is 103 kB. These are Next.js build estimates, not measured network performance or Core Web Vitals. The approved homepage composition, black/gold/ivory palette, real logo and separate rainforest/coast chapters were visually retained.

The public browser preserved configured Codespaces origins while routing transport to local services and retaining actual API response bodies. No tour inventory was mocked. This does not claim external GitHub private-port authentication testing. The homepage title is its existing “Costa Rica Experiences, Thoughtfully Planned”; no branding suffix was added merely to satisfy a test expectation.

The isolated business path submitted a public booking request, recorded supplier contact/availability/confirmation through authenticated Operations APIs, opened the secure payment page and verified its persistent unpaid readiness without initiating checkout. Partner and Staff appearance was checked through their permitted Profile page; Owner Settings remained available. An additional mobile browser check submitted the actual public request form and verified its receipt/focus behavior.

iPad checks use browser emulation; physical iPad/Safari testing remains recommended. Existing controlled publish/restore/concurrency browser tests were not repeated after resume. Temporary earlier test logs were lost with the Codespace restart; their successful outcomes above were observed before interruption and preserved in the conversation.

## Reproduction and isolation

`apps/web/tests/browser/publication.cjs` contains the controlled browser acceptance. It requires Playwright and axe on NODE_PATH, `VV_REVIEW_DIR` containing private generated test credentials and the configured public API origin, and an **isolated** review API/database at local ports 18000/13000/13001. Never point it at business data: it intentionally creates review layout revisions. The normal public visual checks are read-only. No PayPal transaction is permitted.

Code checks:

```sh
docker compose exec api sh -c 'pip install -r requirements-dev.txt && VV_TEST_POSTGRES=1 python -m pytest -q'
docker compose exec web sh -c 'npm run typecheck && npm run lint && npm run build'
docker compose exec web sh -c 'NODE_PATH=/repo/apps/web/node_modules node --test tests/*.cjs /repo/packages/page-builder/tests/*.cjs'
docker compose exec ops sh -c 'npm run typecheck && npm run lint && npm run build'
docker compose exec ops node --test tests/website-management.test.cjs
docker compose config --quiet
docker compose up --build -d
docker compose ps
docker compose exec api alembic upgrade head
```

Disposable app dependency/build volumes may be refreshed after changing the reusable package. Never remove the named PostgreSQL volume. Review accounts, drafts, tokens and servers use a separate temporary database; legitimate business data and immutable production history are not cleanup targets. Final cleanup stopped all three isolated review servers and removed their database, accounts, sessions and generated credentials. Read-only counts and content digests matched across **25 business tables** before and after final acceptance; no business records changed.

## Limitations and scope

No automatic rebase, autosave publication, physical-device certification or production video playback acceptance is claimed. Composite widgets retain Part 2's primary-copy/media editing boundaries. Planning/Contact preserve their existing disabled delivery state. The existing 15-minute editor session is not silently extended. A source code bug outside layout validation still requires ordinary application error handling; schema fallback is not a substitute for application tests.

No Hotels, Packages, public Transportation booking, email, AI, Live PayPal, arbitrary-code widgets, production storage or bulk real-media ingestion was added. The next practical step is reviewed real VV photo/video ingestion and media organization; it has not begun.
