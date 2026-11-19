"""C-MAPSS: raw files -> bronze -> silver -> gold, with data expectations on every output.

Foundry concepts practised here: file-based transform (``filesystem()``), ``@transform_df``,
``Input``/``Output``, data expectations (``Check`` + ``E``), Spark window functions.
"""

from pyspark.sql import functions as F
from transforms import expectations as E
from transforms.api import Check, Input, Output, transform, transform_df

from aerolisa_pipelines import paths
from aerolisa_pipelines.logic import cmapss as L

PK = "Primary key"


# ---------------------------------------------------------------- bronze
@transform(
    out=Output(paths.BRONZE_CMAPSS_RAW, checks=[
        Check(E.col("unit").non_null(), "unit not null", on_error="FAIL"),
        Check(E.col("cycle").gte(1), "cycle >= 1", on_error="FAIL"),
    ]),
    files=Input(paths.RAW_CMAPSS_FILES),
)
def bronze_cmapss_raw(ctx, out, files):
    """Parse every uploaded ``train_FD00x.txt`` / ``test_FD00x.txt`` file as received."""
    fs = files.filesystem()
    rows = []
    for f in fs.ls(glob="*_FD00*.txt"):
        name = f.path.split("/")[-1]
        if name.startswith("RUL_"):
            continue
        with fs.open(f.path, "r") as fh:
            rows.extend(r for r in (L.parse_cycle_line(line, name) for line in fh) if r is not None)
    df = ctx.spark_session.createDataFrame(rows, L.RAW_SCHEMA)
    out.write_dataframe(df.withColumn("ingested_at", F.current_timestamp()))


@transform(
    out=Output(paths.BRONZE_CMAPSS_RUL, checks=[
        Check(E.primary_key("unit", "source_file"), PK, on_error="FAIL"),
        Check(E.col("rul_at_cutoff").gte(0), "RUL >= 0", on_error="FAIL"),
    ]),
    files=Input(paths.RAW_CMAPSS_FILES),
)
def bronze_cmapss_rul(ctx, out, files):
    fs = files.filesystem()
    rows = []
    for f in fs.ls(glob="RUL_FD00*.txt"):
        name = f.path.split("/")[-1]
        with fs.open(f.path, "r") as fh:
            values = [int(line.split()[0]) for line in fh if line.strip()]
        rows.extend((i + 1, v, name) for i, v in enumerate(values))
    out.write_dataframe(ctx.spark_session.createDataFrame(rows, L.RUL_SCHEMA))


# ---------------------------------------------------------------- silver
@transform_df(
    Output(paths.SILVER_CMAPSS_CYCLES, checks=[
        Check(E.primary_key("cycle_id"), PK, on_error="FAIL"),
        Check(E.col("split").is_in("train", "test"), "split is train/test", on_error="FAIL"),
        Check(E.col("sensor_11").non_null(), "key sensor present", on_error="WARN"),
    ]),
    bronze=Input(paths.BRONZE_CMAPSS_RAW),
)
def silver_cmapss_cycles(bronze):
    return L.silver_cycles(bronze)


# ---------------------------------------------------------------- gold
@transform_df(
    Output(paths.GOLD_ENGINE_CYCLE_FEATURES, checks=[
        Check(E.primary_key("cycle_id"), PK, on_error="FAIL"),
        Check(E.col("rul").gte(0), "RUL >= 0", on_error="FAIL"),
        Check(E.col("rul_capped").lte(L.RUL_CAP), "RUL cap applied", on_error="FAIL"),
    ]),
    cycles=Input(paths.SILVER_CMAPSS_CYCLES),
    rul=Input(paths.BRONZE_CMAPSS_RUL),
)
def gold_engine_cycle_features(cycles, rul):
    # one subset at a time keeps 'unit' unambiguous in the RUL join
    fd001 = cycles.filter("subset = 'FD001'")
    rul_fd001 = rul.filter("source_file = 'RUL_FD001.txt'")
    return L.temporal_features(L.rul_labels(fd001, rul_fd001))


@transform_df(
    Output(paths.GOLD_ENGINE_LIFE_RECORDS, checks=Check(E.primary_key("engine_id"), PK, on_error="FAIL")),
    cycles=Input(paths.SILVER_CMAPSS_CYCLES),
)
def gold_engine_life_records(cycles):
    return L.life_records(cycles)
