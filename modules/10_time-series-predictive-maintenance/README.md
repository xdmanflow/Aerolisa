# Module 10 · Time series & predictive maintenance

**Roles:** DS · AI · **Size:** 3 weekends · **Priority:** P0 · **Builds:** Aerolisa M6 (engine health v2), M7 (planner)

## Why this matters
Predictive maintenance is the flagship Skywise use case: S.Predictive Maintenance+ and S.Health Monitoring exist to turn unscheduled maintenance into scheduled maintenance. This module is where my SAA research on C-MAPSS becomes industrial-grade: multiple operating conditions, uncertainty, alert costs, and a decision at the end.

## 🎯 Apprenticeship level (must)
**Time series**
- [ ] Trend, seasonality, noise; stationarity; autocorrelation; resampling; rolling windows; lags; leakage in time
- [ ] Baseline forecasting ideas (naive, moving average, exponential smoothing) and backtesting

**Predictive maintenance**
- [ ] The three framings: RUL **regression**, "fails within N cycles" **classification**, **survival** (time-to-event)
- [ ] C-MAPSS specifics: FD001–FD004, operating conditions, fault modes, piecewise-linear RUL clipping, NASA asymmetric score, last-cycle evaluation on test units
- [ ] Operating-condition normalization (cluster by settings, normalize sensors per cluster)
- [ ] Health indicators: building one degradation score from many sensors
- [ ] Anomaly detection: z-scores, rolling deviation, Isolation Forest, reconstruction error (concept)
- [ ] **Uncertainty:** quantile regression or prediction intervals; why a RUL without an interval is hard to act on
- [ ] Decision layer: alert precision vs recall, cost of a missed failure vs an early removal, threshold choice
- [ ] Deep learning basics in **PyTorch**: tensors, autograd, `nn.Module`, training loop, sliding windows, a 1D-CNN or LSTM on C-MAPSS

## 🚀 Pro level
- [ ] Conformal prediction for calibrated intervals
- [ ] Transformer or temporal convolution models; comparison with boosting on the same split
- [ ] Transfer between FD sets (train on FD001, test on FD003)
- [ ] PHM08 challenge data

## Steps
**Weekend 1: time series + the full C-MAPSS problem**
1. Learn: *Forecasting: Principles and Practice*, chapters on time series graphics and decomposition (concepts); reread the Saxena et al. C-MAPSS paper; my own SAA report.
2. Practice: FD002/FD004 operating-condition normalization; health indicator; compare per-condition sensor trends.
3. Apply: Aerolisa M6, multi-condition features.

**Weekend 2: uncertainty, anomalies, decisions**
4. Learn: quantile regression (LightGBM quantile objective), Isolation Forest docs.
5. Practice: RUL with 10th/90th percentile intervals; anomaly score per cycle; cost-based alert threshold.
6. Apply: Aerolisa M6 snapshots with `rul_p10`, `rul_p50`, `rul_p90`, `anomaly_score`; M7 planner reads them.

**Weekend 3: deep learning**
7. Learn: PyTorch "Learn the basics" tutorial; one LSTM/CNN-for-RUL paper or blog.
8. Practice: 1D-CNN or LSTM on sliding windows; same split and metrics as the boosting model.
9. Apply: Aerolisa M6 model comparison table updated; model card written.

## Exit test (90 min, no AI, docs allowed)
On FD002: normalized features, a model with prediction intervals, an alert threshold justified by a cost table, and a one-paragraph recommendation to a maintenance planner.

## Resources
- C-MAPSS paper (Saxena et al., 2008) · NASA PCoE data · FPP (concepts) · PyTorch tutorials · lifelines docs

## Gaps found
-

## Notes
-

## Work
[`work/`](work)
