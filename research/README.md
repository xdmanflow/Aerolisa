# Research: Scientific Approach Application (SAA, CESI)

**Predictive maintenance of turbofan engines: from remaining-useful-life prediction to fleet inspection decisions.**

| Version | What | Where |
|---|---|---|
| SAA v1 (Feb. 2026) | LR / RF / GB vs LSTM on FD001; RMSE + NASA score; error by zone | `saa_v1/` (scripts, notebooks, Keras model, results, fig1–fig10, original report) |
| SAA v2 (Nov. 2026) | + temporal features, windowed MLP, conformal intervals, health index & anomaly, reliability, cost-based alert, fleet decision; implemented on Foundry | `run_experiments.py`, `results/` (incl. `run_log.txt`), `figures/fig11–fig18`, `report/SAA_Report_Predictive_Maintenance_v2.docx` |

Reproduce SAA v2 (≈ 2 min on CPU): `python research/run_experiments.py`.
The LSTM is not retrained here (TensorFlow not required); its stored SAA v1 test predictions are re-scored
with the same metric code, which reproduces 15.41 / 423.3 exactly. The SAA v1 baselines reproduce to within
0.01 RMSE (scikit-learn version change).

## Research questions
- **RQ1** Which sensors carry signal? (v1, unchanged)
- **RQ2** Snapshot vs sequence: is the LSTM's advantage about recurrence or about temporal information?
- **RQ3** Does the metric (RMSE vs NASA score) change the conclusion? (v1, extended with the late-prediction share)
- **RQ4** Can we attach a calibrated uncertainty to each prediction?
- **RQ5** Does using the uncertainty improve maintenance decisions (alerts, fleet ranking)?

## Key results
`results/saa_v2_results.json`, `results/model_comparison.csv`, `results/alert_policies.csv`, `results/top10_queue.csv`.
