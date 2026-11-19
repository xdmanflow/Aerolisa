"""Health monitoring signals that do not need failure labels.

* Health index (HI): first principal component of the standardised rolling sensor means,
  rescaled so that the fleet's healthy reference = 1 and the failure reference = 0.
* Anomaly score: Isolation Forest trained on healthy cycles only (RUL above the cap),
  the usual set-up when real failures are rare.
* Drivers: which sensors have drifted most from the healthy reference, in sigma, in the
  direction that indicates degradation. Transparent and cheap; the research compares it
  with the global permutation importance of the RUL model.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest

from aerolisa.core.schema import INFORMATIVE_SENSORS, RUL_CAP, SEED, SENSOR_DESCRIPTIONS


@dataclass
class HealthMonitor:
    sensors: list[str] = field(default_factory=lambda: list(INFORMATIVE_SENSORS))
    healthy_rul: int = RUL_CAP
    failure_rul: int = 5
    seed: int = SEED

    def fit(self, train: pd.DataFrame) -> HealthMonitor:
        """``train`` = run-to-failure engines with ``rul`` and ``<sensor>_mean`` columns."""
        means = [f"{s}_mean" for s in self.sensors]
        healthy = train[train["rul"] > self.healthy_rul]
        self.mu_ = healthy[means].mean()
        self.sd_ = healthy[means].std().replace(0, 1.0)
        # degradation direction of each sensor: sign of its drift from healthy to failure
        failing = train[train["rul"] <= self.failure_rul]
        self.direction_ = np.sign(failing[means].mean() - self.mu_).replace(0, 1.0)
        z = (train[means] - self.mu_) / self.sd_
        self.pca_ = PCA(n_components=1, random_state=self.seed).fit(z)
        pc = self.pca_.transform(z)[:, 0]
        h_ref = pc[train["rul"].to_numpy() > self.healthy_rul].mean()
        f_ref = pc[train["rul"].to_numpy() <= self.failure_rul].mean()
        self.h_ref_, self.f_ref_ = float(h_ref), float(f_ref)
        raw = healthy[self.sensors]
        self.raw_mu_, self.raw_sd_ = raw.mean(), raw.std().replace(0, 1.0)
        self.iforest_ = IsolationForest(n_estimators=300, contamination="auto", random_state=self.seed)
        self.iforest_.fit(((raw - self.raw_mu_) / self.raw_sd_).to_numpy())
        # reference distribution of healthy scores -> percentile-based anomaly score in [0, 1]
        self.healthy_scores_ = np.sort(-self.iforest_.score_samples(((raw - self.raw_mu_) / self.raw_sd_).to_numpy()))
        return self

    def health_index(self, df: pd.DataFrame) -> np.ndarray:
        z = (df[[f"{s}_mean" for s in self.sensors]] - self.mu_) / self.sd_
        pc = self.pca_.transform(z)[:, 0]
        return np.clip((pc - self.f_ref_) / (self.h_ref_ - self.f_ref_), -0.25, 1.25)

    def anomaly_score(self, df: pd.DataFrame) -> np.ndarray:
        """Share of healthy reference cycles that look *more normal* than this cycle (0..1)."""
        z = ((df[self.sensors] - self.raw_mu_) / self.raw_sd_).to_numpy()
        s = -self.iforest_.score_samples(z)
        return np.searchsorted(self.healthy_scores_, s, side="right") / len(self.healthy_scores_)

    def drift_sigma(self, df: pd.DataFrame) -> pd.DataFrame:
        means = [f"{s}_mean" for s in self.sensors]
        z = (df[means] - self.mu_) / self.sd_ * self.direction_
        z.columns = self.sensors
        return z

    def top_drivers(self, df: pd.DataFrame, k: int = 3) -> list[str]:
        z = self.drift_sigma(df)
        out = []
        for _, row in z.iterrows():
            top = row.sort_values(ascending=False).head(k)
            parts = [f"{s} ({SENSOR_DESCRIPTIONS[s].split(' ', 1)[0]}) {v:+.1f}σ" for s, v in top.items() if v > 1.0]
            out.append("; ".join(parts) if parts else "no significant drift")
        return out
