# Palantir Foundry & AIP: the skill map

The goal: walk into an Airbus Skywise interview having **built** on Foundry, with the vocabulary to explain it. Learning happens in [module 06](../modules/06_foundry-data-engineering/README.md) and [module 07](../modules/07_foundry-ontology-apps/README.md), with AIP in [module 13](../modules/13_genai-llm-agents-aip/README.md). The proof lives in Aerolisa's Foundry edition.

## Access
- **Developer Tier (free):** build.palantir.com. A real Foundry / AIP environment for individuals; restrictions apply (for example by country). Generally available applications are included.
- **Palantir Learn:** learn.palantir.com. Speedruns, deep dives, role tracks (Data Engineer, Application Developer, Data Analyst, Data Scientist, AI Engineer, Frontend Developer), exam guides, quizzes and badges.
- **Docs:** palantir.com/docs/foundry · **Community:** community.palantir.com · **YouTube:** Palantir Developers.

Rules for my Developer Tier work: public data only; nothing from ALTEN or any employer; check the Developer Tier terms before publishing screenshots or video.

## Learning order
1. *Foundry & AIP Aware* path (overview)
2. *Speedrun: Your First End-to-End Workflow* ✅ (done)
3. *Deep Dive: Creating Your First Data Connection*
4. *Deep Dive: Building Your First Pipeline* (Pipeline Builder)
5. *Deep Dive: Transforming your data with Code Repositories*
6. Data Engineer track: scheduling, data expectations & Data Health, *Pipeline Management* video, *Spark Optimization* video
7. *Deep Dive: Creating Your First Ontology*
8. *Deep Dive: Building Your First Application* + the Workshop video course
9. *Speedrun: Your First Ontology Function*
10. *Deep Dive: Data Analysis in Contour*, *Deep Dive: Data Analysis in Quiver*
11. *Speedrun: Your First AIP Workflow*, *Speedrun: Your First Agentic AIP Workflow*
12. 🚀 Slate video course, *Speedrun: Data Science Fundamentals*, *Speedrun: Mining Your First Business Process*, *Applied Notional Project*

## Tool map

| Tool | What it is | In Airbus postings | Module | Aerolisa Foundry edition | Status |
|---|---|---|---|---|---|
| Projects, Compass, permissions | Where resources live; who can see what | access management | 06 | project setup | ☐ |
| Data Connection | Sources, syncs, uploads, agents | ✓ ingestion | 06 | upload C-MAPSS, flights sample | ☐ |
| Datasets & transactions | Versioned tables/files; snapshot, append, update | ✓ | 06 | all datasets | ☐ |
| Pipeline Builder | Visual / low-code pipelines | ✓ | 06 | cleaning pipeline | ☐ |
| Code Repositories | Git-backed Python/PySpark (and SQL) transforms, tests, PRs | ✓ "Code Repository" | 06 | transforms ported from Aerolisa | ☐ |
| Code Workbook / Code Workspaces | Notebook-style exploration | ✓ (some postings) | 06 | EDA notebook | ☐ |
| Builds & schedules | Running pipelines, triggers | ✓ monitoring | 06 | daily schedule | ☐ |
| Data Lineage | Upstream/downstream graph | ✓ troubleshooting | 06 | screenshot + debug story | ☐ |
| Data expectations, Data Health | Checks in transforms, health checks, alerts | ✓ | 06 | PK, nulls, ranges | ☐ |
| Ontology Manager | Object, link, action types | ✓ "Ontology" | 07 | Aircraft, Engine, Snapshot, Flight | ☐ |
| Object Explorer | Search and explore objects | ✓ | 07 | saved exploration | ☐ |
| Workshop | Operational apps on objects | ✓ | 07 | inspection queue app | ☐ |
| Functions (TypeScript / Python) | Logic on objects, edits behind actions | ✓ TypeScript | 07 | risk score function | ☐ |
| Actions & writeback | Capture decisions in the data | ✓ | 07 | "Schedule inspection" | ☐ |
| Contour | Analysis on datasets | ✓ | 07 | lifetime by fault mode | ☐ |
| Quiver | Time series & object analysis | ✓ | 07 | sensor trends | ☐ |
| Notepad | Reports from analyses | — | 07 | short report | ☐ |
| Slate | Custom HTML/JS apps | ✓ | 07 🚀 | optional page | ☐ |
| Marketplace, templates | Packaging and reuse | ✓ | 07 🚀 | optional | ☐ |
| OSDK | Build external apps on the ontology | — | 07 🚀 | optional | ☐ |
| AIP Logic | LLM-backed functions on the ontology | ✓ AIP | 13 | "explain engine risk" | ☐ |
| AIP Agent Studio | Agents with ontology tools | ✓ AIP | 13 | optional copilot twin | ☐ |
| AIP Evals | Evaluating LLM functions | — | 13 | eval on 10 questions | ☐ |

## Concepts I must explain without notes
- Ontology vs tables; object, link, action types; why actions matter (decisions become data)
- Datasets, transactions, branches, builds, schedules
- Pipeline Builder vs Code Repositories
- Lineage-based debugging
- How AIP keeps a human in control

Certifications: [certifications.md](certifications.md) · Vocabulary: [glossary.md](glossary.md).
