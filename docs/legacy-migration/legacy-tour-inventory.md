# Legacy tour and product inventory

Audit date: 2026-09-07. **13 named product records: 12 tours + 1 shuttle.** These are 13 distinct public IDs/names, not proof of 13 distinct current offers; the two horseback records may be variants or duplicates.

No data was imported. Canonical public contact: **info@volcanvacations.com**. A source-confirmed value is not a current business confirmation.

| Status | Meaning |
| --- | --- |
| VERIFIED_FROM_LEGACY | Clearly present in a public source; not independently confirmed current. |
| LIKELY_VALID | Analyst finds source coherent; still not a current supplier confirmation. |
| NEEDS_PARTNER_VERIFICATION | Missing commercial validation or questionable applicability. |
| MISSING | Not supplied by the inspected public source; no value invented. |
| LEGACY_PLACEHOLDER | Template, dummy, or strongly suspected copied placeholder value; exclude from import. |
| CONFLICTING | Conflicting source claims retained without choosing one. |

## Catalog summary

| Legacy ID / product | Legacy From price | Current verified price / net cost | Comparison | Disposition |
| --- | --- | --- | --- | --- |
| [6198 — Arenal Volcano Horseback Riding & Hot River](https://volcanvacations.com/tour/arenal-volcano-horseback-riding-hot-river/) | $65.00; ISO currency unconfirmed | MISSING / MISSING | POSSIBLE_DUPLICATE | DO_NOT_IMPORT |
| [6135 — Shuttle: SJO – Juan Santamaría International Airport to La Fortuna – Arenal Volcano](https://volcanvacations.com/tour/shuttle-sjo-juan-santamaria-international-airport-to-la-fortuna-arenal-volcano/) | $1.00; ISO currency unconfirmed | MISSING / MISSING | NEEDS_REVIEW | DO_NOT_IMPORT |
| [5993 — Sloth Watching Walk](https://volcanvacations.com/tour/sloth-watching-walk/) | $60.00; ISO currency unconfirmed | MISSING / MISSING | NEW_LEGACY_TOUR | NEEDS_VERIFICATION |
| [5990 — Frog Watching Night Walk](https://volcanvacations.com/tour/frog-watching-night-walk/) | $65.00; ISO currency unconfirmed | MISSING / MISSING | NEW_LEGACY_TOUR | NEEDS_VERIFICATION |
| [5986 — Cano Negro Wildlife Refuge](https://volcanvacations.com/tour/cano-negro-wildlife-refuge/) | $1.00; ISO currency unconfirmed | MISSING / MISSING | NEW_LEGACY_TOUR | NEEDS_VERIFICATION |
| [5981 — Arenal Volcano Horseback Riding](https://volcanvacations.com/tour/arenal-volcano-horseback-riding/) | $1.00; ISO currency unconfirmed | MISSING / MISSING | POSSIBLE_DUPLICATE | NEEDS_VERIFICATION |
| [5978 — Canyoning & Waterfall Rappelling](https://volcanvacations.com/tour/canyoning-waterfall-rappelling/) | $1.00; ISO currency unconfirmed | MISSING / MISSING | NEW_LEGACY_TOUR | NEEDS_VERIFICATION |
| [5975 — Jungle and Maleku’s ATV Tour](https://volcanvacations.com/tour/jungle-and-malekus-atv-tour/) | $1.00; ISO currency unconfirmed | MISSING / MISSING | NEW_LEGACY_TOUR | NEEDS_VERIFICATION |
| [5972 — Arenal Volcano Hike and Hot River](https://volcanvacations.com/tour/arenal-volcano-hike-and-hot-river/) | $1.00; ISO currency unconfirmed | MISSING / MISSING | MATCHES_CURRENT_DEMO | NEEDS_VERIFICATION |
| [5969 — Arenal Hanging Bridges](https://volcanvacations.com/tour/arenal-hanging-bridges/) | $1.00; ISO currency unconfirmed | MISSING / MISSING | MATCHES_CURRENT_DEMO | NEEDS_VERIFICATION |
| [5966 — Rio Celeste Waterfall Hike and Lunch](https://volcanvacations.com/tour/rio-celeste-waterfall-hike-and-lunch-2/) | $1.00; ISO currency unconfirmed | MISSING / MISSING | NEEDS_REVIEW | NEEDS_VERIFICATION |
| [5592 — White Water Rafting Class III & IV on Rio La Balsa](https://volcanvacations.com/tour/white-water-rafting-class-iii-iv-on-rio-la-balsa-2/) | $1.00; ISO currency unconfirmed | MISSING / MISSING | MATCHES_CURRENT_DEMO | NEEDS_VERIFICATION |
| [5502 — La Fortuna Waterfall, Arenal Volcano, & Hot River](https://volcanvacations.com/tour/white-water-rafting-class-iii-iv-on-rio-la-balsa/) | $1.00; ISO currency unconfirmed | MISSING / MISSING | NEEDS_REVIEW | NEEDS_VERIFICATION |

## Shared problems

- 10 of 13 displayed prices are $1. The three other cards show $60/$65; none is current-confirmed. The shuttle body additionally says $55 per person.
- All 13 REST excerpts are identical Latin placeholder copy; all REST tour body fields are empty. Descriptions were recovered from rendered HTML instead.
- 12 repeat 5 Hours, 13+, 08:20 and the same boat-guide/lunch/towels inclusion list.
- Nine share exactly the same waterfall/volcano/hot-river description. The shuttle copies the sloth walk.
- No contracting supplier, current net cost, or tour-specific cancellation policy is established for any product.
- Media and contact defects are recorded separately; gallery images are not supplier evidence.

## Current six demo counterparts

| Current demo | Legacy candidate | Result |
| --- | --- | --- |
| Whitewater Rafting | 5592 | Thematic match only; Balsa/Sarapiquí conflict unresolved. $85/$50/$35 remain demo reference values. |
| Arenal Volcano Hike | 5972 | Thematic match; scope of added hot river/waterfall is unresolved. |
| Hot Springs Experience | MISSING | No standalone hot-springs product found; hot river in combination tours is not an equivalent offer. |
| Wildlife & Hanging Bridges | 5969 | Thematic match; operator/park and scope still unknown. |
| Waterfall Adventure | 5502 or 5966 | Ambiguous: La Fortuna combination versus Río Celeste. Do not choose from the generic demo name. |
| Coffee & Chocolate Tour | MISSING | No identifiable legacy product found. |

PostgreSQL contains 16 products: these six seed tours plus ten audit/test products; all are preserved. It also contains 12 suppliers and 12 image rows, all retained.


## 6198 — Arenal Volcano Horseback Riding & Hot River

Source: https://volcanvacations.com/tour/arenal-volcano-horseback-riding-hot-river/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, POSSIBLE_HORSEBACK_VARIANT_DUPLICATE, UNRELATED_COPIED_WATERFALL_ITINERARY, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS, UNRELATED_STOCK_GALLERY, IDENTICAL_DESCRIPTION_ON_9_PRODUCTS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Arenal Volcano Horseback Riding & Hot River | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | La Fortuna / Arenal volcano / Rio Tabacón (body claims) | NEEDS_PARTNER_VERIFICATION |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 ed06d89edc97f6c8 | CONFLICTING |
| legacy_retail_price | 65.00 | NEEDS_PARTNER_VERIFICATION |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | LEGACY_PLACEHOLDER |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5330; wp-6212; wp-5329; wp-5321 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg; https://volcanvacations.com/wp-content/uploads/2026/02/5-1-1.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

First we go to the majestic La Fortuna waterfall, which is 70 meters high; where if the weather allows it, we will bathe in its crystal clear waters. We will be around one hour and thirty minutes in this place; then we will take the minibus to go to the next point and one of the most spectacular, the incline walk in the rain forest towards the base of the Arenal volcano, where we will visit the lava flows from the years 1525, 1968 and 2010; also while we enjoy this beautiful ecological park we will learn about the trees and animals that inhabit this place. (About two hours up to the base of the volcano, and one hour down to the green lagoon). After the descent we will enjoy a swim in a totally clean green lagoon with volcanic formation. Once we have enjoyed this, we will have a traditional lunch. To finish we return to the bus to go to the natural river of hot springs (Rio Tabacón), where we will enjoy a majestic place, and also enjoy a mud mask from the base of the Arenal volcano. For after a great day of adventure and experience, be returning to La Fortuna around 4pm.


## 6135 — Shuttle: SJO – Juan Santamaría International Airport to La Fortuna – Arenal Volcano

Source: https://volcanvacations.com/tour/shuttle-sjo-juan-santamaria-international-airport-to-la-fortuna-arenal-volcano/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, SHUTTLE_PAGE_CONTAINS_SLOTH_COPY_AND_SLOTH_IMAGES, PRICE_CONFLICT_1_VS_55, DURATION_CONFLICT_5_VS_1_5, SHUTTLE_API_NOT_SUPPORTED, ONE_DOLLAR_PLACEHOLDER_PRICE, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Shuttle: SJO – Juan Santamaría International Airport to La Fortuna – Arenal Volcano | VERIFIED_FROM_LEGACY |
| category | Shuttle | VERIFIED_FROM_LEGACY |
| activities | MISSING | MISSING |
| location | SJO – Juan Santamaría International Airport → La Fortuna – Arenal Volcano | NEEDS_PARTNER_VERIFICATION |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 5c2433d78c10513e | CONFLICTING |
| legacy_retail_price | 1.00 | LEGACY_PLACEHOLDER |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | CONFLICTING |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | Comfortable clothing for walking; Closed-toe hiking shoes; Waterproof jacket; Mosquito repellent; Sunscreen | CONFLICTING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5960; wp-6072 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2026/02/Sloth02.jpg; https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.41-PM.jpeg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

Duration
1.5 Hours – $55 per person
About
Description
It’s an outdoor hiking tour through the rain forest with the help of a naturalistic guide to look for the sloths in the wild. We’ll be finding an average of four to six sloths in the area.
We have about 2 miles trails with a rich biodiversity so we also be able to appreciate some birds, frogs, insects and other wildlife around.
This adventure takes one and a half hours to be done but it’s a gentile hike in a flat land 30 acres property.
Duration:
1.5 hours.
What to Bring:
• Comfortable clothing for walking
• Closed-toe hiking shoes
• Waterproof jacket
• Mosquito repellent
• Sunscreen
Included/Excluded
Professional bilingual guide.
Transportation to and from your hotel in the La Fortuna area.
Entrance fees

Additional claims: 1.5 Hours – $55 per person; 1.5 hours.


## 5993 — Sloth Watching Walk

Source: https://volcanvacations.com/tour/sloth-watching-walk/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Sloth Watching Walk | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | La Fortuna area (hotel pickup stated) | VERIFIED_FROM_LEGACY |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 cd44bc25e190624f | VERIFIED_FROM_LEGACY |
| legacy_retail_price | 60.00 | NEEDS_PARTNER_VERIFICATION |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 1.5 Hours | VERIFIED_FROM_LEGACY |
| departure_times | Hourly 8AM to 4PM | VERIFIED_FROM_LEGACY |
| minimum_age | All Ages | VERIFIED_FROM_LEGACY |
| maximum_group_size | 15 per guide | VERIFIED_FROM_LEGACY |
| difficulty | gentile hike in a flat land | NEEDS_PARTNER_VERIFICATION |
| supplier_operator | MISSING | MISSING |
| whats_included | Professional bilingual guide; Transportation to and from your hotel in the La Fortuna area; Entrance fees | VERIFIED_FROM_LEGACY |
| what_to_bring | Comfortable clothing for walking; Closed-toe hiking shoes; Waterproof jacket; Mosquito repellent; Sunscreen | VERIFIED_FROM_LEGACY |
| pickup_information | Transportation to and from your hotel in the La Fortuna area | VERIFIED_FROM_LEGACY |
| transportation_information | Transportation to and from your hotel in the La Fortuna area | VERIFIED_FROM_LEGACY |
| cancellation_information | MISSING | MISSING |
| images | wp-5960; wp-6072 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2026/02/Sloth02.jpg; https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.41-PM.jpeg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | All Ages; Hourly 8AM to 4PM; Duration 1.5 Hours; Max 15 Per Guide | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

It’s an outdoor hiking tour through the rain forest with the help of a naturalistic guide to look for the sloths in the wild. We’ll be finding an average of four to six sloths in the area.

We have about 2 miles trails with a rich biodiversity so we also be able to appreciate some birds, frogs, insects and other wildlife around.

This adventure takes one and a half hours to be done but it’s a gentile hike in a flat land 30 acres property.


## 5990 — Frog Watching Night Walk

Source: https://volcanvacations.com/tour/frog-watching-night-walk/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, NIGHT_TOUR_VS_08_20_DEPARTURE, BOAT_GUIDE_LUNCH_TEMPLATE_ON_NIGHT_WALK, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Frog Watching Night Walk | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | Arenal Oasis | NEEDS_PARTNER_VERIFICATION |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 16eb6422df058b3e | NEEDS_PARTNER_VERIFICATION |
| legacy_retail_price | 65.00 | NEEDS_PARTNER_VERIFICATION |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | LEGACY_PLACEHOLDER |
| departure_times | 08:20 | CONFLICTING |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-6086; wp-6085; wp-6090 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM6.jpeg; https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM7.jpeg; https://volcanvacations.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-02-03-at-3.31.05-PM2.jpeg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

Step into the magical realm of Arenal Oasis after dark, where the symphony of nature takes on a whole new rhythm.

Our night tour isn’t just an exploration; it’s a journey into the mysterious and enchanting nocturnal world of Costa Rica’s rainforest.

As the sun dips below the horizon, the forest comes alive with a cacophony of sounds and a spectacle of sights unseen by daylight.

Led by our knowledgeable guides, you’ll embark on an adventure that will awaken your senses and ignite your imagination.

Imagine walking through the dimly lit pathways, your senses heightened as you listen to the haunting calls of nocturnal creatures echoing through the trees.

With each step, you’ll discover the hidden treasures of the forest, from the mesmerizing glow of bioluminescent fungi to colorful frogs, from camouflage reptiles to the stealthy movements of nocturnal mammals like armadillos and kinkajous.

But our night tour is more than just a thrilling encounter with wildlife; it’s a journey of discovery and conservation.

By joining us, you become part of our mission to protect these fragile ecosystems and the creatures that call them home.

So come, immerse yourself in the mystery and magic of Arenal Oasis after dark.

Whether you’re a nature enthusiast or an adventurous spirit seeking new experiences, this tour promises to leave you spellbound and with memories that will last a lifetime.


## 5986 — Cano Negro Wildlife Refuge

Source: https://volcanvacations.com/tour/cano-negro-wildlife-refuge/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, UNRELATED_COPIED_WATERFALL_ITINERARY, NAME_SPELLING_REVIEW_CANO_NEGRO, ONE_DOLLAR_PLACEHOLDER_PRICE, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS, UNRELATED_STOCK_GALLERY, IDENTICAL_DESCRIPTION_ON_9_PRODUCTS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Cano Negro Wildlife Refuge | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | Cano Negro Wildlife Refuge | NEEDS_PARTNER_VERIFICATION |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 ed06d89edc97f6c8 | CONFLICTING |
| legacy_retail_price | 1.00 | LEGACY_PLACEHOLDER |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | LEGACY_PLACEHOLDER |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5330; wp-5329; wp-5321 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

First we go to the majestic La Fortuna waterfall, which is 70 meters high; where if the weather allows it, we will bathe in its crystal clear waters. We will be around one hour and thirty minutes in this place; then we will take the minibus to go to the next point and one of the most spectacular, the incline walk in the rain forest towards the base of the Arenal volcano, where we will visit the lava flows from the years 1525, 1968 and 2010; also while we enjoy this beautiful ecological park we will learn about the trees and animals that inhabit this place. (About two hours up to the base of the volcano, and one hour down to the green lagoon). After the descent we will enjoy a swim in a totally clean green lagoon with volcanic formation. Once we have enjoyed this, we will have a traditional lunch. To finish we return to the bus to go to the natural river of hot springs (Rio Tabacón), where we will enjoy a majestic place, and also enjoy a mud mask from the base of the Arenal volcano. For after a great day of adventure and experience, be returning to La Fortuna around 4pm.


## 5981 — Arenal Volcano Horseback Riding

Source: https://volcanvacations.com/tour/arenal-volcano-horseback-riding/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, POSSIBLE_HORSEBACK_VARIANT_DUPLICATE, UNRELATED_COPIED_WATERFALL_ITINERARY, ONE_DOLLAR_PLACEHOLDER_PRICE, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS, UNRELATED_STOCK_GALLERY, IDENTICAL_DESCRIPTION_ON_9_PRODUCTS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Arenal Volcano Horseback Riding | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | La Fortuna / Arenal volcano / Rio Tabacón (body claims) | NEEDS_PARTNER_VERIFICATION |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 ed06d89edc97f6c8 | CONFLICTING |
| legacy_retail_price | 1.00 | LEGACY_PLACEHOLDER |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | LEGACY_PLACEHOLDER |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5330; wp-5329; wp-5321 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

First we go to the majestic La Fortuna waterfall, which is 70 meters high; where if the weather allows it, we will bathe in its crystal clear waters. We will be around one hour and thirty minutes in this place; then we will take the minibus to go to the next point and one of the most spectacular, the incline walk in the rain forest towards the base of the Arenal volcano, where we will visit the lava flows from the years 1525, 1968 and 2010; also while we enjoy this beautiful ecological park we will learn about the trees and animals that inhabit this place. (About two hours up to the base of the volcano, and one hour down to the green lagoon). After the descent we will enjoy a swim in a totally clean green lagoon with volcanic formation. Once we have enjoyed this, we will have a traditional lunch. To finish we return to the bus to go to the natural river of hot springs (Rio Tabacón), where we will enjoy a majestic place, and also enjoy a mud mask from the base of the Arenal volcano. For after a great day of adventure and experience, be returning to La Fortuna around 4pm.


## 5978 — Canyoning & Waterfall Rappelling

Source: https://volcanvacations.com/tour/canyoning-waterfall-rappelling/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, UNRELATED_COPIED_WATERFALL_ITINERARY, ONE_DOLLAR_PLACEHOLDER_PRICE, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS, UNRELATED_STOCK_GALLERY, IDENTICAL_DESCRIPTION_ON_9_PRODUCTS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Canyoning & Waterfall Rappelling | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | La Fortuna / Arenal volcano / Rio Tabacón (body claims) | NEEDS_PARTNER_VERIFICATION |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 ed06d89edc97f6c8 | CONFLICTING |
| legacy_retail_price | 1.00 | LEGACY_PLACEHOLDER |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | LEGACY_PLACEHOLDER |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5330; wp-5329; wp-5321 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

First we go to the majestic La Fortuna waterfall, which is 70 meters high; where if the weather allows it, we will bathe in its crystal clear waters. We will be around one hour and thirty minutes in this place; then we will take the minibus to go to the next point and one of the most spectacular, the incline walk in the rain forest towards the base of the Arenal volcano, where we will visit the lava flows from the years 1525, 1968 and 2010; also while we enjoy this beautiful ecological park we will learn about the trees and animals that inhabit this place. (About two hours up to the base of the volcano, and one hour down to the green lagoon). After the descent we will enjoy a swim in a totally clean green lagoon with volcanic formation. Once we have enjoyed this, we will have a traditional lunch. To finish we return to the bus to go to the natural river of hot springs (Rio Tabacón), where we will enjoy a majestic place, and also enjoy a mud mask from the base of the Arenal volcano. For after a great day of adventure and experience, be returning to La Fortuna around 4pm.


## 5975 — Jungle and Maleku’s ATV Tour

Source: https://volcanvacations.com/tour/jungle-and-malekus-atv-tour/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, UNRELATED_COPIED_WATERFALL_ITINERARY, ONE_DOLLAR_PLACEHOLDER_PRICE, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS, UNRELATED_STOCK_GALLERY, IDENTICAL_DESCRIPTION_ON_9_PRODUCTS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Jungle and Maleku’s ATV Tour | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | La Fortuna / Arenal volcano / Rio Tabacón (body claims) | NEEDS_PARTNER_VERIFICATION |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 ed06d89edc97f6c8 | CONFLICTING |
| legacy_retail_price | 1.00 | LEGACY_PLACEHOLDER |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | LEGACY_PLACEHOLDER |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5330; wp-5329; wp-5321 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

First we go to the majestic La Fortuna waterfall, which is 70 meters high; where if the weather allows it, we will bathe in its crystal clear waters. We will be around one hour and thirty minutes in this place; then we will take the minibus to go to the next point and one of the most spectacular, the incline walk in the rain forest towards the base of the Arenal volcano, where we will visit the lava flows from the years 1525, 1968 and 2010; also while we enjoy this beautiful ecological park we will learn about the trees and animals that inhabit this place. (About two hours up to the base of the volcano, and one hour down to the green lagoon). After the descent we will enjoy a swim in a totally clean green lagoon with volcanic formation. Once we have enjoyed this, we will have a traditional lunch. To finish we return to the bus to go to the natural river of hot springs (Rio Tabacón), where we will enjoy a majestic place, and also enjoy a mud mask from the base of the Arenal volcano. For after a great day of adventure and experience, be returning to La Fortuna around 4pm.


## 5972 — Arenal Volcano Hike and Hot River

Source: https://volcanvacations.com/tour/arenal-volcano-hike-and-hot-river/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, COPIED_ITINERARY_INCLUDES_WATERFALL_NOT_IN_TITLE, ONE_DOLLAR_PLACEHOLDER_PRICE, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS, UNRELATED_STOCK_GALLERY, IDENTICAL_DESCRIPTION_ON_9_PRODUCTS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Arenal Volcano Hike and Hot River | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | La Fortuna / Arenal volcano / Rio Tabacón (body claims) | NEEDS_PARTNER_VERIFICATION |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 ed06d89edc97f6c8 | CONFLICTING |
| legacy_retail_price | 1.00 | LEGACY_PLACEHOLDER |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | LEGACY_PLACEHOLDER |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5330; wp-5329; wp-5321 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

First we go to the majestic La Fortuna waterfall, which is 70 meters high; where if the weather allows it, we will bathe in its crystal clear waters. We will be around one hour and thirty minutes in this place; then we will take the minibus to go to the next point and one of the most spectacular, the incline walk in the rain forest towards the base of the Arenal volcano, where we will visit the lava flows from the years 1525, 1968 and 2010; also while we enjoy this beautiful ecological park we will learn about the trees and animals that inhabit this place. (About two hours up to the base of the volcano, and one hour down to the green lagoon). After the descent we will enjoy a swim in a totally clean green lagoon with volcanic formation. Once we have enjoyed this, we will have a traditional lunch. To finish we return to the bus to go to the natural river of hot springs (Rio Tabacón), where we will enjoy a majestic place, and also enjoy a mud mask from the base of the Arenal volcano. For after a great day of adventure and experience, be returning to La Fortuna around 4pm.


## 5969 — Arenal Hanging Bridges

Source: https://volcanvacations.com/tour/arenal-hanging-bridges/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, UNRELATED_COPIED_WATERFALL_ITINERARY, ONE_DOLLAR_PLACEHOLDER_PRICE, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS, UNRELATED_STOCK_GALLERY, IDENTICAL_DESCRIPTION_ON_9_PRODUCTS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Arenal Hanging Bridges | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | Arenal Hanging Bridges | NEEDS_PARTNER_VERIFICATION |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 ed06d89edc97f6c8 | CONFLICTING |
| legacy_retail_price | 1.00 | LEGACY_PLACEHOLDER |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | LEGACY_PLACEHOLDER |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5330; wp-5329; wp-5321 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

First we go to the majestic La Fortuna waterfall, which is 70 meters high; where if the weather allows it, we will bathe in its crystal clear waters. We will be around one hour and thirty minutes in this place; then we will take the minibus to go to the next point and one of the most spectacular, the incline walk in the rain forest towards the base of the Arenal volcano, where we will visit the lava flows from the years 1525, 1968 and 2010; also while we enjoy this beautiful ecological park we will learn about the trees and animals that inhabit this place. (About two hours up to the base of the volcano, and one hour down to the green lagoon). After the descent we will enjoy a swim in a totally clean green lagoon with volcanic formation. Once we have enjoyed this, we will have a traditional lunch. To finish we return to the bus to go to the natural river of hot springs (Rio Tabacón), where we will enjoy a majestic place, and also enjoy a mud mask from the base of the Arenal volcano. For after a great day of adventure and experience, be returning to La Fortuna around 4pm.


## 5966 — Rio Celeste Waterfall Hike and Lunch

Source: https://volcanvacations.com/tour/rio-celeste-waterfall-hike-and-lunch-2/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, RIO_CELESTE_TITLE_VS_LA_FORTUNA_ITINERARY, ONE_DOLLAR_PLACEHOLDER_PRICE, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS, UNRELATED_STOCK_GALLERY, IDENTICAL_DESCRIPTION_ON_9_PRODUCTS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | Rio Celeste Waterfall Hike and Lunch | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | Rio Celeste Waterfall Hike and Lunch | CONFLICTING |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 ed06d89edc97f6c8 | CONFLICTING |
| legacy_retail_price | 1.00 | LEGACY_PLACEHOLDER |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | LEGACY_PLACEHOLDER |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5330; wp-5329; wp-5321 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

First we go to the majestic La Fortuna waterfall, which is 70 meters high; where if the weather allows it, we will bathe in its crystal clear waters. We will be around one hour and thirty minutes in this place; then we will take the minibus to go to the next point and one of the most spectacular, the incline walk in the rain forest towards the base of the Arenal volcano, where we will visit the lava flows from the years 1525, 1968 and 2010; also while we enjoy this beautiful ecological park we will learn about the trees and animals that inhabit this place. (About two hours up to the base of the volcano, and one hour down to the green lagoon). After the descent we will enjoy a swim in a totally clean green lagoon with volcanic formation. Once we have enjoyed this, we will have a traditional lunch. To finish we return to the bus to go to the natural river of hot springs (Rio Tabacón), where we will enjoy a majestic place, and also enjoy a mud mask from the base of the Arenal volcano. For after a great day of adventure and experience, be returning to La Fortuna around 4pm.


## 5592 — White Water Rafting Class III & IV on Rio La Balsa

Source: https://volcanvacations.com/tour/white-water-rafting-class-iii-iv-on-rio-la-balsa-2/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, RIVER_CONFLICT_BALSA_TITLE_VS_SARAPIQUI_BODY, TWO_HOURS_RAFTING_VS_FIVE_HOURS_TOTAL_UNRESOLVED, RAFTING_MISTAGGED_CULTURAL, ONE_DOLLAR_PLACEHOLDER_PRICE, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS, UNRELATED_STOCK_GALLERY

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | White Water Rafting Class III & IV on Rio La Balsa | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Cultural & Thematic Tours; Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | Rio La Balsa (title); Rio Sarapiqui (description) | CONFLICTING |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 0dd40053795f7971 | CONFLICTING |
| legacy_retail_price | 1.00 | LEGACY_PLACEHOLDER |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | LEGACY_PLACEHOLDER |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | MISSING | MISSING |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5330; wp-5329; wp-5321 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

Enjoy our most challenging adventure, a white water rafting tour with rapids III & IV, this thrilling adventure of 2 hours is the best option for adrenaline junkies. Raft 9 miles (14.5 kilometers) down the Rio Sarapiqui with over 30 continues rapids, while leaving enough time to swim and snack on Costa Rican fruit.

Afterwards, your guide rewards you with water, towels and takes you to a local restaurant at La Fortuna for lunch. Rio Sarapiqui is also surrounded by lush vegetation, giving the opportunity to observe a variety of wildlife during the tour; including sloths, iguanas, tucans and monkeys.

Additional claims: adventure of 2 hours


## 5502 — La Fortuna Waterfall, Arenal Volcano, & Hot River

Source: https://volcanvacations.com/tour/white-water-rafting-class-iii-iv-on-rio-la-balsa/

**Flags:** LATIN_TEMPLATE_EXCERPT, MISSING_OPERATOR_NET_COST_CANCELLATION, LEGACY_PRICE_NOT_CURRENT, CONTACT_EMAIL_TYPO, URL_SLUG_RAFTING_BUT_CONTENT_WATERFALL_COMBO, FIVE_HOURS_VS_08_20_TO_16_00, UNVERIFIED_GEOLOGY_AND_SWIMMING_CLAIMS, ONE_DOLLAR_PLACEHOLDER_PRICE, REPEATED_5_HOURS_13_PLUS_08_20, REPEATED_BOAT_GUIDE_INCLUSIONS, UNRELATED_STOCK_GALLERY, IDENTICAL_DESCRIPTION_ON_9_PRODUCTS

| Field | Extracted source value | Status |
| --- | --- | --- |
| tour_name | La Fortuna Waterfall, Arenal Volcano, & Hot River | VERIFIED_FROM_LEGACY |
| category | MISSING | MISSING |
| activities | Wild & Adventure Tours | NEEDS_PARTNER_VERIFICATION |
| location | La Fortuna / Arenal volcano / Rio Tabacón (body claims) | NEEDS_PARTNER_VERIFICATION |
| short_description | Donec id elit non mi porta gravida at eget metus. Nulla vitae elit libero, a pharetra augue. Etiam porta sem malesuada magna mollis euismod. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. | LEGACY_PLACEHOLDER |
| full_description | Full source text preserved below and in JSON; SHA-256 ed06d89edc97f6c8 | NEEDS_PARTNER_VERIFICATION |
| legacy_retail_price | 1.00 | LEGACY_PLACEHOLDER |
| legacy_currency | $ (ISO currency not stated) | NEEDS_PARTNER_VERIFICATION |
| current_verified_retail_price | MISSING | MISSING |
| supplier_cost | MISSING | MISSING |
| vv_gross_margin | MISSING | MISSING |
| duration | 5 Hours | CONFLICTING |
| departure_times | 08:20 | LEGACY_PLACEHOLDER |
| minimum_age | 13+ | LEGACY_PLACEHOLDER |
| maximum_group_size | MISSING | MISSING |
| difficulty | incline walk in the rain forest | NEEDS_PARTNER_VERIFICATION |
| supplier_operator | MISSING | MISSING |
| whats_included | Transportation From Most Hotels; Bilingual Boat Guides; Fruit & Snacks; Lunch & Towels; Bottled Water | NEEDS_PARTNER_VERIFICATION |
| what_to_bring | MISSING | MISSING |
| pickup_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| transportation_information | Transportation From Most Hotels | NEEDS_PARTNER_VERIFICATION |
| cancellation_information | MISSING | MISSING |
| images | wp-5330; wp-5329; wp-5321 | VERIFIED_FROM_LEGACY |
| gallery_images | https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_764972821.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_759608542.jpg; https://volcanvacations.com/wp-content/uploads/2019/04/shutterstock_720444505.jpg | VERIFIED_FROM_LEGACY |
| videos | MISSING | MISSING |
| additional_notes | Departure Time 08:20; 5 Hours; Min Age : 13+ | VERIFIED_FROM_LEGACY |

**Full recovered description (unapproved source copy):**

First we go to the majestic La Fortuna waterfall, which is 70 meters high; where if the weather allows it, we will bathe in its crystal clear waters. We will be around one hour and thirty minutes in this place; then we will take the minibus to go to the next point and one of the most spectacular, the incline walk in the rain forest towards the base of the Arenal volcano, where we will visit the lava flows from the years 1525, 1968 and 2010; also while we enjoy this beautiful ecological park we will learn about the trees and animals that inhabit this place. (About two hours up to the base of the volcano, and one hour down to the green lagoon). After the descent we will enjoy a swim in a totally clean green lagoon with volcanic formation. Once we have enjoyed this, we will have a traditional lunch. To finish we return to the bus to go to the natural river of hot springs (Rio Tabacón), where we will enjoy a majestic place, and also enjoy a mud mask from the base of the Arenal volcano. For after a great day of adventure and experience, be returning to La Fortuna around 4pm.

Additional claims: returning to La Fortuna around 4pm

