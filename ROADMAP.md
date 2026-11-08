# Roadmap

Twelve milestones, in order. No dates: each milestone has a size (in Sunday build sessions), numbered steps, and a "done when" line.

**Rules**
- **Always demoable.** After M1, `main` always has a working live demo. A milestone that would break it lands on a branch.
- **Cut scope, not the milestone.** When behind, ship the "done when" line and move the rest to the 🚀 list at the bottom of the milestone.
- **First version without AI.** AI reviews my code; it doesn't write the first version.
- **Every milestone ends with the showcase checklist** (bottom of this file).
- The Renaissance module that teaches each milestone is named next to it.

---

## M0 · Clean slate
**Size:** ½ session · **Learn:** Renaissance 00

1. [ ] Push this restructured repository; check CI is green.
2. [ ] `make install`, `pre-commit install`, `make test` pass locally.
3. [ ] Repository description, topics (`aviation`, `predictive-maintenance`, `palantir-foundry`, `data-engineering`, `ontology`, `pyspark`), pinned on my profile.
4. [ ] Accounts ready: OpenSky API client (`credentials.json`, git-ignored), Palantir Developer Tier.
5. [ ] Download NASA C-MAPSS manually into `data/raw/cmapss/` (git-ignored); note the file checksums in `docs/data-sources.md`.
6. [ ] Create GitHub milestones M1–M11 and one issue per step of M1.

**Done when:** CI green, data downloaded, M1 issues exist.

---

## M1 · MVP: engine health slice → `v0.1.0`
**Size:** 3 sessions · **Learn:** Renaissance 01 (+ my SAA work on C-MAPSS)

The thinnest end-to-end version: one dataset, one model, one live app. This is the version that goes on my CV first.

1. [ ] **Ingest:** `pipelines` reads raw FD001 text files and writes `bronze/cmapss_raw` (Parquet, columns as strings or raw types, plus `source_file`, `ingested_at`).
2. [ ] **Clean:** `silver/cmapss_cycles`: named columns (unit, cycle, 3 settings, 21 sensors), types, constant sensors dropped, train/test flag.
3. [ ] **Label:** `gold/engine_cycle_features`: RUL label (clipped at a documented value), rolling means for the kept sensors.
4. [ ] **Model:** baseline (constant mean RUL) + one better model, reusing the approach of my Turbofan-RUL research (cite it; don't paste the notebook). Unit-grouped validation. RMSE + NASA score.
5. [ ] **Predict:** `gold/engine_health_snapshot`: one row per test engine (engine id, last cycle, predicted RUL, model version).
6. [ ] **App:** Streamlit `app/Home.py`: engines sorted by predicted RUL; `app/pages/Engine.py`: one engine's sensor trends and prediction.
7. [ ] **Tests:** each transform tested on `sample_data/` (a truncated slice of a few units).
8. [ ] **Deploy:** Streamlit Community Cloud (or Hugging Face Spaces) running on sample/precomputed data.
9. [ ] **README:** GIF, live link, results table (baseline vs model), limitations in 3 bullets. Tag `v0.1.0`.

**Done when:** a stranger opens the link and understands what Aerolisa does in 30 seconds.

🚀 Later: FD002–FD004 (that's M6).

---

## M2 · Data platform → `v0.2.0`
**Size:** 4 sessions · **Learn:** Renaissance 02, 03, 04, 05

Make the pipelines look and behave like Foundry's, so they port 1:1 into Code Repositories in M4.

1. [ ] **Transform API** in `core/transforms.py`: `@transform(output=Output("..."), **inputs=Input("..."))` registers a function that takes and returns DataFrames (see `core/README.md`). Tests.
2. [ ] **Dataset catalog** in `core/catalog.py` (+ `catalog.yaml`): every dataset with layer, owner, schema, description, primary key.
3. [ ] **Port the C-MAPSS transforms to PySpark** (Renaissance 04). Keep pandas versions only if they're useful for tests.
4. [ ] **Reference data:** OurAirports → `silver/airports`; OpenSky aircraft database → `silver/aircraft_registry` (filter to A320 family and A350 typecodes).
5. [ ] **Build runner:** `aerolisa build <dataset>` resolves upstream inputs by topological sort and runs only what's needed; `--all`; run ID and timing in logs.
6. [ ] **Quality checks** in `pipelines/quality.py` (Renaissance 05): schema, primary key uniqueness, nulls, ranges, cycle continuity; `fail` vs `warn`; a markdown report per run in `reports/quality/`.
7. [ ] **Lineage:** `aerolisa lineage` writes a Mermaid graph of the catalog to `docs/lineage.md`.
8. [ ] **Serving:** DuckDB file over the gold layer; first 10 documented queries in `sql/` (Renaissance 02).
9. [ ] **Data health page** in the app: last run, checks passed/failed.
10. [ ] Update README architecture; tag `v0.2.0`.

**Done when:** `aerolisa build --all` rebuilds everything from raw files with quality reports, on a clean clone.

🚀 Later: incremental builds (only new files), partitioned outputs.

---

## M3 · Ontology → `v0.3.0`
**Size:** 2 sessions · **Learn:** Renaissance 03, 07

1. [ ] Finalize the design in [docs/ontology.md](docs/ontology.md): object types, primary keys, properties, links, action types.
2. [ ] Write the definitions in `ontology/ontology.yaml` (object types, link types, action types with parameters and rules).
3. [ ] `core/ontology.py`: Pydantic models for each object type; loader that validates `ontology.yaml`.
4. [ ] Object tables materialized from gold datasets by transforms (`objects/engine`, `objects/aircraft`, …).
5. [ ] **Integrity tests:** every link resolves; primary keys unique; required properties present.
6. [ ] **Actions & writeback:** `core/actions.py` applies an action type (e.g. `ScheduleInspection`) after validating parameters and submission criteria; appends to `writeback/work_orders` with who / when / why; never mutates source data.
7. [ ] Generate `docs/ontology-reference.md` from the YAML.
8. [ ] App: an "object view" for Engine that shows its links (aircraft, snapshots, work orders). Tag `v0.3.0`.

**Done when:** every app page reads objects (not raw tables), and one action writes back with an audit trail.

---

## M4 · Foundry edition → `v0.4.0`
**Size:** 4 sessions · **Learn:** Renaissance 06, 07

The same flow on Palantir Foundry (Developer Tier). Public data only. Everything documented in [foundry/](foundry/README.md).

1. [ ] Project and folder structure in Foundry mirroring `bronze / silver / gold / objects`.
2. [ ] Upload raw C-MAPSS files as a dataset (Data Connection upload).
3. [ ] **Pipeline Builder:** cleaning pipeline to `silver/cmapss_cycles` (names, types, RUL label).
4. [ ] **Code Repository:** port the M2 PySpark transforms (`transforms.api`), same dataset names.
5. [ ] Unit tests and **data expectations** (primary key, non-null, ranges) in the repository.
6. [ ] Branch → pull request → merge → build. Write in `foundry/README.md` how the local `@transform` compares with Foundry's.
7. [ ] **Schedule** the pipeline; break an input on purpose; find the cause in **Data Lineage**; confirm the **health check** fires. Screenshots.
8. [ ] **Ontology:** object types Engine, EngineHealthSnapshot, Aircraft (static sample), links between them.
9. [ ] **Workshop app** "Inspection queue": engine table sorted by risk, engine detail with sensor chart.
10. [ ] **Action type** `ScheduleInspection` with writeback; **TypeScript Function** computing the risk score shown in the app.
11. [ ] **Contour** analysis (lifetime by fault mode) and **Quiver** analysis (sensor trends, healthy vs degrading engine).
12. [ ] Screenshots + a 2-minute screen recording; `foundry/README.md` complete. Tag `v0.4.0`.
13. [ ] *(done at M10)* **AIP Logic** function "explain this engine's risk" grounded on the snapshot properties.

**Done when:** I can open Foundry in an interview and walk raw file → pipeline → ontology → Workshop → action in 5 minutes.

---

## M5 · Fleet from real flights → `v0.5.0`
**Size:** 3 sessions · **Learn:** Renaissance 04, 05, 08

1. [ ] Pick one operator's A320-family airframes from `silver/aircraft_registry` (a manageable number); document the choice.
2. [ ] `pipelines/sources/opensky.py`: OAuth2 client-credentials auth, flights-by-aircraft requests within the endpoint's time-window limit, retry with backoff, **daily credit budget** respected, raw JSON → `bronze/opensky_flights`.
3. [ ] `silver/flights`: deduplicated, airports joined, durations computed; quality checks (impossible durations, missing airports).
4. [ ] `fleet`: cycles and flight hours per airframe per day; utilization statistics with confidence intervals (Renaissance 08).
5. [ ] **Engine assignment** (simulated, labelled everywhere): two C-MAPSS engines per airframe, each with a starting cycle; `engine age = start cycle + real cycles flown since assignment`.
6. [ ] Snapshot logic: engine health is computed at each engine's current simulated cycle.
7. [ ] Scheduled refresh (local cron or GitHub Actions schedule) that only fetches new days.
8. [ ] App: Aircraft page (flights, utilization, its two engines). Tag `v0.5.0`.

**Done when:** an aircraft that flies more makes its engines age faster in the app, from real data.

🚀 Later: ADS-B state-vector segmentation with gaps-and-islands for airframes without flight records.

---

## M6 · Engine health v2 → `v0.6.0`
**Size:** 4 sessions · **Learn:** Renaissance 08, 09, 10

1. [ ] FD001–FD004 with **operating-condition normalization**.
2. [ ] Leak-free validation: GroupKFold by unit, last-cycle evaluation on test units.
3. [ ] Model comparison table: baseline, linear, random forest, LightGBM/XGBoost, 1D-CNN or LSTM (PyTorch); RMSE, MAE, NASA score; in `reports/evaluation.md`.
4. [ ] **Intervals:** quantile models → `rul_p10`, `rul_p50`, `rul_p90`; coverage measured.
5. [ ] **Anomaly score** per cycle (Isolation Forest or health-indicator deviation).
6. [ ] **Alert model** "fails within N cycles" with a threshold chosen from a cost table (missed failure vs early removal).
7. [ ] **Explanations:** SHAP top drivers stored on each `EngineHealthSnapshot`.
8. [ ] **Reliability view:** Kaplan–Meier and Weibull fit on engine lifetimes; β interpreted.
9. [ ] **MLflow:** every run tracked; best model registered and loaded by the pipeline.
10. [ ] [docs/model-card.md](docs/model-card.md) filled. Tag `v0.6.0`.

**Done when:** every snapshot carries an interval, an anomaly score and its top drivers, from a registered model.

---

## M7 · Planner & operational app → `v0.7.0`
**Size:** 3 sessions · **Learn:** Renaissance 10, 12

1. [ ] **Risk model** in `planner`: from P10/P50/P90, estimate P(RUL < cycles until next planned check); convert cycles to **days** with the airframe's real cycles per day; add the anomaly signal; document the formula.
2. [ ] **Ranking + explanation:** each engine gets a rank and a plain-English reason ("high utilization: 7.1 cycles/day; P10 RUL 18 cycles; sensor drift on T50").
3. [ ] **What-if:** "if we delay this inspection by N days, how does the risk change?"
4. [ ] `objects/inspection_recommendation` refreshed on every build.
5. [ ] **FastAPI** (`api`): `GET` objects (aircraft, engines, snapshots, flights), `GET /planner/ranking`, `POST /actions/{action_type}`; tests; OpenAPI docs.
6. [ ] **App pages** (Workshop-like): Fleet overview, Aircraft, Engine, Inspection queue with action buttons, Data health.
7. [ ] Action flow end to end: schedule inspection in the app → writeback → the queue updates. Tag `v0.7.0`.

**Done when:** a planner can go from the queue to a scheduled inspection in three clicks, and see why.

---

## M8 · Analytics pack → `v0.8.0`
**Size:** 2 sessions · **Learn:** Renaissance 02, 11

The data-analyst proof: a business question, SQL, KPIs, a dashboard, a memo.

1. [ ] Ingest Eurocontrol performance data (e.g. airport arrival delays by cause) → `silver/delays`.
2. [ ] Ingest Airbus monthly orders & deliveries → `silver/deliveries`.
3. [ ] KPI dictionary in `analytics/README.md` (definition, formula, grain, caveats).
4. [ ] 10 documented SQL analyses in `sql/` (window functions, YoY, rankings, cause mix).
5. [ ] Dashboard: Streamlit "Analytics" page **and/or** a Power BI report (screenshots in `reports/analytics/`).
6. [ ] 1-page insight memo in `reports/analytics/memo.md`: answer first, 3 findings, 1 recommendation, limits.
7. [ ] 3-minute recorded presentation of the memo. Tag `v0.8.0`.

**Done when:** the memo answers one clear question with numbers I can defend.

---

## M9 · Industrialization → `v0.9.0`
**Size:** 2 sessions · **Learn:** Renaissance 12

1. [ ] `infra/` Dockerfiles for the app and the API (slim images, non-root user).
2. [ ] `docker-compose.yml`: app, api, mlflow; one command starts everything on sample data.
3. [ ] Makefile targets all working (`up`, `build`, `app`, `api`, `quality`).
4. [ ] CI: lint → tests → build images on every PR; coverage reported.
5. [ ] Scheduled workflow: daily OpenSky refresh + rebuild + quality report (secrets in GitHub Actions secrets).
6. [ ] Logging and error handling reviewed; `.env.example` complete.
7. [ ] Fresh-clone test on another machine; fix what breaks. Tag `v0.9.0`.

**Done when:** a teammate can clone and run the whole stack with two commands.

🚀 Later: Airflow in compose with one DAG per source (`dags/`); deploy the API on AWS free tier.

---

## M10 · Copilot → `v1.0.0`
**Size:** 3 sessions · **Learn:** Renaissance 13

1. [ ] Corpus: FAA Aviation Maintenance Technician Handbooks (public domain) and other licence-clean documents, each listed in [copilot/corpus_sources.md](src/aerolisa/copilot/corpus_sources.md).
2. [ ] Ingestion: PDF → text → chunks with page references.
3. [ ] Retrieval: embeddings + BM25 hybrid search, re-ranking; answers **with citations**; refuses when sources don't cover the question.
4. [ ] Evaluation set: 30 questions with expected sources; retrieval recall and answer correctness in `reports/copilot-eval.md`.
5. [ ] Compare 2 chunking strategies on the eval set; keep the better one.
6. [ ] **Tools on the API:** `get_engine`, `get_aircraft`, `rank_inspections`, `explain_engine` (read-only).
7. [ ] **Proposed actions:** `propose_schedule_inspection` returns a draft; the user confirms in the app; only then the action runs. Every tool call logged.
8. [ ] Copilot page in the app.
9. [ ] **AIP twin:** M4 step 13 (AIP Logic "explain engine risk") on the Foundry edition. Tag `v1.0.0`.

**Done when:** the copilot answers the eval set with citations above my target, and cannot change data without a human click.

---

## M11 · Showcase
**Size:** 2 sessions · **Learn:** Renaissance 14, 15

1. [ ] [docs/case-study.md](docs/case-study.md): problem, users, approach, results, limits, what changes with real airline data.
2. [ ] 3-minute demo video following [docs/demo-script.md](docs/demo-script.md); Foundry segment included.
3. [ ] README top screen: one-sentence pitch, GIF, live link, video link, results table.
4. [ ] Portfolio page (GitHub Pages) linking Aerolisa, the Foundry video, Renaissance, Turbofan-RUL.
5. [ ] LinkedIn post: the full story with the video.

**Done when:** the README's first screen gets an interviewer to click the demo.

---

## Showcase checklist (after every milestone)
- [ ] README milestone table and Results section updated
- [ ] GIF / screenshots refreshed if the app changed
- [ ] CHANGELOG entry and tag
- [ ] One LinkedIn post: what I built, one lesson, one image
- [ ] CV line updated if the milestone adds a new skill

## Parking lot (not planned; only after M11)
- Trajectory efficiency: flown route vs great-circle distance per city pair; wind-aware A* on a grid
- Streaming ingestion of live ADS-B state vectors
- OSDK front-end on the Foundry edition
- Spare-parts demand forecast linked to removals
