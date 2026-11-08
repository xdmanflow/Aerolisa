# Foundry edition

The core Aerolisa flow rebuilt on **Palantir Foundry** (Developer Tier, public data only). Milestone **M4**, AIP step at **M10**. Learn: Renaissance modules 06, 07, 13.

## What to put in this folder

```text
foundry/
├── README.md            # this file: what was built, how, comparison with local
├── code-repo/           # transforms exported from the Foundry Code Repository
├── ontology.md          # object, link and action types as configured in Foundry
├── workshop.md          # app layout, widgets, variables, actions, functions
├── functions/           # TypeScript function source (risk score)
└── screenshots/         # numbered: 01_project.png, 02_pipeline_builder.png, …
```

## Build log (fill while doing M4)

| Step | Foundry tool | What I did | Screenshot |
|---|---|---|---|
| 1 | Projects | Folder structure `bronze / silver / gold / objects` | |
| 2 | Data Connection | Uploaded raw C-MAPSS files | |
| 3 | Pipeline Builder | Cleaning pipeline → `silver/cmapss_cycles` | |
| 4 | Code Repositories | Ported M2 PySpark transforms | |
| 5 | Code Repositories | Unit tests + data expectations | |
| 6 | Code Repositories | Branch → PR → merge → build | |
| 7 | Schedules, Data Lineage, Data Health | Schedule; broke an input; traced; health check fired | |
| 8 | Ontology Manager | Engine, EngineHealthSnapshot, Aircraft + links | |
| 9 | Workshop | Inspection queue app | |
| 10 | Actions + Functions | `ScheduleInspection` + TypeScript risk score | |
| 11 | Contour, Quiver | Lifetime by fault mode; sensor trends | |
| 12 | — | 2-minute recording | |
| 13 | AIP Logic | "Explain this engine's risk" (M10) | |

## Local vs Foundry transforms

| | Local (`aerolisa.core.transforms`) | Foundry (`transforms.api`) |
|---|---|---|
| Declaration | `@transform(output=Output(...), x=Input(...))` | `@transform_df(Output(...), x=Input(...))` |
| Engine | PySpark local mode | Spark on Foundry |
| Paths | dataset names → `data/<layer>/<name>.parquet` | Foundry dataset paths / RIDs |
| Tests | pytest + local SparkSession | repository tests |
| Checks | `pipelines/quality.py` | data expectations + health checks |
| Lineage | generated Mermaid graph | Data Lineage app |

_Fill the differences I actually hit while porting: that paragraph is interview material._

## Rules
- Public data only. Nothing from ALTEN or any employer.
- Check the Developer Tier terms before publishing screenshots or video.
