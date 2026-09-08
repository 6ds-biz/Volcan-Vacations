# RideCR route inventory

Retrieved from [RideCR’s official shared-shuttle page](https://ridecr.com/shuttle/) on **2026-09-07**. Publisher effective dates were not supplied. These are published reference departures, not supplier-confirmed seat availability. RideCR’s page states daily routes. Repeated desktop/mobile timetable blocks were deduplicated. Times such as “15:30 p.m.” were normalized to 24-hour `15:30`.

The bounded reviewed catalog has **9 nodes, 24 directed canonical routes, 24 RideCR services and 29 RideCR departure definitions**. No theoretical pairs or reverse schedules were generated. The six Interbus overlaps add six services and six schedule references.

| Origin | Destination | RideCR departures (Costa Rica) | Review |
| --- | --- | --- | --- |
| La Fortuna | La Pavona | 05:30 | Routine source freshness |
| La Fortuna | Sarapiquí | 05:30 | Source question |
| La Fortuna | Guápiles | 05:30 | Interbus recurrence unknown |
| La Fortuna | SJO Airport | 07:45, 15:30 | Source question |
| La Fortuna | LIR Airport | 07:45 | Source question |
| La Fortuna | Monteverde | 07:45, 15:30 | Source question; Interbus recurrence unknown |
| La Fortuna | Tamarindo | 07:45 | Interbus recurrence unknown |
| SJO Airport | La Fortuna | 07:00, 13:30 | Source question |
| SJO Airport | Manuel Antonio | 07:00 | Source question |
| SJO Airport | Monteverde | 13:30 | Source question |
| Monteverde | LIR Airport | 07:45 | Source question |
| Monteverde | SJO Airport | 07:45 | Source question |
| Monteverde | La Fortuna | 07:45 | Source question |
| LIR Airport | SJO Airport | 07:15, 16:15 | Source question |
| LIR Airport | Manuel Antonio | 07:15 | Source question |
| LIR Airport | La Fortuna | 16:15 | Source question |
| Manuel Antonio | SJO Airport | 07:30, 15:00 | Source question |
| Manuel Antonio | La Fortuna | 15:00 | Interbus recurrence unknown |
| Manuel Antonio | Monteverde | 15:00 | Interbus recurrence unknown |
| Guápiles | La Fortuna | 07:00 | Interbus recurrence unknown |
| Guápiles | Sarapiquí | 07:00 | Source question |
| La Pavona | La Fortuna | 07:00 | Routine source freshness |
| La Pavona | Sarapiquí | 07:00 | Source question |
| La Pavona | Guápiles | 07:00 | Routine source freshness |

**21 routes need review:** 16 have canonical source questions and six have unknown Interbus recurrence (one route belongs to both sets).

## Interpretation and gaps

- Airport nodes retain the explicitly named airport component of combined “San José / SJO Airport” and “Guanacaste / Liberia Airport” labels. City-wide and province-wide routes were **not** separately inferred. Routes involving those labels retain a review note requiring confirmation of exact airport/zone pickup and applicability.
- RideCR’s broad Sarapiquí label is not automatically equated to Interbus’s Puerto Viejo de Sarapiquí. Sarapiquí, Guápiles and La Pavona remain unmapped to the current Destination tree; no approximate geography was invented.
- La Fortuna/Monteverde appears in the shuttle timetable. [RideCR’s lake-crossing page](https://ridecr.com/lake-crossing/) establishes a separate service concept but does not supply a machine-readable timetable or establish which shuttle departures use it. No additional lake-crossing services/schedules were inferred.
- Nosara, Papagayo, Puerto Viejo and hotel-specific nodes were not added because this RideCR shuttle timetable does not publish those route pairs. They remain possible later reviewed expansions.
- No reliable VV negotiated vendor rates were available in these public sources. **All 30 imported vendor services require vendor-rate entry.** No retail prices were harvested or recast as costs.
- Interbus operating weekdays and effective dates remain unknown from its route table. Its six references are visible to Operations but excluded from date-specific search until recurrence is entered. RideCR effective dates are unspecified; search treats the published daily timetable as an open-ended reference and always requires confirmation.

## Geography mappings

| Node | Existing destination slug |
| --- | --- |
| La Fortuna | arenal-la-fortuna |
| La Pavona | Unmapped — review |
| Sarapiquí | Unmapped — review |
| Guápiles | Unmapped — review |
| SJO Airport | sjo-airport |
| LIR Airport | lir-airport |
| Monteverde | monteverde |
| Tamarindo | tamarindo |
| Manuel Antonio | manuel-antonio-central-pacific |

## Controlled import

The reviewable source is `services/api/app/data/transportation-2026-09-07.json`. The command is never invoked at startup or by a migration.

```bash
# Inspect prospective inserts; transaction is rolled back.
docker compose exec api python -m app.import_transportation
# Apply the reviewed catalog explicitly.
docker compose exec api python -m app.import_transportation --apply
```

Import matches nodes by stable slug/name, routes by ordered endpoints, and supplier services by vendor/route/type. RideCR/Ride CR and Interbus identities are reused where names match; ambiguous vendor/node identities stop the transaction. New suppliers use the existing capability architecture and unreviewed commercial status. Existing supplier fields, commercial agreements and edited schedules are retained. Stable import keys prevent schedule recreation after manual edits; no date-specific rows are generated. A new catalog revision requires human review and explicit schedule amendments rather than overwriting imported/manual values.
