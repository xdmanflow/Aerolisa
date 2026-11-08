# Airflow DAGs (optional, M9 🚀)

The default scheduler is a GitHub Actions scheduled workflow calling `aerolisa refresh` and `aerolisa build` (M9 step 5). Airflow is an optional extra to practise the most common orchestrator in data engineering postings.

If done: one DAG per source (`opensky_daily`, `eurocontrol_monthly`, `airbus_od_monthly`), each task calling the CLI. Logic stays in `aerolisa.pipelines`; DAG files only orchestrate.
