# Legacy copy and contact audit

Source material only. **Approved new homepage copy was not changed.** `VERIFIED_FROM_LEGACY` means observed, not current-confirmed. Full reusable/reviewable source blocks are in [legacy-copy-audit.json](legacy-copy-audit.json).

## Editorial findings

| Source/content | Classification | Treatment |
| --- | --- | --- |
| `/about/`: La Fortuna base, local expertise, nature/adventure range | REWRITE | Useful positioning; remove generic superlatives, confirm actual team/service scope. |
| `/about/`: transportation and hotel-booking assistance | REWRITE | Business-service claims only; no hotel, transport operator, schedule, or rates are established. Do not invent bookable hotel products. |
| `/01-homepage/`: Costa Rica beaches/rainforests/cities introduction | REWRITE | Useful destination-storytelling seed; confirm itinerary coverage. |
| Home transportation “over two decades” paragraph | DUPLICATE | Same block appears in `/homepage-2/` beside Swiss/Alps copy. Do not treat tenure/expertise claims as verified. Home Learn More resolves back to homepage. |
| Current `/contact/` email | REUSE | Use only user-confirmed info@volcanvacations.com. |
| Contact phone, Liverpool address, contact variants | LOW_VALUE | Theme placeholder details; quarantine and ask partner for correct phone/address. |
| `/homepage/`: 700+ destinations, 40% summer discount, testimonials | OUTDATED / LOW_VALUE | Unsupported promotional/template claims, no current validity. No testimonial authenticity assumed. |
| `/homepage-2/`, `/01-hiking-home/`: Alps/Swiss travel | LOW_VALUE | Unrelated destination template; exclude. |
| About-us variants: architect/designer teams, awards, Latin copy | LOW_VALUE | Not evidence of VV personnel, history, services or credentials. |
| Catalog layout variants | DUPLICATE | Same 13 products, not additional inventory. |
| `/destinations/`, `/products/` | LOW_VALUE | Empty shells; no populated destination terms or additional products. |
| `/01-test-shuttle/` | LOW_VALUE | Empty To/From/date search prototype, not another transport offer. |
| Footer SSL/payment claim and dated/theme support promises | REWRITE | Future wording must reflect the actual production payment/support configuration. |

## Every observed email/contact defect

| Observed address/link | Pages | Classification | Migration action |
| --- | --- | --- | --- |
| EMPTY_MAILTO | 1 | EMPTY_OR_PLACEHOLDER_LINK | DO_NOT_IMPORT |
| # | 4 | EMPTY_OR_PLACEHOLDER_LINK | DO_NOT_IMPORT |
| Contact@goodlayers.com | 1 | THEME_VENDOR_ADDRESS_NOT_VV | DO_NOT_IMPORT |
| Help@goodlayers.com | 35 | THEME_VENDOR_ADDRESS_NOT_VV | DO_NOT_IMPORT |
| contact@infinitewptheme.com | 1 | THEME_VENDOR_ADDRESS_NOT_VV | DO_NOT_IMPORT |
| info@volcanvacations.com | 255 | CANONICAL_USER_CONFIRMED | USE_AS_PRIMARY_PUBLIC_CONTACT |
| info@volcanvactions.com | 13 | MISSPELLED_VV_ADDRESS | DO_NOT_IMPORT |

The exact affected URL list for every address is in [legacy-contact-audit.json](legacy-contact-audit.json). `mailto:#` appears on contact variants, including the otherwise correctly spelled primary address; empty mailto is also recorded. The canonical email spelling must not be changed to a payments alias. The payments alias spelling is MISSING; ask only when implementing payment communications.

## Useful recovered source blocks

### about-1 — REWRITE

Source: https://volcanvacations.com/about/

Welcome to Volcan Vacations, your premier tour company nestled in the heart of La Fortuna, Costa Rica. At Volcan Vacations, we specialize in providing unforgettable adventures and experiences that showcase the natural beauty and cultural richness of this stunning region. With our passionate team of local experts, we aim to curate immersive and authentic tours that leave a lasting impression on every traveler.

Useful local/company/service positioning; verify business claims and edit before use.

### about-2 — REWRITE

Source: https://volcanvacations.com/about/

La Fortuna, with its breathtaking landscapes, lush rainforests, and majestic volcanoes, serves as our playground for exploration. From thrilling hikes to serene hot springs, we offer a diverse range of tours tailored to suit every adventurer’s taste and preference. Whether you’re seeking adrenaline-pumping adventures, wildlife encounters, or simply a relaxing escape into nature, Volcan Vacations has something for everyone.

Useful local/company/service positioning; verify business claims and edit before use.

### about-3 — REWRITE

Source: https://volcanvacations.com/about/

In addition to our exceptional tours, Volcan Vacations offers hassle-free transportation and hotel booking assistance. Whether you’re arriving from the airport or need accommodation, our reliable services ensure a smooth journey and a comfortable stay. With our local expertise, we’ll find the perfect lodging to complement your adventure, allowing you to focus on making unforgettable memories in Costa Rica’s tropical paradise.

Useful local/company/service positioning; verify business claims and edit before use.

### 01-homepage-2 — REWRITE

Source: https://volcanvacations.com/01-homepage/

Discover the heart of Costa Rica with us—a travel hub where adventure intertwines with tranquility. Immerse yourself in the enchanting beauty and diverse landscapes of this top destination through our expertly crafted itineraries, exploring pristine beaches, lush rain forests, and vibrant cities.

Source material only; duplicated/template claims are not approved business facts.

### -1 — DUPLICATE

Source: https://volcanvacations.com/

It’s our passion and our expertise, and has been for over two decades. We know the trails and the towns inside and out. We know the hoteliers and their rooms, and restauranteurs and their menus. We don’t guide on any route we haven’t done many times before. Our expertise gives you a richer, more enjoyable experience, and we will makes better use of your time.

Source material only; duplicated/template claims are not approved business facts.

### homepage-2-1 — DUPLICATE

Source: https://volcanvacations.com/homepage-2/

It’s our passion and our expertise, and has been for over two decades. We know the trails and the towns inside and out. We know the hoteliers and their rooms, and restauranteurs and their menus. We don’t guide on any route we haven’t done many times before. Our expertise gives you a richer, more enjoyable experience, and we will makes better use of your time. We provide a thorough and complete orientation, so you are fully prepared to make the most of your Swiss vacation or Alps hiking adventure. Your expert trip leader is with you for the entire trip.

Source material only; duplicated/template claims are not approved business facts.

### homepage-2-2 — LOW_VALUE

Source: https://volcanvacations.com/homepage-2/

The Alps are the highest and most extensive mountain range system that lies entirely in Europe, separating Southern from Central and Western Europe and stretching approximately 1,200 kilometres across eight Alpine countries: France, Switzerland, Italy, Monaco, Liechtenstein, Austria, Germany, and Slovenia. To make the most of your vacation experience, you’ll want to plan your itinerary and activities to take advantage of the best weather and optimal conditions. Remember, the Alps is located at a latitude between 46° and 47° north.

Source material only; duplicated/template claims are not approved business facts.

### contact-5 — LOW_VALUE

Source: https://volcanvacations.com/contact/

4 apt. Flawing Street. The Grand Avenue. Liverpool, UK 33342

Source material only; duplicated/template claims are not approved business facts.

### canonical-contact — REUSE

Source: https://volcanvacations.com/contact/

info@volcanvacations.com


### unverified-promotions — OUTDATED

Source: https://volcanvacations.com/homepage/

Enjoy Summer Deals / Up to 40% Discount!

Undated template promotion has no current validity evidence; do not migrate as an offer.

