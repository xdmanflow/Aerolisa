# Changelog

All notable changes are documented here. Format: [Keep a Changelog](https://keepachangelog.com), versions follow [Semantic Versioning](https://semver.org).

## [Unreleased]

### Changed
- Project refocused on one flagship question: which engines to inspect first, why, and what happens if we wait.
- Roadmap rebuilt as twelve milestones (M0–M11) without dates; M1 is an end-to-end slice with a live demo.
- Storage moved to a local lakehouse (Parquet + DuckDB) with Foundry-style transforms; PostgreSQL and Airflow made optional.
- `modules/market` and `modules/operations` merged into `analytics`; `modules/` flattened into top-level components.
- `dashboard/` replaced by `app/`, a Workshop-like operational app with actions.

### Added
- Foundry edition (`foundry/`) as milestone M4.
- Ontology action types and writeback design; ontology design v1.
- Skywise & Foundry mapping, case study, model card and demo script templates.
- ADRs 0004 (vertical slices), 0005 (local lakehouse), 0006 (Foundry-style transforms).
- Architecture test enforcing the dependency rule.

### Removed
- Trajectory optimization module (moved to the roadmap's parking lot).
- Standalone source-catalog CLI mini-project (the CLI is now the platform's build tool).

## Planned releases
- **0.1.0** M1 MVP engine health slice · **0.2.0** M2 data platform · **0.3.0** M3 ontology · **0.4.0** M4 Foundry edition · **0.5.0** M5 fleet · **0.6.0** M6 engine health v2 · **0.7.0** M7 planner & app · **0.8.0** M8 analytics · **0.9.0** M9 industrialization · **1.0.0** M10 copilot
