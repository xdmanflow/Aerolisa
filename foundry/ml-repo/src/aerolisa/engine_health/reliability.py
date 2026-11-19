"""Fleet reliability: Kaplan-Meier survival and a 2-parameter Weibull fit."""

from __future__ import annotations

from math import gamma

import numpy as np
import pandas as pd
from scipy import stats


def kaplan_meier(durations, observed) -> pd.DataFrame:
    """Product-limit estimator. ``observed`` = 1 for a failure, 0 for right-censored."""
    d = pd.DataFrame({"t": np.asarray(durations, float), "e": np.asarray(observed, int)}).sort_values("t")
    times = np.sort(d.loc[d["e"] == 1, "t"].unique())
    surv, s = [], 1.0
    for t in times:
        at_risk = (d["t"] >= t).sum()
        deaths = ((d["t"] == t) & (d["e"] == 1)).sum()
        s *= 1 - deaths / at_risk
        surv.append((t, at_risk, deaths, s))
    return pd.DataFrame(surv, columns=["cycle", "at_risk", "failures", "survival"])


def weibull_fit(lifetimes) -> dict:
    """MLE of shape (beta) and scale (eta) with location fixed at 0; B10 = 10 % failed."""
    x = np.asarray(lifetimes, float)
    beta, _, eta = stats.weibull_min.fit(x, floc=0)
    b10 = eta * (-np.log(0.9)) ** (1 / beta)
    mttf = eta * gamma(1 + 1 / beta)
    ks = stats.kstest(x, "weibull_min", args=(beta, 0, eta))
    return {"beta": round(float(beta), 2), "eta": round(float(eta), 1), "b10": round(float(b10), 1),
            "mttf": round(float(mttf), 1), "ks_pvalue": round(float(ks.pvalue), 3), "n": int(len(x))}
