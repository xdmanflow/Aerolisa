"""RUL models: point estimate + calibrated P10/P50/P90 interval.

The production model ("EngineHealthModel") is what the Foundry Model Training repo
wraps in a ``palantir_models`` ModelAdapter (``foundry/models-repo``). Keep it
dependency-light (scikit-learn only) so it runs identically in both places.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

from aerolisa.core.schema import RUL_CAP, SEED


def hgb(loss: str = "squared_error", quantile: float | None = None, seed: int = SEED) -> HistGradientBoostingRegressor:
    kwargs = dict(max_iter=400, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=40,
                  l2_regularization=1.0, random_state=seed)
    if loss == "quantile":
        return HistGradientBoostingRegressor(loss="quantile", quantile=quantile, **kwargs)
    return HistGradientBoostingRegressor(loss=loss, **kwargs)


@dataclass
class EngineHealthModel:
    """Point RUL + conformalized quantile interval (CQR, Romano et al., 2019).

    1. Fit quantile regressors for ``alpha/2`` and ``1-alpha/2`` and a squared-error model.
    2. On a calibration set (held-out engines, truncated like in-service engines) compute
       conformity scores ``E = max(q_lo - y, y - q_hi)``.
    3. Widen both bounds by the ``(1-alpha)(1+1/n)`` empirical quantile of ``E``.
    The guarantee is marginal coverage under exchangeability; we *measure* the real
    coverage on the test engines instead of assuming it.
    """

    features: list[str]
    alpha: float = 0.2                       # 80 % interval -> P10 / P90
    cap: int = RUL_CAP
    seed: int = SEED
    point_: HistGradientBoostingRegressor | None = field(default=None, repr=False)
    lo_: HistGradientBoostingRegressor | None = field(default=None, repr=False)
    hi_: HistGradientBoostingRegressor | None = field(default=None, repr=False)
    q_hat_: float = 0.0
    version: str = "aerolisa-ehm-1.0.0"

    def fit(self, X: pd.DataFrame, y: pd.Series) -> EngineHealthModel:
        Xf = X[self.features]
        self.point_ = hgb(seed=self.seed).fit(Xf, y)
        self.lo_ = hgb("quantile", self.alpha / 2, self.seed).fit(Xf, y)
        self.hi_ = hgb("quantile", 1 - self.alpha / 2, self.seed).fit(Xf, y)
        return self

    def _raw(self, X: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        Xf = X[self.features]
        p = self.point_.predict(Xf)
        lo, hi = self.lo_.predict(Xf), self.hi_.predict(Xf)
        lo, hi = np.minimum(lo, hi), np.maximum(lo, hi)
        return p, lo, hi

    def calibrate(self, X_cal: pd.DataFrame, y_cal: pd.Series) -> EngineHealthModel:
        _, lo, hi = self._raw(X_cal)
        y = np.asarray(y_cal, float)
        scores = np.maximum(lo - y, y - hi)
        n = len(scores)
        level = min(1.0, np.ceil((n + 1) * (1 - self.alpha)) / n)
        self.q_hat_ = float(np.quantile(scores, level, method="higher"))
        return self

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        p, lo, hi = self._raw(X)
        lo, hi = lo - self.q_hat_, hi + self.q_hat_
        p = np.clip(p, 0, self.cap)
        p10 = np.clip(np.minimum(lo, p), 0, self.cap)
        p90 = np.clip(np.maximum(hi, p), 0, None)
        return pd.DataFrame({"rul_p10": p10, "rul_p50": p, "rul_p90": p90}, index=X.index)
