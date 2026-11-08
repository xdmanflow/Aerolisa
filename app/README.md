# App

Streamlit multipage operational app, designed like a Foundry **Workshop** app: it reads ontology objects, shows decisions, and lets a planner act.

Run: `make app` (from M1).

| Page | File | Shows | Milestone |
|---|---|---|---|
| Fleet overview | `Home.py` | Engines ranked by risk (M1: by predicted RUL), fleet KPIs, simulation disclaimer | M1 → M7 |
| Engine | `pages/1_Engine.py` | Sensor trends, RUL with interval, anomaly score, top drivers, linked aircraft and work orders | M1 → M6 |
| Data health | `pages/2_Data_health.py` | Last build, quality checks passed/failed, lineage link | M2 |
| Aircraft | `pages/3_Aircraft.py` | Flights, utilization, its two engines | M5 |
| Inspection queue | `pages/4_Inspection_queue.py` | Ranked recommendations with reasons; **Schedule inspection** action; what-if | M7 |
| Analytics | `pages/5_Analytics.py` | European operations + Airbus deliveries KPIs | M8 |
| Copilot | `pages/6_Copilot.py` | Questions with citations; proposed actions to confirm | M10 |

## Rules
- Before M7 the app reads object tables through `aerolisa.core`; from M7 it calls the API only.
- The "simulated engines" disclaimer is visible on every page that shows an engine.
- The public deployment runs on sample or precomputed data, never on raw OpenSky data.
