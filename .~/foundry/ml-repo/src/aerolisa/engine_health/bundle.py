"""The deployable engine-health model: RUL interval + health index + anomaly + drivers + alert rule.

``train_bundle`` is the single training entry point used by:
* the local pipeline (``aerolisa.pipelines.graph``), and
* the Foundry training transform (``foundry/models-repo/.../train_engine_health.py``),
so the model published to Foundry is trained by exactly the code tested here.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from aerolisa.core.schema import ALERT_HORIZON, CRITICAL_RUL, N_VAL_ENGINES, SEED
from aerolisa.engine_health.features import feature_columns, last_cycle, truncation_sample, validation_engines
from aerolisa.engine_health.health import HealthMonitor
from aerolisa.engine_health.metrics import interval_coverage, rmse, summary
from aerolisa.engine_health.models import EngineHealthModel

SNAPSHOT_COLUMNS = ["rul_p10", "rul_p50", "rul_p90", "health_index", "anomaly_score", "top_drivers", "alert", "model_version"]


@dataclass
class EngineHealthBundle:
    rul_model: EngineHealthModel
    monitor: HealthMonitor
    alert_threshold_cycles: int
    metrics: dict = field(default_factory=dict)

    @property
    def version(self) -> str:
        return self.rul_model.version

    @property
    def features(self) -> list[str]:
        return self.rul_model.features

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """``df``: rows of gold/engine_cycle_features. Returns df + snapshot columns."""
        out = df.copy()
        out[["rul_p10", "rul_p50", "rul_p90"]] = self.rul_model.predict(df).to_numpy()
        out["health_index"] = self.monitor.health_index(df)
        out["anomaly_score"] = self.monitor.anomaly_score(df)
        out["top_drivers"] = self.monitor.top_drivers(df)
        out["alert"] = out["rul_p10"] <= self.alert_threshold_cycles
        out["model_version"] = self.version
        return out


def choose_alert_threshold(y_true: np.ndarray, stat: np.ndarray, horizon: int = ALERT_HORIZON,
                           cost_fn: float = 10.0, cost_fp: float = 1.0, max_k: int = 100) -> int:
    """Smallest-cost k for the rule 'alert if stat <= k' (positives: true RUL <= horizon)."""
    pos = y_true <= horizon
    ks = np.arange(0, max_k + 1)
    costs = [cost_fn * np.sum(pos & (stat > k)) + cost_fp * np.sum(~pos & (stat <= k)) for k in ks]
    return int(ks[int(np.argmin(costs))])


def train_bundle(features: pd.DataFrame, seed: int = SEED, alpha: float = 0.2,
                 cost_fn: float = 10.0, cost_fp: float = 1.0) -> EngineHealthBundle:
    """``features``: gold/engine_cycle_features (both splits). Trains on HIST engines only."""
    hist = features[features["split"] == "train"]
    val_units = validation_engines(hist["unit"].unique(), n_val=N_VAL_ENGINES, seed=seed)
    tr = hist[~hist["unit"].isin(val_units)]
    va = hist[hist["unit"].isin(val_units)]
    cal = truncation_sample(va, per_engine=10, seed=seed)

    model = EngineHealthModel(features=feature_columns("temporal"), alpha=alpha, seed=seed).fit(tr, tr["rul_capped"])
    model.calibrate(cal, cal["rul_capped"])
    monitor = HealthMonitor(seed=seed).fit(tr)
    cal_pred = model.predict(cal)
    k = choose_alert_threshold(cal["rul"].to_numpy(), cal_pred["rul_p10"].to_numpy(), cost_fn=cost_fn, cost_fp=cost_fp)

    metrics = {"val_rmse_all_cycles": round(rmse(va["rul_capped"], model.predict(va)["rul_p50"]), 2),
               "cal_coverage": round(interval_coverage(cal["rul_capped"], cal_pred["rul_p10"], cal_pred["rul_p90"]), 3),
               "q_hat": round(model.q_hat_, 2), "alert_threshold_cycles": k, "n_train_engines": int(tr["engine_id"].nunique()),
               "n_val_engines": int(va["engine_id"].nunique())}
    fleet = features[features["split"] == "test"]
    if not fleet.empty:                      # official C-MAPSS test protocol: last cycle per engine
        te = last_cycle(fleet)
        pt = model.predict(te)
        y = te["rul"].to_numpy()
        crit = y < CRITICAL_RUL
        metrics.update({f"test_{k_}": v for k_, v in summary(y, pt["rul_p50"]).items()})
        metrics["test_rmse_critical"] = round(rmse(y[crit], pt["rul_p50"].to_numpy()[crit]), 2)
        metrics["test_interval_coverage"] = round(interval_coverage(np.minimum(y, model.cap), pt["rul_p10"], pt["rul_p90"]), 3)
    return EngineHealthBundle(model, monitor, k, metrics)
