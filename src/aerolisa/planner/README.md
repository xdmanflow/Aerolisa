# Planner

> Ranks engines to inspect first by combining predicted remaining life (with its uncertainty), anomaly signals and **real aircraft utilization**, and explains every rank in plain English.

**Milestone:** M7 (simple version can appear earlier in the Foundry edition, M4)
**May import:** `aerolisa.core`, `aerolisa.engine_health`, `aerolisa.fleet`
**Learn:** Renaissance 08, 10

## How it works
1. Read each engine's latest `EngineHealthSnapshot` (P10 / P50 / P90, anomaly score, top drivers).
2. Read its aircraft's cycles per day from `fleet`.
3. **Cycles → days:** days to threshold ≈ RUL ÷ cycles per day, computed for P10, P50 and P90.
4. **Risk:** probability that the engine reaches the threshold before its next planned check (from the P10–P90 spread), adjusted by the anomaly score. The exact formula is documented here when chosen, with its assumptions.
5. **Rank + reason:** a sentence built from the drivers, e.g. "high utilization (7.1 cycles/day), P10 RUL 18 cycles, drift on T50".
6. **What-if:** risk if the inspection is delayed by N days.
7. Output `gold/inspection_recommendation`; the app and API read it as `InspectionRecommendation` objects.

## Steps
1. [ ] Write the risk formula and its assumptions here first; review it against Renaissance 08
2. [ ] Implement cycles → days with real utilization; unit tests with hand-computed cases
3. [ ] Risk + ranking + reason generator; tests on edge cases (no flights, very wide interval)
4. [ ] What-if function
5. [ ] `gold/inspection_recommendation` transform
6. [ ] Exposed through the API and the app's Inspection queue

## Definition of done
- [ ] Ranked list with an explanation for every engine
- [ ] Visible in the app and through the API
- [ ] The 3-minute demo explains one decision end to end
