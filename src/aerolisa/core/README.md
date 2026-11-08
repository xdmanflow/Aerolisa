# Core

> The contract every other component relies on: configuration, the Foundry-style transform API and build runner, the dataset catalog, ontology models and the action engine.

**Milestones:** M1 (config, paths) · M2 (transforms, catalog, build, lineage) · M3 (ontology, actions)
**May import:** nothing from Aerolisa.

## Planned files

| File | Contents | Milestone |
|---|---|---|
| `config.py` | settings from `.env` (data dir, MLflow URI, OpenSky credentials path) | M1 |
| `paths.py` | dataset name → file path (`silver/flights` → `data/silver/flights.parquet`) | M1 |
| `transforms.py` | `Input`, `Output`, `@transform`, registry | M2 |
| `build.py` | dependency graph, topological sort, run, run IDs, timings | M2 |
| `catalog.py` + `catalog.yaml` | dataset metadata: layer, owner, schema, primary key, description | M2 |
| `lineage.py` | Mermaid graph from the registry | M2 |
| `ontology.py` | load and validate `ontology/ontology.yaml`; Pydantic models per object type | M3 |
| `actions.py` | apply an action type: validate parameters and submission criteria, append to `writeback/` with audit fields | M3 |

## Target API (design, not implementation)

```python
from aerolisa.core.transforms import Input, Output, transform


@transform(
    output=Output("silver/cmapss_cycles"),
    raw=Input("bronze/cmapss_raw"),
)
def clean_cmapss(raw):
    """Pure function: DataFrames in, DataFrame out. No file I/O here."""
    ...
```

`aerolisa build silver/cmapss_cycles` finds `bronze/cmapss_raw` upstream, builds it if missing or stale, then runs `clean_cmapss` and writes the output. Compare with Foundry's `transforms.api` in [foundry/README.md](../../../foundry/README.md).

## Steps
1. [ ] `config.py` and `paths.py` with tests (M1)
2. [ ] `Input`, `Output`, `@transform` and a registry; tests with two toy transforms (M2)
3. [ ] Build runner with topological sort; cycle detection raises a clear error (M2)
4. [ ] Catalog YAML + loader; every registered transform's output must be in the catalog (test) (M2)
5. [ ] Lineage graph writer (M2)
6. [ ] Ontology loader + Pydantic models + integrity checks (M3)
7. [ ] Action engine + writeback + audit fields (M3)

## Done when
- [ ] Every dataset in the repo is produced by a registered transform and described in the catalog
- [ ] Every object type has a definition, a model and a test
- [ ] Actions never modify source datasets
