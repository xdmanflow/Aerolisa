import numpy as np

from aerolisa.core.schema import RUL_CAP
from aerolisa.engine_health.features import feature_columns, last_cycle, truncation_sample, validation_engines


def test_shapes_and_keys(gold):
    assert len(gold) == 20631 + 13096
    assert gold["cycle_id"].is_unique
    assert gold.groupby("split")["engine_id"].nunique().to_dict() == {"test": 100, "train": 100}


def test_rul_labels(gold):
    hist1 = gold[gold["engine_id"] == "FD001-HIST-001"]
    assert hist1["rul"].iloc[-1] == 0 and hist1["rul"].iloc[0] == len(hist1) - 1
    fleet1 = gold[gold["engine_id"] == "FD001-FLEET-001"]
    assert fleet1["rul"].iloc[-1] == 112            # first line of RUL_FD001.txt
    assert gold["rul_capped"].max() == RUL_CAP


def test_slope_matches_polyfit(gold):
    e = gold[gold["engine_id"] == "FD001-HIST-007"]
    w = e.iloc[-30:]
    assert np.isclose(e["sensor_11_slope"].iloc[-1], np.polyfit(w["cycle"], w["sensor_11"], 1)[0])


def test_features_are_causal(gold):
    """Truncating an engine's history must not change its features up to the cut."""
    from aerolisa.engine_health.features import temporal_features

    e = gold[gold["engine_id"] == "FD001-HIST-003"].drop(columns=[c for c in gold if c.endswith(("_mean", "_std", "_slope"))])
    full = temporal_features(e)
    cut = temporal_features(e[e["cycle"] <= 50])
    cols = feature_columns("temporal")
    assert np.allclose(full[full["cycle"] <= 50][cols].to_numpy(), cut[cols].to_numpy())


def test_split_matches_saa_v1():
    assert list(validation_engines(np.arange(1, 101))) == [1, 5, 11, 13, 19, 23, 31, 32, 34, 40, 45, 46, 54, 71, 74, 77, 78, 81, 84, 91]


def test_truncation_and_last_cycle(gold):
    hist = gold[gold["split"] == "train"]
    s = truncation_sample(hist, per_engine=3)
    assert len(s) == 300 and s["cycle"].min() >= 31
    assert len(last_cycle(gold[gold["split"] == "test"])) == 100
