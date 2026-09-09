# 6DS Web Builder — Phase 1

The standalone design tool lives in `apps/page-builder` and runs on port **3002**. It reuses `packages/page-builder` for the Page → Section → Column → Widget contract, renderer, validation, history, movement and media controls. Its only initial project is Volcan Vacations.

## Start

From the repository root:

```sh
cd apps/page-builder
npm ci
npm run dev
```

Open http://localhost:3002. Only this app needs to run. Its VV adapter imports presentation source and public assets from `apps/web`; it does not start that app, install its dependencies, use its handoff, or connect to Operations or the API. `npm run assets`, automatically run by dev/build, copies public images, branding and fonts to the ignored builder `public/` directory.

An independent Compose file avoids changing the existing stack:

```sh
docker compose -f compose.builder.yml up --build
```

The builder has no authentication, production publishing, booking, payment, database or production media-storage service. Keep this local design tool separate from the public production deployment.

## Use

1. Select a page, then use its current VV default or open **Import** and choose a JSON file or paste a complete layout.
2. Select a Section, Column or Widget through **Structure** or its canvas control. **Settings** edits presentation and structured text. **Widgets** inserts registered components. **Media** chooses from the reviewed VV catalog.
3. Use drag handles or Move Up/Down/Left/Right. Columns use a bounded 12-column grid; width 12 stacks a column. Width, alignment, visibility, spacing and ordering apply to the selected device. Shared structure and text edits apply across devices.
4. **Preview** removes editing controls and uses a real 1440px, 900px or 390px iframe viewport. The viewport scales to fit the workspace. Device buttons and Back to editor remain outside the page.
5. **Export** validates and downloads deterministic project-aware JSON. Import accepts that format for the selected project and page.

Working pages remain in memory when switching pages. Switching therefore does not discard changes. Loading a default or replacing a changed layout asks before discarding it; closing/reloading the tab warns about unexported work across pages. Undo/redo is bounded to 50 edits in the currently mounted page editor; switching pages preserves the layout, but starts a fresh undo history. Export files are the Phase 1 saving mechanism. There is no localStorage, autosave, snapshots or backup system.

Public contact stays `info@volcanvacations.com`. Only public design copy belongs in text fields. Layout validation rejects unknown fields, HTML, scripts, arbitrary CSS, foreign projects, unsupported devices, unknown media and noncanonical email addresses. It is not a general detector of sensitive prose entered manually by a designer.

## Validation

```sh
cd apps/page-builder
npm run typecheck
npm run lint
npm run build
npm test
npx playwright install --with-deps chromium
# Start npm run dev (or npm start after a build) in another terminal.
npm run test:browser
```

`npm test` runs nine portable-layout scenarios and the 22-test reusable core suite. Browser acceptance covers all six defaults, 18 device previews, editing, media/crops, structure, movement, history, file/paste import, rejection, deterministic downloads, discard protection and 1440/1024/768 touch layouts. It writes screenshots and results to ignored `apps/page-builder/test-results/`. `BUILDER_URL` selects an alternative test origin. `PLAYWRIGHT_BROWSERS_PATH` may select an installed browser directory.

For public-app regressions run typecheck, lint and build in both `apps/web` and `apps/ops`. Reinstall file dependencies after changing the reusable package (`npm ci`) so these applications test the current package source. Validate Compose with `docker compose -f compose.builder.yml config --quiet` and `docker compose config --quiet`.

The existing public editor handoff remains in place. This milestone does not change its origin/proxy behavior or begin VV draft-import/publish integration.

## Recorded acceptance — 2026-09-09

| Check | Result |
| --- | --- |
| Standalone typecheck, lint, production build | Passed; lint has no warnings |
| Portable layout scenarios | 9 passed |
| Shared core regression suite | 22 passed |
| Browser acceptance | Passed all six pages and 18 device previews |
| Editing | Text/CTA/tokens, media replacement/reset/decorative status, focal point, responsive assets/crops/visibility, undo/redo passed |
| Structure | Sections, columns, widths, duplication/removal, precise movement and pointer-drag order assertion passed |
| JSON | File/paste import, invalid import rejection, export filenames and byte-for-byte round trip passed |
| Isolation | Separate source copy built and typechecked with no web/Operations dependencies installed |
| Public web | Typecheck, lint, production build and 19 public website tests passed |
| Operations | Typecheck, lint, production build and its website-management regression test passed |
| Compose | Both independent builder and existing Compose configurations validated |
| Visual review | Screenshots inspected at 1440, 1024 and 768; desktop/tablet/mobile previews reviewed |
| Network and state | Browser assertions found zero API/payment requests, zero localStorage entries and zero runtime errors |

The touch review used Chromium emulation, not physical iPad/Safari hardware. Canvas controls retain 44px targets and readable labels when the website is scaled. Phone page previews are supported; phone editing is not the target workspace.

The API, PostgreSQL and booking/availability/payment/Transportation/authentication implementations were not changed. No live backend, database or payment-provider regression transactions were run. The pre-existing `apps/ops/Dockerfile` working-tree edit was preserved. No commit, push, production publication or VV draft-import integration was performed.
