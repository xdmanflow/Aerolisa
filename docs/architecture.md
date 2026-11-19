# Architecture

## Layers (identical names locally and in Foundry)
| Layer | Datasets | Produced by |
|---|---|---|
| raw | `raw/cmapss_files` (uploaded .txt) | upload |
| bronze | `bronze/cmapss_raw`, `bronze/cmapss_rul` (+ `bronze/opensky_flights`, optional) | pipelines repo |
| silver | `silver/cmapss_cycles` (typed, keyed, one row per engine-cycle) | pipelines repo |
| gold | `gold/engine_cycle_features`, `gold/engine_life_records` | pipelines repo (PySpark) |
| gold | `gold/fleet_aircraft`, `gold/aircraft_utilization_daily`, `gold/engine_assignment`, `gold/engine_health_model_metrics`, `gold/engine_health_snapshot`, `gold/inspection_recommendation`, `gold/reliability_km` | ML repo (pandas + model) |
| model | `models/engine-health-model` (versions) | ML repo |
| objects | `objects/engine`, `objects/aircraft`, `objects/operator` | pipelines repo (PySpark joins) |
| writeback | `writeback/work_orders` (seed; rows created by actions) | actions |

Generated lineage of the local twin: [lineage.md](lineage.md).

## Dependency rule (local package)
| Component | May import |
|---|---|
| `core` | nothing from Aerolisa |
| `pipelines`, `engine_health`, `fleet`, `planner` | `core` |
| `cli` | everything (it wires the graph) |

Enforced by `tests/test_architecture.py`. Domain modules never import each other: the graph (`cli/graph.py`, or
Foundry dataset paths) connects them, the way Foundry transforms connect through datasets.

## Contracts that keep the two editions identical
1. Column contract: each PySpark function in `foundry/pipelines-repo/.../logic/` returns the columns of its pandas twin.
2. Package contract: `foundry/ml-repo/src/aerolisa` == `src/aerolisa` (`scripts/sync_foundry.py --check`).
3. Ontology contract: every property in `ontology.yaml` maps to a column of its backing dataset (`tests/test_ontology_contract.py`).
4. Formula contract: the risk CDF in TypeScript equals the Python one (`functions-repo/src/quantileCdf.test.ts` + Python tests).

## Decisions
See [adr/](adr), notably 0007 (two repos, one package) and 0008 (gradient boosting in production).
