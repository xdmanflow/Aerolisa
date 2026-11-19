"""Pure PySpark logic (no Foundry imports): DataFrames in, DataFrames out.

Each function mirrors a pandas function of the local twin (``src/aerolisa``) and must
produce the same columns. Unit tests: ``src/test/test_logic.py`` (Foundry's
``spark_session`` fixture). Keeping logic free of ``transforms.api`` is what makes it
testable and reusable.
"""

from __future__ import annotations

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F
from pyspark.sql import types as T

OP_SETTINGS = ["op1", "op2", "op3"]
SENSORS = [f"sensor_{i}" for i in range(1, 22)]
RAW_COLUMNS = ["unit", "cycle", *OP_SETTINGS, *SENSORS]
DROPPED_SENSORS = ["sensor_1", "sensor_5", "sensor_10", "sensor_16", "sensor_18", "sensor_19"]
INFORMATIVE_SENSORS = [s for s in SENSORS if s not in DROPPED_SENSORS]
RUL_CAP = 125
WINDOW = 30

RAW_SCHEMA = T.StructType(
    [T.StructField("unit", T.IntegerType(), False), T.StructField("cycle", T.IntegerType(), False)]
    + [T.StructField(c, T.DoubleType(), True) for c in OP_SETTINGS + SENSORS]
    + [T.StructField("source_file", T.StringType(), False)]
)
RUL_SCHEMA = T.StructType([
    T.StructField("unit", T.IntegerType(), False),
    T.StructField("rul_at_cutoff", T.IntegerType(), False),
    T.StructField("source_file", T.StringType(), False),
])


def parse_cycle_line(line: str, source_file: str):
    """One whitespace-separated C-MAPSS line -> tuple matching RAW_SCHEMA (None for blank lines)."""
    vals = line.split()
    if not vals:
        return None
    return (int(vals[0]), int(vals[1]), *[float(v) for v in vals[2:26]], source_file)


def silver_cycles(bronze: DataFrame) -> DataFrame:
    """Typed, keyed, one row per engine-cycle. ``engine_id`` e.g. FD001-FLEET-007."""
    subset = F.regexp_extract("source_file", r"(FD00\d)", 1)
    split = F.when(F.col("source_file").startswith("train"), F.lit("train")).otherwise(F.lit("test"))
    role = F.when(split == "train", F.lit("HIST")).otherwise(F.lit("FLEET"))
    engine_id = F.concat_ws("-", subset, role, F.lpad(F.col("unit").cast("string"), 3, "0"))
    df = bronze.select(
        engine_id.alias("engine_id"), subset.alias("subset"), split.alias("split"),
        F.col("unit").cast("int").alias("unit"), F.col("cycle").cast("int").alias("cycle"),
        *[F.col(c).cast("double").alias(c) for c in OP_SETTINGS + SENSORS],
    )
    cycle_id = F.concat_ws("-", "engine_id", F.lpad(F.col("cycle").cast("string"), 3, "0"))
    return df.select(cycle_id.alias("cycle_id"), *df.columns)


def rul_labels(cycles: DataFrame, rul: DataFrame) -> DataFrame:
    """train: last - cycle; test: last - cycle + RUL at cut-off (NASA ground truth)."""
    by_engine = Window.partitionBy("engine_id")
    df = cycles.withColumn("_last", F.max("cycle").over(by_engine))
    df = df.join(rul.select("unit", "rul_at_cutoff"), on="unit", how="left")
    base = F.col("_last") - F.col("cycle")
    df = df.withColumn("rul", F.when(F.col("split") == "test", base + F.col("rul_at_cutoff")).otherwise(base).cast("int"))
    df = df.withColumn("rul_capped", F.least(F.col("rul"), F.lit(RUL_CAP)))
    df = df.withColumn("failure_cycle", (F.col("cycle") + F.col("rul")).cast("int"))
    return df.drop("_last", "rul_at_cutoff")


def temporal_features(df: DataFrame, sensors: list[str] = INFORMATIVE_SENSORS, window: int = WINDOW) -> DataFrame:
    """Causal rolling mean / std / slope over the last ``window`` cycles of each engine.

    slope = covar_samp(x, cycle) / var_samp(cycle) over the window (least-squares slope).
    std and slope are 0 when the window holds a single cycle (pandas twin: fillna(0)).
    """
    w = Window.partitionBy("engine_id").orderBy("cycle").rowsBetween(-(window - 1), 0)
    cyc = F.col("cycle").cast("double")
    var_c = F.var_samp(cyc).over(w)
    feats = []
    for s in sensors:
        feats.append(F.avg(s).over(w).alias(f"{s}_mean"))
        feats.append(F.coalesce(F.stddev_samp(s).over(w), F.lit(0.0)).alias(f"{s}_std"))
        feats.append(F.coalesce(F.covar_samp(F.col(s), cyc).over(w) / var_c, F.lit(0.0)).alias(f"{s}_slope"))
    return df.select("*", *feats)


def life_records(cycles: DataFrame) -> DataFrame:
    g = cycles.groupBy("engine_id", "split").agg(F.max("cycle").alias("observed_cycles"))
    failed = F.col("split") == "train"
    return g.select(
        "engine_id", "observed_cycles", failed.alias("failed"),
        F.when(failed, "run-to-failure history").otherwise("in service (right-censored)").alias("role"),
    )
