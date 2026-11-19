# Contributing

Aerolisa is a personal project, but it follows team conventions on purpose: it's how industrial data teams work.

## Workflow
1. One issue per roadmap step (template: *Milestone step*).
2. Branch from `main`: `feat/m2-build-runner`, `fix/opensky-time-window`, `docs/ontology`.
3. Commit with [Conventional Commits](https://www.conventionalcommits.org): `feat(fleet): cycles per airframe per day`.
4. Pull request with the template; CI green before merging; `main` always demoable.
5. Tag each milestone (`v0.1.0` …) and update `CHANGELOG.md`.

## Rules
- **Dependency rule** from [docs/architecture.md](docs/architecture.md); cross-component imports are absolute (`from aerolisa.core …`). Enforced by `tests/test_architecture.py`.
- **Transforms are pure** functions declared with `@transform`; no I/O inside them.
- **Every dataset** is in the catalog with a primary key and at least one quality check.
- **Every feature** ships with tests (local twin) and, for PySpark, tests in the Foundry repository.
- **One source of truth:** edit `src/aerolisa`, then `make sync` to update `foundry/ml-repo/src/aerolisa` (CI fails otherwise).
- **Notebooks** are for exploration; reusable code moves to `src/`.
- **No secrets, no employer data, no files over 1 MB** in Git except the public NASA C-MAPSS FD001 files (pre-commit enforces it).

## Setup
```bash
make install
pre-commit install
make test
make build
```
