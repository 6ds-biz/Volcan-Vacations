# Proposed legacy URL preservation

**No redirects were implemented.** Full URL-level map: [legacy-url-redirect-map.json](legacy-url-redirect-map.json). Every one of the 262 discovered public content URLs is classified. No analytics/backlink evidence was supplied, so SEO value is potential, not measured.

Current new routes include `/`, `/tours`, `/about`, `/contact`, `/plan-your-trip`, `/request`, and token-based `/pay`. **`/tours/{slug}` and `/transportation/{slug}` do not exist yet.** Product redirects are blocked until real destination pages are built and return 200; never redirect to a missing route or a private payment token.

| Old URL | Proposed destination | Gate |
| --- | --- | --- |
| https://volcanvacations.com/ | / | KEEP_PATH_OR_NORMALIZE_TRAILING_SLASH |
| https://volcanvacations.com/about/ | /about | KEEP_PATH_OR_NORMALIZE_TRAILING_SLASH |
| https://volcanvacations.com/contact/ | /contact | KEEP_PATH_OR_NORMALIZE_TRAILING_SLASH |
| https://volcanvacations.com/tour/ | /tours | PROPOSE_301 |
| https://volcanvacations.com/tour/arenal-hanging-bridges/ | /tours/arenal-hanging-bridges | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/arenal-volcano-hike-and-hot-river/ | /tours/arenal-volcano-hike-hot-river | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/arenal-volcano-horseback-riding-hot-river/ | /tours/arenal-horseback-hot-river | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/arenal-volcano-horseback-riding/ | /tours/arenal-volcano-horseback-riding | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/cano-negro-wildlife-refuge/ | /tours/cano-negro-wildlife-refuge | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/canyoning-waterfall-rappelling/ | /tours/canyoning-waterfall-rappelling | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/frog-watching-night-walk/ | /tours/frog-watching-night-walk | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/jungle-and-malekus-atv-tour/ | /tours/jungle-maleku-atv | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/rio-celeste-waterfall-hike-and-lunch-2/ | /tours/rio-celeste-waterfall-hike-lunch | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/shuttle-sjo-juan-santamaria-international-airport-to-la-fortuna-arenal-volcano/ | /transportation/sjo-la-fortuna | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/sloth-watching-walk/ | /tours/sloth-watching-walk | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/white-water-rafting-class-iii-iv-on-rio-la-balsa-2/ | /tours/whitewater-rafting-confirm-river | PROPOSE_301_AFTER_DESTINATION_EXISTS |
| https://volcanvacations.com/tour/white-water-rafting-class-iii-iv-on-rio-la-balsa/ | /tours/la-fortuna-waterfall-arenal-hot-river | PROPOSE_301_AFTER_DESTINATION_EXISTS |

The unsuffixed rafting slug currently displays the **La Fortuna waterfall/volcano/hot-river combination**. The `-2` rafting slug displays rafting. Preserve that observed distinction; do not map both to rafting. The rafting destination slug stays provisional until Balsa versus Sarapiquí is resolved.

Catalog layout/taxonomy clones may consolidate to `/tours` only after checking their content, backlinks and query intent. Empty destinations, theme portfolios, widgets, login/payment demos and broken vendor paths are retirement candidates, not automatic homepage redirects. Confirm legitimate old customer/payment URLs separately before returning 404/410.

Before cutover: export Search Console/analytics/backlinks; choose canonical slugs; preserve useful media URLs or provide asset redirects; test old→new URLs for one-hop redirects, no loops, equivalent content, query handling, HTTPS, canonicals and sitemap membership. Keep a reversible map and monitor 404s after launch.

