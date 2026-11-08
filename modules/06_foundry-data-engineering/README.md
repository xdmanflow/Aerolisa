# Module 06 · Foundry I: data engineering

**Roles:** DE · DA · **Size:** 3 weekends · **Priority:** P0 · **Builds:** Aerolisa M4 (Foundry edition, data part)

## Why this matters
Skywise **is** Palantir Foundry with Airbus data and applications on top. Airbus Skywise postings list "Code Repository, Pipeline Builder, Access management, Ontology, Object Explorer, Workshop, Templates, Marketplace, Quiver, Slate". Most apprentices arrive having never touched Foundry; arriving with a real build on it, on aviation data, is my biggest differentiator.

Access: the free **Developer Tier** (build.palantir.com) gives a real Foundry/AIP environment. Full tool map and course list: [palantir/README.md](../../palantir/README.md).

## 🎯 Apprenticeship level (must)
- [ ] Platform model: projects, folders, resources, permissions; what Compass is
- [ ] Datasets: files vs tabular, schemas, **transactions** (snapshot, append, update, delete), views, branches
- [ ] Data Connection: sources, syncs, uploading files; agents (concept)
- [ ] **Pipeline Builder:** inputs, transforms, joins, unions, expressions, outputs to datasets and objects, previews, deploy
- [ ] **Code Repositories:** Python transforms with `transforms.api` (`@transform_df`, `@transform`, `Input`, `Output`), PySpark inside, unit tests, branches, pull requests, checks, build
- [ ] Incremental transforms (concept + one example)
- [ ] Builds and **schedules**; what triggers a rebuild; build failures and how to read logs
- [ ] **Data Lineage** app: navigating upstream/downstream, finding the cause of a broken dataset
- [ ] **Data expectations** in transforms and **health checks** in Data Health; alerting on failures
- [ ] Code Workbook / Code Workspaces (awareness: notebook-style exploration)
- [ ] Explaining the difference between Pipeline Builder and Code Repositories, and when to use each

## 🚀 Pro level
- [ ] Spark optimization in Foundry (Palantir Learn video), transform profiles
- [ ] Media sets (documents, images) for later RAG work
- [ ] Marketplace: packaging a pipeline as a product (if available on Developer Tier)
- [ ] Data Engineer certification exam guide fully covered

## Steps
**Weekend 1: orientation and first pipeline**
1. Learn: Palantir Learn *Foundry & AIP Aware* path (start), *Deep Dive: Creating Your First Data Connection*, *Deep Dive: Building Your First Pipeline*. Commute: Foundry docs overview pages.
2. Practice: upload C-MAPSS FD001 raw files to a Developer Tier project; build the cleaning pipeline in **Pipeline Builder** (column names, types, RUL label).
3. Apply: Aerolisa M4 steps 1–3.

**Weekend 2: code**
4. Learn: *Deep Dive: Transforming your data with Code Repositories*; Data Engineer track courses on scheduling and data expectations.
5. Practice: re-implement the same cleaning as a **Python transform** in a Code Repository; add unit tests and expectations (primary key, non-null, ranges); open and merge a PR on a branch.
6. Apply: Aerolisa M4 steps 4–6. Compare the Foundry transform with Aerolisa's local `@transform` structure; write the comparison in `foundry/README.md`.

**Weekend 3: operate**
7. Learn: *Pipeline Management* video; Data Lineage and Data Health docs.
8. Practice: schedule the pipeline; break an input on purpose; find the failure in lineage; fix it; confirm the health check alerts.
9. Apply: Aerolisa M4 step 7 (screenshots + notes), then take the Data Engineer associate quiz on Palantir Learn.

## Exit test (2 h, no AI, docs allowed)
In a fresh Foundry project, from raw C-MAPSS upload to a scheduled, tested, expectation-checked clean dataset, without following a tutorial. Then a 10-minute verbal: datasets & transactions, Pipeline Builder vs Code Repositories, how I'd debug a failed build.

## Resources
- Palantir Learn (Data Engineer track) · Foundry docs (Data integration, Transforms) · Palantir Community

## Gaps found
-

## Notes
Never upload anything non-public (no ALTEN data, no personal data) to the Developer Tier. Check the Developer Tier terms before publishing screenshots or videos.

## Work
[`work/`](work)
