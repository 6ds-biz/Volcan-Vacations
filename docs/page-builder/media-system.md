# Media system

`MediaProvider` supplies asynchronous `list(query, category)` and `get(id)`, a source validator, optional categories and optional upload/archive hooks. V1's VV adapter does not implement upload or archive. The core neither fetches a business database nor owns asset storage.

`MediaAsset` includes stable ID, image/video type, source, filename, MIME type, nullable dimensions, alt, optional caption/attribution, rights status, provenance, tags, creation time and poster ID. Unknown metadata remains unknown. Rights are consumer-provided facts, never inferred by the engine.

The picker supports search, categories, thumbnails, metadata, replacement, removal and reset. Layouts store approved asset references, never URLs or embedded data. Runtime resolves the reference through the provider and validates the resolved source. Missing/unavailable assets produce a placeholder. `NEEDS_RIGHTS_REVIEW` is visible; VV rejects publishing/restoring unapproved references server-side, including hidden and responsive assets.

Images use cover/contain, focal x/y (0–100%), wide/square/portrait/natural ratios, bounded radius and black overlays (`none/light/medium/dark`). Text remains a separate React layer. Meaningful images require alt text; an empty override uses asset alt metadata, while decorative images render empty alt. Replacing an asset clears the old alt override so a previous image description is not reused accidentally. Responsive images use the same alt override when explicitly supplied; choose wording valid for each image or rely on per-asset alt metadata.

Video is a foundation: provider-owned source, poster reference, controls, loop and muted autoplay. Controls cannot be disabled and autoplay cannot have sound and is disabled for reduced-motion users. VV currently registers images only. There is no video upload, processing, hosting, third-party embed or automatic media acquisition.

For real media ingestion, review provenance/rights, assign stable IDs, record dimensions and meaningful alt text, then extend the consumer catalog. Never mark prospects' hotel imagery approved without a rights record. Existing generated VV placeholders remain explicitly illustrative. [VV catalog details](vv-integration.md#media).
