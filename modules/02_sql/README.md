# Module 02 · SQL

**Roles:** DE · DA · DS · **Size:** 3 weekends · **Priority:** P0 · **Builds:** Aerolisa M2 (gold layer), `sql/` folder, M8

## Why this matters
SQL is the most tested skill in data interviews, and Skywise postings list it next to PySpark. In Foundry, SQL shows up in Pipeline Builder expressions, Contour and SQL transforms. A data analyst apprentice who writes window functions fluently is rare and remembered.

## 🎯 Apprenticeship level (must)
- [ ] `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, aliases
- [ ] Aggregates, `GROUP BY`, `HAVING`; `COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)`
- [ ] Joins: inner, left, right, full, self-join, anti-join (`LEFT JOIN … WHERE b.id IS NULL`, `NOT EXISTS`), join fan-out traps
- [ ] Subqueries (scalar, `IN`, correlated) and CTEs (`WITH`)
- [ ] Window functions: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`/`LEAD`, `SUM() OVER` running totals, moving averages with frames, `NTILE`, `FIRST_VALUE`
- [ ] `CASE WHEN`, `COALESCE`, `NULL` logic (three-valued), date/time functions, string functions
- [ ] Set operations: `UNION` vs `UNION ALL`, `INTERSECT`, `EXCEPT`
- [ ] Classic patterns: deduplication (latest record per key), top-N per group, gaps-and-islands, year-over-year, cohort/retention, pivot with `CASE`
- [ ] Reading a query plan at a basic level; what an index is and when it helps
- [ ] DuckDB (local analytics) and PostgreSQL (classic database) both used at least once

## 🚀 Pro level
- [ ] Recursive CTEs (e.g. aircraft → engine → module hierarchies)
- [ ] `MERGE` / upserts, slowly changing dimension type 2 in SQL
- [ ] Query optimization: predicate pushdown, partition pruning, avoiding `SELECT *` on wide tables
- [ ] Spark SQL differences
- [ ] 30 DataLemur medium/hard questions

## Steps
**Weekend 1: foundations**
1. Learn: SQLBolt lessons 1–18 (fast), then the PostgreSQL docs chapter on joins and aggregates.
2. Practice: LeetCode SQL 50, first half. Save each solution as `work/leetcode/NNN_name.sql` with one comment line: the trick.
3. Apply: load C-MAPSS gold tables into DuckDB (Aerolisa M2 step) and write 10 questions + queries in Aerolisa `sql/` ("which units fail earliest?", "average lifetime per fault mode", …).

**Weekend 2: windows and patterns**
4. Learn: PostgreSQL docs on window functions; one article each on gaps-and-islands and top-N per group.
5. Practice: LeetCode SQL 50, second half + 10 DataLemur window-function questions.
6. Apply: on flight-like data (start with a synthetic sample if OpenSky data isn't there yet), detect consecutive "airborne" rows as one flight with gaps-and-islands. This is the logic Aerolisa M5 needs.

**Weekend 3: speed and explanation**
7. Practice timed: 3 sessions of 5 problems in 45 minutes. Say the approach out loud before typing (that's what an interview looks like).
8. Apply: finish 20 documented queries in Aerolisa `sql/`, each with the business question, the query, and a one-line result.

## Exit test (45 min, no AI, no docs)
5 problems: one join + aggregate, one top-N per group, one running total, one gaps-and-islands, one "find the bug" in a wrong query. Then explain one solution out loud in 2 minutes.

## Resources
- SQLBolt · LeetCode SQL 50 · DataLemur · PostgreSQL docs · DuckDB docs

## Gaps found
-

## Notes
-

## Work
[`work/`](work)
