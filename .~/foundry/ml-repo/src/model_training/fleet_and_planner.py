"""Simulated fleet, inspection planner and reliability, as pandas transforms.

All logic lives in the vendored ``aerolisa`` package; these functions only wire datasets.
"""

import pandas as pd
from model_training import paths
from transforms.api import Input, Output, transform

from aerolisa.engine_health.reliability import kaplan_meier, weibull_fit
from aerolisa.fleet.simulate import assign_engines, simulate_aircraft, simulate_utilization, utilization_stats
from aerolisa.planner.risk import rank_inspections


@transform(out=Output(paths.GOLD_FLEET_AIRCRAFT))
def fleet_aircraft(out):
    out.write_pandas(simulate_aircraft())


@transform(out=Output(paths.GOLD_AIRCRAFT_UTILIZATION_DAILY), aircraft=Input(paths.GOLD_FLEET_AIRCRAFT))
def aircraft_utilization_daily(out, aircraft):
    out.write_pandas(simulate_utilization(aircraft.pandas()))


@transform(out=Output(paths.GOLD_ENGINE_ASSIGNMENT), aircraft=Input(paths.GOLD_FLEET_AIRCRAFT),
           cycles=Input(paths.SILVER_CMAPSS_CYCLES))
def engine_assignment(out, aircraft, cycles):
    ids = [r["engine_id"] for r in cycles.dataframe().filter("split = 'test'").select("engine_id").distinct().collect()]
    out.write_pandas(assign_engines(aircraft.pandas(), sorted(ids)))


@transform(
    out=Output(paths.GOLD_INSPECTION_RECOMMENDATION),
    snapshot=Input(paths.GOLD_ENGINE_HEALTH_SNAPSHOT),
    assignment=Input(paths.GOLD_ENGINE_ASSIGNMENT),
    aircraft=Input(paths.GOLD_FLEET_AIRCRAFT),
    utilization=Input(paths.GOLD_AIRCRAFT_UTILIZATION_DAILY),
    metrics=Input(paths.GOLD_ENGINE_HEALTH_MODEL_METRICS),
)
def inspection_recommendation(out, snapshot, assignment, aircraft, utilization, metrics):
    snap = snapshot.pandas()
    latest = snap[snap["is_latest"]].drop(columns=["is_latest"])
    m = metrics.pandas().sort_values("trained_at").iloc[-1]
    df = (latest.merge(assignment.pandas()[["engine_id", "tail_id", "position"]], on="engine_id")
          .merge(aircraft.pandas()[["tail_id", "next_check_date"]], on="tail_id")
          .merge(utilization_stats(utilization.pandas()), on="tail_id"))
    df["days_to_next_check"] = (pd.to_datetime(df["next_check_date"]) - pd.Timestamp(paths.AS_OF)).dt.days
    rec = rank_inspections(df, float(m["alert_threshold_cycles"]), paths.AS_OF)
    cols = ["recommendation_id", "engine_id", "tail_id", "position", "rank", "band", "alert", "risk_before_check",
            "rul_p10", "rul_p50", "rul_p90", "cycles_per_day", "days_p10", "days_p50", "days_to_next_check",
            "next_check_date", "anomaly_score", "health_index", "top_drivers", "reason", "status", "created_at", "model_version"]
    out.write_pandas(rec[cols])


@transform(out=Output(paths.GOLD_RELIABILITY_KM), life=Input(paths.GOLD_ENGINE_LIFE_RECORDS))
def reliability_km(out, life):
    lf = life.pandas()
    km = kaplan_meier(lf["observed_cycles"], lf["failed"].astype(int))
    for k, v in weibull_fit(lf.loc[lf["failed"], "observed_cycles"]).items():
        km[f"weibull_{k}"] = v
    out.write_pandas(km)
