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
- **Every feature** ships with tests that run on `sample_data/`.
- **Notebooks** are for exploration; reusable code moves to `src/`.
- **No raw data, secrets or files over 1 MB** in Git (pre-commit enforces it). OpenSky, Eurocontrol and Airbus samples are synthetic.
- **First version of the code written without AI**; AI is used for review.

## Setup
```bash
make install
pre-commit install
make test
```
