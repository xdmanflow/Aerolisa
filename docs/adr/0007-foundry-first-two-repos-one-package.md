# ADR 0007: Foundry first, two code repositories, one tested package

**Status:** accepted (Nov. 2026)

**Context:** the project merges Turbofan-RUL (CESI research) and Aerolisa (Skywise-style platform) and must be shown on
Palantir Foundry. Foundry's Model Training template is the supported way to publish models, and model adapters cannot be
authored in a plain Python-transforms repository. Spark is not available on the developer laptop.

**Decision:**
- `aerolisa-pipelines` (Python transforms): PySpark for ingestion, cleaning, features and object tables; logic in `logic/`
  without Foundry imports, unit-tested in Foundry.
- `aerolisa-ml` (Model Training template): model adapter, training, inference, fleet, planner, reliability, all in pandas,
  calling a vendored copy of `src/aerolisa`.
- `src/aerolisa` is the single source of truth; `scripts/sync_foundry.py` copies it; CI fails if the copy drifts; the
  ML repo's wiring is executed locally against fakes of `transforms.api` and `palantir_models`.

**Consequences:** the model in Foundry is trained by code with 34 local tests; the PySpark code is only tested inside
Foundry (accepted risk, mitigated by pandas twins with identical column contracts and the ontology contract test).
