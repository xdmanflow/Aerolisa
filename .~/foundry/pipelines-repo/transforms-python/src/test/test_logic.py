"""Unit tests for the PySpark logic. In Foundry Code Repositories, pytest provides a
``spark_session`` fixture; run them with the "Tests" check on every branch/PR."""

import pytest
from aerolisa_pipelines.logic import cmapss as L
from pyspark.sql import Row


def _bronze(spark, n=40, unit=1, source="train_FD001.txt"):
    rows = []
    for c in range(1, n + 1):
        sensors = [float(c) if s == "sensor_11" else 1.0 for s in L.SENSORS]
        rows.append((unit, c, 0.0, 0.0, 100.0, *sensors, source))
    return spark.createDataFrame(rows, L.RAW_SCHEMA)


def test_parse_cycle_line():
    line = "1 2 " + " ".join(["0.5"] * 24)
    t = L.parse_cycle_line(line, "train_FD001.txt")
    assert t[0] == 1 and t[1] == 2 and len(t) == 27
    assert L.parse_cycle_line("   ", "x") is None


def test_silver_keys(spark_session):
    s = L.silver_cycles(_bronze(spark_session))
    first = s.orderBy("cycle").first()
    assert first["engine_id"] == "FD001-HIST-001"
    assert first["cycle_id"] == "FD001-HIST-001-001"
    assert s.select("cycle_id").distinct().count() == s.count()


def test_rul_labels_train_and_test(spark_session):
    train = L.silver_cycles(_bronze(spark_session, n=10))
    test = L.silver_cycles(_bronze(spark_session, n=5, source="test_FD001.txt"))
    rul = spark_session.createDataFrame([Row(unit=1, rul_at_cutoff=7, source_file="RUL_FD001.txt")])
    out = {(r["split"], r["cycle"]): r["rul"] for r in L.rul_labels(train.unionByName(test), rul).collect()}
    assert out[("train", 10)] == 0 and out[("train", 1)] == 9
    assert out[("test", 5)] == 7 and out[("test", 1)] == 11


def test_temporal_features_slope(spark_session):
    df = L.silver_cycles(_bronze(spark_session, n=40))
    f = L.temporal_features(df, sensors=["sensor_11"], window=30).orderBy("cycle").collect()
    assert f[0]["sensor_11_std"] == 0.0 and f[0]["sensor_11_slope"] == 0.0   # single-cycle window
    assert f[-1]["sensor_11_slope"] == pytest.approx(1.0)                     # sensor_11 == cycle
    assert f[-1]["sensor_11_mean"] == pytest.approx(sum(range(11, 41)) / 30)  # last 30 cycles only
