"""From predictions to decisions: risk before the next check, ranking, reasons, what-if.

Risk formula (documented in docs/planner-risk.md):
    cycles_to_check = days_to_next_check x cycles_per_day
    risk = P(RUL < cycles_to_check), read from a piecewise-linear CDF through
           (P10, 0.1), (P50, 0.5), (P90, 0.9) with linear tails to 0 and 1.
Alert (from the research, SAA v2 section 4.7): rul_p10 <= alert_threshold_cycles.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def quantile_cdf(x: float, p10: float, p50: float, p90: float) -> float:
    eps = 1e-6
    p50 = max(p50, p10 + eps)
    p90 = max(p90, p50 + eps)
    x_lo = p10 - 0.1 * (p50 - p10) / 0.4
    x_hi = p90 + 0.1 * (p90 - p50) / 0.4
    return float(np.interp(x, [x_lo, p10, p50, p90, x_hi], [0.0, 0.1, 0.5, 0.9, 1.0]))


def risk_before(cycles: float, p10: float, p50: float, p90: float) -> float:
    return quantile_cdf(cycles, p10, p50, p90)


def band(alert: bool, risk: float) -> str:
    if alert or risk >= 0.5:
        return "RED"
    if risk >= 0.1:
        return "AMBER"
    return "GREEN"


def reason(row: pd.Series) -> str:
    parts = [f"P10 RUL {row['rul_p10']:.0f} cycles (~{row['days_p10']:.0f} days at {row['cycles_per_day']:.1f} cycles/day)"]
    parts.append(f"{row['risk_before_check']:.0%} risk before next check in {row['days_to_next_check']:.0f} days")
    if row.get("anomaly_score", 0) >= 0.99:
        parts.append(f"anomaly score {row['anomaly_score']:.2f}")
    if row.get("top_drivers") and row["top_drivers"] != "no significant drift":
        parts.append(f"drift: {row['top_drivers']}")
    return "; ".join(parts)


def rank_inspections(snap: pd.DataFrame, alert_threshold_cycles: float, as_of: str) -> pd.DataFrame:
    """``snap``: one row per in-service engine with rul_p10/p50/p90, cycles_per_day,
    days_to_next_check, anomaly_score, top_drivers. Returns InspectionRecommendation rows."""
    df = snap.copy()
    cpd = df["cycles_per_day"].clip(lower=0.1)
    df["days_p10"] = df["rul_p10"] / cpd
    df["days_p50"] = df["rul_p50"] / cpd
    df["cycles_to_next_check"] = df["days_to_next_check"] * cpd
    df["risk_before_check"] = [risk_before(c, a, b, d) for c, a, b, d in
                               zip(df["cycles_to_next_check"], df["rul_p10"], df["rul_p50"], df["rul_p90"], strict=True)]
    df["alert"] = df["rul_p10"] <= alert_threshold_cycles
    df["band"] = [band(a, r) for a, r in zip(df["alert"], df["risk_before_check"], strict=True)]
    df = df.sort_values(["alert", "risk_before_check", "days_p10"], ascending=[False, False, True]).reset_index(drop=True)
    df["rank"] = np.arange(1, len(df) + 1)
    df["reason"] = df.apply(reason, axis=1)
    df["recommendation_id"] = "REC-" + as_of.replace("-", "") + "-" + df["engine_id"]
    df["status"] = "OPEN"
    df["created_at"] = as_of
    return df


def what_if_delay(row: pd.Series, delay_days: float) -> float:
    cycles = (row["days_to_next_check"] + delay_days) * max(row["cycles_per_day"], 0.1)
    return risk_before(cycles, row["rul_p10"], row["rul_p50"], row["rul_p90"])
