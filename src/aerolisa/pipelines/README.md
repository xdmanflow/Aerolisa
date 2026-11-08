# Pipelines

> All ingestion and dataset transforms, declared with the Foundry-style `@transform` API: raw files and API responses in, bronze → silver → gold → object tables out, with quality checks on every run.

**Milestones:** M1 (C-MAPSS, pandas) · M2 (PySpark, reference data, quality) · M5 (OpenSky) · M8 (Eurocontrol, Airbus O&D)
**May import:** `aerolisa.core`
**Learn:** Renaissance 01, 02, 04, 05

## Planned layout

```text
pipelines/
├── sources/          # one module per source: download / read raw, write bronze
│   ├── cmapss.py
│   ├── ourairports.py
│   ├── opensky.py
│   ├── eurocontrol.py
│   └── airbus_od.py
├── silver/           # cleaning transforms, one file per dataset family
├── gold/             # features, model inputs/outputs, aggregates
├── objects/          # ontology object tables from gold
└── quality.py        # checks + report writer
```

## Datasets

`pipelines` owns ingestion, cleaning and object tables. Domain modules own the gold datasets they compute, using the same `@transform` API.

| Dataset | Layer | From | Owner | Milestone |
|---|---|---|---|---|
| `bronze/cmapss_raw` | bronze | NASA text files | pipelines | M1 |
| `silver/cmapss_cycles` | silver | `bronze/cmapss_raw` | pipelines | M1 |
| `gold/engine_cycle_features` | gold | `silver/cmapss_cycles` | engine_health | M1 → M6 |
| `gold/engine_health_snapshot` | gold | features + registered model | engine_health | M1 → M6 |
| `silver/airports` | silver | OurAirports | pipelines | M2 |
| `silver/aircraft_registry` | silver | OpenSky aircraft database | pipelines | M2 |
| `bronze/opensky_flights` | bronze | OpenSky REST API | pipelines | M5 |
| `silver/flights` | silver | `bronze/opensky_flights`, `silver/airports` | pipelines | M5 |
| `gold/aircraft_utilization_daily` | gold | `silver/flights` | fleet | M5 |
| `gold/engine_assignment` | gold | registry + C-MAPSS units | fleet | M5 |
| `gold/inspection_recommendation` | gold | snapshots + utilization | planner | M7 |
| `silver/delays` | silver | Eurocontrol | pipelines | M8 |
| `silver/deliveries` | silver | Airbus O&D | pipelines | M8 |
| `gold/analytics_*` | gold | delays, deliveries | analytics | M8 |
| `objects/*` | objects | gold datasets | pipelines | M3 → |

## Steps
1. [ ] C-MAPSS source + silver + gold transforms in pandas, tested on `sample_data/` (M1 steps 1–3)
2. [ ] Port to PySpark with a local SparkSession fixture (M2 step 3)
3. [ ] OurAirports and aircraft registry (M2 step 4)
4. [ ] `quality.py`: checks per dataset declared next to the transform; `fail` / `warn`; markdown report in `reports/quality/<run_id>.md` (M2 step 6)
5. [ ] OpenSky source: OAuth2 client credentials, time-window limits, retries, credit budget, cache by day (M5 step 2)
6. [ ] Flights silver + utilization gold + engine assignment (M5 steps 3–5)
7. [ ] Eurocontrol and Airbus O&D sources (M8 steps 1–2)

## Rules
- Raw is kept exactly as received in bronze, plus `source_file` / `ingested_at`.
- Transforms are pure: no network or file I/O inside the decorated function.
- Every dataset has a primary key and at least one quality check.

## Done when
- [ ] `aerolisa build --all` runs unattended from raw files
- [ ] Quality report produced on every run, failures stop the build
- [ ] Explainable in 5 minutes with the lineage graph
