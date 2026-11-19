"""SAA v2 experiments: everything the revised report states is computed here.

Run from the repository root:  python research/run_experiments.py
Writes research/results/*.json|csv and research/figures/fig11-fig17*.png.
Figures fig1-fig10 and the LSTM results come from SAA v1 (research/saa_v1, Keras),
which this script re-reads but does not retrain (TensorFlow is not a dependency here).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import roc_auc_score
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aerolisa.core.schema import (  # noqa: E402
    ALERT_HORIZON,
    CRITICAL_RUL,
    INFORMATIVE_SENSORS,
    OP_SETTINGS,
    RUL_CAP,
    SEED,
    WINDOW,
)
from aerolisa.engine_health.features import (  # noqa: E402
    feature_columns,
    last_cycle,
    temporal_features,
    truncation_sample,
    validation_engines,
)
from aerolisa.engine_health.health import HealthMonitor  # noqa: E402
from aerolisa.engine_health.metrics import interval_coverage, interval_width, rmse, summary  # noqa: E402
from aerolisa.engine_health.models import EngineHealthModel, hgb  # noqa: E402
from aerolisa.engine_health.reliability import kaplan_meier, weibull_fit  # noqa: E402
from aerolisa.fleet.simulate import assign_engines, simulate_aircraft, simulate_utilization, utilization_stats  # noqa: E402
from aerolisa.pipelines.cmapss import bronze_cmapss, gold_rul_labels, silver_cmapss_cycles  # noqa: E402
from aerolisa.planner.risk import rank_inspections  # noqa: E402

RES = ROOT / "research" / "results"
FIG = ROOT / "research" / "figures"
V1 = ROOT / "research" / "saa_v1" / "results"
RES.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

# palette (validated reference palette, light mode) -------------------------------
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948")
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
STATUS = {"GREEN": "#0ca30c", "AMBER": "#fab219", "RED": "#d03b3b"}
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150, "savefig.bbox": "tight",
    "legend.frameon": False,
})

T0 = time.time()
log: dict = {}


def save(fig, name):
    fig.savefig(FIG / name, facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------------------------
# 0. Data: the same pipeline the Foundry edition runs (bronze -> silver -> gold)
# ------------------------------------------------------------------------------------
bronze, rul_file = bronze_cmapss()
silver = silver_cmapss_cycles(bronze)
gold = temporal_features(gold_rul_labels(silver, rul_file), window=WINDOW)
hist = gold[gold["split"] == "train"].copy()
fleet = gold[gold["split"] == "test"].copy()

val_units = validation_engines(hist["unit"].unique(), seed=SEED)
tr = hist[~hist["unit"].isin(val_units)].copy()
va = hist[hist["unit"].isin(val_units)].copy()
te = last_cycle(fleet)
va_trunc = truncation_sample(va, per_engine=10, seed=SEED)
y_tr = tr["rul_capped"]
y_va = va["rul_capped"]
y_te = te["rul"].to_numpy()
crit = y_te < CRITICAL_RUL

log["data"] = {
    "train_rows": int(len(hist)), "test_rows": int(len(fleet)), "train_engines_fit": int(tr["engine_id"].nunique()),
    "val_engines": [int(u) for u in val_units], "test_engines": int(len(te)),
    "test_critical_engines": int(crit.sum()), "test_alert_positives_rul_le_30": int((y_te <= ALERT_HORIZON).sum()),
    "val_truncation_samples": int(len(va_trunc)),
    "lifetime_min": int(hist.groupby("engine_id")["cycle"].max().min()),
    "lifetime_max": int(hist.groupby("engine_id")["cycle"].max().max()),
    "lifetime_mean": round(float(hist.groupby("engine_id")["cycle"].max().mean()), 1),
}
print("data", log["data"])

# ------------------------------------------------------------------------------------
# 1. Model comparison: snapshot (SAA v1) vs temporal features (SAA v2)
# ------------------------------------------------------------------------------------
SNAP = feature_columns("snapshot")
TEMP = feature_columns("temporal")


def evaluate(name, family, feats, model, scale=False):
    m = make_pipeline(MinMaxScaler(), model) if scale else model
    t0 = time.time()
    m.fit(tr[feats], y_tr)
    secs = time.time() - t0
    pv = np.clip(m.predict(va[feats]), 0, None)
    pt = np.clip(m.predict(te[feats]), 0, None)
    row = {"model": name, "features": family, "val_rmse": round(rmse(y_va, pv), 2), **{f"test_{k}": v for k, v in summary(y_te, pt).items()},
           "test_rmse_critical": round(rmse(y_te[crit], pt[crit]), 2), "test_rmse_noncritical": round(rmse(y_te[~crit], pt[~crit]), 2),
           "train_time_s": round(secs, 2)}
    print(row)
    return row, pt, m


rows, preds = [], {"engine_id": te["engine_id"], "unit": te["unit"], "rul_true": y_te}
specs = [
    ("Linear Regression", "snapshot", SNAP, LinearRegression(), False),
    ("Random Forest", "snapshot", SNAP, RandomForestRegressor(n_estimators=300, max_depth=10, min_samples_leaf=5, random_state=SEED, n_jobs=-1), False),
    ("Gradient Boosting", "snapshot", SNAP, GradientBoostingRegressor(n_estimators=300, max_depth=3, learning_rate=0.05, random_state=SEED), False),
    ("Linear Regression", "temporal", TEMP, LinearRegression(), False),
    ("Random Forest", "temporal", TEMP, RandomForestRegressor(n_estimators=300, max_depth=10, min_samples_leaf=5, random_state=SEED, n_jobs=-1), False),
    ("Hist. Gradient Boosting", "temporal", TEMP, hgb(), False),
]
for name, fam, feats, model, scale in specs:
    r, p, _ = evaluate(name, fam, feats, model, scale)
    rows.append(r)
    preds[f"{name}|{fam}"] = p


# windowed MLP: a neural sequence model trainable with scikit-learn (30 x 15 raw window)
def windows(df, is_last=False):
    X, y = [], []
    sc_cols = OP_SETTINGS + INFORMATIVE_SENSORS
    for _, g in df.groupby("engine_id", sort=True):
        v = g.sort_values("cycle")[sc_cols].to_numpy()
        lab = g.sort_values("cycle")["rul_capped"].to_numpy()
        if is_last:
            seq = v[-WINDOW:] if len(v) >= WINDOW else np.vstack([np.repeat(v[:1], WINDOW - len(v), 0), v])
            X.append(seq.ravel())
            continue
        for i in range(len(v) - WINDOW + 1):
            X.append(v[i:i + WINDOW].ravel())
            y.append(lab[i + WINDOW - 1])
    return np.array(X), np.array(y)


mm = MinMaxScaler().fit(tr[OP_SETTINGS + INFORMATIVE_SENSORS])
scale_df = lambda d: d.assign(**dict(zip(OP_SETTINGS + INFORMATIVE_SENSORS, mm.transform(d[OP_SETTINGS + INFORMATIVE_SENSORS]).T, strict=True)))  # noqa: E731
Xw_tr, yw_tr = windows(scale_df(tr))
Xw_va, yw_va = windows(scale_df(va))
Xw_te, _ = windows(scale_df(fleet), is_last=True)
mlp = MLPRegressor(hidden_layer_sizes=(128, 64), alpha=1e-3, learning_rate_init=1e-3, batch_size=128, max_iter=200,
                   early_stopping=True, validation_fraction=0.1, n_iter_no_change=10, random_state=SEED)
t0 = time.time()
mlp.fit(Xw_tr, yw_tr)
secs = time.time() - t0
pv, pt = np.clip(mlp.predict(Xw_va), 0, None), np.clip(mlp.predict(Xw_te), 0, None)
r = {"model": "Windowed MLP", "features": "window 30", "val_rmse": round(rmse(yw_va, pv), 2), **{f"test_{k}": v for k, v in summary(y_te, pt).items()},
     "test_rmse_critical": round(rmse(y_te[crit], pt[crit]), 2), "test_rmse_noncritical": round(rmse(y_te[~crit], pt[~crit]), 2),
     "train_time_s": round(secs, 2)}
print(r)
rows.append(r)
preds["Windowed MLP|window 30"] = pt

# LSTM from SAA v1 (Keras run, read back, not retrained)
lstm = pd.read_csv(V1 / "lstm_test_predictions.csv").set_index("unit").loc[te["unit"]]
v1 = json.loads((V1 / "lstm_results.json").read_text())
pl = lstm["pred_LSTM"].to_numpy()
assert np.allclose(lstm["RUL"].to_numpy(), y_te)
r = {"model": "LSTM (SAA v1)", "features": "window 30", "val_rmse": v1["val_rmse"], **{f"test_{k}": v for k, v in summary(y_te, pl).items()},
     "test_rmse_critical": round(rmse(y_te[crit], pl[crit]), 2), "test_rmse_noncritical": round(rmse(y_te[~crit], pl[~crit]), 2),
     "train_time_s": v1["train_time_s"]}
rows.append(r)
preds["LSTM (SAA v1)|window 30"] = pl
comparison = pd.DataFrame(rows)
comparison.to_csv(RES / "model_comparison.csv", index=False)
pd.DataFrame(preds).to_csv(RES / "test_predictions_all_models.csv", index=False)

# reproduction check against SAA v1
v1b = json.loads((V1 / "baseline_results.json").read_text())
repro = {}
for name in ("Linear Regression", "Random Forest", "Gradient Boosting"):
    row = comparison[(comparison.model == name) & (comparison.features == "snapshot")].iloc[0]
    repro[name] = {"v1_test_rmse": v1b[name]["test_rmse"], "v2_test_rmse": row["test_rmse"],
                   "v1_nasa": v1b[name]["test_nasa_score"], "v2_nasa": row["test_nasa_score"]}
log["reproduction"] = repro
print("repro", repro)

# fig11: RMSE overall vs critical zone
fig, ax = plt.subplots(figsize=(7.2, 3.6))
order = comparison.copy()
short = {"Linear Regression": "Linear", "Random Forest": "Random\nForest", "Gradient Boosting": "Gradient\nBoosting",
         "Hist. Gradient Boosting": "Hist. Grad.\nBoosting", "Windowed MLP": "Windowed\nMLP", "LSTM (SAA v1)": "LSTM\n(SAA v1)"}
labels = [f"{short[m]}\n[{f}]" for m, f in zip(order["model"], order["features"], strict=True)]
x = np.arange(len(order))
ax.bar(x - 0.2, order["test_rmse"], width=0.38, color=BLUE, label="All 100 test engines")
ax.bar(x + 0.2, order["test_rmse_critical"], width=0.38, color=ORANGE, label="Critical zone (true RUL < 50)")
for xi, (a, b) in enumerate(zip(order["test_rmse"], order["test_rmse_critical"], strict=True)):
    ax.text(xi - 0.2, a + 0.4, f"{a:.1f}", ha="center", fontsize=7, color=INK2)
    ax.text(xi + 0.2, b + 0.4, f"{b:.1f}", ha="center", fontsize=7, color=INK2)
ax.set_xticks(x, labels, fontsize=7)
ax.set_ylabel("Test RMSE (cycles)")
ax.legend(loc="upper right", fontsize=8)
ax.set_title("Snapshot vs temporal features vs sequence models (FD001 test set)", fontsize=10, color=INK, loc="left")
save(fig, "fig11_model_comparison_v2.png")

# ------------------------------------------------------------------------------------
# 2. Uncertainty: conformalized quantile intervals (production model)
# ------------------------------------------------------------------------------------
ehm = EngineHealthModel(features=TEMP, alpha=0.2).fit(tr, y_tr)
raw_p, raw_lo, raw_hi = ehm._raw(te)
ehm.calibrate(va_trunc, va_trunc["rul_capped"])
iv = ehm.predict(te)
y_te_cap = np.minimum(y_te, RUL_CAP)
iv_val = ehm.predict(va_trunc)
interval = {
    "alpha": 0.2, "nominal_coverage": 0.8, "q_hat_cycles": round(ehm.q_hat_, 2),
    "test_coverage_uncalibrated": round(interval_coverage(y_te_cap, np.clip(raw_lo, 0, None), raw_hi), 3),
    "test_coverage_calibrated": round(interval_coverage(y_te_cap, iv["rul_p10"], iv["rul_p90"]), 3),
    "test_coverage_calibrated_critical": round(interval_coverage(y_te_cap[crit], iv["rul_p10"][crit], iv["rul_p90"][crit]), 3),
    "test_mean_width_uncalibrated": round(interval_width(np.clip(raw_lo, 0, None), raw_hi), 1),
    "test_mean_width_calibrated": round(interval_width(iv["rul_p10"], iv["rul_p90"]), 1),
    "test_mean_width_critical": round(interval_width(iv["rul_p10"][crit], iv["rul_p90"][crit]), 1),
    "test_p50_rmse": round(rmse(y_te, iv["rul_p50"]), 2),
    "test_p50_rmse_critical": round(rmse(y_te[crit], iv["rul_p50"].to_numpy()[crit]), 2),
    "test_share_true_below_p10": round(float(np.mean(y_te_cap < iv["rul_p10"])), 3),
    "test_share_true_above_p90": round(float(np.mean(y_te_cap > iv["rul_p90"])), 3),
    "val_trunc_coverage": round(interval_coverage(va_trunc["rul_capped"], iv_val["rul_p10"], iv_val["rul_p90"]), 3),
}
log["interval"] = interval
print("interval", interval)

fig, ax = plt.subplots(figsize=(7.2, 3.4))
o = np.argsort(y_te)
xs = np.arange(len(o))
ax.fill_between(xs, iv["rul_p10"].to_numpy()[o], iv["rul_p90"].to_numpy()[o], color="#b7d3f6", label="Calibrated P10–P90 interval", step="mid")
ax.plot(xs, iv["rul_p50"].to_numpy()[o], color=BLUE, lw=1.6, label="Predicted RUL (point)")
ax.plot(xs, y_te[o], color=INK, lw=1.2, ls="--", label="True RUL")
ax.axhline(RUL_CAP, color=INK2, lw=0.8, ls=":")
ax.text(1, RUL_CAP + 3, "cap = 125 cycles", fontsize=7, color=INK2)
ax.set_xlabel("Test engines, sorted by true RUL")
ax.set_ylabel("RUL (cycles)")
ax.set_ylim(-5, 160)
ax.legend(loc="lower right", fontsize=8)
ax.set_title(f"Production model: 80 % interval, measured coverage {interval['test_coverage_calibrated']:.0%} on the 100 test engines",
             fontsize=10, color=INK, loc="left")
save(fig, "fig12_intervals.png")

# ------------------------------------------------------------------------------------
# 3. Health monitoring without labels: health index + anomaly score
# ------------------------------------------------------------------------------------
hm = HealthMonitor().fit(tr)
va = va.assign(health_index=hm.health_index(va), anomaly_score=hm.anomaly_score(va))
rho = stats.spearmanr(va["health_index"], va["rul"]).statistic
mask = (va["rul"] < CRITICAL_RUL) | (va["rul"] > RUL_CAP)
auc_anom = roc_auc_score((va.loc[mask, "rul"] < CRITICAL_RUL).astype(int), va.loc[mask, "anomaly_score"])
auc_hi = roc_auc_score((va.loc[mask, "rul"] < CRITICAL_RUL).astype(int), -va.loc[mask, "health_index"])
# sustained alarm: anomaly_score >= 0.99 on 5 consecutive cycles
lead, false_alarm_engines = [], 0
for _, g in va.sort_values("cycle").groupby("engine_id"):
    flag = (g["anomaly_score"].to_numpy() >= 0.99).astype(int)
    run = np.convolve(flag, np.ones(5, int), "valid")
    idx = np.where(run == 5)[0]
    if len(idx):
        first = idx[0] + 4
        lead.append(int(g["rul"].to_numpy()[first]))
        if g["rul"].to_numpy()[first] > RUL_CAP:
            false_alarm_engines += 1
healthy_alarm_rate = float(np.mean(va.loc[va["rul"] > RUL_CAP, "anomaly_score"] >= 0.99))
health = {"hi_spearman_vs_rul": round(float(rho), 3), "auc_anomaly_critical_vs_healthy": round(float(auc_anom), 3),
          "auc_health_index_critical_vs_healthy": round(float(auc_hi), 3), "sustained_alarm_engines": len(lead),
          "val_engines": int(va["engine_id"].nunique()), "median_alarm_lead_cycles": float(np.median(lead)) if lead else None,
          "min_alarm_lead_cycles": int(min(lead)) if lead else None, "max_alarm_lead_cycles": int(max(lead)) if lead else None,
          "alarms_while_healthy_engines": false_alarm_engines, "healthy_cycle_alarm_rate": round(healthy_alarm_rate, 4),
          "pca_explained_variance": round(float(hm.pca_.explained_variance_ratio_[0]), 3)}
log["health"] = health
print("health", health)

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0))
for i, (eid, g) in enumerate(list(va.groupby("engine_id"))[:5]):
    c = [BLUE, ORANGE, AQUA, VIOLET, MAGENTA][i]
    axes[0].plot(g["rul"], g["health_index"], color=c, lw=1.1, label=eid.replace("FD001-HIST-", "engine "))
axes[0].invert_xaxis()
axes[0].set_xlabel("True RUL (cycles, failure at 0)")
axes[0].set_ylabel("Health index (1 = healthy, 0 = failure ref.)")
axes[0].legend(fontsize=6.5, loc="lower left")
axes[0].set_title("Health index, 5 validation engines", fontsize=9, loc="left", color=INK)
bins = pd.cut(va["rul"], [-1, 25, 50, 75, 100, 125, 400], labels=["0–25", "26–50", "51–75", "76–100", "101–125", ">125"])
m = va.groupby(bins, observed=True)["anomaly_score"].mean()
axes[1].bar(range(len(m)), m.values, color=BLUE, width=0.6)
for xi, v in enumerate(m.values):
    axes[1].text(xi, v + 0.01, f"{v:.2f}", ha="center", fontsize=7, color=INK2)
axes[1].set_xticks(range(len(m)), m.index, fontsize=7)
axes[1].set_xlabel("True RUL bucket (cycles)")
axes[1].set_ylabel("Mean anomaly score (0–1)")
axes[1].set_title("Anomaly score rises near failure", fontsize=9, loc="left", color=INK)
save(fig, "fig13_health_monitoring.png")

# ------------------------------------------------------------------------------------
# 4. Reliability: Kaplan-Meier + Weibull on the 100 run-to-failure lifetimes
# ------------------------------------------------------------------------------------
life = hist.groupby("engine_id")["cycle"].max().to_numpy()
fleet_obs = fleet.groupby("engine_id")["cycle"].max().to_numpy()
km = kaplan_meier(life, np.ones_like(life))
km_c = kaplan_meier(np.r_[life, fleet_obs], np.r_[np.ones_like(life), np.zeros_like(fleet_obs)])
wb = weibull_fit(life)
log["reliability"] = wb
print("weibull", wb)
km.to_csv(RES / "kaplan_meier.csv", index=False)

fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.step(np.r_[0, km["cycle"]], np.r_[1, km["survival"]], where="post", color=BLUE, lw=1.6, label="Kaplan–Meier (100 failures)")
ax.step(np.r_[0, km_c["cycle"]], np.r_[1, km_c["survival"]], where="post", color=AQUA, lw=1.2, ls="--",
        label="Kaplan–Meier + 100 in-service engines (censored)")
t = np.linspace(0, 400, 400)
ax.plot(t, stats.weibull_min.sf(t, wb["beta"], 0, wb["eta"]), color=ORANGE, lw=1.6,
        label=f"Weibull fit (β = {wb['beta']}, η = {wb['eta']} cycles)")
ax.axvline(wb["b10"], color=INK2, lw=0.8, ls=":")
ax.text(wb["b10"] - 4, 0.55, f"B10 = {wb['b10']:.0f} cycles", fontsize=7, color=INK2, ha="right")
ax.set_xlabel("Cycles since start of record")
ax.set_ylabel("Share of engines not yet failed")
ax.legend(fontsize=7, loc="upper right")
ax.set_title("Fleet reliability: wear-out (β > 1)", fontsize=10, loc="left", color=INK)
save(fig, "fig14_reliability.png")

# ------------------------------------------------------------------------------------
# 5. From prediction to decision: cost-based alert threshold
# ------------------------------------------------------------------------------------
y_va_trunc = va_trunc["rul"].to_numpy()
pos_va = y_va_trunc <= ALERT_HORIZON
pos_te = y_te <= ALERT_HORIZON
ks = np.arange(0, 101)
alert_rows = {}
for ratio in (5, 10, 20):
    for stat_name in ("rul_p10", "rul_p50"):
        cost = [ratio * np.sum(pos_va & ~(iv_val[stat_name].to_numpy() <= k)) + np.sum(~pos_va & (iv_val[stat_name].to_numpy() <= k)) for k in ks]
        k_star = int(ks[int(np.argmin(cost))])
        a = iv[stat_name].to_numpy() <= k_star
        tp, fp, fn = int(np.sum(a & pos_te)), int(np.sum(a & ~pos_te)), int(np.sum(~a & pos_te))
        alert_rows[f"{stat_name}|{ratio}"] = {"policy": stat_name, "cost_ratio_fn_fp": ratio, "threshold_cycles": k_star,
                                              "test_tp": tp, "test_fp": fp, "test_fn": fn,
                                              "test_recall": round(tp / max(tp + fn, 1), 3), "test_precision": round(tp / max(tp + fp, 1), 3),
                                              "test_cost": int(ratio * fn + fp)}
# point-model policy for comparison: LSTM and point HGB at the same threshold logic (threshold picked on val for HGB)
alert = pd.DataFrame(alert_rows.values())
alert.to_csv(RES / "alert_policies.csv", index=False)
log["alert"] = alert_rows
print(alert)
chosen = alert_rows["rul_p10|10"]
ALERT_K = chosen["threshold_cycles"]

fig, ax = plt.subplots(figsize=(6.2, 3.0))
for stat_name, c, lab in (("rul_p10", BLUE, "Alert on P10 (lower bound)"), ("rul_p50", ORANGE, "Alert on point estimate")):
    cost = [10 * np.sum(pos_va & ~(iv_val[stat_name].to_numpy() <= k)) + np.sum(~pos_va & (iv_val[stat_name].to_numpy() <= k)) for k in ks]
    ax.plot(ks, cost, color=c, lw=1.6, label=lab)
    kk = int(ks[int(np.argmin(cost))])
    ax.scatter([kk], [min(cost)], color=c, s=40, zorder=3, edgecolor="white", linewidth=1.5)
    ax.annotate(f"k* = {kk}", (kk, min(cost)), xytext=(kk + (8 if stat_name == "rul_p50" else -22), min(cost) + (70 if stat_name == "rul_p50" else 45)),
                fontsize=7, color=INK2, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6))
ax.set_xlabel("Alert threshold k (alert if statistic ≤ k cycles)")
ax.set_ylabel("Validation cost (10 × missed + 1 × early)")
ax.legend(fontsize=8)
ax.set_title("Choosing the alert threshold from a cost table (illustrative 10:1)", fontsize=10, loc="left", color=INK)
save(fig, "fig15_alert_cost.png")

# ------------------------------------------------------------------------------------
# 6. Fleet decision: simulated fleet, risk before next check, ranking
# ------------------------------------------------------------------------------------
AS_OF = "2026-11-19"
aircraft = simulate_aircraft()
util = simulate_utilization(aircraft)
ustats = utilization_stats(util)
assign = assign_engines(aircraft, list(te["engine_id"]))
te_h = te.assign(health_index=hm.health_index(te), anomaly_score=hm.anomaly_score(te), top_drivers=hm.top_drivers(te))
snap = (te_h[["engine_id", "cycle", "rul", "health_index", "anomaly_score", "top_drivers"]]
        .join(iv.set_index(te_h.index))
        .merge(assign, on="engine_id").merge(aircraft[["tail_id", "next_check_date", "typecode"]], on="tail_id")
        .merge(ustats, on="tail_id"))
snap["days_to_next_check"] = (pd.to_datetime(snap["next_check_date"]) - pd.Timestamp(AS_OF)).dt.days
rec = rank_inspections(snap, ALERT_K, AS_OF)
rec["fails_before_check_truth"] = rec["rul"] < rec["cycles_to_next_check"]
bands = rec["band"].value_counts().to_dict()
truth = rec["fails_before_check_truth"]
fleet_eval = {"alert_threshold_cycles": ALERT_K, "bands": bands, "engines_failing_before_check_truth": int(truth.sum()),
              "of_which_red": int((truth & (rec["band"] == "RED")).sum()), "of_which_amber": int((truth & (rec["band"] == "AMBER")).sum()),
              "of_which_green": int((truth & (rec["band"] == "GREEN")).sum()),
              "red_engines_not_failing_before_check": int((~truth & (rec["band"] == "RED")).sum()),
              "aircraft": int(len(aircraft)), "mean_cycles_per_day": round(float(ustats["cycles_per_day"].mean()), 2)}
log["fleet"] = fleet_eval
print("fleet", fleet_eval)
rec.to_csv(RES / "inspection_recommendations.csv", index=False)
rec.head(10)[["rank", "engine_id", "tail_id", "position", "band", "rul_p10", "rul_p50", "rul_p90", "cycles_per_day",
              "days_p10", "days_to_next_check", "risk_before_check", "rul", "reason"]].round(2).to_csv(RES / "top10_queue.csv", index=False)

fig, ax = plt.subplots(figsize=(6.4, 3.4))
for b in ("GREEN", "AMBER", "RED"):
    d = rec[rec["band"] == b]
    ax.scatter(d["days_p10"], d["risk_before_check"], s=26, color=STATUS[b], edgecolor="white", linewidth=1.0,
               label=f"{b.title()} ({len(d)})", zorder=3)
ax.set_xlim(-1, min(45, rec["days_p10"].max() + 2))
ax.set_xlabel("Days until P10 RUL is consumed (at each aircraft's simulated utilisation)")
ax.set_ylabel("P(RUL < cycles to next check)")
ax.legend(fontsize=8, loc="upper right", title="Band", title_fontsize=8)
ax.set_title("Inspection queue: 100 engines on 50 simulated A320-family aircraft", fontsize=10, loc="left", color=INK)
save(fig, "fig16_fleet_risk.png")

# ------------------------------------------------------------------------------------
# 7. Global explanation: permutation importance grouped by sensor
# ------------------------------------------------------------------------------------
pi = permutation_importance(ehm.point_, va_trunc[TEMP], va_trunc["rul_capped"], n_repeats=5, random_state=SEED,
                            scoring="neg_root_mean_squared_error", n_jobs=-1)
imp = pd.Series(pi.importances_mean, index=TEMP)
grouped = imp.groupby(lambda c: c.rsplit("_", 1)[0] if c.startswith("sensor") else c).sum().sort_values(ascending=False)
grouped.round(3).to_csv(RES / "permutation_importance_by_sensor.csv", header=["rmse_increase"])
log["importance_top5"] = grouped.head(5).round(2).to_dict()
# joint check: correlated sensors share signal, so per-sensor permutation understates them
rng = np.random.default_rng(SEED)
base = rmse(va_trunc["rul_capped"], ehm.point_.predict(va_trunc[TEMP]))
sens_cols = [c for c in TEMP if c != "cycle"]
joint = {}
for label, cols in (("all_sensor_features", sens_cols), ("cycle_only", ["cycle"])):
    inc = []
    for _ in range(5):
        Xp = va_trunc[TEMP].copy()
        perm = rng.permutation(len(Xp))
        Xp[cols] = Xp[cols].to_numpy()[perm]
        inc.append(rmse(va_trunc["rul_capped"], ehm.point_.predict(Xp)) - base)
    joint[label] = round(float(np.mean(inc)), 2)
log["importance_joint"] = joint
print("joint importance", joint)
fig, ax = plt.subplots(figsize=(6.0, 3.2))
top = grouped.head(10)[::-1]
ax.barh(range(len(top)), top.values, color=BLUE, height=0.6)
ax.set_yticks(range(len(top)), top.index, fontsize=8)
for yi, v in enumerate(top.values):
    ax.text(v + 0.1, yi, f"{v:.1f}", va="center", fontsize=7, color=INK2)
ax.set_xlabel("RMSE increase when the sensor's features are shuffled (cycles)")
ax.set_title("What the production model relies on (permutation importance)", fontsize=10, loc="left", color=INK)
save(fig, "fig17_permutation_importance.png")

log["runtime_s"] = round(time.time() - T0, 1)
(RES / "saa_v2_results.json").write_text(json.dumps(log, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
print("done in", log["runtime_s"], "s")
