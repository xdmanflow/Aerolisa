# Model card: engine health (fill at M6)

## Model
- **Name / version:** (MLflow registered model + version)
- **Task:** RUL regression with P10 / P50 / P90; "fails within N cycles" alert; anomaly score
- **Algorithm(s):**
- **Training data:** C-MAPSS FD001–FD004 (simulated), preprocessing summary

## Intended use
Demonstration of predictive maintenance decision support on simulated engines. **Not** for real maintenance decisions.

## Evaluation
| Metric | Baseline | Model | Split |
|---|---|---|---|
| RMSE (last cycle, test units) | | | |
| MAE | | | |
| NASA score | | | |
| P10–P90 coverage | | | |
| Alert precision / recall at chosen threshold | | | |

## Threshold choice
Cost table used (missed failure vs early inspection) and the resulting threshold.

## Explanations
How top drivers are computed (SHAP) and how they're shown to users.

## Limits and risks
- Simulated degradation; real engines have maintenance actions, installation changes, sensor faults
- Distribution shift between operating conditions
- What the model must never be used for
