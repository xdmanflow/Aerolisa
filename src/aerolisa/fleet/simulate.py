"""A seeded, clearly-labelled simulated fleet.

Real airframes and real cycles come from OpenSky when that connector is enabled
(``fleet/opensky.py`` and the Foundry external transform). Until then, and for every
offline run, this module builds a reproducible demo fleet: 50 A320-family aircraft,
two engines each (the 100 C-MAPSS FD001 in-service engines), daily utilisation, and a
next-planned-check date. Every row carries ``simulated = True``.
"""

from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

from aerolisa.core.schema import SEED

TYPECODES = [("A20N", "A320neo", 0.45), ("A21N", "A321neo", 0.30), ("A320", "A320ceo", 0.15), ("A319", "A319ceo", 0.10)]
BASES = ["LFBO", "LFPG", "LFML", "LFLL", "LEBL", "LEMD", "EDDM", "LSZH"]


def simulate_aircraft(n_aircraft: int = 50, as_of: date = date(2026, 11, 19), seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    codes = rng.choice(len(TYPECODES), size=n_aircraft, p=[t[2] for t in TYPECODES])
    rows = []
    for i in range(n_aircraft):
        code, model, _ = TYPECODES[codes[i]]
        rate = float(np.clip(rng.normal(5.2, 1.3), 2.0, 9.0))     # short/medium-haul cycles per day
        rows.append({
            "tail_id": f"SIM-{i + 1:03d}",
            "registration": f"F-ZA{chr(65 + i // 26)}{chr(65 + i % 26)}",   # fictitious, F-Z reserved-style
            "operator_code": "AER",
            "operator_name": "Aerolisa Demo Airline (simulated)",
            "typecode": code,
            "model": model,
            "family": "A320",
            "home_base_icao": BASES[int(rng.integers(len(BASES)))],
            "utilization_rate_target": round(rate, 2),
            "next_check_date": (as_of + timedelta(days=int(rng.integers(2, 22)))).isoformat(),  # next hangar slot
            "simulated": True,
        })
    return pd.DataFrame(rows)


def simulate_utilization(aircraft: pd.DataFrame, days: int = 90, as_of: date = date(2026, 11, 19),
                         seed: int = SEED) -> pd.DataFrame:
    """Daily cycles and block hours per aircraft (Poisson around each aircraft's rate)."""
    rng = np.random.default_rng(seed + 1)
    rows = []
    for _, ac in aircraft.iterrows():
        for d in range(days, 0, -1):
            day = as_of - timedelta(days=d)
            cycles = int(rng.poisson(ac["utilization_rate_target"]))
            if rng.random() < 0.03:                      # occasional ground day (maintenance, AOG)
                cycles = 0
            hours = round(cycles * float(rng.normal(1.7, 0.25)), 2) if cycles else 0.0
            rows.append({"utilization_id": f"{ac['tail_id']}-{day.isoformat()}", "tail_id": ac["tail_id"],
                         "date": day.isoformat(), "cycles": cycles, "block_hours": max(hours, 0.0),
                         "simulated": True})
    return pd.DataFrame(rows)


def assign_engines(aircraft: pd.DataFrame, engine_ids: list[str], seed: int = SEED) -> pd.DataFrame:
    """Two engines per aircraft (positions 1 and 2), seeded shuffle."""
    if len(engine_ids) != 2 * len(aircraft):
        raise ValueError("need exactly two engines per aircraft")
    rng = np.random.default_rng(seed + 2)
    shuffled = list(rng.permutation(sorted(engine_ids)))
    rows = []
    for i, tail in enumerate(aircraft["tail_id"]):
        for pos in (1, 2):
            eid = shuffled[2 * i + pos - 1]
            rows.append({"engine_id": eid, "tail_id": tail, "position": pos,
                         "engine_model": "CFM LEAP-1A-like (C-MAPSS simulated)", "simulated": True})
    return pd.DataFrame(rows)


def utilization_stats(util: pd.DataFrame, window_days: int = 30) -> pd.DataFrame:
    """Mean cycles/day over the last ``window_days`` with a normal-approx 95 % CI."""
    util = util.copy()
    util["date"] = pd.to_datetime(util["date"])
    cutoff = util["date"].max() - pd.Timedelta(days=window_days - 1)
    recent = util[util["date"] >= cutoff]
    g = recent.groupby("tail_id")["cycles"]
    out = g.agg(cycles_per_day="mean", sd="std", n="count").reset_index()
    half = 1.96 * out["sd"] / np.sqrt(out["n"])
    out["cycles_per_day_lo"] = (out["cycles_per_day"] - half).clip(lower=0)
    out["cycles_per_day_hi"] = out["cycles_per_day"] + half
    return out.drop(columns=["sd", "n"]).round(2)
