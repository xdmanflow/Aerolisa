import numpy as np
import pandas as pd

from aerolisa.engine_health.bundle import choose_alert_threshold
from aerolisa.engine_health.metrics import interval_coverage, nasa_score, rmse
from aerolisa.engine_health.models import EngineHealthModel
from aerolisa.engine_health.reliability import kaplan_meier, weibull_fit


def test_nasa_score_is_asymmetric():
    assert nasa_score([50], [60]) > nasa_score([50], [40]) > 0
    assert np.isclose(nasa_score([50], [50]), 0.0)
    assert np.isclose(rmse([0, 0], [3, 4]), np.sqrt(12.5))


def test_conformal_interval_covers_on_synthetic():
    rng = np.random.default_rng(0)
    X = pd.DataFrame({"x": rng.uniform(0, 10, 3000)})
    y = pd.Series(3 * X["x"] + rng.normal(0, 2, 3000))
    m = EngineHealthModel(features=["x"], alpha=0.2, cap=1000).fit(X[:2000], y[:2000]).calibrate(X[2000:2500], y[2000:2500])
    p = m.predict(X[2500:])
    assert (p["rul_p10"] <= p["rul_p50"]).all() and (p["rul_p50"] <= p["rul_p90"]).all()
    assert 0.72 <= interval_coverage(y[2500:], p["rul_p10"], p["rul_p90"]) <= 0.9


def test_alert_threshold_prefers_catching_failures():
    y = np.array([5, 10, 20, 60, 80, 100])
    stat = np.array([8, 12, 28, 40, 90, 110])
    assert choose_alert_threshold(y, stat, horizon=30, cost_fn=10) >= 28


def test_weibull_recovers_shape():
    rng = np.random.default_rng(1)
    fit = weibull_fit(200 * rng.weibull(3.0, 2000))
    assert abs(fit["beta"] - 3.0) < 0.2 and abs(fit["eta"] - 200) < 8


def test_kaplan_meier_with_censoring():
    km = kaplan_meier([1, 2, 2, 3], [1, 1, 0, 1])
    assert np.allclose(km["survival"], [0.75, 0.5, 0.0])
