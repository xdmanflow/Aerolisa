# Module 05 · Pipelines & data quality

**Roles:** DE · DA · **Size:** 1 weekend · **Priority:** P0 · **Builds:** Aerolisa M2 (quality checks, lineage, `aerolisa build`)

## Why this matters
Skywise apprentices and interns are asked to support "implementation, testing and optimization of data pipelines and data ingestion flows", and to do "pipeline monitoring and troubleshooting". A pipeline that silently produces wrong data is worse than no pipeline; quality checks and lineage are what make a data engineer trustworthy.

## 🎯 Apprenticeship level (must)
- [ ] Pipeline design: idempotent steps, deterministic outputs, snapshot vs incremental, backfills, reruns
- [ ] Dependencies as a DAG; build order by topological sort; partial rebuilds downstream of a change
- [ ] Data contracts: schema, types, allowed ranges, keys, freshness
- [ ] Quality dimensions: completeness, validity, uniqueness, consistency, timeliness, accuracy
- [ ] Writing checks as code (pandera or plain assertions) and choosing fail vs warn
- [ ] Volume and distribution checks (row counts vs last run, null rate drift)
- [ ] Testing transforms with tiny fixtures; testing the pipeline end to end on `sample_data/`
- [ ] Logging, run IDs, a quality report per run
- [ ] Lineage: which outputs depend on which inputs, and why that matters when a source breaks
- [ ] Orchestration concepts: schedules, triggers, retries, sensors (Airflow vocabulary: DAG, task, operator, scheduler), and how Foundry does it (builds, schedules, health checks)

## 🚀 Pro level
- [ ] Airflow hands-on (done in module 12 / Aerolisa M9)
- [ ] Great Expectations, dbt tests (concepts)
- [ ] Writing an incident runbook and a post-mortem

## Steps
1. **Learn (Saturday AM).** *Fundamentals of Data Engineering*, chapters on ingestion and orchestration; pandera docs; Airflow "core concepts" page.
2. **Practice (Saturday PM)** in `work/`:
   - Write a check suite for C-MAPSS silver data (schema, unit/cycle uniqueness, sensor ranges, no gaps in cycles per unit).
   - Break the data on purpose 5 ways; confirm each check catches it.
   - Write a one-page runbook: "the OpenSky refresh failed / produced half the usual rows: what do I check, in which order?"
3. **Apply (Sunday):** Aerolisa M2 steps on quality reports, lineage graph and the `aerolisa build` command.

## Exit test (45 min, no AI)
Given a pipeline description with three silent bugs, find them, write the checks that would have caught them, and explain the rebuild order after the fix.

## Resources
- *Fundamentals of Data Engineering* · pandera docs · Airflow concepts docs · Foundry docs: data health

## Gaps found
-

## Notes
-

## Work
[`work/`](work)
