# SQL analyses

Documented queries run with DuckDB over the gold and object tables. Learn: Renaissance module 02.

## Format
One file per question: `NNN_short_name.sql`, starting with:

```sql
-- Question: which fault mode shortens engine life the most?
-- Datasets: silver/cmapss_cycles
-- Technique: GROUP BY + window function
-- Result (one line, filled after running):
```

Run: `duckdb data/aerolisa.duckdb < sql/NNN_short_name.sql`

## Catalog

| # | Question | Technique | Milestone |
|---|---|---|---|
| 001 | | | M2 |

Targets: 10 queries at M2 (engines), 10 more at M8 (operations and market), including running totals, top-N per group, year-over-year, and gaps-and-islands.
