# CLI

> The command-line entry point of the platform: build datasets, run quality checks, draw lineage, refresh sources.

**Milestone:** M2 (first commands) · grows with each milestone
**May import:** anything in Aerolisa
**Learn:** Renaissance 01 (packaging), 05

## Planned commands

| Command | Does | Milestone |
|---|---|---|
| `aerolisa build <dataset>` | Builds a dataset and whatever it depends on, in topological order | M2 |
| `aerolisa build --all` | Rebuilds everything | M2 |
| `aerolisa quality [<dataset>]` | Runs checks, writes the report | M2 |
| `aerolisa lineage` | Writes `docs/lineage.md` (Mermaid) | M2 |
| `aerolisa catalog` | Lists datasets with layer, owner, last build | M2 |
| `aerolisa refresh opensky --days N` | Fetches missing days within the credit budget | M5 |
| `aerolisa ontology docs` | Generates `docs/ontology-reference.md` | M3 |

## Steps
1. [ ] `argparse` (or Typer) app with `build`, `quality`, `lineage`, `catalog`
2. [ ] Enable the `[project.scripts]` entry in `pyproject.toml`
3. [ ] Tests for argument parsing and one end-to-end build on sample data
4. [ ] README usage example (30 seconds to understand)

## Definition of done
- [ ] Every command tested
- [ ] Used by the Makefile and the scheduled workflow
