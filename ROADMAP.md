# Roadmap

Rules kept from Aerolisa v0: **always demoable** (main always works), **cut scope, not the milestone**,
every phase ends with the showcase checklist. Sizes are in Sunday build sessions.

## Phase 0 · Merge (done, Nov. 2026)
- [x] Turbofan-RUL + Aerolisa merged into one repo; SAA v1 preserved in `research/saa_v1`
- [x] Local twin: pipelines, engine health (intervals, health index, anomaly, reliability), fleet, planner; 34 tests
- [x] Foundry code: pipelines repo (PySpark), ML repo (ModelAdapter), Functions (TypeScript), ontology spec, app/AIP specs
- [x] SAA v2 research + revised report

## Phase 1 · Predictive maintenance on Foundry · 6–8 sessions · **the demo for applications**
Follow [docs/foundry-build-guide.md](docs/foundry-build-guide.md) steps 1–15.
**Done when:** in 5 minutes on Foundry, raw file → pipeline → model → ontology → Workshop → action → AIP explanation,
and every number matches `foundry/README.md` "Expected values".

## Phase 2 · Trust: XAI & certification readiness (use case 10) + documentation copilot (use case 3) · 4 sessions
Assurance-case document, robustness tests (noise, missing sensor), drift monitor; FAA-handbook RAG with citations,
30-question eval, AIP tools on the ontology.

## Phase 3 · Predictive maintenance v2 · 3 sessions
FD002–FD004 and N-CMAPSS with operating-condition normalisation; windowed-MLP/1D-CNN ensemble; MC-free uncertainty
comparison; real cycles from OpenSky (build guide step 16).

## Phase 4 · Supply chain linked to maintenance (use case 8) · 3 sessions
Predicted removals → spare-parts demand → inventory decisions, on the same ontology.

## Phase 5 · Flight efficiency & emissions (use cases 4 and 6) · 4 sessions
OpenSky trajectories, OpenAP fuel, ERA5 winds; CO₂ ledger, contrail flag, SAF scenario.

## Phase 6 · Showcase · 2 sessions
Demo video (docs/demo-script.md), case study, LinkedIn post, portfolio page.

## Later (designed in docs/use-cases.md)
Visual inspection (2) · air & space traffic (5) · generative design (7) · autonomy & cockpit assistance (9).

## Showcase checklist (after every phase)
- [ ] README results and status tables updated · [ ] screenshots refreshed · [ ] CHANGELOG + tag
- [ ] one LinkedIn post (what I built, one lesson, one image) · [ ] CV line updated
