# Module 07 · Foundry II: ontology, apps & analytics

**Roles:** DE · DA · AI · **Size:** 3 weekends · **Priority:** P0 · **Builds:** Aerolisa M3 (ontology, local), M4 (Foundry edition, ontology + app)

## Why this matters
The Ontology is what makes Foundry more than a data lake: real-world objects (aircraft, engines, work orders), their links, and the **actions** people take on them. Skywise teams "expand the business ontology and craft intuitive tools" for business users, in **Workshop**, with logic in **TypeScript** Functions. Airbus lead roles rate "Foundry Ontology / Workshop / Slate" and TypeScript explicitly.

## 🎯 Apprenticeship level (must)
- [ ] **Ontology Manager:** object types, backing datasets, properties, primary key, title property, property types (incl. time series), object type groups
- [ ] **Link types:** foreign-key links, many-to-many via join datasets
- [ ] **Action types:** parameters, rules (create / modify / delete objects), submission criteria, writeback, side effects; why actions capture decisions in the data
- [ ] **Object Explorer:** search, filter, explore links, saved explorations
- [ ] **Workshop:** layouts, sections, widgets (object table, object view, filter list, charts, metric cards, button group), variables, events, action buttons
- [ ] **TypeScript** basics: types, interfaces, functions, `async`/`await`, arrays and maps
- [ ] **Functions on objects** (TypeScript, and Python where available): read objects, traverse links, compute a value; ontology edit functions behind actions
- [ ] **Contour:** analysis paths, boards, joins, aggregations on datasets
- [ ] **Quiver:** time series and object analysis (Airbus uses it on large-scale sensor data)
- [ ] Notepad / reports (sharing an analysis)
- [ ] Awareness: Slate (custom HTML/JS apps, still in Airbus postings), Fusion (spreadsheets), Vertex (graphs), Map, Machinery (process mining), OSDK (building external apps on the ontology), Marketplace, templates

## 🚀 Pro level
- [ ] OSDK: a tiny TypeScript or Python app reading Aerolisa objects from outside Foundry
- [ ] Slate: one small page
- [ ] Application Developer exam guide fully covered
- [ ] Speedrun: *Mining Your First Business Process*

## Steps
**Weekend 1: ontology**
1. Learn: *Deep Dive: Creating Your First Ontology*, Ontology docs (object types, links, actions); TypeScript handbook "basics" + "everyday types" (commute).
2. Practice: in Foundry, create object types **Engine**, **EngineCycle** (or time series property), **EngineHealthSnapshot** backed by the module 06 datasets; links between them; explore in Object Explorer.
3. Apply: Aerolisa M3 (local ontology in YAML + Pydantic, mirroring the Foundry design) and M4 step 8.

**Weekend 2: applications**
4. Learn: *Deep Dive: Building Your First Application*, the Workshop video course, *Speedrun: Your First Ontology Function*.
5. Practice: Workshop app "Engine watchlist": table of engines sorted by risk, engine detail view, sensor chart; an action type **Schedule inspection** with a writeback; a TypeScript function computing a simple risk score.
6. Apply: Aerolisa M4 steps 9–10.

**Weekend 3: analysis**
7. Learn: *Deep Dive: Data Analysis in Contour*, *Deep Dive: Data Analysis in Quiver*.
8. Practice: Contour analysis (lifetime per fault mode); Quiver analysis comparing sensor trends of a healthy vs degrading engine.
9. Apply: Aerolisa M4 steps 11–12 (screenshots, 2-minute video), then the Application Developer track quiz/badge if available.

## Exit test (3 h, no AI, docs allowed)
From existing datasets: an ontology with 3 object types and 2 links, a Workshop app with a working action and a TypeScript function, and one Quiver analysis. Then a 10-minute verbal: ontology vs tables, what an action type is for, how I'd design Skywise-style "inspect first" tooling for a reliability engineer.

## Resources
- Palantir Learn (Application Developer and Data Analyst tracks) · Foundry docs (Ontology, Workshop, Functions) · TypeScript handbook

## Gaps found
-

## Notes
-

## Work
[`work/`](work)
