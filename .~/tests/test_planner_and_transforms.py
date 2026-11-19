import pandas as pd
import pytest

from aerolisa.core import transforms as T
from aerolisa.planner.risk import quantile_cdf, rank_inspections, what_if_delay


def test_cdf_hits_quantiles_and_is_monotone():
    assert quantile_cdf(10, 10, 20, 40) == pytest.approx(0.1)
    assert quantile_cdf(20, 10, 20, 40) == pytest.approx(0.5)
    assert quantile_cdf(40, 10, 20, 40) == pytest.approx(0.9)
    vals = [quantile_cdf(x, 10, 20, 40) for x in range(0, 60)]
    assert vals == sorted(vals) and vals[0] == 0 and vals[-1] == 1


def _snap():
    return pd.DataFrame({
        "engine_id": ["A", "B", "C"], "rul_p10": [5, 30, 90], "rul_p50": [12, 60, 110], "rul_p90": [20, 80, 125],
        "cycles_per_day": [5, 5, 5], "days_to_next_check": [7, 7, 7], "anomaly_score": [1.0, 0.5, 0.1],
        "top_drivers": ["sensor_11 (Ps30) +4.0σ", "no significant drift", "no significant drift"],
    })


def test_ranking_and_bands():
    rec = rank_inspections(_snap(), alert_threshold_cycles=25, as_of="2026-11-19")
    assert list(rec["engine_id"]) == ["A", "B", "C"]
    assert list(rec["band"]) == ["RED", "AMBER", "GREEN"]
    assert "Ps30" in rec.loc[0, "reason"] and rec["recommendation_id"].is_unique


def test_what_if_delay_increases_risk():
    row = rank_inspections(_snap(), 25, "2026-11-19").iloc[1]
    assert what_if_delay(row, 5) > what_if_delay(row, 0)


def test_registry_build_order_and_checks(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "REGISTRY", {})

    @T.transform(T.Output("a/x", checks=[T.primary_key("id")]))
    def x():
        return pd.DataFrame({"id": [1, 2]})

    @T.transform(T.Output("a/y"), x=T.Input("a/x"))
    def y(x):
        return x.assign(v=x["id"] * 2)

    assert T.build_order(["a/y"]) == ["a/x", "a/y"]
    T.build(data_dir=tmp_path, verbose=False)
    assert T.read_dataset("a/y", tmp_path)["v"].tolist() == [2, 4]

    @T.transform(T.Output("a/bad", checks=[T.primary_key("id")]))
    def bad():
        return pd.DataFrame({"id": [1, 1]})

    with pytest.raises(ValueError, match="duplicates"):
        T.build(["a/bad"], data_dir=tmp_path, verbose=False)
