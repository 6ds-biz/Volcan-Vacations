# Integrating 6DS Page Builder

1. Add the local package dependency (VV: `file:../../packages/page-builder`) and transpile it in the consumer bundler. VV uses Next.js `transpilePackages` and `.npmrc` `install-links=true`; build from the repository root so the package path is available.
2. Import runtime CSS and provide theme tokens (`--pb-base`, `--pb-panel`, `--pb-accent`, `--line`, `--muted`, gold tokens). Do not import editor code into the normal runtime entry.
3. Create a compiled registry with `genericRuntime()` plus business wrappers. Give every business widget a config validator, context requirements and permission predicate. Reuse existing query results and action handlers.
4. Define stable source-controlled defaults for each page. Validate persisted layouts before rendering and fall back safely to these defaults.
5. Implement a `MediaProvider` using your approved catalog and source policy. Keep unknown rights unknown and enforce publication rules server-side.
6. Supply `RenderContext` with current device, authenticated permissions, live page context and media provider. Render `PageRenderer` with page, fallback and registry.
7. Only for authorized authors, dynamically import `@6ds/page-builder/editor`. Supply initial draft/published layout, defaults, registry/context, current version, exit callback and `RevisionAdapter`.
8. Implement independent schema validation, owner authorization, optimistic versions, transactions, immutable revisions and audit actors in your backend. The package has no database dependency.
9. Test role denials, stale saves, invalid imports, media rights, responsive layouts, keyboard/touch interaction and unchanged business workflows.

Example integration: `apps/ops/components/page-builder/page-surface.tsx`. Core tests run with the consumer's installed React/TypeScript dependencies:

```sh
docker compose exec -T ops sh -c 'NODE_PATH=/repo/apps/ops/node_modules node --test /repo/packages/page-builder/tests/core.test.cjs'
```

For Nova or another 6DS app, reuse the package, supply new registry/defaults/media/persistence adapters, and keep its business APIs outside the engine. Do not copy VV widgets or its role model into the reusable package.
