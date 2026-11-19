"""PySpark joins that build the ontology backing datasets (twin: ``src/aerolisa/cli/graph.py``)."""

from __future__ import annotations

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def utilization_stats(util: DataFrame, window_days: int = 30) -> DataFrame:
    """Mean cycles/day over the last ``window_days`` + normal-approximation 95 % CI."""
    d = util.withColumn("date", F.to_date("date"))
    max_date = d.agg(F.max("date").alias("m")).collect()[0]["m"]
    recent = d.filter(F.col("date") >= F.date_sub(F.lit(max_date), window_days - 1))
    g = recent.groupBy("tail_id").agg(F.avg("cycles").alias("cpd"), F.stddev_samp("cycles").alias("sd"), F.count("*").alias("n"))
    half = F.lit(1.96) * F.col("sd") / F.sqrt("n")
    return g.select(
        "tail_id",
        F.round("cpd", 2).alias("cycles_per_day"),
        F.round(F.greatest(F.col("cpd") - half, F.lit(0.0)), 2).alias("cycles_per_day_lo"),
        F.round(F.col("cpd") + half, 2).alias("cycles_per_day_hi"),
    )


def engine_objects(assignment: DataFrame, snapshot: DataFrame, rec: DataFrame) -> DataFrame:
    latest = snapshot.filter(F.col("is_latest")).select("engine_id", F.col("cycle").alias("current_cycle"))
    r = rec.select("engine_id", "rank", "band", "alert", "risk_before_check", "rul_p10", "rul_p50", "rul_p90",
                   "health_index", "anomaly_score", "top_drivers", "model_version")
    return assignment.join(latest, "engine_id").join(r, "engine_id")


def aircraft_objects(aircraft: DataFrame, util: DataFrame, rec: DataFrame) -> DataFrame:
    worst = rec.groupBy("tail_id").agg(
        F.max("risk_before_check").alias("worst_engine_risk"),
        F.sum(F.when(F.col("band") == "RED", 1).otherwise(0)).cast("int").alias("engines_in_red"),
    )
    return aircraft.join(utilization_stats(util), "tail_id").join(worst, "tail_id")


def operator_objects(aircraft: DataFrame) -> DataFrame:
    return aircraft.groupBy("operator_code", "operator_name").agg(F.count("*").alias("fleet_size")).withColumn("simulated", F.lit(True))


def latest_per_engine(df: DataFrame, order_col: str = "cycle") -> DataFrame:
    w = Window.partitionBy("engine_id").orderBy(F.col(order_col).desc())
    return df.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")
