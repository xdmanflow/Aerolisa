# API

> FastAPI layer exposing ontology objects, planner results and action types. Used by the app and by the copilot's tools.

**Milestone:** M7 (containerized in M9)
**May import:** `aerolisa.core`, `aerolisa.engine_health`, `aerolisa.fleet`, `aerolisa.analytics`, `aerolisa.planner`
**Learn:** Renaissance 12

## Planned endpoints

| Method | Path | Returns |
|---|---|---|
| GET | `/aircraft`, `/aircraft/{icao24}` | Aircraft objects (+ linked engines, utilization) |
| GET | `/engines`, `/engines/{engine_id}` | Engine objects (+ latest snapshot, work orders) |
| GET | `/engines/{engine_id}/snapshots` | EngineHealthSnapshot history |
| GET | `/flights?aircraft=` | Flight objects |
| GET | `/planner/ranking` | InspectionRecommendation objects, ranked |
| GET | `/planner/what-if?engine_id=&delay_days=` | Risk if delayed |
| POST | `/actions/{action_type}` | Applies an action type (validated), returns the writeback record |
| GET | `/analytics/kpis` | KPI values for the Analytics page |
| GET | `/health` | Service and data freshness |

## Steps
1. [ ] Pydantic response models generated from / aligned with the ontology
2. [ ] Read endpoints over object tables (DuckDB)
3. [ ] Planner endpoints
4. [ ] Action endpoint calling `core.actions`; errors return clear messages (which submission criterion failed)
5. [ ] Tests with `TestClient` on sample data
6. [ ] OpenAPI docs at `/docs` checked and readable

## Definition of done
- [ ] Every app page and every copilot tool uses the API
- [ ] Tests cover every endpoint
