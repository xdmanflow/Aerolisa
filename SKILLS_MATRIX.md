# Skills matrix

What Airbus and the wider ASD industry ask for in data & AI postings, where I learn it, and where I **prove** it. A skill counts as acquired only when the proof column links to something real.

Sources: Airbus apprenticeship, internship and job postings for Skywise / data / AI roles read in 2025–2026 (Toulouse, Copenhagen, Albacete, Bangalore, Atlanta), plus Skywise partner postings. Re-check against new postings every month and add rows.

**Roles:** DE data engineer · DA data analyst · DS data scientist · AI AI engineer
**Priority:** P0 on almost every Skywise posting · P1 often · P2 sometimes / differentiator

## Core technical

| Skill | Roles | Priority | Learn | Prove in Aerolisa | Status |
|---|---|---|---|---|---|
| Python (clean, tested, packaged) | all | P0 | [01](modules/01_python-for-data/README.md) | `src/aerolisa/*`, CI green | ☐ |
| pandas / NumPy | all | P0 | [01](modules/01_python-for-data/README.md) | M1 pipelines | ☐ |
| SQL incl. window functions | all | P0 | [02](modules/02_sql/README.md) | `sql/`, M2 gold layer, M8 | ☐ |
| PySpark | DE · DS | P0 | [04](modules/04_pyspark/README.md) | M2 transforms | ☐ |
| Data modeling (relational, dimensional, ontology) | DE · DA | P0 | [03](modules/03_data-modeling-architecture/README.md) | M3 `ontology/` | ☐ |
| Data pipelines, ETL/ELT, incremental builds | DE | P0 | [05](modules/05_pipelines-data-quality/README.md) | M2 `aerolisa build` | ☐ |
| Data quality & monitoring | DE · DA | P1 | [05](modules/05_pipelines-data-quality/README.md) | M2 quality reports | ☐ |
| TypeScript (Foundry Functions, front-end logic) | DE · AI | P1 | [07](modules/07_foundry-ontology-apps/README.md) | M4 Foundry Functions | ☐ |
| Git, code review, CI/CD | all | P1 | [12](modules/12_software-engineering-mlops-cloud/README.md) | PRs, `.github/workflows` | ☐ |
| Docker | DE · DS | P1 | [12](modules/12_software-engineering-mlops-cloud/README.md) | M9 compose stack | ☐ |
| REST APIs (FastAPI) | DE · AI | P1 | [12](modules/12_software-engineering-mlops-cloud/README.md) | M7 API | ☐ |
| AWS fundamentals | DE | P2 | [12](modules/12_software-engineering-mlops-cloud/README.md) | M9 (optional deploy) | ☐ |
| Orchestration (Airflow concepts, schedules) | DE | P2 | [05](modules/05_pipelines-data-quality/README.md) · [12](modules/12_software-engineering-mlops-cloud/README.md) | M9 scheduled refresh | ☐ |

## Palantir Foundry & AIP (the Skywise stack)

| Skill | Roles | Priority | Learn | Prove | Status |
|---|---|---|---|---|---|
| Datasets, builds, branches, schedules, lineage | DE | P0 | [06](modules/06_foundry-data-engineering/README.md) | M4 | ☐ |
| Pipeline Builder | DE · DA | P0 | [06](modules/06_foundry-data-engineering/README.md) | M4 | ☐ |
| Code Repositories (Python/PySpark transforms) | DE | P0 | [06](modules/06_foundry-data-engineering/README.md) | M4 + M2 (same structure locally) | ☐ |
| Data expectations, health checks | DE | P1 | [06](modules/06_foundry-data-engineering/README.md) | M4 | ☐ |
| Ontology: object, link and action types | all | P0 | [07](modules/07_foundry-ontology-apps/README.md) | M3 + M4 | ☐ |
| Object Explorer | DA | P1 | [07](modules/07_foundry-ontology-apps/README.md) | M4 | ☐ |
| Workshop applications | DE · DA · AI | P0 | [07](modules/07_foundry-ontology-apps/README.md) | M4 + M7 (Streamlit twin) | ☐ |
| Contour | DA | P1 | [07](modules/07_foundry-ontology-apps/README.md) | M4 | ☐ |
| Quiver (time series, sensor data) | DA · DS | P1 | [07](modules/07_foundry-ontology-apps/README.md) | M4 | ☐ |
| Functions (TypeScript / Python) | DE · AI | P1 | [07](modules/07_foundry-ontology-apps/README.md) | M4 | ☐ |
| Slate, Marketplace, templates, access management | DE | P2 | [07](modules/07_foundry-ontology-apps/README.md) | awareness, notes | ☐ |
| AIP Logic, Agent Studio, AIP Evals | AI | P1 | [13](modules/13_genai-llm-agents-aip/README.md) | M10 Foundry step | ☐ |

## Data science & AI

| Skill | Roles | Priority | Learn | Prove | Status |
|---|---|---|---|---|---|
| Statistics & inference | DA · DS | P0 | [08](modules/08_statistics-probability/README.md) | M5 · M8 reports | ☐ |
| Reliability & survival analysis (Weibull, Kaplan–Meier) | DS | P1 | [08](modules/08_statistics-probability/README.md) · [10](modules/10_time-series-predictive-maintenance/README.md) | M6 | ☐ |
| Regression, random forest, gradient boosting | DS | P0 | [09](modules/09_machine-learning/README.md) | M6 model comparison | ☐ |
| Leak-free validation (grouped, time-based) | DS | P0 | [09](modules/09_machine-learning/README.md) | M6 evaluation report | ☐ |
| Time-series features & anomaly detection | DS · AI | P0 | [10](modules/10_time-series-predictive-maintenance/README.md) | M6 | ☐ |
| Predictive maintenance (RUL, alerts, cost trade-offs) | DS | P0 | [10](modules/10_time-series-predictive-maintenance/README.md) | M6 · M7 | ☐ |
| Deep learning (PyTorch, sequence models) | DS · AI | P2 | [10](modules/10_time-series-predictive-maintenance/README.md) | M6 | ☐ |
| Explainability (SHAP, permutation importance) | DS | P1 | [09](modules/09_machine-learning/README.md) | M6 · M7 explanations | ☐ |
| MLOps (MLflow tracking & registry) | DS · AI | P1 | [12](modules/12_software-engineering-mlops-cloud/README.md) | M6 · M9 | ☐ |
| LLMs, prompt engineering | AI | P0 | [13](modules/13_genai-llm-agents-aip/README.md) | M10 | ☐ |
| RAG with citations, evaluation | AI | P0 | [13](modules/13_genai-llm-agents-aip/README.md) | M10 eval report | ☐ |
| Agents, tool calling, human-in-the-loop | AI | P1 | [13](modules/13_genai-llm-agents-aip/README.md) | M10 | ☐ |

## Analytics & business

| Skill | Roles | Priority | Learn | Prove | Status |
|---|---|---|---|---|---|
| KPI design & dashboards | DA | P0 | [11](modules/11_analytics-bi-storytelling/README.md) | M8 | ☐ |
| Power BI (data model, DAX) | DA | P1 | [11](modules/11_analytics-bi-storytelling/README.md) | M8 + ALTEN (described, approved) | ☐ |
| Google Sheets / Excel advanced | DA | P1 | [11](modules/11_analytics-bi-storytelling/README.md) | M8 | ☐ |
| Qlik Sense, SAP Analytics Cloud (seen at Airbus) | DA | P2 | [11](modules/11_analytics-bi-storytelling/README.md) | awareness | ☐ |
| Insight writing & presenting to stakeholders | all | P0 | [11](modules/11_analytics-bi-storytelling/README.md) | M8 memo, M11 video | ☐ |
| Gathering business requirements | all | P0 | [15](modules/15_interviews-applications/README.md) | `docs/case-study.md` | ☐ |
| Agile / Scrum ways of working | all | P1 | [12](modules/12_software-engineering-mlops-cloud/README.md) | GitHub issues & milestones | ☐ |
| Aviation maintenance & operations vocabulary | all | P0 | [14](modules/14_aerospace-domain/README.md) | case study, interviews | ☐ |
| SAP data basics (work orders, materials) | DE · DA | P2 | [14](modules/14_aerospace-domain/README.md) | notes | ☐ |

## Languages & soft skills

| Skill | Priority | Where | Proof | Status |
|---|---|---|---|---|
| English B2+ (certified) | P0 | [career/languages.md](career/languages.md) | TOEIC score | ☐ |
| French professional | P0 | daily | already | ☑ |
| German (plus for some Airbus roles) | P2 | [career/languages.md](career/languages.md) | — | ☐ |
| Clear technical communication | P0 | [15](modules/15_interviews-applications/README.md) | demo video, pitches | ☐ |
