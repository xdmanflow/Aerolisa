# ADR 0008: Temporal-feature gradient boosting in production, LSTM kept as research baseline

**Status:** accepted (Nov. 2026), based on SAA v2 results

**Context:** SAA v1 found the LSTM best (test RMSE 15.41, NASA 423.3). SAA v2 gave tabular models 30-cycle rolling
mean/std/slope features computed by a Spark window.

**Decision:** production model = HistGradientBoosting (P50) + quantile models (P10/P90) + conformal calibration.

**Why:** better test RMSE (14.01 vs 15.41) and NASA score (292 vs 423), similar critical-zone error (5.69 vs 6.14),
training in ~2 s vs ~220 s, native quantile loss for intervals, scikit-learn only (simple ModelAdapter, no GPU), and
features a planner can read (rolling slope of Ps30). The windowed MLP has the best critical-zone error (3.89) and is the
candidate for a future ensemble.

**Consequences:** features must be computed identically online and offline (one Spark window definition, tested);
sequence models stay in `research/` until they beat the production model on the decision metrics, not only RMSE.
