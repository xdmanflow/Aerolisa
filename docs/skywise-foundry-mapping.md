# Skywise & Foundry mapping

How each part of Aerolisa relates to Palantir Foundry and to the publicly described Skywise products, and what to say about it in an interview. Aerolisa is inspired by public descriptions only; it reproduces no Airbus or Palantir code, data or design.

## Skywise products (public descriptions) → Aerolisa

| Skywise product | Public description (short) | Aerolisa equivalent |
|---|---|---|
| S.Health Monitoring | Helps line maintenance, MCC and engineering identify, prioritise and handle in-service events | Anomaly scores + inspection queue + actions (M6, M7) |
| S.Predictive Maintenance+ | Early alerts on upcoming degradation; unscheduled → scheduled | RUL with intervals + alert model (M6) |
| S.Fleet Reliability | Integrates reliability data, benchmarks the fleet, finds root causes | Reliability view: Kaplan–Meier, Weibull, lifetime by fault mode (M6) |
| Skywise Core | Entry-level platform to view and analyse fleet data | Data platform + ontology + app (M2, M3, M7) |

## Foundry concepts → Aerolisa

| Foundry | Aerolisa local | Aerolisa Foundry edition | What I can say |
|---|---|---|---|
| Data Connection, syncs | `pipelines/sources/*` | file upload | "Ingestion is isolated per source, with raw kept as received." |
| Datasets & transactions | Parquet datasets per layer, run IDs | datasets | "Outputs are fully recomputed (snapshot) except OpenSky, which appends new days." |
| Code Repositories (`transforms.api`) | `@transform` + `Input`/`Output` in `aerolisa.core` | same transforms ported | "I wrote the local API to match Foundry's, so the code ports almost unchanged." |
| Pipeline Builder | — | cleaning pipeline | "I used Pipeline Builder for the simple cleaning and code for the windowed features." |
| Builds & schedules | `aerolisa build` (topological sort), scheduled workflow | schedule | "A build only recomputes what's downstream of a change." |
| Data Lineage | `aerolisa lineage` → Mermaid graph | lineage app | "When a source broke, I traced it through lineage." |
| Data expectations / health checks | `pipelines/quality.py` + reports | expectations + health checks | "Checks fail the build on key violations and warn on drift." |
| Ontology: object types, links | `ontology/ontology.yaml`, object tables | Ontology Manager | "Apps read objects, not tables, so every page agrees on what an engine is." |
| Action types & writeback | `core/actions.py`, `writeback/` | action types | "Decisions become data, with an audit trail." |
| Functions | planner functions behind the API | TypeScript Function (risk score) | "Business logic lives in one place and every app calls it." |
| Workshop | Streamlit app | Workshop app | "Same pages: queue, engine view, action button." |
| Object Explorer | app search page | Object Explorer | |
| Contour | `sql/` analyses on DuckDB | Contour analysis | |
| Quiver | sensor trends page | Quiver analysis | "Quiver is how Skywise users analyse sensor data; I did the healthy vs degrading comparison there." |
| Modeling / model registry | MLflow registry | — | |
| AIP Logic / Agent Studio | `copilot` with tools + confirmation | AIP Logic function | "The LLM proposes; a human confirms through an action." |
| Markings, permissions | not implemented (single user); described | project permissions | "With real airline data, access would be restricted per customer and per data owner." |

## What would change with real data
- Sensor data from ACMS / ACARS reports and fault messages instead of C-MAPSS simulations
- Maintenance records (work orders, removals, findings) from the operator's MRO system or SAP
- Installation history (engines move between aircraft)
- Strict access control per airline and data owner; no external LLM calls on sensitive data
