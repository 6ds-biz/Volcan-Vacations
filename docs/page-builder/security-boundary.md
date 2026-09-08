# Security boundary

Layout authoring changes presentation, never authorization or business state. Registries are compiled application code. Validate incoming layouts independently on the server before persistence or publication. Reject unknown widgets/config, incompatible contexts, arbitrary CSS/HTML/JavaScript/URLs, unsupported versions and oversized input. Do not put booking/customer/supplier/payment data into layout config.

The runtime receives authenticated permissions and current live context from the consumer. Each business widget must also rely on the existing protected API for all reads and mutations. A hidden or inserted widget cannot grant a role new permissions. Edit/preview content is inert; publication endpoints only write layout tables and an authenticated audit record.

Media validation must resolve IDs against a trusted catalog, check source safety and require approved rights before publication. Never trust a layout's claimed rights or a browser-supplied URL. User-provided alt text is plain text, not HTML.

VV uses existing session, CSRF and Origin checks, plus explicit Owner-only draft/publish/restore/revision authorization. Display names, dashboard profile overrides and client-supplied actor fields cannot confer ownership. Expected versions and database row locking prevent stale overwrite; append-only revisions and restore-as-new preserve history. PostgreSQL triggers also reject raw SQL updates/deletes to revision rows.

Theme preferences, appearance, authentication, supplier confirmation, price snapshots, payment eligibility, provider verification and booking workflow remain owned by their existing services. No PayPal calls are part of the builder.
