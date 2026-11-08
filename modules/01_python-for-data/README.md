# Module 01 · Python for data

**Roles:** DE · DA · DS · **Size:** 1 weekend (fast track if the diagnostic says so) · **Priority:** P0 · **Builds:** Aerolisa M1 (MVP engine health slice)

## Why this matters
Python is on every Skywise posting, usually as "Python, PySpark, SQL". Interviewers check that I write clean, tested code, not notebooks full of copy-paste. Foundry Code Repositories are plain Python packages with decorators, so the habits here carry straight into Foundry.

## 🎯 Apprenticeship level (must)
- [ ] Core: types, functions, comprehensions, `dataclasses`, `pathlib`, exceptions, `logging`, f-strings, type hints
- [ ] Decorators (how `@something` wraps a function): needed for Foundry-style transforms
- [ ] Modules and packages, `pyproject.toml`, virtual environments, editable installs
- [ ] pandas: read CSV / text / Parquet, dtypes, `loc`/`iloc`, filtering, `groupby` + `agg`, `merge`, `pivot_table`, `melt`, datetimes, missing values, method chaining
- [ ] NumPy: arrays, vectorization, broadcasting, why loops are slow
- [ ] Plotting: matplotlib basics, Plotly express for the app
- [ ] pytest: tests, fixtures, parametrize, testing a data function with a tiny DataFrame
- [ ] Git: branches, commits, pull requests, merge conflicts
- [ ] Algorithms that data work actually uses: Big-O intuition, dict/set lookups, sorting, two pointers, BFS, **topological sort** (pipeline dependencies)

## 🚀 Pro level
- [ ] Generators and iterators, context managers, `functools`
- [ ] Polars basics and when it beats pandas
- [ ] Profiling (`cProfile`, `line_profiler`), memory with `pandas.DataFrame.memory_usage`
- [ ] 20 LeetCode Easy/Medium on arrays, hash maps, strings, graphs

## Steps
1. **Learn (Saturday AM).** *Python for Data Analysis* chapters on pandas essentials, data loading, data cleaning, group operations. Skim what I know, slow down on what I don't.
2. **Practice (Saturday PM)** in `work/`:
   - Write `load_cmapss(path) -> DataFrame` that names the 26 columns (unit, cycle, 3 settings, 21 sensors) and sets dtypes; test it on a 10-line sample.
   - Write `add_rul(df, clip=None)` that adds the remaining-useful-life label per unit, optionally clipped; test with a hand-computed example.
   - Write a small decorator `@timed` that logs a function's duration.
   - Implement topological sort on a dict of dependencies; test it, including a cycle that must raise.
3. **Apply in Aerolisa (Sunday):** M1 steps 1–3 (ingest, clean, RUL label), reusing these functions properly inside `src/aerolisa/`.

## Exit test (60 min, no AI, docs allowed)
From a raw C-MAPSS file: load, name columns, drop constant sensors, add clipped RUL, compute per-unit lifetime statistics, plot 3 sensors for one unit, all as tested functions, pushed with CI green.

## Resources
- *Python for Data Analysis* (free online) · pandas user guide · pytest docs · Missing Semester (Git lecture)

## Gaps found
-

## Notes
-

## Work
[`work/`](work)
