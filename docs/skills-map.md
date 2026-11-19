# Skills map: what each part of Aerolisa trains

Target roles (vision board): Data Engineer → Data Analyst → Data Scientist → AI Engineer →
Data & AI Architect → Head of Data & AI → CTO. First stop: data roles on a Skywise / Foundry team in Toulouse.

| Skill | Where you practise it in Aerolisa | Proof to show |
|---|---|---|
| **Palantir Foundry: pipelines** | Code Repositories (Python transforms), Pipeline Builder, schedules, Data Lineage, Data Health | build guide steps 2–8, screenshots 01–11 |
| **Foundry: Ontology** | object/link/action types, edits, writeback (`ontology.yaml`) | steps 9–11 |
| **Foundry: apps** | Workshop, Quiver, Contour | steps 12–13 |
| **Foundry: AIP** | AIP Logic grounded on objects, evaluation set | step 14 |
| **Foundry: ML** | `palantir_models` ModelAdapter, ModelOutput/ModelInput, model versions | step 5 |
| **Python** | `src/aerolisa` (typed, tested, packaged), CLI | `make test` |
| **PySpark / Apache Spark** | window functions (rolling mean/std/slope), joins, aggregations, schemas, file ingestion | `pipelines-repo/logic/` |
| **SQL** | `sql/*.sql`: windows, ranking, KPIs on the gold datasets | Foundry SQL / Contour |
| **Data quality** | data expectations (primary key, ranges, domains), local checks, contract tests | step 7 (break & trace) |
| **Data modelling** | bronze/silver/gold/objects layers, primary keys, ontology design | `docs/architecture.md` |
| **Statistics** | conformal intervals, coverage, Kaplan–Meier, Weibull, CI on utilisation | research results |
| **Machine learning** | gradient boosting, quantile regression, anomaly detection, PCA, leakage-free validation | SAA v2 |
| **Deep learning** | LSTM (SAA v1), windowed MLP; next: 1D-CNN/Transformer on N-CMAPSS | research |
| **Decision science** | cost-based thresholds, risk ranking, what-if | `docs/planner-risk.md` |
| **TypeScript** | Functions on objects, OntologyEditFunction | `functions-repo` |
| **GenAI** | AIP Logic prompt, grounding, evaluation; next: RAG copilot (use case 3) | `foundry/aip/` |
| **Engineering practice** | Git branches & PRs (in Foundry and GitHub), CI, ADRs, model card | repo history |
| **Cloud** | Foundry is the managed cloud platform here; next: the same pipeline on Databricks or Snowflake as a comparison | vision board stack |
| **Communication** | README, demo script, report, Workshop UX | `docs/demo-script.md` |

## Interview questions this project prepares you for
1. Walk me through a Foundry pipeline from raw file to Workshop. *(steps 2–12)*
2. Why gradient boosting and not your LSTM in production? *(research: same or better accuracy, intervals, cost, explainability)*
3. How do you know the interval is right? *(conformal calibration on held-out engines; measured 81 %)*
4. How do you avoid leakage? *(engine-level split, causal windows, scaler/thresholds fit on training engines only)*
5. What happens when an upstream dataset breaks? *(expectations fail the build; lineage shows where; step 7)*
6. How does a planner's decision get back into the data? *(action → WorkOrder edits; closing finding = future label)*
7. What would change with real airline data? *(multiple fault modes, maintenance resets, sensor faults, drift monitoring, certification evidence)*
