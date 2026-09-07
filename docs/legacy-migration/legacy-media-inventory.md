# Legacy media inventory

**346 unique image source URLs**, including 334 public media-library image originals; **18 uploaded MP4 files**, plus 5 external video URL references representing 4 distinct external videos. Two other library assets are one audio file and one font. WordPress generated renditions are grouped, not counted as new originals.

**15 exact-byte duplicate image groups** (30 files; 15 redundant copies), one duplicate external-video reference, and **10 HTTP-404 images**. All broken media are old external GoodLayers demo screenshots. There were no broken uploaded MP4 URLs in the HEAD checks. HEAD reachability is not a playback test.

## Recommendations

| Recommendation | Sources |
| --- | --- |
| BROKEN | 10 |
| DUPLICATE | 16 |
| LOW_QUALITY | 8 |
| POSSIBLE_KEEP | 64 |
| REPLACE_WITH_USER_MEDIA | 273 |

No asset is marked KEEP without rights confirmation. The 64 POSSIBLE_KEEP candidates comprise 46 images and 18 uploaded videos; this is a review shortlist, not publication permission. LOW_QUALITY uses a conservative <800px longest-edge threshold for photos; it is not a measured aesthetic score. Video metadata shows compressed WhatsApp files (mostly 848×480 or 464×832); request originals before hero use. Ten referenced stylesheets were also inspected; their decorative/font/theme-background URLs are recorded separately in [legacy-stylesheet-audit.json](legacy-stylesheet-audit.json), excluded from the 371 source rows below and not individually downloaded.

## Material findings

- Reviewed 67 recent image thumbnails plus five questionable template assets. Wildlife/frog, sloth, volcano, waterfall, horse, ATV and shuttle images provide a useful review queue.
- `wp-5330`, `wp-5329`, and `wp-5321` are non-Costa Rican coastal/canal stock imagery reused in tour galleries; replace. Stock filenames do not establish a transferable licence.
- The shuttle uses the sloth featured image/gallery. Association is preserved as a defect, not as a transportation-image recommendation.
- The horseback offers reuse the same featured photo. Several recent originals are byte-identical copies under different filenames. Similar wildlife sequences are flagged for human review, not automatically deleted.
- Four newly attached hanging-bridge images are only 630px wide. Use for small previews only if approved; request high-resolution originals.
- Served dimensions sometimes differ from WordPress metadata (e.g. 2560px reported versus 1600px delivered). JSON preserves both and flags the discrepancy.
- Existing approved new-site branding should remain; legacy logo variants, generic icons and the WooCommerce placeholder are replacement/quarantine candidates.
- Rights, photographer, release status, and actual tour/venue identity remain unconfirmed. Do not infer suppliers from photos, watermarks, or filenames.

## Full source register

The JSON has exact URLs, page/role associations, observed renditions, dimensions, status, hashes, duplicates and rights flags for every row. The table below is complete at source-URL level.

| ID / source | Type | Dimensions (served for images) | Page associations | HTTP | Duplicate | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| [wp-6217 — hanging bridges](https://volcanvacations.com/wp-content/uploads/2026/02/hanging-bridges.jpg) | image | 630 × 473 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | LOW_QUALITY |
| [wp-6216 — hanging bridges 3](https://volcanvacations.com/wp-content/uploads/2026/02/hanging-bridges-3.jpg) | image | 630 × 420 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | LOW_QUALITY |
| [wp-6215 — hanging bridges 2](https://volcanvacations.com/wp-content/uploads/2026/02/hanging-bridges-2.jpg) | image | 630 × 354 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | LOW_QUALITY |
| [wp-6214 — hanging brdiges 4](https://volcanvacations.com/wp-content/uploads/2026/02/hanging-brdiges-4.jpg) | image | 630 × 419 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | LOW_QUALITY |
| [wp-6212 — 5-1](https://volcanvacations.com/wp-content/uploads/2026/02/5-1-1.jpg) | image | 1600 × 900 | 1 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-6160 — transportation_12251543](https://volcanvacations.com/wp-content/uploads/2026/02/transportation_12251543-e1770494872476.png) | image | 100 × 100 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-6155 — Shuttle01](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-06-at-5.33.20-PM.jpeg) | image | 1083 × 1280 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6154 — Shuttle02](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-06-at-5.33.20-PM1.jpeg) | image | 1280 × 960 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6145 — Transport](https://volcanvacations.com/wp-content/uploads/2026/02/camper-van_3621220-e1770493663194.png) | image | 60 × 60 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-6096 — WhatsApp Video 2026-02-03 at 3.30.53 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.30.53-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6095 — WhatsApp Video 2026-02-03 at 3.30.59 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.30.59-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6094 — WhatsApp Video 2026-02-03 at 3.31.01 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.31.01-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6093 — WhatsApp Video 2026-02-03 at 3.31.04 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.31.04-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6092 — WhatsApp Image 2026-02-03 at 3.31.05 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM.jpeg) | image | 960 × 1280 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6091 — WhatsApp Image 2026-02-03 at 3.31.05 PM(1)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM1.jpeg) | image | 960 × 1280 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6090 — WhatsApp Image 2026-02-03 at 3.31.05 PM(2)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM2.jpeg) | image | 1280 × 960 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6089 — WhatsApp Image 2026-02-03 at 3.31.05 PM(3)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM3.jpeg) | image | 1280 × 960 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6088 — WhatsApp Image 2026-02-03 at 3.31.05 PM(4)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM4.jpeg) | image | 1280 × 960 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6087 — WhatsApp Image 2026-02-03 at 3.31.05 PM(5)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM5.jpeg) | image | 1280 × 960 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6086 — WhatsApp Image 2026-02-03 at 3.31.05 PM(6)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM6.jpeg) | image | 1280 × 960 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6085 — WhatsApp Image 2026-02-03 at 3.31.05 PM(7)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM7.jpeg) | image | 1280 × 960 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6084 — WhatsApp Image 2026-02-03 at 3.31.05 PM(8)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM8.jpeg) | image | 960 × 1280 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6083 — WhatsApp Video 2026-02-03 at 3.31.11 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.31.11-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6082 — WhatsApp Video 2026-02-03 at 3.31.19 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.31.19-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6081 — WhatsApp Video 2026-02-03 at 3.31.26 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.31.26-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6080 — WhatsApp Video 2026-02-03 at 3.31.32 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.31.32-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6079 — WhatsApp Image 2026-02-03 at 3.31.33 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.33-PM.jpeg) | image | 720 × 1280 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6078 — WhatsApp Image 2026-02-03 at 3.31.33 PM(1)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.33-PM1.jpeg) | image | 1280 × 720 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6077 — WhatsApp Video 2026-02-03 at 3.31.35 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.31.35-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6076 — WhatsApp Image 2026-02-03 at 3.31.36 PM(2)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.36-PM2.jpeg) | image | 960 × 1280 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6075 — WhatsApp Video 2026-02-03 at 3.31.36 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.31.36-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6074 — WhatsApp Video 2026-02-03 at 3.31.37 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.31.37-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6073 — WhatsApp Video 2026-02-03 at 3.31.40 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.31.40-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6072 — WhatsApp Image 2026-02-03 at 3.31.41 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.41-PM.jpeg) | image | 1200 × 1600 | 4 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6071 — WhatsApp Image 2026-02-03 at 3.31.41 PM(1)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.41-PM1.jpeg) | image | 1280 × 960 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6070 — WhatsApp Image 2026-02-03 at 3.31.41 PM(2)](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.41-PM2.jpeg) | image | 1280 × 924 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6069 — WhatsApp Image 2026-02-03 at 3.31.42 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.42-PM.jpeg) | image | 1280 × 894 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6068 — WhatsApp Image 2026-02-03 at 3.31.47 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.47-PM.jpeg) | image | 1200 × 1600 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-6067 — WhatsApp Video 2026-02-03 at 3.34.07 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.34.07-PM.mp4) | video | 848 × 480 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6066 — WhatsApp Video 2026-02-03 at 3.34.08 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.34.08-PM.mp4) | video | 464 × 832 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6065 — WhatsApp Video 2026-02-03 at 3.34.10 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.34.10-PM.mp4) | video | 464 × 832 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6064 — WhatsApp Video 2026-02-03 at 3.34.12 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.34.12-PM.mp4) | video | 464 × 832 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6063 — WhatsApp Video 2026-02-03 at 3.34.14 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.34.14-PM.mp4) | video | 464 × 832 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6062 — WhatsApp Video 2026-02-03 at 3.34.21 PM](https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Video-2026-02-03-at-3.34.21-PM.mp4) | video | 464 × 832 | 0 | 200 | NOT_BYTE_CHECKED | POSSIBLE_KEEP |
| [wp-6057 — Volcan Vacations Sm](https://volcanvacations.com/wp-content/uploads/2026/02/Volcan-Vacations-Sm-e1770258638503.png) | image | 548 × 512 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5999 — Frogs](https://volcanvacations.com/wp-content/uploads/2026/02/Frogs.jpeg) | image | 1280 × 720 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5998 — Frogs02](https://volcanvacations.com/wp-content/uploads/2026/02/Frogs02.jpeg) | image | 1280 × 720 | 95 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5997 — 2×1-hero-banner-ATV-homepage-1](https://volcanvacations.com/wp-content/uploads/2026/02/2x1-hero-banner-ATV-homepage-1.webp) | image | 2550 × 1440 | 68 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5987 — Wildlife-Boat-Trip-Cano-Negro-Costa-Rica-La-Fortuna-1](https://volcanvacations.com/wp-content/uploads/2026/02/Wildlife-Boat-Trip-Cano-Negro-Costa-Rica-La-Fortuna-1.webp) | image | 1680 × 945 | 76 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5985 — 5-1](https://volcanvacations.com/wp-content/uploads/2026/02/5-1.jpg) | image | 1600 × 900 | 96 | 200 | EXACT_BYTES_DUPLICATE | POSSIBLE_KEEP |
| [wp-5984 — 1-1-scaled](https://volcanvacations.com/wp-content/uploads/2026/02/1-1-scaled-1.jpg) | image | 1280 × 720 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5983 — 4-2-scaled](https://volcanvacations.com/wp-content/uploads/2026/02/4-2-scaled-1.jpg) | image | 1280 × 720 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5965 — DSC00797rs](https://volcanvacations.com/wp-content/uploads/2026/02/DSC00797rs-1.jpg) | image | 1280 × 699 | 0 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5964 — GFALL01(1)](https://volcanvacations.com/wp-content/uploads/2026/02/GFALL011.jpg) | image | 1600 × 1067 | 0 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5963 — Arenal01(1)](https://volcanvacations.com/wp-content/uploads/2026/02/Arenal011.jpeg) | image | 1600 × 1067 | 1 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5962 — rafting-scaled-1(1)](https://volcanvacations.com/wp-content/uploads/2026/02/rafting-scaled-11.jpg) | image | 1600 × 1067 | 2 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5961 — Waterfall01](https://volcanvacations.com/wp-content/uploads/2026/02/Waterfall01.jpg) | image | 800 × 533 | 47 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5960 — Sloth02](https://volcanvacations.com/wp-content/uploads/2026/02/Sloth02.jpg) | image | 800 × 600 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5959 — RC01](https://volcanvacations.com/wp-content/uploads/2026/02/RC01.jpg) | image | 1024 × 576 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5958 — 10-550×550-1](https://volcanvacations.com/wp-content/uploads/2026/02/10-550x550-1.jpg) | image | 550 × 550 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | LOW_QUALITY |
| [wp-5957 — Iron-Man](https://volcanvacations.com/wp-content/uploads/2026/02/Iron-Man.jpg) | image | 1280 × 871 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5956 — Sloth04](https://volcanvacations.com/wp-content/uploads/2026/02/Sloth04.jpg) | image | 800 × 600 | 98 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5955 — RC02](https://volcanvacations.com/wp-content/uploads/2026/02/RC02.png) | image | 800 × 546 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5954 — night-walk03](https://volcanvacations.com/wp-content/uploads/2026/02/night-walk03.jpg) | image | 800 × 528 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5953 — SKY-SM-e1689402453656](https://volcanvacations.com/wp-content/uploads/2026/02/SKY-SM-e1689402453656.jpg) | image | 945 × 817 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5952 — Canyoning01-scaled-e1689398055252](https://volcanvacations.com/wp-content/uploads/2026/02/Canyoning01-scaled-e1689398055252.jpg) | image | 1000 × 667 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5951 — IMG_6851-scaled-e1689398587705](https://volcanvacations.com/wp-content/uploads/2026/02/IMG_6851-scaled-e1689398587705.jpg) | image | 1000 × 666 | 68 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5950 — LFWH(1)](https://volcanvacations.com/wp-content/uploads/2026/02/LFWH1.jpg) | image | 768 × 512 | 53 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5949 — LFWF01](https://volcanvacations.com/wp-content/uploads/2026/02/LFWF01.jpg) | image | 768 × 508 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | LOW_QUALITY |
| [wp-5948 — IMG_2324](https://volcanvacations.com/wp-content/uploads/2026/02/IMG_2324.jpg) | image | 1600 × 1200 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5947 — arenal-hanging-bridges-1](https://volcanvacations.com/wp-content/uploads/2026/02/arenal-hanging-bridges-1.jpg) | image | 900 × 600 | 45 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5946 — 11-550×550-1](https://volcanvacations.com/wp-content/uploads/2026/02/11-550x550-1.jpg) | image | 550 × 550 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | LOW_QUALITY |
| [wp-5945 — tree01](https://volcanvacations.com/wp-content/uploads/2026/02/tree01.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5944 — Waterfall02](https://volcanvacations.com/wp-content/uploads/2026/02/Waterfall02.jpg) | image | 800 × 533 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5943 — DSC0325rs-s](https://volcanvacations.com/wp-content/uploads/2026/02/DSC0325rs-s.jpg) | image | 800 × 483 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | POSSIBLE_KEEP |
| [wp-5942 — trip-bookies-volcano-1-e1708755235396](https://volcanvacations.com/wp-content/uploads/2026/02/trip-bookies-volcano-1-e1708755235396.png) | image | 85 × 68 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5941 — IMG_0992-scaled-e1708836415346](https://volcanvacations.com/wp-content/uploads/2026/02/IMG_0992-scaled-e1708836415346-1.jpg) | image | 1600 × 1067 | 1 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5851 — IMG_0992-scaled-e1708836415346](https://volcanvacations.com/wp-content/uploads/2026/02/IMG_0992-scaled-e1708836415346.jpg) | image | 1600 × 1067 | 0 | 200 | EXACT_BYTES_DUPLICATE | POSSIBLE_KEEP |
| [wp-5849 — LFWH](https://volcanvacations.com/wp-content/uploads/2026/02/LFWH.jpg) | image | 768 × 512 | 40 | 200 | EXACT_BYTES_DUPLICATE | LOW_QUALITY |
| [wp-5636 — GFALL01](https://volcanvacations.com/wp-content/uploads/2026/02/GFALL01.jpg) | image | 1600 × 1067 | 5 | 200 | EXACT_BYTES_DUPLICATE | POSSIBLE_KEEP |
| [wp-5628 — Arenal01](https://volcanvacations.com/wp-content/uploads/2026/02/Arenal01.jpeg) | image | 1600 × 1067 | 2 | 200 | EXACT_BYTES_DUPLICATE | POSSIBLE_KEEP |
| [wp-5516 — woocommerce-placeholder](https://volcanvacations.com/wp-content/uploads/woocommerce-placeholder.webp) | image | 1200 × 1200 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5503 — rafting-scaled-1](https://volcanvacations.com/wp-content/uploads/2026/02/rafting-scaled-1.jpg) | image | 1600 × 1067 | 45 | 200 | EXACT_BYTES_DUPLICATE | POSSIBLE_KEEP |
| [wp-5490 — Volcan-Vacations-e1745799384479](https://volcanvacations.com/wp-content/uploads/2026/02/Volcan-Vacations-e1745799384479.png) | image | 500 × 48 | 255 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5481 — DSC00797rs](https://volcanvacations.com/wp-content/uploads/2026/02/DSC00797rs.jpg) | image | 1280 × 699 | 0 | 200 | EXACT_BYTES_DUPLICATE | POSSIBLE_KEEP |
| [wp-5480 — shutterstock_465949868](https://volcanvacations.com/wp-content/uploads/2019/05/shutterstock_465949868.jpg) | image | 1600 × 822 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5479 — braden-jarvis-383867-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/braden-jarvis-383867-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5475 — shutterstock_647526577](https://volcanvacations.com/wp-content/uploads/2019/05/shutterstock_647526577.jpg) | image | 1600 × 1068 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5747 — sidebar-bg](https://volcanvacations.com/wp-content/uploads/2019/05/sidebar-bg.jpg) | image | 800 × 600 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5684 — marco-meyer-598648-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/marco-meyer-598648-unsplash.jpg) | image | 1600 × 1066 | 7 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5676 — oziel-gomez-555955-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/oziel-gomez-555955-unsplash.jpg) | image | 1600 × 1066 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5675 — fabrizio-conti-568771-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/fabrizio-conti-568771-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5672 — sander-crombach-722287-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/sander-crombach-722287-unsplash.jpg) | image | 1600 × 985 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5668 — george-stackpole-114522-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/george-stackpole-114522-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5658 — gerson-repreza-590945-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/gerson-repreza-590945-unsplash.jpg) | image | 1600 × 1069 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5657 — single-icon-distance](https://volcanvacations.com/wp-content/uploads/2019/05/single-icon-distance.png) | image | 37 × 27 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5654 — single-icon-type](https://volcanvacations.com/wp-content/uploads/2019/05/single-icon-type-1.png) | image | 34 × 25 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5652 — single-icon-difficulty](https://volcanvacations.com/wp-content/uploads/2019/05/single-icon-difficulty-2.png) | image | 30 × 24 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5650 — single-icon-difficulty](https://volcanvacations.com/wp-content/uploads/2019/05/single-icon-difficulty.png) | image | 33 × 33 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5821 — ryan-stone-1266847-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/ryan-stone-1266847-unsplash-1.jpg) | image | 1600 × 1066 | 0 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5813 — red-hat-factory-768348-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/red-hat-factory-768348-unsplash-1.jpg) | image | 1600 × 1066 | 0 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5796 — Great Lake](https://volcanvacations.com/wp-content/uploads/2019/05/paul-gilmore-96153-unsplash.jpg) | image | 1600 × 900 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5826 — Skiing Trip](https://volcanvacations.com/wp-content/uploads/2019/05/pamela-saunders-384317-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5825 — eberhard-grossgasteiger-628147-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/eberhard-grossgasteiger-628147-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5822 — asoggetti-659941-unsplash-(1)](https://volcanvacations.com/wp-content/uploads/2019/05/asoggetti-659941-unsplash-1.jpg) | image | 1600 × 1068 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5814 — Landscape View](https://volcanvacations.com/wp-content/uploads/2019/05/andreas-wagner-724219-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5798 — Treking at night](https://volcanvacations.com/wp-content/uploads/2019/05/aaker-567870-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5824 — joshua-earle-234740-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/joshua-earle-234740-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5817 — Treking](https://volcanvacations.com/wp-content/uploads/2019/05/aaron-benson-200753-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5807 — single-top-bg](https://volcanvacations.com/wp-content/uploads/2019/05/single-top-bg.jpg) | image | 1600 × 512 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5622 — shutterstock_666258808-768×512](https://volcanvacations.com/wp-content/uploads/2019/05/shutterstock_666258808-768x512-1.jpg) | image | 768 × 512 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5621 — psinfinite2-768×597](https://volcanvacations.com/wp-content/uploads/2019/05/psinfinite2-768x597-1.jpg) | image | 768 × 597 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5828 — photo-1428931996691-a5108d4cdbf5-683×1024](https://volcanvacations.com/wp-content/uploads/2019/05/photo-1428931996691-a5108d4cdbf5-683x1024-1.jpg) | image | 683 × 1024 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5827 — TNK87N7464](https://volcanvacations.com/wp-content/uploads/2019/05/TNK87N7464.jpg) | image | 1600 × 1067 | 0 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5613 — tyler-nix-567726-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/tyler-nix-567726-unsplash-scaled.jpg) | image | 1600 × 2400 | 3 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5612 — ryan-stone-1266847-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/ryan-stone-1266847-unsplash.jpg) | image | 1600 × 1066 | 3 | 200 | EXACT_BYTES_DUPLICATE | REPLACE_WITH_USER_MEDIA |
| [wp-5611 — Trekking at Canyon](https://volcanvacations.com/wp-content/uploads/2019/05/red-hat-factory-768348-unsplash.jpg) | image | 1600 × 1066 | 4 | 200 | EXACT_BYTES_DUPLICATE | REPLACE_WITH_USER_MEDIA |
| [wp-5610 — pablo-acevedo-111046-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/pablo-acevedo-111046-unsplash.jpg) | image | 1600 × 1064 | 3 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5609 — jasper-guy-201670-unsplash](https://volcanvacations.com/wp-content/uploads/2019/05/jasper-guy-201670-unsplash.jpg) | image | 1600 × 1200 | 3 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5811 — testimonial-bg](https://volcanvacations.com/wp-content/uploads/2019/04/testimonial-bg-1.jpg) | image | 1600 × 582 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5803 — product-8](https://volcanvacations.com/wp-content/uploads/2019/04/product-8.jpg) | image | 1082 × 800 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5790 — product-7](https://volcanvacations.com/wp-content/uploads/2019/04/product-7.jpg) | image | 800 × 800 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5820 — product-6](https://volcanvacations.com/wp-content/uploads/2019/04/product-6.jpg) | image | 1082 × 800 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5815 — product-5](https://volcanvacations.com/wp-content/uploads/2019/04/product-5.jpg) | image | 1082 × 800 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5808 — Camping](https://volcanvacations.com/wp-content/uploads/2019/04/product-4.jpg) | image | 1082 × 800 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5802 — product-3](https://volcanvacations.com/wp-content/uploads/2019/04/product-3.jpg) | image | 800 × 800 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5788 — product-2](https://volcanvacations.com/wp-content/uploads/2019/04/product-2.jpg) | image | 800 × 800 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5823 — product-1](https://volcanvacations.com/wp-content/uploads/2019/04/product-1.jpg) | image | 1082 × 800 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5818 — testimonial-bg](https://volcanvacations.com/wp-content/uploads/2019/04/testimonial-bg.jpg) | image | 1600 × 582 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5804 — tour-item-bg](https://volcanvacations.com/wp-content/uploads/2019/04/tour-item-bg.jpg) | image | 1600 × 735 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5789 — column-bg](https://volcanvacations.com/wp-content/uploads/2019/04/column-bg.jpg) | image | 1600 × 400 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5784 — logo-hiking-mobile](https://volcanvacations.com/wp-content/uploads/2019/04/logo-hiking-mobile-1.png) | image | 364 × 59 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5812 — woocommerce-placeholder](https://volcanvacations.com/wp-content/uploads/2019/04/woocommerce-placeholder.png) | image | 1200 × 1200 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5810 — logo-hiking-mobile](https://volcanvacations.com/wp-content/uploads/2019/04/logo-hiking-mobile.png) | image | 364 × 59 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5809 — logo-hiking](https://volcanvacations.com/wp-content/uploads/2019/04/logo-hiking-1.png) | image | 350 × 128 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5801 — hiking-slider-text-2](https://volcanvacations.com/wp-content/uploads/2019/04/hiking-slider-text-2-1.png) | image | 804 × 233 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5787 — hiking-slider-text-1](https://volcanvacations.com/wp-content/uploads/2019/04/hiking-slider-text-1.png) | image | 740 × 348 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5819 — hiking-slider-1](https://volcanvacations.com/wp-content/uploads/2019/04/hiking-slider-1.png) | image | 604 × 169 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5806 — hiking-slider](https://volcanvacations.com/wp-content/uploads/2019/04/hiking-slider.jpg) | image | 1600 × 655 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5805 — logo-hiking](https://volcanvacations.com/wp-content/uploads/2019/04/logo-hiking.png) | image | 255 × 128 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5391 — page-title](https://volcanvacations.com/wp-content/uploads/2019/04/page-title.jpg) | image | 1600 × 444 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5390 — banner-5](https://volcanvacations.com/wp-content/uploads/2019/04/banner-5.png) | image | 300 × 129 | 1 | 200 | EXACT_BYTES_DUPLICATE | REPLACE_WITH_USER_MEDIA |
| [wp-5389 — banner-4](https://volcanvacations.com/wp-content/uploads/2019/04/banner-4.png) | image | 300 × 129 | 1 | 200 | EXACT_BYTES_DUPLICATE | REPLACE_WITH_USER_MEDIA |
| [wp-5388 — banner-3](https://volcanvacations.com/wp-content/uploads/2019/04/banner-3.png) | image | 300 × 129 | 1 | 200 | EXACT_BYTES_DUPLICATE | REPLACE_WITH_USER_MEDIA |
| [wp-5387 — banner-2](https://volcanvacations.com/wp-content/uploads/2019/04/banner-2.png) | image | 300 × 129 | 1 | 200 | EXACT_BYTES_DUPLICATE | REPLACE_WITH_USER_MEDIA |
| [wp-5386 — banner-1](https://volcanvacations.com/wp-content/uploads/2019/04/banner-1.png) | image | 300 × 129 | 1 | 200 | EXACT_BYTES_DUPLICATE | REPLACE_WITH_USER_MEDIA |
| [wp-5385 — title-bg-testimonial](https://volcanvacations.com/wp-content/uploads/2019/04/title-bg-testimonial-2.jpg) | image | 1030 × 241 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5382 — title-bg-recommended](https://volcanvacations.com/wp-content/uploads/2019/04/title-bg-recommended-1.jpg) | image | 1030 × 241 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5381 — title-bg-popular](https://volcanvacations.com/wp-content/uploads/2019/04/title-bg-popular-3.jpg) | image | 1030 × 241 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5377 — title-bg-articles](https://volcanvacations.com/wp-content/uploads/2019/04/title-bg-articles.jpg) | image | 1030 × 241 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5360 — creditcard-logo](https://volcanvacations.com/wp-content/uploads/2019/04/creditcard-logo.png) | image | 254 × 47 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5355 — widget-bg](https://volcanvacations.com/wp-content/uploads/2019/04/widget-bg-1.jpg) | image | 600 × 407 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5337 — shutterstock_1017748132](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_1017748132.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5336 — shutterstock_1011917770](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_1011917770.jpg) | image | 1600 × 1116 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5335 — shutterstock_791325658](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_791325658.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5334 — shutterstock_789412159](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_789412159.jpg) | image | 1600 × 1086 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5333 — shutterstock_781012480](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_781012480.jpg) | image | 1600 × 1068 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5332 — shutterstock_772769227](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_772769227.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5331 — shutterstock_772769215](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_772769215.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5330 — shutterstock_764972821](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg) | image | 1600 × 1066 | 10 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5329 — shutterstock_759608542](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg) | image | 1600 × 1164 | 10 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5328 — shutterstock_758979559](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_758979559.jpg) | image | 1600 × 1069 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5327 — shutterstock_755477821](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_755477821.jpg) | image | 1600 × 910 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5326 — shutterstock_749469604](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_749469604.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5325 — shutterstock_749309983](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_749309983.jpg) | image | 1600 × 1009 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5324 — shutterstock_743964940](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_743964940.jpg) | image | 1600 × 768 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5323 — shutterstock_743910991](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_743910991.jpg) | image | 1600 × 987 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5322 — shutterstock_733898962](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_733898962.jpg) | image | 1600 × 874 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5321 — shutterstock_720444505](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg) | image | 1600 × 1019 | 10 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5320 — shutterstock_713063371](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_713063371.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5319 — shutterstock_712575202](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_712575202.jpg) | image | 1600 × 1027 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5318 — shutterstock_700247896](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_700247896.jpg) | image | 1600 × 930 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5317 — shutterstock_695392744](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_695392744.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5316 — shutterstock_678153238](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_678153238.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5315 — single-icon-6](https://volcanvacations.com/wp-content/uploads/2019/04/single-icon-6.png) | image | 22 × 22 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5314 — single-icon-5](https://volcanvacations.com/wp-content/uploads/2019/04/single-icon-5.png) | image | 30 × 23 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5313 — single-icon-4](https://volcanvacations.com/wp-content/uploads/2019/04/single-icon-4.png) | image | 36 × 22 | 12 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5312 — single-icon-3](https://volcanvacations.com/wp-content/uploads/2019/04/single-icon-3.png) | image | 30 × 21 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5311 — single-icon-2](https://volcanvacations.com/wp-content/uploads/2019/04/single-icon-2.png) | image | 36 × 18 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5287 — logo-v3](https://volcanvacations.com/wp-content/uploads/2019/04/logo-v3.png) | image | 250 × 52 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5286 — ArcaMajora3-Heavy](https://volcanvacations.com/wp-content/uploads/2019/04/ArcaMajora3-Heavy.eot) | application | MISSING × MISSING | 0 | 200 | NOT_BYTE_CHECKED | REPLACE_WITH_USER_MEDIA |
| [wp-5792 — mountian-](https://volcanvacations.com/wp-content/uploads/2019/04/mountian-.jpg) | image | 1207 × 650 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5786 — banner-5](https://volcanvacations.com/wp-content/uploads/2019/04/banner-5-1.png) | image | 300 × 129 | 0 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5800 — banner-4](https://volcanvacations.com/wp-content/uploads/2019/04/banner-4-1.png) | image | 300 × 129 | 0 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5501 — banner-3](https://volcanvacations.com/wp-content/uploads/2019/04/banner-3-1.png) | image | 300 × 129 | 1 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5500 — banner-1](https://volcanvacations.com/wp-content/uploads/2019/04/banner-1-1.png) | image | 300 × 129 | 1 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5797 — banner-2](https://volcanvacations.com/wp-content/uploads/2019/04/banner-2-1.png) | image | 300 × 129 | 0 | 200 | EXACT_BYTES_DUPLICATE | DUPLICATE |
| [wp-5498 — coffee](https://volcanvacations.com/wp-content/uploads/2019/04/coffee.jpg) | image | 785 × 375 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5261 — psinfinite2](https://volcanvacations.com/wp-content/uploads/2019/04/psinfinite2.jpg) | image | 900 × 700 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5260 — shutterstock_666258808](https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_666258808.jpg) | image | 1600 × 1066 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5259 — photo-1428931996691-a5108d4cdbf5](https://volcanvacations.com/wp-content/uploads/2019/04/photo-1428931996691-a5108d4cdbf5-scaled.jpg) | image | 1600 × 2400 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5816 — customer-review](https://volcanvacations.com/wp-content/uploads/2019/04/customer-review.jpg) | image | 1600 × 781 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5478 — counter-bg](https://volcanvacations.com/wp-content/uploads/2019/04/counter-bg.png) | image | 193 × 141 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5253 — tvicon5](https://volcanvacations.com/wp-content/uploads/2019/03/tvicon5.png) | image | 71 × 71 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5252 — bgtravel2](https://volcanvacations.com/wp-content/uploads/2019/03/bgtravel2.jpg) | image | 1600 × 767 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5251 — tvicon4](https://volcanvacations.com/wp-content/uploads/2019/03/tvicon4.png) | image | 134 × 28 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5250 — logo-copy1](https://volcanvacations.com/wp-content/uploads/2019/03/logo-copy1.png) | image | 172 × 36 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5249 — shutterstock_636413090](https://volcanvacations.com/wp-content/uploads/2019/03/shutterstock_636413090.jpg) | image | 1600 × 1150 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5248 — christopher-czermak-705859-unsplash](https://volcanvacations.com/wp-content/uploads/2019/03/christopher-czermak-705859-unsplash.jpg) | image | 1600 × 1060 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5247 — shutterstock_791333146](https://volcanvacations.com/wp-content/uploads/2019/03/shutterstock_791333146.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5246 — angel-origgi-1198759-unsplash](https://volcanvacations.com/wp-content/uploads/2019/03/angel-origgi-1198759-unsplash.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5245 — charles-postiaux-792896-unsplash](https://volcanvacations.com/wp-content/uploads/2019/03/charles-postiaux-792896-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5244 — joseph-barrientos-49318-unsplash](https://volcanvacations.com/wp-content/uploads/2019/03/joseph-barrientos-49318-unsplash.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5243 — shutterstock_1024139929](https://volcanvacations.com/wp-content/uploads/2019/03/shutterstock_1024139929.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5468 — bg-2](https://volcanvacations.com/wp-content/uploads/2019/03/bg-2.jpg) | image | 1600 × 400 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5460 — bg2](https://volcanvacations.com/wp-content/uploads/2019/03/bg2.jpg) | image | 1600 × 400 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5459 — mountain-bg-2](https://volcanvacations.com/wp-content/uploads/2019/03/mountain-bg-2-2.jpg) | image | 1135 × 641 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5458 — mountain-bg-2](https://volcanvacations.com/wp-content/uploads/2019/03/mountain-bg-2-1.jpg) | image | 1259 × 641 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5457 — mountain-bg-2](https://volcanvacations.com/wp-content/uploads/2019/03/mountain-bg-2.jpg) | image | 1259 × 641 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5456 — mountain-bg-1](https://volcanvacations.com/wp-content/uploads/2019/03/mountain-bg-1.jpg) | image | 1450 × 550 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5455 — flag](https://volcanvacations.com/wp-content/uploads/2019/03/flag.png) | image | 55 × 50 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5451 — drawing](https://volcanvacations.com/wp-content/uploads/2019/03/drawing.jpg) | image | 800 × 885 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5427 — backpack](https://volcanvacations.com/wp-content/uploads/2019/03/backpack.png) | image | 60 × 60 | 5 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5426 — map](https://volcanvacations.com/wp-content/uploads/2019/03/map.png) | image | 60 × 60 | 5 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5425 — knife](https://volcanvacations.com/wp-content/uploads/2019/03/knife.png) | image | 60 × 60 | 4 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5424 — clibing](https://volcanvacations.com/wp-content/uploads/2019/03/clibing.png) | image | 60 × 60 | 5 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5232 — tvicon3](https://volcanvacations.com/wp-content/uploads/2019/03/tvicon3.png) | image | 51 × 51 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5231 — tvicon2.1](https://volcanvacations.com/wp-content/uploads/2019/03/tvicon2.1.png) | image | 48 × 50 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5230 — tvicon2](https://volcanvacations.com/wp-content/uploads/2019/03/tvicon2.png) | image | 48 × 50 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5398 — binoculars](https://volcanvacations.com/wp-content/uploads/2019/03/binoculars.png) | image | 45 × 45 | 4 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5229 — tvicon1.1](https://volcanvacations.com/wp-content/uploads/2019/03/tvicon1.1.png) | image | 59 × 59 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5224 — tvicon1](https://volcanvacations.com/wp-content/uploads/2019/03/tvicon1.png) | image | 59 × 59 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5223 — bgtravel](https://volcanvacations.com/wp-content/uploads/2019/03/bgtravel.jpg) | image | 1600 × 622 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5304 — single-icon-pin](https://volcanvacations.com/wp-content/uploads/2018/06/single-icon-pin.png) | image | 30 × 23 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5303 — single-icon-user](https://volcanvacations.com/wp-content/uploads/2018/06/single-icon-user-1.png) | image | 36 × 22 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5302 — single-icon-wifi](https://volcanvacations.com/wp-content/uploads/2018/06/single-icon-wifi.png) | image | 30 × 21 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5301 — single-icon-users](https://volcanvacations.com/wp-content/uploads/2018/06/single-icon-users.png) | image | 36 × 18 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5300 — single-icon-user](https://volcanvacations.com/wp-content/uploads/2018/06/single-icon-user.png) | image | 22 × 22 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5299 — single-icon-cal](https://volcanvacations.com/wp-content/uploads/2018/06/single-icon-cal.png) | image | 22 × 22 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5795 — review-2](https://volcanvacations.com/wp-content/uploads/2018/06/review-2.jpg) | image | 400 × 400 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5793 — review-1](https://volcanvacations.com/wp-content/uploads/2018/06/review-1.jpg) | image | 400 × 400 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5791 — icon.clock](https://volcanvacations.com/wp-content/uploads/2018/06/icon.clock_.png) | image | 51 × 51 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5785 — icon.destination](https://volcanvacations.com/wp-content/uploads/2018/06/icon.destination.png) | image | 52 × 52 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5794 — icon.suitcase](https://volcanvacations.com/wp-content/uploads/2018/06/icon.suitcase.png) | image | 50 × 50 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5241 — icon-play](https://volcanvacations.com/wp-content/uploads/2018/06/icon-play.png) | image | 89 × 89 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5237 — icon-user](https://volcanvacations.com/wp-content/uploads/2018/06/icon-user.png) | image | 43 × 40 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5236 — icon-bed](https://volcanvacations.com/wp-content/uploads/2018/06/icon-bed.png) | image | 47 × 43 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5235 — icon-wifi](https://volcanvacations.com/wp-content/uploads/2018/06/icon-wifi.png) | image | 55 × 39 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5234 — icon-yacht](https://volcanvacations.com/wp-content/uploads/2018/06/icon-yacht.png) | image | 52 × 53 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5233 — service-bg](https://volcanvacations.com/wp-content/uploads/2018/06/service-bg.jpg) | image | 1600 × 578 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5799 — svc-bg](https://volcanvacations.com/wp-content/uploads/2018/06/svc-bg.jpg) | image | 1600 × 583 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5211 — shutterstock_151616084](https://volcanvacations.com/wp-content/uploads/2017/07/shutterstock_151616084.jpg) | image | 1600 × 1068 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5110 — pexels-photo-copy](https://volcanvacations.com/wp-content/uploads/2017/02/pexels-photo-copy.jpg) | image | 1600 × 1068 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5109 — photo-1447834353189-91c48abf20e1](https://volcanvacations.com/wp-content/uploads/2017/02/photo-1447834353189-91c48abf20e1.jpg) | image | 1600 × 1297 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5018 — landing-logo](https://volcanvacations.com/wp-content/uploads/2017/02/landing-logo.png) | image | 237 × 31 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-5014 — landing-bg](https://volcanvacations.com/wp-content/uploads/2017/02/landing-bg.jpg) | image | 1600 × 935 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4925 — travel-tour-logo](https://volcanvacations.com/wp-content/uploads/2017/01/travel-tour-logo.png) | image | 160 × 23 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4924 — widget-bg](https://volcanvacations.com/wp-content/uploads/2017/01/widget-bg.jpg) | image | 400 × 271 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4905 — TNK87N7464](https://volcanvacations.com/wp-content/uploads/2017/01/TNK87N7464.jpg) | image | 1600 × 1067 | 1 | 200 | EXACT_BYTES_DUPLICATE | REPLACE_WITH_USER_MEDIA |
| [wp-4904 — photo-1428931996691-a5108d4cdbf5](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1428931996691-a5108d4cdbf5-scaled.jpg) | image | 1600 × 2400 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4890 — tf-logo](https://volcanvacations.com/wp-content/uploads/2017/01/tf-logo.jpg) | image | 80 × 80 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4850 — award-2](https://volcanvacations.com/wp-content/uploads/2017/01/award-2.png) | image | 156 × 150 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4849 — award-1](https://volcanvacations.com/wp-content/uploads/2017/01/award-1.png) | image | 205 × 86 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4847 — slider-3](https://volcanvacations.com/wp-content/uploads/2017/01/slider-3.jpg) | image | 1600 × 750 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4846 — slider-2](https://volcanvacations.com/wp-content/uploads/2017/01/slider-2.jpg) | image | 1600 × 750 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4842 — search-bg-3](https://volcanvacations.com/wp-content/uploads/2017/01/search-bg-3.jpg) | image | 600 × 1693 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4689 — stunning-bg-2](https://volcanvacations.com/wp-content/uploads/2017/01/stunning-bg-2.jpg) | image | 1600 × 578 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4688 — tour-bg-3](https://volcanvacations.com/wp-content/uploads/2017/01/tour-bg-3.jpg) | image | 1600 × 985 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4686 — search-bg-2](https://volcanvacations.com/wp-content/uploads/2017/01/search-bg-2.jpg) | image | 1600 × 533 | 4 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4681 — testimonial-bg](https://volcanvacations.com/wp-content/uploads/2017/01/testimonial-bg.jpg) | image | 1600 × 622 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4672 — tour-bg-2](https://volcanvacations.com/wp-content/uploads/2017/01/tour-bg-2.jpg) | image | 1600 × 436 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4664 — stunning-bg](https://volcanvacations.com/wp-content/uploads/2017/01/stunning-bg.jpg) | image | 1600 × 622 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4663 — search-bg](https://volcanvacations.com/wp-content/uploads/2017/01/search-bg.jpg) | image | 1600 × 767 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4661 — search-bg-top](https://volcanvacations.com/wp-content/uploads/2017/01/search-bg-top.jpg) | image | 1600 × 342 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4652 — slider-1](https://volcanvacations.com/wp-content/uploads/2017/01/slider-1.jpg) | image | 1600 × 750 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4638 — rio-de-janeiro-olympics-2016-niteroi-brazil-161212](https://volcanvacations.com/wp-content/uploads/2017/01/rio-de-janeiro-olympics-2016-niteroi-brazil-161212.jpeg) | image | 1600 × 768 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4636 — pexels-photo-176400](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo-176400.jpeg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4633 — pexels-photo-164276](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo-164276.jpeg) | image | 1600 × 913 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4631 — St. Julians Bay – Malta](https://volcanvacations.com/wp-content/uploads/2017/01/photodune-248725-st-julians-bay-malta-m.jpg) | image | 1600 × 1066 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4630 — Venice](https://volcanvacations.com/wp-content/uploads/2017/01/photodune-488847-venice-m.jpg) | image | 1600 × 1063 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4629 — Trevi Fountain](https://volcanvacations.com/wp-content/uploads/2017/01/photodune-4051544-trevi-fountain-m.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4628 — Golden Gate Bridge](https://volcanvacations.com/wp-content/uploads/2017/01/photodune-4791527-golden-gate-bridge-m.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4626 — pexels-photo-14676](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo-14676.png) | image | 1600 × 1000 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4625 — pexels-photo-91216](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo-91216.jpeg) | image | 1600 × 1068 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4624 — pexels-photo-172221](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo-172221.jpeg) | image | 1600 × 1068 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4622 — pexels-photo-47426](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo-47426.jpeg) | image | 1600 × 900 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4615 — shutterstock_246506902](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_246506902.jpg) | image | 1600 × 1065 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4614 — shutterstock_234539515](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_234539515.jpg) | image | 1600 × 1149 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4613 — shutterstock_179675966](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_179675966.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4612 — shutterstock_152727797](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_152727797.jpg) | image | 1600 × 1259 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4611 — shutterstock_150557642](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_150557642.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4610 — shutterstock_149105702](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_149105702.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4609 — shutterstock_120562819](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_120562819.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4603 — pexels-photo](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo.jpeg) | image | 1600 × 1199 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4602 — pexels-photo copy 2](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo-copy-2.jpg) | image | 1600 × 1063 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4593 — city-landmark-lights-night](https://volcanvacations.com/wp-content/uploads/2017/01/city-landmark-lights-night.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4592 — Fotolia_16069076_Subscription_Monthly_XXL](https://volcanvacations.com/wp-content/uploads/2017/01/Fotolia_16069076_Subscription_Monthly_XXL.jpg) | image | 1000 × 1000 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4588 — banner-5](https://volcanvacations.com/wp-content/uploads/2017/01/banner-5.png) | image | 151 × 33 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4587 — banner-4](https://volcanvacations.com/wp-content/uploads/2017/01/banner-4.png) | image | 132 × 46 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4586 — banner-3](https://volcanvacations.com/wp-content/uploads/2017/01/banner-3.png) | image | 148 × 44 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4585 — banner-2](https://volcanvacations.com/wp-content/uploads/2017/01/banner-2.png) | image | 141 × 45 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4584 — banner-1](https://volcanvacations.com/wp-content/uploads/2017/01/banner-1.png) | image | 138 × 49 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4583 — icon-9](https://volcanvacations.com/wp-content/uploads/2017/01/icon-9.png) | image | 41 × 50 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4582 — icon-8](https://volcanvacations.com/wp-content/uploads/2017/01/icon-8.png) | image | 38 × 50 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4581 — icon-7](https://volcanvacations.com/wp-content/uploads/2017/01/icon-7.png) | image | 29 × 48 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4574 — icon-6](https://volcanvacations.com/wp-content/uploads/2017/01/icon-6.png) | image | 50 × 47 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4573 — icon-5](https://volcanvacations.com/wp-content/uploads/2017/01/icon-5.png) | image | 50 × 40 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4558 — pexels-photo-50632](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo-50632.jpeg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4557 — city-sunny-people-street](https://volcanvacations.com/wp-content/uploads/2017/01/city-sunny-people-street.jpg) | image | 1600 × 1063 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4556 — italian-landscape-mountains-nature](https://volcanvacations.com/wp-content/uploads/2017/01/italian-landscape-mountains-nature.jpg) | image | 1600 × 1067 | 3 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4555 — photo-1451337516015-6b6e9a44a8a3](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1451337516015-6b6e9a44a8a3.jpg) | image | 1600 × 1297 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4554 — photo-1448518184296-a22facb4446f](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1448518184296-a22facb4446f.jpg) | image | 1600 × 1067 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4553 — photo-1447876394678-42a7efa1b6db](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1447876394678-42a7efa1b6db.jpg) | image | 1600 × 1008 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4552 — photo-1443890484047-5eaa67d1d630](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1443890484047-5eaa67d1d630.jpg) | image | 1600 × 1297 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4551 — photo-1443479579455-1860f114bf77](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1443479579455-1860f114bf77.jpg) | image | 1600 × 1076 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4550 — photo-1441716844725-09cedc13a4e7](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1441716844725-09cedc13a4e7.jpg) | image | 1600 × 1076 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4549 — photo-1441155472722-d17942a2b76a](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1441155472722-d17942a2b76a.jpg) | image | 1600 × 1076 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4548 — photo-1440470177828-6381dc5074ba](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1440470177828-6381dc5074ba.jpg) | image | 1600 × 1076 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4547 — photo-1439853949127-fa647821eba0](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1439853949127-fa647821eba0.jpg) | image | 1600 × 1076 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4546 — photo-1437651025703-2858c944e3eb](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1437651025703-2858c944e3eb.jpg) | image | 1600 × 1076 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4535 — adg3com_crypticpsyche](https://volcanvacations.com/wp-content/uploads/2017/01/adg3com_crypticpsyche.mp3) | audio | MISSING × MISSING | 0 | 200 | NOT_BYTE_CHECKED | REPLACE_WITH_USER_MEDIA |
| [wp-4529 — section-bg-4](https://volcanvacations.com/wp-content/uploads/2017/01/section-bg-4.jpg) | image | 1600 × 760 | 15 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4528 — section-bg-3](https://volcanvacations.com/wp-content/uploads/2017/01/section-bg-3.jpg) | image | 1600 × 760 | 7 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4527 — section-bg-2](https://volcanvacations.com/wp-content/uploads/2017/01/section-bg-2.jpg) | image | 1600 × 622 | 8 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4526 — section-bg-1](https://volcanvacations.com/wp-content/uploads/2017/01/section-bg-1.jpg) | image | 1600 × 622 | 5 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4517 — Field](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1442589031151-61d5645469d7.jpg) | image | 1600 × 1060 | 3 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4516 — Forest](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1459255418679-d6424da9ee33.jpg) | image | 1600 × 1069 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4515 — Snow mountain](https://volcanvacations.com/wp-content/uploads/2017/01/photo-1443890923422-7819ed4101c0.jpg) | image | 1600 × 1067 | 3 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4514 — above-adventure-aerial-air](https://volcanvacations.com/wp-content/uploads/2017/01/above-adventure-aerial-air.jpg) | image | 1600 × 1089 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4513 — sunrise-phu-quoc-island-ocean](https://volcanvacations.com/wp-content/uploads/2017/01/sunrise-phu-quoc-island-ocean.jpg) | image | 1600 × 1056 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4512 — pexels-photo-67386](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo-67386.jpeg) | image | 1600 × 1067 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4511 — shutterstock_280938698](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_280938698.jpg) | image | 1600 × 1135 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4510 — shutterstock_255194035](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_255194035.jpg) | image | 1600 × 1067 | 3 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4509 — shutterstock_254090041](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_254090041.jpg) | image | 1600 × 1067 | 5 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4508 — shutterstock_245507692](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_245507692.jpg) | image | 1600 × 1067 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4507 — Paris](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_242387536.jpg) | image | 1600 × 1067 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4506 — Lake](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_220323652.jpg) | image | 1600 × 1131 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4505 — Forest](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_210601591.jpg) | image | 1600 × 1067 | 4 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4504 — Canoe](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_198556997.jpg) | image | 1600 × 1067 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4503 — shutterstock_178807262](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_178807262.jpg) | image | 1600 × 1067 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4502 — shutterstock_154497503](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_154497503.jpg) | image | 1600 × 1067 | 3 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4501 — shutterstock_147744218](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_147744218.jpg) | image | 1600 × 1068 | 3 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4500 — shutterstock_139999093](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_139999093.jpg) | image | 1600 × 1067 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4499 — shutterstock_136984760](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_136984760.jpg) | image | 1600 × 1052 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4498 — shutterstock_134373716](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_134373716.jpg) | image | 1600 × 1065 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4497 — shutterstock_132927353](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_132927353.jpg) | image | 1600 × 1067 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4496 — shutterstock_129132983](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_129132983.jpg) | image | 1600 × 1068 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4495 — shutterstock_124333858](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_124333858.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4494 — shutterstock_117062077](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_117062077.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4493 — shutterstock_109075058](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_109075058.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4492 — Canyon](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_94851763.jpg) | image | 1600 × 1062 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4491 — Paris](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_74901229.jpg) | image | 1600 × 1067 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4490 — shutterstock_61340065](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_61340065.jpg) | image | 1600 × 1067 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4489 — Traveller](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_195507533.jpg) | image | 1600 × 1067 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4488 — Backpack](https://volcanvacations.com/wp-content/uploads/2017/01/pexels-photo.jpg) | image | 1600 × 1067 | 2 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4486 — Urban](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_151616084.jpg) | image | 1280 × 854 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4485 — shutterstock_166193831](https://volcanvacations.com/wp-content/uploads/2017/01/shutterstock_166193831.jpg) | image | 1280 × 854 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4113 — personnel-6](https://volcanvacations.com/wp-content/uploads/2016/11/personnel-6.jpg) | image | 1300 × 961 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4111 — personnel-5](https://volcanvacations.com/wp-content/uploads/2016/11/personnel-5.jpg) | image | 552 × 619 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4110 — personnel-4](https://volcanvacations.com/wp-content/uploads/2016/11/personnel-4.jpg) | image | 600 × 662 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4109 — personnel-3](https://volcanvacations.com/wp-content/uploads/2016/11/personnel-3.jpg) | image | 600 × 662 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4108 — personnel-2](https://volcanvacations.com/wp-content/uploads/2016/11/personnel-2.jpg) | image | 600 × 662 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-4107 — personnel-1](https://volcanvacations.com/wp-content/uploads/2016/11/personnel-1.jpg) | image | 1139 × 1279 | 1 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [wp-1376 — service-bg-2](https://volcanvacations.com/wp-content/uploads/2016/06/service-bg-2.jpg) | image | 945 × 575 | 0 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [url-2b972fcc5cb2 — creditcard-logo.png](https://demo.goodlayers.com/traveltour/citytour/wp-content/uploads/2017/07/creditcard-logo.png) | image | 254 × 47 | 255 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [url-29cfc4f9e0a8 — watch](https://www.youtube.com/watch?v=F0uq5gyqIf8) | video | MISSING × MISSING | 1 | 200 | NOT_BYTE_CHECKED | REPLACE_WITH_USER_MEDIA |
| [url-1d7847c98f21 — 110891225](https://vimeo.com/110891225) | video | MISSING × MISSING | 1 | 200 | NOT_BYTE_CHECKED | REPLACE_WITH_USER_MEDIA |
| [url-6e46a0cb247d — 141591617](https://vimeo.com/141591617) | video | MISSING × MISSING | 1 | 200 | NOT_BYTE_CHECKED | REPLACE_WITH_USER_MEDIA |
| [url-8213f74b09d1 — sidebar-bg.jpg](https://demo.goodlayers.com/traveltour/hiking/wp-content/uploads/2019/05/sidebar-bg.jpg) | image | 800 × 600 | 48 | 200 | NO_EXACT_DUPLICATE_FOUND | REPLACE_WITH_USER_MEDIA |
| [url-47c9ca370219 — admin-transaction-1.jpg](https://demo.goodlayers.com/traveltour/main3/wp-content/uploads/2017/01/admin-transaction-1.jpg) | image | MISSING × MISSING | 1 | 404 | NOT_BYTE_CHECKED | BROKEN |
| [url-a028b11ba1f9 — admin-transaction-2.jpg](https://demo.goodlayers.com/traveltour/main3/wp-content/uploads/2017/01/admin-transaction-2.jpg) | image | MISSING × MISSING | 1 | 404 | NOT_BYTE_CHECKED | BROKEN |
| [url-ee509c20a9e1 — customer-dashboard-1.jpg](https://demo.goodlayers.com/traveltour/main3/wp-content/uploads/2017/01/customer-dashboard-1.jpg) | image | MISSING × MISSING | 1 | 404 | NOT_BYTE_CHECKED | BROKEN |
| [url-a2a9340e69af — customer-bookings.jpg](https://demo.goodlayers.com/traveltour/main3/wp-content/uploads/2017/01/customer-bookings.jpg) | image | MISSING × MISSING | 1 | 404 | NOT_BYTE_CHECKED | BROKEN |
| [url-dfc735995c44 — customer-booking-single.jpg](https://demo.goodlayers.com/traveltour/main3/wp-content/uploads/2017/01/customer-booking-single.jpg) | image | MISSING × MISSING | 1 | 404 | NOT_BYTE_CHECKED | BROKEN |
| [url-e4fdc01f45ef — customer-review.jpg](https://demo.goodlayers.com/traveltour/main3/wp-content/uploads/2017/01/customer-review.jpg) | image | MISSING × MISSING | 1 | 404 | NOT_BYTE_CHECKED | BROKEN |
| [url-0f9b0eb92833 — customer-invoice-list.jpg](https://demo.goodlayers.com/traveltour/main3/wp-content/uploads/2017/01/customer-invoice-list.jpg) | image | MISSING × MISSING | 1 | 404 | NOT_BYTE_CHECKED | BROKEN |
| [url-ae339046bc32 — customer-invoice.jpg](https://demo.goodlayers.com/traveltour/main3/wp-content/uploads/2017/01/customer-invoice.jpg) | image | MISSING × MISSING | 1 | 404 | NOT_BYTE_CHECKED | BROKEN |
| [url-2451f27d0092 — customer-wishlist.jpg](https://demo.goodlayers.com/traveltour/main3/wp-content/uploads/2017/01/customer-wishlist.jpg) | image | MISSING × MISSING | 1 | 404 | NOT_BYTE_CHECKED | BROKEN |
| [url-cdbbca7090d8 — Screen-Shot-2017-01-31-at-16.35.33.png](https://demo.goodlayers.com/traveltour/main3/wp-content/uploads/2017/01/Screen-Shot-2017-01-31-at-16.35.33.png) | image | MISSING × MISSING | 1 | 404 | NOT_BYTE_CHECKED | BROKEN |
| [url-5cb528cc2764 — watch](https://www.youtube.com/watch?v=HODmbzOT288) | video | MISSING × MISSING | 1 | 200 | NOT_BYTE_CHECKED | REPLACE_WITH_USER_MEDIA |
| [url-356657cb1d68 — watch](https://www.youtube.com/watch?v=HODmbzOT288&list=PLNIFTA4Bjp3stwYxIB6Aokpr9bfRQYO73) | video | MISSING × MISSING | 1 | 200 | SAME_EXTERNAL_VIDEO_REFERENCE | DUPLICATE |
