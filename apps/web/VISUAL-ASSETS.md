# Visual assets

These seven images were generated using the built-in imagegen tool for this redesign. They are illustrative concepts, not photographs documenting actual suppliers, travelers, or exact Costa Rica viewpoints. No stock-photo license or real-world provenance is claimed. Replace them with approved VV photography before representing a particular provider or venue.

All images are stored locally under `apps/web/public/images/` as WebP. The source PNGs remain in the generation workspace. Scenic hero/CTA artwork remains presentation-only. Since Milestone 2, demo tour image references are inserted explicitly by `services/api/app/seed_inventory.py` and managed as ProductImage content through Operations; public cards use API-provided image URLs rather than hardcoded visual keys.

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

## Homepage refinement: toucan-waterfall.webp

Generated with the built-in `image_gen` tool for the homepage refinement. Saved at `public/images/toucan-waterfall.webp` (1536 × 1024, 312 KB, WebP quality 86). This is illustrative scenic artwork, not a documentary photograph of La Fortuna or a supplier. The homepage uses a single decorative image across both the planning and destination stories, with soft outer fades and responsive cropping. Replace this local file or the `ScenicImage` source independently of tour inventory; tour imagery still comes exclusively from API ProductImage records.

Final prompt:

> Use case: photorealistic-natural. Asset type: continuous wide scenic background for a premium Costa Rica homepage, landscape 1536x1024. Create ONE seamless cinematic tropical rainforest scene: a beautiful realistic keel-billed toucan perched on a mossy branch in the upper left foreground (bird fully visible, within left 28% and upper 50%); a tall magnificent single waterfall on the right half descending through dense rainforest into a turquoise pool in the lower right, wet rocks and natural tropical foliage at bottom. Subtle warm sunset light and mist through distant canopy. Upper middle area dark softly detailed rainforest for overlaying website text; lower left area dark shaded foliage for another text block. Rich natural greens, colorful yellow and rainbow toucan beak, turquoise water, restrained warm golden light. High-end travel editorial photography aesthetic, natural feathers, realistic anatomy and rainforest textures. Composition must flow naturally from toucan foreground to waterfall background, no collage, no horizontal seam, no panels, no divider. No text, logo, watermark, UI, borders, buildings or people. Illustrative scenic concept rather than documentary location photo.

### Mobile art direction: toucan-waterfall-mobile-v2.webp

Built-in `image_gen` output saved at `public/images/toucan-waterfall-mobile-v2.webp` (768 × 2048, WebP quality 84). A native `<picture>` source selects this portrait composition at 600px and below, so mobile keeps both wildlife and waterfall in one continuous scene without downloading two displayed layers. The same illustrative-artwork limitations apply.

Final prompt:

> Use case: photorealistic-natural. Asset type: mobile portrait scenic website background, 1024x1536. Create one seamless cinematic Costa Rica rainforest photograph-like scene, not a collage. A vivid realistic keel-billed toucan perched on a mossy branch in UPPER LEFT quadrant, head at x35% y18% with yellow chest and rainbow beak, fully visible bird. Tall tropical waterfall in RIGHT HALF below the bird, beginning at x68% y45% and descending into turquoise water at y78%. Deep lush rainforest connects foreground toucan naturally to background waterfall. Dark softly detailed charcoal-shadow rainforest through middle left and bottom left for later website text overlays. Warm subtle sunset light through upper canopy, natural green leaves, turquoise river, wet rocks. Premium editorial travel photography aesthetic, believable bird anatomy and feathers, fine natural textures. One continuous landscape seen vertically. No horizontal seams or dividers, no text, no typography, no logos, no frames, no UI, no people, no buildings. Illustrative scenic concept, not documentary photo of an exact location.


Final mobile refinement prompt (built-in image edit, using the first portrait as the reference):

> Use case: compositing / mobile art direction. Edit this scenic artwork to a MUCH TALLER AND NARROWER 768x2048 portrait composition, matching a long mobile website story. Preserve realistic photographic style, vivid keel-billed toucan, lush rainforest and the single white waterfall with turquoise water; one seamless continuous scene. Recompose for this narrow frame rather than crop: toucan occupies upper 10–28% of canvas, fully visible on mossy branch, head centered at x40%; dark softly detailed rainforest in middle 32–58% of canvas for later white website text; waterfall well inside right half, centered x70%, begins at y52%, descends to turquoise pool at y85%. Dark shadow foliage left and bottom for later text. Both bird and entire waterfall must stay comfortably inside the central 80% width. Subtle golden light at top, naturally connected jungle landscape all the way down, no dividing line, no panels, no typography, no text, no logos, no UI, no people. Output 768 pixels wide by 2048 pixels tall.
