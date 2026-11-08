# Renaissance: the Data & AI curriculum to Airbus Skywise

> My public curriculum to become a complete **data engineer, data analyst and data scientist for aerospace**, with **Palantir Foundry** (the platform behind Airbus Skywise) at its centre. Every module is applied in **[Aerolisa](https://github.com/xdmanflow/Aerolisa)**, my flagship project. Independent learning project, not affiliated with, endorsed by, or connected to Airbus, Skywise or Palantir.

## North star

1. **Next:** a data apprenticeship (alternance) at **Airbus, Skywise ecosystem, Toulouse**, starting September 2027, and a first job there after it.
2. **Then:** a data & AI specialist in the aerospace, space & defence (ASD) industry, in Europe or the US.

Everything in this repository is ordered by how much it moves me toward step 1. Nothing is here "just because".

## Two repositories, one system

| Repository | Role | When |
|---|---|---|
| **Renaissance** (this repo) | *Learn*: modules, exercises, notes, exit tests, career prep | Saturday + commute |
| **[Aerolisa](https://github.com/xdmanflow/Aerolisa)** | *Build*: the flagship platform where every module is applied and shown to recruiters | Sunday |

Each Renaissance module names the Aerolisa milestone it feeds. Learning without building is not allowed; building without the learning behind it is fragile.

## How it works

- **16 modules, done in order** (`00` → `13`). Two tracks run **in parallel** the whole time: `14` aerospace domain (mostly on the commute) and `15` interviews & applications.
- **Two levels in every module.** 🎯 *Apprenticeship level* is what an Airbus interviewer expects from an apprentice: it is mandatory. 🚀 *Pro level* is what makes me a strong junior: do it when ahead, or later. "100%" is reached through the Pro levels, over time, without blocking the critical path.
- **Sizes, not dates.** Each module is sized in weekends. The order never changes; the speed does.
- **Three gates.** Each gate is a state I must reach, checked honestly in [PROGRESS.md](PROGRESS.md):
  - **Gate 1: Application-ready.** Modules 00–07 at 🎯 level. Aerolisa live with a demo link and a Foundry build.
  - **Gate 2: Interview-ready.** Modules 08–10 at 🎯 level. Aerolisa engine health v2 and planner done.
  - **Gate 3: Complete profile.** Modules 11–13 at 🎯 level. Aerolisa analytics pack, industrialization, copilot.
- **Exit tests** close every module: closed-book, timed, no AI. Scores go in [checkpoints/](checkpoints/README.md).

Full plan: **[PLAN.md](PLAN.md)** · What Airbus asks for and where I learn it: **[SKILLS_MATRIX.md](SKILLS_MATRIX.md)**.

## The weekly rhythm

| Slot | What | Where |
|---|---|---|
| Saturday (1 session, 3–4 h) | Learn + exercises of the current module | Renaissance `modules/NN/work/` |
| Sunday (1 session, 3–4 h) | Next step of the paired Aerolisa milestone | Aerolisa |
| Commute / phone | Module 14 reading, Foundry docs, flashcards, interview answers out loud | Anki + notes |
| Sunday evening (15 min) | [Weekly review](WEEKLY_REVIEW_TEMPLATE.md) | GitHub issue |

If weekdays free up, add a third session. The order stays the same.

## My rules

1. **Ship every weekend.** At least one pushed commit in Aerolisa or Renaissance.
2. **Floor on bad weekends:** one session and one commit. Never a zero week.
3. **First attempt without AI.** AI reviews my work; it never writes the first version.
4. **Build beats reading.** Every module ends with something in Aerolisa.
5. **Cut the 🚀 Pro level, never the build.** When behind, drop Pro items, keep the milestone.
6. **Apply before feeling ready.** A posting that matches 60–70% gets an application.
7. **Protect rest.** One free half-day every weekend, one full weekend off every six.

## Modules

| # | Module | Roles | Size | Feeds Aerolisa |
|---|---|---|---|---|
| 00 | [Launch](modules/00_launch/README.md) | all | 1 wk | M0 |
| 01 | [Python for data](modules/01_python-for-data/README.md) | DE · DA · DS | 1 wk | M1 |
| 02 | [SQL](modules/02_sql/README.md) | DE · DA · DS | 3 wk | M2 |
| 03 | [Data modeling & architecture](modules/03_data-modeling-architecture/README.md) | DE · DA | 1 wk | M2 · M3 |
| 04 | [PySpark](modules/04_pyspark/README.md) | DE · DS | 2 wk | M2 |
| 05 | [Pipelines & data quality](modules/05_pipelines-data-quality/README.md) | DE | 1 wk | M2 |
| 06 | [Foundry I: data engineering](modules/06_foundry-data-engineering/README.md) | DE | 3 wk | M4 |
| 07 | [Foundry II: ontology, apps & analytics](modules/07_foundry-ontology-apps/README.md) | DE · DA · AI | 3 wk | M3 · M4 |
| 08 | [Statistics & probability](modules/08_statistics-probability/README.md) | DA · DS | 2 wk | M5 · M6 |
| 09 | [Machine learning](modules/09_machine-learning/README.md) | DS · AI | 3 wk | M6 |
| 10 | [Time series & predictive maintenance](modules/10_time-series-predictive-maintenance/README.md) | DS · AI | 3 wk | M6 · M7 |
| 11 | [Analytics, BI & storytelling](modules/11_analytics-bi-storytelling/README.md) | DA | 2 wk | M8 |
| 12 | [Software engineering, MLOps & cloud](modules/12_software-engineering-mlops-cloud/README.md) | DE · DS | 2 wk | M7 · M9 |
| 13 | [GenAI, LLMs, agents & AIP](modules/13_genai-llm-agents-aip/README.md) | AI · DS | 3 wk | M10 |
| 14 | [Aerospace & ASD domain](modules/14_aerospace-domain/README.md) | all | parallel | M11 |
| 15 | [Interviews & applications](modules/15_interviews-applications/README.md) | all | parallel + 2 wk | M11 |

`wk` = weekend (one Saturday session + one Sunday session). Total ≈ 32 weekends of focused work, plus the parallel tracks.

## Repository structure

```text
Renaissance/
├── modules/
│   └── NN_topic/
│       ├── README.md         # why, 🎯 and 🚀 levels, steps, exit test, resources
│       └── work/             # my notes, solutions, code and tests
├── career/                   # Airbus & ASD knowledge, CV, applications, pay, interviews
├── palantir/                 # Foundry & AIP skill map, certifications, glossary
├── checkpoints/README.md     # exit tests and score log
├── PLAN.md                   # the ordered path, gates, rhythm, what to do when behind
├── SKILLS_MATRIX.md          # job-posting requirement → module → proof
├── PROGRESS.md               # modules, gates, certifications, Aerolisa, career
├── RESOURCES.md              # curated, free first
├── WEEKLY_REVIEW_TEMPLATE.md
└── .github/                  # CI for exercise tests, issue templates
```

## Getting started

```bash
git clone https://github.com/xdmanflow/Renaissance.git
cd Renaissance
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q   # runs every test_*.py found under modules/*/work/
```

## Author

**Manil DOUDOU**, engineering student in computer science (AI & Data Science), CESI Toulouse.

## License

Code under the [MIT License](LICENSE). Notes may be reused with attribution.
