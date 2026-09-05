# Black UI color correction

Only `app/globals.css` and `app/home.css` change application behavior, through color declarations. All photography and the real logo are unchanged (SHA-256 verified). Page markup, dimensions, typography, responsive rules, booking/API code, Operations, backend, database and deployment configuration are preserved.

## Color system

The six required tokens are defined verbatim. `html`, `body`, the homepage and section canvas use `--vv-black` (`#050809`). Cards, menu panels, request messages and callouts use `--vv-charcoal` (`#0c1011`); form-status panels use `--vv-black-soft` (`#071011`). Existing light forms/controls use `--vv-ivory`. Gold remains on branding, icons, actions and selected controls.

Both legacy forest tokens are removed completely. All photographic overlays now use `#050809` with the original opacity and stop positions; transparent gradient stops explicitly use the same black at zero opacity. Gold button gradients become solid approved gold so every remaining UI gradient is black. Borders and muted text are neutral gray; green-tinted form text is black/charcoal or neutral gray.

The source audit covered all public CSS and TSX, including mobile rules, pseudo-elements, backgrounds, borders, box/text shadows, RGB/HSL colors, inline styles and state components. No other green RGB/HSL backgrounds or green shadows were found. Photographic filenames and copy mentioning rainforest are retained.

## Exhaustive removed/replaced color values

This inventory includes all replaced green treatments plus adjacent blue/olive/off-palette neutrals normalized during the audit. Alpha suffixes are listed explicitly. Existing gold accent borders/shadows and semantic red error text are retained.

| Previous value | Replacement |
| --- | --- |
| `#020a0a05` | `#05080905` |
| `#020a0a80` | `#05080980` |
| `#020a0a99` | `#05080999` |
| `#020a0aeb` | `#050809eb` |
| `#03080c40` | `#05080940` |
| `#03080c80` | `#05080980` |
| `#04090d55` | `#05080955` |
| `#04090df2` | `#050809f2` |
| `#040a0d` | `var(--vv-black)` |
| `#040b0c` | `var(--vv-black)` |
| `#05090d0a` | `#0508090a` |
| `#05090d22` | `#05080922` |
| `#05090d35` | `#05080935` |
| `#05090d40` | `#05080940` |
| `#05090d44` | `#05080944` |
| `#05090d45` | `#05080945` |
| `#05090d55` | `#05080955` |
| `#05090d75` | `#05080975` |
| `#05090d80` | `#05080980` |
| `#05090d85` | `#05080985` |
| `#05090dc9` | `#050809c9` |
| `#05090dea` | `#050809ea` |
| `#050b0e` | `var(--vv-black)` |
| `#050b10aa` | `#050809aa` |
| `#050d0e` | `var(--vv-black)` |
| `#06130b75` | `#05080975` |
| `#06130b9c` | `#0508099c` |
| `#06130bcc` | `#050809cc` |
| `#06130be0` | `#050809e0` |
| `#071011` | `var(--vv-black)` |
| `#07101138` | `#05080938` |
| `#07101155` | `#05080955` |
| `#07101166` | `#05080966` |
| `#071011c7` | `#050809c7` |
| `#071011d9` | `#050809d9` |
| `#071011f0` | `#050809f0` |
| `#090f12` | `var(--vv-charcoal)` |
| `#0a1515` | `var(--vv-black)` |
| `#0b1817` | `var(--vv-charcoal)` |
| `#0c1115` | `var(--vv-charcoal)` |
| `#0d181b` | `var(--vv-charcoal)` |
| `#10160f` | `var(--vv-black)` |
| `#15191c` | `var(--vv-charcoal)` |
| `#153a2ed9` | `rgba(12, 16, 17, 0.85)` |
| `#161b1e` | `var(--vv-charcoal)` |
| `#1b2b22` | `var(--vv-black)` |
| `#233f31` | `var(--vv-ivory)` |
| `#24362e` | `var(--vv-charcoal)` |
| `#263b30` | `var(--vv-charcoal)` |
| `#303639` | `var(--line)` |
| `#304738` | `var(--vv-charcoal)` |
| `#343a3c` | `var(--line)` |
| `#353a3c` | `var(--line)` |
| `#46504b` | `var(--line)` |
| `#50594b` | `var(--muted)` |
| `#535b4d` | `var(--muted)` |
| `#586052` | `#555555` |
| `#697364` | `#666666` |
| `#6d715d` | `var(--line)` |
| `#a7ac9c` | `#999999` |
| `#aba487` | `var(--line)` |
| `#b1b2a3` | `#999999` |
| `#c9cabe` | `var(--muted)` |
| `#d1d0c9` | `var(--gold-light) on featured-tour metadata`; `var(--vv-ivory)` |
| `#d2cbb9` | `#bdbdbd` |
| `#d5ccad` | `var(--vv-charcoal)` |
| `#deddd6` | `var(--vv-ivory)` |
| `#e0e0d7` | `var(--vv-ivory)` |
| `#e5dfcf` | `var(--vv-black-soft)` |
| `#fffdf7` | `var(--vv-ivory)` |
| `--background: #071011` | `--background: var(--vv-black) / #050809` |
| `--forest-deep: #0b2923 / var(--forest-deep)` | `var(--vv-black) / #050809; old token removed` |
| `--forest: #153a2e / var(--forest)` | `var(--vv-charcoal) / #0c1011; old token removed` |
| `--line: #34413c` | `#343434` |
| `--muted: #b8bdb4` | `#bdbdbd` |
| `linear-gradient(180deg, #f2d595, var(--gold))` | `var(--vv-gold) / #D7A84B (solid gold action)` |
| `linear-gradient(var(--gold-light), var(--gold))` | `var(--vv-gold) / #D7A84B (solid gold action)` |
| `transparent gradient stops` | `rgba(5, 8, 9, 0)` |

Additional color-only declarations: `html` now explicitly paints black; category-card image slots paint charcoal; tour duration/category metadata uses light gold. No spacing, border widths, typography, image cropping, or section geometry changes.

## Validation and rendered inspection

Reviewed the actual rebuilt homepage at **1440px, 900px and 390px**, both normally and with photographs temporarily hidden only inside the browser review. In all three views, the interface reads **black + gold**. The image-hidden review leaves the real gold logo visible and exposes the structural page, cards, menu, section canvas, overlays, and footer. Photography is fully restored in the running application and all normal screenshots.

Before/after element geometry, typography and image crop measurements are **identical** across seven public route variants at all three widths (21 comparisons). There is no horizontal overflow. Inspected planner/contact ivory form panels, request forms, tour cards, mobile menu, and their black/charcoal surroundings. All 3,318 computed background, gradient and shadow color occurrences across the 21 views, including pseudo-elements, belong to the approved black/charcoal/ivory/gold palette or transparent black. All remaining rendered gradients use black/charcoal only.

| Validation | Result |
| --- | --- |
| Public TypeScript | PASS |
| Public ESLint | PASS — no warnings/errors; existing Next lint deprecation notice only |
| Public production build | PASS |
| Operations build | PASS |
| Docker Compose configuration | PASS |
| postgres, api, web and ops health | PASS — all four healthy |
| Public routes | PASS — HTTP 200 for `/`, `/tours`, `/plan-your-trip`, `/about`, `/contact`, `/request`, and selected-tour `/request` |
| Loading/error/empty/request states and hover | PASS — black/charcoal surfaces; retry reloads six live tours |
| Real API inventory | PASS — six live database-backed featured tours and selected-tour request form load |
| Rendered layout preservation | PASS — exact before/after geometry and typography equality at all three sizes |
| Photography and logo preservation | PASS — all ten asset SHA-256 checks unchanged |

Checks run in the existing Compose app containers. The public service was restarted to serve the completed production build. No Docker or deployment configuration files were changed. Review uses local web transport while retaining the configured Codespaces browser origin and real forwarded API calls, because the forwarded web port requires GitHub sign-in; port visibility is unchanged.

Review scripts, normal/image-hidden screenshots, and before/after snapshots: `/tmp/vv-black-review/`. Application changes are restricted to two CSS files; this report records the exhaustive audit. Changes remain uncommitted and unpushed.

State review held/aborted a request to inspect loading and failure, then retried against the real API. An empty response was supplied only inside the isolated browser test; no application or database inventory was changed. Existing hover animation was allowed to finish before its final color assertion.
