# ADR 0005: Local lakehouse on Parquet + DuckDB

**Status:** accepted (replaces the earlier PostgreSQL-centred design)

**Context:** one developer, weekend sessions, zero budget. Foundry stores datasets as files processed by Spark; analytics need SQL. A PostgreSQL server plus Airflow from day one adds infrastructure without adding skills recruiters ask for.

**Decision:** datasets are Parquet files in `data/{bronze,silver,gold,objects,writeback}/`; DuckDB serves SQL over gold and object tables; PySpark runs transforms in local mode. PostgreSQL and Airflow are optional later (M9 🚀).

**Consequences:** nothing to install beyond Python and Java; the layout matches how Foundry datasets behave; SQL practice runs on the same data. Concurrent writes and access control are out of scope (documented as such).
