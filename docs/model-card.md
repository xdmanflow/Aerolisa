# Model card: engine-health model `aerolisa-ehm-1.0.0`

## Model
- **What it outputs, per engine-cycle:** RUL point estimate (P50) and a calibrated 80 % interval (P10–P90);
  health index (1 = healthy reference, 0 = failure reference); anomaly score (0–1); top drifting sensors; alert flag.
- **Algorithms:** scikit-learn `HistGradientBoostingRegressor` (squared error for P50; quantile loss 0.1 / 0.9),
  widened by conformalized quantile regression (Romano et al., 2019). PCA health index. Isolation Forest anomaly score.
- **Features (46):** engine age in cycles + rolling mean, std and least-squares slope over the last 30 cycles
  for the 15 informative sensors (sensors 1, 5, 10, 16, 18, 19 dropped: near-constant in FD001).
- **Target:** RUL capped at 125 cycles (piecewise-linear target).
- **Training data:** NASA C-MAPSS FD001, 80 run-to-failure engines; 20 engines held out (same split as SAA v1)
  for calibration (10 random cut-offs per engine = 200 samples) and threshold choice.
- **Code:** `src/aerolisa/engine_health/bundle.py::train_bundle` (identical in Foundry).

## Intended use
Demonstrating decision support for engine inspection planning on **simulated** engines.
**Not** for real maintenance decisions, airworthiness, or any certified use.

## Evaluation (official FD001 protocol: last cycle of each of the 100 test engines)
| Metric | Baseline (SAA v1 Random Forest) | This model |
|---|---|---|
| RMSE (cycles) | 18.09 | **13.98** |
| MAE | 12.98 | 10.14 |
| NASA asymmetric score | 914.7 | **291.1** |
| RMSE in critical zone (true RUL < 50, n = 30) | 16.48 | **5.69** |
| P10–P90 coverage vs capped truth (target 80 %) | n/a | **81 %** (93 % in critical zone) |
| Mean interval width | n/a | 32.2 cycles (19.7 in critical zone) |
| Share of predictions later than truth | 0.58 | 0.61 (point) · P10 below truth for 85 % of engines |

## Alert threshold
Rule: alert if `rul_p10 ≤ k`. Cost table (illustrative): missed failure within 30 cycles = 10, unnecessary early
inspection = 1. k chosen on validation cut-offs: **k = 25** (same k for cost ratios 5, 10 and 20).
On test: 25/25 positives caught, 2 false alarms. Using the point estimate instead (k = 31) misses 3 positives.

## Explanations
- Per engine: sensors with the largest drift from the healthy fleet reference, in σ, in the direction that
  indicates degradation (e.g. "sensor_11 (Ps30) +3.7σ").
- Global: permutation importance. Shuffling all sensor features together raises RMSE by 40.3 cycles; shuffling
  engine age alone by 3.6. Per-sensor importance is spread because sensors are strongly correlated.

## Limits and risks
- Simulated degradation, one operating condition, one fault mode (HPC). Real engines have maintenance events,
  sensor faults, installation effects and several failure modes.
- The interval guarantee is marginal and assumes new engines resemble the calibration engines; coverage is measured, not assumed.
- Predictions above ~125 cycles are saturated by design (the cap): "≥ 125" means "no visible degradation yet".
- The point estimate is late (optimistic) for 61 % of engines; decisions therefore use P10, not P50.
- The health-index/anomaly reference comes from training engines; a different engine type needs re-fitting.
