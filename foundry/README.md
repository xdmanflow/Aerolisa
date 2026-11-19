# Foundry edition

Everything needed to rebuild Aerolisa's predictive-maintenance slice on Palantir Foundry.
**How:** [../docs/foundry-build-guide.md](../docs/foundry-build-guide.md).

| Folder | Foundry resource | Status |
|---|---|---|
| `pipelines-repo/` | Code Repository, Python transforms (PySpark) | code ready · to build |
| `ml-repo/` | Code Repository, Model Training template | code ready (wiring tested locally) · to build |
| `functions-repo/` | Code Repository, TypeScript Functions | code ready · to build |
| `ontology/ontology.yaml` | Ontology Manager | spec ready (contract-tested) · to configure |
| `workshop/` | Workshop app | spec ready · to build |
| `analyses/` | Quiver, Contour | spec ready · to build |
| `pipeline-builder/` | Pipeline Builder | spec ready · to build |
| `aip/` | AIP Logic | spec + eval ready · to build |
| `screenshots/` | evidence, numbered as in the build guide | empty |

## Expected values (from the local twin: Foundry must match)
| Dataset | Rows | Spot checks |
|---|---|---|
| `silver/cmapss_cycles` | 33,727 | `FD001-HIST-001` has 192 cycles |
| `gold/engine_cycle_features` | 33,727 × 78 | `FD001-FLEET-001` last cycle `rul = 112` |
| `gold/engine_health_model_metrics` | 1 per version | test_rmse 13.98 · coverage 0.81 · alert threshold 25 |
| `gold/engine_health_snapshot` | 13,096 | 100 rows with `is_latest = true` |
| `gold/inspection_recommendation` | 100 | rank 1 = `FD001-FLEET-076` (RED) · 34 RED / 12 AMBER / 54 GREEN |
| `objects/aircraft` | 50 | |

## Local vs Foundry transforms
| | Local (`aerolisa.core.transforms`) | Foundry (`transforms.api`) |
|---|---|---|
| Declaration | `@transform(Output(...), x=Input(...))` | `@transform_df(Output(...), x=Input(...))` / `@transform(...)` |
| Engine | pandas | Spark (pipelines repo), pandas inside transforms (ML repo) |
| Storage | `data/<layer>/<name>.csv` | datasets (paths / RIDs), transactions, branches |
| Checks | `primary_key`, `non_null`, `in_range` callables | data expectations (`Check`, `E`) + Data Health |
| Lineage | `python -m aerolisa.cli lineage` (Mermaid) | Data Lineage app |
| Models | Python objects in memory | `ModelOutput` → model versions → `ModelInput` |

## What I hit while porting (fill as you go: interview material)
-
