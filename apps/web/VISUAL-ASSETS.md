# Visual assets

These seven images were generated using the built-in imagegen tool for this redesign. They are illustrative concepts, not photographs documenting actual suppliers, travelers, or exact Costa Rica viewpoints. No stock-photo license or real-world provenance is claimed. Replace them with approved VV photography before representing a particular provider or venue.

All images are stored locally under `apps/web/public/images/` as WebP. The source PNGs remain in the generation workspace. `components/scenic-image.tsx` maps presentation assets to existing tour visual keys; inventory data and API configuration are unchanged.

The Allura accent font is locally hosted under `public/fonts/`; its SIL OFL license is included alongside it.

## Logo

The approved original is `public/branding/volcan-vacations-logo.png` (11944 × 1154, white RGBA with transparency). `components/brand.tsx`, shared by the header and footer, presents this exact PNG through a CSS alpha mask filled with `var(--gold)` (`#D7A84B`). Standard and WebKit mask declarations use centered `contain` sizing with no repetition; the display box retains the original `11944 / 1154` aspect ratio. No tracing, cropping, stretching, filter approximation, or generated replacement is used. The separate existing header tagline retains `#E8C675`. The home link retains its accessible name and a minimum 44px height.

The source PNG is unchanged. SHA-256: `8d094931f098a36b59836a6fad86b8a496e60b10df0873819c2456b1ab68cfad`.

## Final generation prompts

### arenal.webp

Use case: photorealistic-natural. Asset type: wide cinematic Costa Rica travel website hero background, 1536x1024. Arenal-style conical volcano toward center right above dense lush tropical rainforest at golden sunset, wisps of mist in valley, emerald foliage framing edges, natural dramatic orange clouds and rich green canopy. Left third shaded forest with space for white website text, beautiful mountain fully visible to right. Photorealistic scenic concept, natural believable topography. No text, logo, watermark, buildings, graphic panels or UI. Premium travel photography aesthetic, restrained realistic colors. This is illustrative concept imagery, not documentation of a specific viewpoint.

### rafting.webp

Use case: photorealistic-natural. Website travel image, landscape 1536x1024. Adults wearing properly fastened orange helmets and life jackets paddling a blue raft on whitewater rapids, lush Costa Rica rainforest river, joyful realistic outdoor action, wide composition, all paddles held naturally. Premium editorial photography aesthetic. Realistic textures, natural colors. No text, watermark, logos, UI or collage. Illustrative concept imagery, not a real supplier or location claim.

### springs.webp

Use case: photorealistic-natural. Website travel image, landscape 1536x1024. Beautiful naturalistic stone thermal pools in a lush Costa Rican tropical garden, warm steam, tropical leaves, turquoise mineral water, soft late afternoon sunlight, no people or buildings. Premium editorial photography aesthetic. Realistic textures, natural colors. No text, watermark, logos, UI or collage. Illustrative concept imagery, not a real supplier or location claim.

### bridges.webp

Use case: photorealistic-natural. Website travel image, landscape 1536x1024. A traveler with a red backpack viewed from behind walking on a secure suspension footbridge through lush Costa Rica rainforest canopy, green foliage, morning light, realistic bridge cables and handrails. Premium editorial photography aesthetic. Realistic textures, natural colors. No text, watermark, logos, UI or collage. Illustrative concept imagery, not a real supplier or location claim.

### waterfall.webp

Use case: photorealistic-natural. Website travel image, landscape 1536x1024. Tall single waterfall descending from a lush tropical cliff into a clear turquoise pool, Costa Rica rainforest, vivid natural greens, soft sunshine and mist, no people. Premium editorial photography aesthetic. Realistic textures, natural colors. No text, watermark, logos, UI or collage. Illustrative concept imagery, not a real supplier or location claim.

### coffee.webp

Use case: photorealistic-natural. Website travel image, landscape 1536x1024. Premium rustic coffee and cacao still life in Costa Rica, a ceramic cup of black coffee with gentle steam, red coffee cherries and cacao pods with dark chocolate pieces, tropical foliage softly blurred behind, warm natural light. Premium editorial photography aesthetic. Realistic textures, natural colors. No text, watermark, logos, UI or collage. Illustrative concept imagery, not a real supplier or location claim.

### rainforest.webp

Use case: photorealistic-natural. Website travel image, landscape 1536x1024. Costa Rican red-eyed tree frog resting naturally on a glossy tropical leaf on the far right of a wide composition, soft lush rainforest bokeh across left two thirds for website text, rich emerald green, realistic wildlife macro photography. Premium editorial photography aesthetic. Realistic textures, natural colors. No text, watermark, logos, UI or collage. Illustrative concept imagery, not a real supplier or location claim.
