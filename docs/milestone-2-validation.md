# Milestone 2 validation — 2026-09-05

## Starting state and preservation

The worktree was clean. Starting commit: `fa5fa51` (Complete Volcan Vacations visual redesign); earlier commits: `6300345`, `87bf47b`.

`0001_initial_schema`, Docker Compose/Dockerfiles, Codespaces configuration, original VV logo, and unrelated domain models were not changed. The logo SHA-256 remains `8d094931f098a36b59836a6fad86b8a496e60b10df0873819c2456b1ab68cfad`. Only inventory presentation wiring and its loading/filter/photo states changed in the approved public design. No commits or pushes were made.

## Database

- PASS: forward upgrade from `0001_initial_schema` to `0002_tour_inventory` against the existing Compose PostgreSQL database.
- PASS: repeated `docker compose exec -T api alembic upgrade head`.
- PASS: `alembic check` reports no new upgrade operations.
- PASS: direct PostgreSQL inspection confirms both prices are `NUMERIC(12,2)` and the partial unique primary-image index exists.
- No database or named volume was dropped/recreated. There were zero suppliers/products before this milestone.

## Tests and builds

| Check | Result |
| --- | --- |
| Backend `python -m pytest -q` | PASS — 11 tests |
| Public `npm run typecheck` | PASS |
| Public `npm run lint` | PASS — no lint warnings/errors |
| Public `npm run build` | PASS |
| Operations `npm run typecheck` | PASS |
| Operations `npm run lint` | PASS — no lint warnings/errors |
| Operations `npm run build` | PASS |
| `docker compose config --quiet` | PASS |
| `docker compose up --build -d` | PASS |
| postgres / api / web / ops | All healthy |
| Public routes `/`, `/tours`, `/plan-your-trip`, `/about`, `/contact` | All HTTP 200 |
| Operations `/`, `/tours`, `/suppliers`, new/edit pages for both entities | All HTTP 200 |
| `git diff --check` | PASS |

Tests cover active/featured/category filtering, public slug detail, inactive exclusion, private-field exclusion, internal cost/margin, supplier and tour create/update, slug conflicts, money validation, image ownership, primary switching, ordering, deletion/promotion, and unsafe URL rejection. The backend suite uses isolated SQLite fixtures; PostgreSQL migration and actual persistence were verified separately. Existing Next lint, TestClient/httpx, and datetime deprecation notices remain informational. An initial sandboxed async test attempt stalled; the successful suite ran in a temporary environment outside that restriction. Initial URL-validation tests caught a Pydantic adapter issue; it was fixed and all tests rerun successfully.

## Browser acceptance

The final `scripts/milestone2-e2e.cjs` run completed successfully against the production Compose applications and real API/PostgreSQL:

1. Opened Operations; created and edited a labeled DEMO supplier with private contact fields.
2. Created a tour, assigned that supplier, entered $85.00 retail / $50.00 cost, and verified $35.00 gross margin in the UI and API.
3. Verified the inactive tour's public detail returned 404.
4. Added rafting as primary and waterfall as a second image; reordered waterfall and switched it to primary.
5. Updated the tour name and marked active/featured.
6. Verified the updated tour, $85 retail, and selected primary photo appeared on both homepage and `/tours`, without source changes or a rebuild.
7. Checked public list, featured list, and detail JSON for absence of supplier cost, margin, supplier ID/contact details, and private values.
8. Removed the primary image through Operations; confirmed the remaining image was promoted.
9. Checked all five public and seven Operations routes at 390px and 1440px: HTTP 200, no page-level overflow or JavaScript page errors. Operations tables intentionally scroll within their own focusable regions on narrow screens.
10. Separately simulated API failure and empty responses; verified safe messages and no hardcoded inventory fallback.
11. Deactivated only the acceptance records and verified the tour returned public 404 again. No source image files or supplier/tour records were deleted.

Final acceptance identifiers: supplier `5`, tour `8`, slug `demo-e2e-rafting-1788592385362`. Earlier test records (suppliers 3/4, tour 7) also remain inactive and recoverable. Direct PostgreSQL inspection confirms only the six requested seed tours remain active/featured.

Screenshots were inspected with images decoded, including desktop publication, mobile public catalog, Operations editor/gallery, and mobile Operations table. Files are under `/tmp/vv-m2-review/` for this Codespace session. Screenshots containing the extra active DEMO E2E tour document the publication step before test cleanup.

The configured GitHub-forwarded API URL redirects unauthenticated requests to login. The test retained those origins but mapped requests to local running containers using the documented local-transport option; inventory and application responses were real, not mocked. This verifies the application stack, not GitHub forwarding login. Port visibility was not changed. Only the explicitly labeled error/empty state tests used simulated responses.

## Seed and security status

Two labeled demo suppliers and all six requested tours were seeded explicitly. A second seed run inserted zero tours and preserved every existing record. All six use existing illustrative generated website images. Pricing and imagery are demo-only, not current production supplier offers.

Public/private field checks passed. Operations authentication remains deliberately deferred: Operations and `/ops/*` are **not production-secure**. A trusted access boundary must protect both frontend and API before public production use. Images are managed by URL; persistent production object storage/upload controls remain deferred. No paid resources or out-of-scope business features were created.

## Remaining Milestone 2 issues

None identified in the implemented scope. Deferred production authentication/storage and GitHub's private-port login are documented deployment boundaries, not implemented milestone features. Changes remain uncommitted and unpushed.
