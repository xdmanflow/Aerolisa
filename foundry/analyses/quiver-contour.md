# Quiver and Contour analyses

## Quiver · "Engine health over time"
1. Object set: EngineHealthSnapshot, filter engineId ∈ {FD001-FLEET-076, FD001-FLEET-022} (one RED, one GREEN).
2. Time-series-like XY plot: x = cycle, y = rulP50 with rulP10/rulP90 band; one card per engine.
3. Second plot: healthIndex vs cycle; third: ps30Mean vs cycle.
4. Takeaway text card, written from what you see (locally: FLEET-076 health index goes from 1.15 at cycle 1 to 0.91 sixty cycles before its last cycle, then to 0.14; FLEET-022 is at 0.86 after 39 cycles).
5. Save to the `Aerolisa` project; embed the dashboard in Workshop page 3 if you like.

## Contour · "Fleet KPIs"
Board 1, dataset `gold/inspection_recommendation`:
- Pivot: count by band → KPI.
- Group by tailId: max riskBeforeCheck, sum(alert) → aircraft at risk.
- Histogram: daysP10.

Board 2, dataset `gold/engine_life_records`:
- Filter failed = true → histogram of observedCycles (lifetime distribution, compare with fig2 of the report).
- Summary: mean / min / max lifetime (expect 206.3 / 128 / 362).

Board 3, dataset `gold/engine_health_model_metrics`: a table of model versions over time (model governance).

Each board ends with a one-line takeaway (data-analyst habit).
