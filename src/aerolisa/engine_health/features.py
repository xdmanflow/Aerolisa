"""Gold features for engine health (owned by ``engine_health``, as in the Aerolisa design).

Spark twin: ``foundry/pipelines-repo/.../logic/features.py``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from aerolisa.core.schema import INFORMATIVE_SENSORS, OP_SETTINGS


# --- gold: temporal features --------------------------------------------------------
def temporal_features(df: pd.DataFrame, sensors: list[str] = INFORMATIVE_SENSORS, window: int = 30) -> pd.DataFrame:
    """Per-engine rolling features over the last ``window`` cycles (causal: no future data).

    For each sensor: rolling mean, rolling std, and least-squares slope vs cycle.
    Spark twin: ``Window.partitionBy('engine_id').orderBy('cycle').rowsBetween(-(w-1), 0)``
    with ``avg``, ``stddev_samp`` and ``covar_samp / var_samp``.
    """
    df = df.sort_values(["engine_id", "cycle"]).reset_index(drop=True)
    g = df.groupby("engine_id", sort=False)
    out = {}
    cyc = df["cycle"].astype(float)
    cyc_var = g["cycle"].rolling(window, min_periods=2).var().reset_index(level=0, drop=True)
    for s in sensors:
        roll = g[s].rolling(window, min_periods=1)
        out[f"{s}_mean"] = roll.mean().reset_index(level=0, drop=True)
        out[f"{s}_std"] = g[s].rolling(window, min_periods=2).std().reset_index(level=0, drop=True).fillna(0.0)
        cov = (
            df.assign(_c=cyc)
            .groupby("engine_id", sort=False)[[s, "_c"]]
            .rolling(window, min_periods=2)
            .cov()
        )
        cov = cov.xs("_c", level=-1)[s].reset_index(level=0, drop=True)
        out[f"{s}_slope"] = (cov / cyc_var).fillna(0.0)
    feats = pd.DataFrame(out, index=df.index)
    return pd.concat([df, feats], axis=1)


def feature_columns(kind: str, sensors: list[str] = INFORMATIVE_SENSORS) -> list[str]:
    """Feature sets compared in the research (SAA v2, section 3.3)."""
    if kind == "snapshot":           # SAA v1: one cycle, raw values
        return OP_SETTINGS + sensors
    if kind == "temporal":           # SAA v2: rolling statistics over the window + age
        return ["cycle"] + [f"{s}_{k}" for s in sensors for k in ("mean", "std", "slope")]
    raise ValueError(kind)


def validation_engines(train_units: np.ndarray, n_val: int = 20, seed: int = 42) -> np.ndarray:
    """Exactly the engine-level split of SAA v1 (``RandomState(42).choice``)."""
    rng = np.random.RandomState(seed)
    return np.sort(rng.choice(np.sort(train_units), size=n_val, replace=False))


def last_cycle(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values("cycle").groupby("engine_id").tail(1).sort_values("engine_id").reset_index(drop=True)


def truncation_sample(df: pd.DataFrame, per_engine: int = 10, seed: int = 42, min_cycles: int = 31) -> pd.DataFrame:
    """Emulate the test protocol on run-to-failure engines: pick random cut-off cycles.

    Used to calibrate intervals and pick alert thresholds on validation engines with the
    same 'observed up to now' situation as the test (in-service) engines.
    """
    rng = np.random.RandomState(seed)
    picks = []
    for _, g in df.groupby("engine_id"):
        g = g.sort_values("cycle")
        candidates = g[g["cycle"] >= min_cycles]
        if candidates.empty:
            continue
        idx = rng.choice(candidates.index, size=min(per_engine, len(candidates)), replace=False)
        picks.append(g.loc[idx])
    return pd.concat(picks).sort_values(["engine_id", "cycle"]).reset_index(drop=True)
