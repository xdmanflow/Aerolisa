# Planner: from predicted cycles to an inspection decision

Code: `src/aerolisa/planner/risk.py` (Python) and `foundry/functions-repo/src/index.ts` (TypeScript, same formula, verified equal).

1. **Utilisation.** `cycles_per_day` = mean daily cycles of the aircraft over the last 30 days (with a 95 % CI).
2. **Cycles until the next maintenance opportunity:** `cycles_to_check = days_to_next_check × cycles_per_day`.
3. **Risk before the check:** `risk = P(RUL < cycles_to_check)`, read from a piecewise-linear CDF through
   (P10, 0.1), (P50, 0.5), (P90, 0.9), extended linearly to 0 and 1 (tails of length ¼ of the adjacent gap).
   Assumption: the conformal interval is a reasonable 80 % predictive interval (measured: 81 % coverage).
4. **Alert** (model level): `rul_p10 ≤ 25` cycles (cost-based threshold, see the model card).
5. **Band:** RED if alert or risk ≥ 0.5 · AMBER if risk ≥ 0.1 · GREEN otherwise.
6. **Rank:** alert first, then risk (desc), then days until P10 is consumed (asc).
7. **Reason:** P10 in cycles and days, risk before the check, anomaly score if ≥ 0.99, top drifting sensors.
8. **What-if:** risk recomputed with `days_to_next_check + delay`.

## Demo fleet result (simulated, as of 2026-11-19)
50 aircraft, 100 engines, mean 4.8 cycles/day, next maintenance slot in 2–21 days.
Bands: 34 RED, 12 AMBER, 54 GREEN. Using the simulation's ground truth, 31 engines would reach failure before
their next slot: 28 are RED, 2 AMBER, 1 GREEN; 6 RED engines would not have failed before the slot (early inspections).

## Limits
- Days are derived from simulated degradation cycles; on real data, cycles come from real flights (OpenSky step).
- Utilisation uncertainty (the CI) is shown but not yet propagated into the risk.
- The risk ignores the cost of grounding the aircraft for the inspection; that is the planner's decision, not the model's.
