# Module 04 · PySpark

**Roles:** DE · DS · **Size:** 2 weekends · **Priority:** P0 · **Builds:** Aerolisa M2 (transforms in PySpark)

## Why this matters
Skywise is built on Spark: the postings describe it as a big data landscape "developed on the Spark framework" and ask for PySpark at a high level. Foundry Code Repositories transforms are PySpark DataFrame code. This is the single most valuable technical skill for a Skywise apprentice after SQL.

## 🎯 Apprenticeship level (must)
- [ ] Architecture: driver, executors, partitions, tasks, stages; lazy evaluation; transformations vs actions
- [ ] DataFrame API: `select`, `withColumn`, `filter`, `groupBy().agg()`, `join` (all types), `union`, `distinct`, `orderBy`
- [ ] `pyspark.sql.functions`: `col`, `when`, `coalesce`, date functions, string functions, `explode`, arrays and structs
- [ ] Window functions in PySpark (`Window.partitionBy().orderBy()`, `lag`, `row_number`, rolling frames)
- [ ] Spark SQL on temp views
- [ ] Schemas: explicit `StructType`, schema enforcement, nullability
- [ ] Reading/writing Parquet, partitioned writes, overwrite vs append
- [ ] Why built-in functions beat Python UDFs; pandas UDFs when needed
- [ ] Shuffles, broadcast joins, `cache`/`persist`, reading `explain()` at a basic level
- [ ] Testing transforms with a local `SparkSession` fixture in pytest

## 🚀 Pro level
- [ ] Data skew and salting; adaptive query execution
- [ ] Partition sizing, file compaction
- [ ] Structured Streaming concepts
- [ ] Delta Lake locally

## Steps
**Weekend 1: the API**
1. Learn: Spark docs "Getting started" and "Spark SQL, DataFrames" guide; *Learning Spark* chapters on the DataFrame API (or the Data Engineering Zoomcamp Spark module).
2. Practice: rewrite the module 01 functions (`load_cmapss`, `add_rul`, rolling sensor means per unit) in PySpark, with pytest + a local SparkSession fixture.
3. Apply: Aerolisa M2 step "port the C-MAPSS transforms to PySpark".

**Weekend 2: performance and patterns**
4. Learn: Spark tuning guide (joins, caching, partitions); Palantir Learn *Spark Optimization* video when I have Foundry access.
5. Practice: one broadcast vs shuffle join comparison with `explain()`; gaps-and-islands with windows (same as module 02, now in PySpark).
6. Apply: reference data transforms (airports, aircraft database) and the first flights transform in Aerolisa.

## Exit test (60 min, no AI, docs allowed)
Rewrite 5 pandas transforms in PySpark with tests; explain the physical plan of one join and how I'd make it cheaper.

## Resources
- Spark docs · *Learning Spark*, 2nd ed. · Data Engineering Zoomcamp (Spark module)

## Gaps found
-

## Notes
Setup: PySpark needs Java 17. `pip install pyspark` inside the venv.

## Work
[`work/`](work)
