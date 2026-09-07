# Supplier/operator audit

**No contracting operator is established for any of the 13 legacy products.** All supplier costs are MISSING. Existing PostgreSQL suppliers are development/demo records and must not be reused as real supplier identities.

| Explicitly named lead | Type | Associated product | Public contact | Source | Status / proposed treatment |
| --- | --- | --- | --- | --- | --- |
| Arenal Oasis | Venue or brand lead; contracting supplier role unconfirmed | 5990 — Frog Watching Night Walk | MISSING | [Legacy frog tour](https://volcanvacations.com/tour/frog-watching-night-walk/) says “Arenal Oasis after dark” | NEEDS_PARTNER_VERIFICATION; ask whether venue and operator are the same entity; no Supplier insert proposed |

The remaining records have no named operator lead that can be assigned confidently. The full per-product unknown list and source URLs are in [legacy-supplier-audit.json](legacy-supplier-audit.json).

Do not turn these into suppliers by inference:

- La Fortuna, Arenal, Caño Negro, Río Balsa, Río Sarapiquí, Río Tabacón, Río Celeste and the airport are places or route names.
- “Bilingual Boat Guides” and “Professional bilingual guide” are generic inclusion text.
- Maleku in the ATV title is not a contracting company identity.
- GoodLayers/theme contacts, photo filenames, stock marks and imagery are not supplier evidence.
- `info@volcanvacations.com` is VV's canonical public contact, not automatically the operator's email for every tour.

Ask the partner for each actual operator's name, type, associated tour IDs, net rate/currency/effective date and available business contact/reference sheet. Reuse one confirmed supplier across its actual associated tours. Supplier contacts can remain explicitly missing if unavailable; required operator relationships and net rates must be resolved before real product import. Do not create a fake Unknown supplier or zero net costs to satisfy database constraints.
