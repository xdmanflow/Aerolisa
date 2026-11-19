"""The full local pipeline graph, declared with the Foundry-style transform API.

Dataset names match the Foundry edition one to one (``foundry/README.md``), so the
lineage graph produced here is the lineage you will see in Foundry's Data Lineage app.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from aerolisa.core.schema import WINDOW
from aerolisa.core.transforms import Input, Output, in_range, non_null, primary_key, transform
from aerolisa.engine_health.bundle import SNAPSHOT_COLUMNS, train_bundle
from aerolisa.engine_health.features import temporal_features
from aerolisa.engine_health.reliability import kaplan_meier, weibull_fit
from aerolisa.fleet.simulate import assign_engines, simulate_aircraft, simulate_utilization, utilization_stats
from aerolisa.pipelines.cmapss import bronze_cmapss, gold_rul_labels, silver_cmapss_cycles
from aerolisa.planner.risk import rank_inspections

AS_OF = "2026-11-19"
_BUNDLE: dict = {}  # in-process cache: the model trained by gold/engine_health_model_metrics


# --- bronze (sources: no inputs) ------------------------------------------------------
@transform(Output("bronze/cmapss_raw", checks=[non_null("unit", "cycle", "source_file")]))
def cmapss_raw() -> pd.DataFrame:
    return bronze_cmapss()[0]


@transform(Output("bronze/cmapss_rul", checks=[primary_key("unit"), in_range("rul_at_cutoff", 0)]))
def cmapss_rul() -> pd.DataFrame:
    return bronze_cmapss()[1]


# --- silver -----------------------------------------------------------------------------
@transform(Output("silver/cmapss_cycles", checks=[primary_key("cycle_id"), in_range("cycle", 1)]),
           raw=Input("bronze/cmapss_raw"))
def cmapss_cycles(raw: pd.DataFrame) -> pd.DataFrame:
    return silver_cmapss_cycles(raw)


# --- gold: features ------------------------------------------------------------------------
@transform(Output("gold/engine_cycle_features", checks=[primary_key("cycle_id"), in_range("rul", 0)]),
           cycles=Input("silver/cmapss_cycles"), rul=Input("bronze/cmapss_rul"))
def engine_cycle_features(cycles: pd.DataFrame, rul: pd.DataFrame) -> pd.DataFrame:
    return temporal_features(gold_rul_labels(cycles, rul), window=WINDOW)


# --- gold: model (Foundry: ModelOutput 'engine-health-model' + this metrics dataset) --------
@transform(Output("gold/engine_health_model_metrics"), features=Input("gold/engine_cycle_features"))
def engine_health_model_metrics(features: pd.DataFrame) -> pd.DataFrame:
    bundle = train_bundle(features)
    _BUNDLE["model"] = bundle
    return pd.DataFrame([{"model_version": bundle.version, "trained_at": AS_OF, "metrics_json": json.dumps(bundle.metrics),
                          **{k: v for k, v in bundle.metrics.items() if isinstance(v, (int, float))}}])


def _bundle(features: pd.DataFrame):
    if "model" not in _BUNDLE:
        _BUNDLE["model"] = train_bundle(features)
    return _BUNDLE["model"]


@transform(Output("gold/engine_health_snapshot", checks=[primary_key("snapshot_id"), in_range("rul_p10", 0)]),
           features=Input("gold/engine_cycle_features"), metrics=Input("gold/engine_health_model_metrics"))
def engine_health_snapshot(features: pd.DataFrame, metrics: pd.DataFrame) -> pd.DataFrame:
    """Inference on every observed cycle of the in-service (FLEET) engines -> health history."""
    fleet = features[features["split"] == "test"]
    pred = _bundle(features).predict(fleet)
    pred["snapshot_id"] = pred["cycle_id"]
    pred["is_latest"] = pred["cycle"] == pred.groupby("engine_id")["cycle"].transform("max")
    keep = ["snapshot_id", "engine_id", "cycle", *SNAPSHOT_COLUMNS, "is_latest",
            "sensor_11_mean", "sensor_4_mean", "sensor_9_mean", "sensor_7_mean", "rul"]
    out = pred[keep].rename(columns={"rul": "rul_truth_simulation_only"})
    num = out.select_dtypes("number").columns
    out[num] = out[num].round(3)
    return out


# --- gold: fleet (simulated until the OpenSky source is switched on) ------------------------
@transform(Output("gold/fleet_aircraft", checks=[primary_key("tail_id")]))
def fleet_aircraft() -> pd.DataFrame:
    return simulate_aircraft()


@transform(Output("gold/aircraft_utilization_daily", checks=[primary_key("utilization_id"), in_range("cycles", 0)]),
           aircraft=Input("gold/fleet_aircraft"))
def aircraft_utilization_daily(aircraft: pd.DataFrame) -> pd.DataFrame:
    return simulate_utilization(aircraft)


@transform(Output("gold/engine_assignment", checks=[primary_key("engine_id")]),
           aircraft=Input("gold/fleet_aircraft"), cycles=Input("silver/cmapss_cycles"))
def engine_assignment(aircraft: pd.DataFrame, cycles: pd.DataFrame) -> pd.DataFrame:
    fleet_ids = sorted(cycles.loc[cycles["split"] == "test", "engine_id"].unique())
    return assign_engines(aircraft, fleet_ids)


# --- gold: planner ----------------------------------------------------------------------------
@transform(Output("gold/inspection_recommendation", checks=[primary_key("recommendation_id"), in_range("risk_before_check", 0, 1)]),
           snapshot=Input("gold/engine_health_snapshot"), assignment=Input("gold/engine_assignment"),
           aircraft=Input("gold/fleet_aircraft"), utilization=Input("gold/aircraft_utilization_daily"),
           metrics=Input("gold/engine_health_model_metrics"))
def inspection_recommendation(snapshot, assignment, aircraft, utilization, metrics) -> pd.DataFrame:
    latest = snapshot[snapshot["is_latest"]].drop(columns=["is_latest"])
    snap = (latest.merge(assignment[["engine_id", "tail_id", "position"]], on="engine_id")
            .merge(aircraft[["tail_id", "next_check_date"]], on="tail_id")
            .merge(utilization_stats(utilization), on="tail_id"))
    snap["days_to_next_check"] = (pd.to_datetime(snap["next_check_date"]) - pd.Timestamp(AS_OF)).dt.days
    rec = rank_inspections(snap, float(metrics["alert_threshold_cycles"].iloc[0]), AS_OF)
    cols = ["recommendation_id", "engine_id", "tail_id", "position", "rank", "band", "alert", "risk_before_check",
            "rul_p10", "rul_p50", "rul_p90", "cycles_per_day", "days_p10", "days_p50", "days_to_next_check",
            "next_check_date", "anomaly_score", "health_index", "top_drivers", "reason", "status", "created_at", "model_version"]
    out = rec[cols].copy()
    num = out.select_dtypes("number").columns
    out[num] = out[num].round(3)
    return out


# --- gold: reliability ------------------------------------------------------------------------
@transform(Output("gold/engine_life_records", checks=[primary_key("engine_id")]), cycles=Input("silver/cmapss_cycles"))
def engine_life_records(cycles: pd.DataFrame) -> pd.DataFrame:
    g = cycles.groupby(["engine_id", "split"])["cycle"].max().reset_index(name="observed_cycles")
    g["failed"] = g["split"] == "train"
    g["role"] = np.where(g["failed"], "run-to-failure history", "in service (right-censored)")
    return g.drop(columns=["split"])


@transform(Output("gold/reliability_km"), life=Input("gold/engine_life_records"))
def reliability_km(life: pd.DataFrame) -> pd.DataFrame:
    km = kaplan_meier(life["observed_cycles"], life["failed"].astype(int))
    wb = weibull_fit(life.loc[life["failed"], "observed_cycles"])
    for k, v in wb.items():
        km[f"weibull_{k}"] = v
    return km


# --- objects (ontology backing datasets) ------------------------------------------------------
@transform(Output("objects/engine", checks=[primary_key("engine_id")]),
           assignment=Input("gold/engine_assignment"), rec=Input("gold/inspection_recommendation"),
           snapshot=Input("gold/engine_health_snapshot"))
def obj_engine(assignment, rec, snapshot) -> pd.DataFrame:
    latest = snapshot[snapshot["is_latest"]][["engine_id", "cycle"]].rename(columns={"cycle": "current_cycle"})
    r = rec[["engine_id", "rank", "band", "alert", "risk_before_check", "rul_p10", "rul_p50", "rul_p90",
             "health_index", "anomaly_score", "top_drivers", "model_version"]]
    return assignment.merge(latest, on="engine_id").merge(r, on="engine_id")


@transform(Output("objects/aircraft", checks=[primary_key("tail_id")]),
           aircraft=Input("gold/fleet_aircraft"), utilization=Input("gold/aircraft_utilization_daily"),
           rec=Input("gold/inspection_recommendation"))
def obj_aircraft(aircraft, utilization, rec) -> pd.DataFrame:
    worst = rec.groupby("tail_id").agg(worst_engine_risk=("risk_before_check", "max"),
                                       engines_in_red=("band", lambda b: int((b == "RED").sum()))).reset_index()
    return aircraft.merge(utilization_stats(utilization), on="tail_id").merge(worst, on="tail_id")


@transform(Output("objects/operator", checks=[primary_key("operator_code")]), aircraft=Input("gold/fleet_aircraft"))
def obj_operator(aircraft) -> pd.DataFrame:
    return aircraft.groupby(["operator_code", "operator_name"]).size().reset_index(name="fleet_size").assign(simulated=True)


@transform(Output("writeback/work_orders", checks=[primary_key("work_order_id")]))
def work_orders() -> pd.DataFrame:
    """Empty backing dataset: rows are created only by the ScheduleInspection action."""
    return pd.DataFrame(columns=["work_order_id", "engine_id", "recommendation_id", "work_type", "planned_date", "status",
                                 "comment", "created_by", "created_at", "closed_at", "finding"])
