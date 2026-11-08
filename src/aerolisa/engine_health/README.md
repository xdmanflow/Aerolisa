# Engine health

> Remaining-useful-life prediction **with intervals**, anomaly detection and per-engine explanations on NASA C-MAPSS, evaluated without leakage and tracked in MLflow. Produces `EngineHealthSnapshot` objects for the planner.

**Milestones:** M1 (baseline + one model, FD001) · M6 (full version)
**May import:** `aerolisa.core`
**Learn:** Renaissance 08, 09, 10 · builds on my Turbofan-RUL research (SAA project)

## Why
Predictive maintenance is the core promise of fleet data platforms: see a degradation early enough to turn an unscheduled removal into a planned one. A prediction without an interval or an explanation is hard for an engineer to act on; this module delivers all three.

## Outputs
`gold/engine_health_snapshot`, one row per engine per as-of cycle: `engine_id`, `cycle`, `rul_p10`, `rul_p50`, `rul_p90`, `anomaly_score`, `health_index`, `alert` (bool), `top_drivers`, `model_version`.

## Steps
**M1**
1. [ ] Features: drop constant sensors; rolling means; clipped RUL label (value documented)
2. [ ] Baseline (mean RUL) + one model; GroupKFold by unit; RMSE + NASA score
3. [ ] Snapshot for each test engine

**M6**
4. [ ] FD001–FD004; operating-condition clustering and per-condition normalization
5. [ ] Comparison: baseline, linear, random forest, LightGBM/XGBoost, 1D-CNN or LSTM (PyTorch)
6. [ ] Quantile models → P10 / P50 / P90; measure interval coverage
7. [ ] Anomaly score (Isolation Forest or health-indicator deviation)
8. [ ] Alert model "fails within N cycles" with a cost-based threshold
9. [ ] SHAP top drivers per snapshot
10. [ ] Reliability view: Kaplan–Meier and Weibull on lifetimes
11. [ ] MLflow tracking + registry; pipeline loads the registered model
12. [ ] `reports/evaluation.md` + [docs/model-card.md](../../../docs/model-card.md)

## Definition of done
- [ ] Beats the baseline on the official test split, reported honestly
- [ ] Every snapshot has an interval, an anomaly score and top drivers
- [ ] Fully reproducible from a clean clone

## Results
_Added at M1 and M6._
