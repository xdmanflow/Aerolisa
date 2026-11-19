# AIP Logic: "Explain this engine's risk"

A grounded explanation, not a chatbot: the function reads ontology properties only and
must say "not available" when a value is missing. It never schedules anything itself;
the planner clicks the action.

## Function
- **Input:** `engine` (Engine object)
- **Retrieval blocks (Get object properties / traverse links):**
  - Engine: engineId, tailId, position, rulP10, rulP50, rulP90, healthIndex, anomalyScore, topDrivers, band, modelVersion
  - linked InspectionRecommendation (latest): riskBeforeCheck, daysP10, daysToNextCheck, cyclesPerDay, reason, status
  - linked Aircraft: registration, model, cyclesPerDay
  - linked EngineHealthSnapshot (last 30 by cycle): rulP50, healthIndex, anomalyScore (trend)
  - linked ModelVersion: testRmseCritical, testIntervalCoverage, alertThresholdCycles
- **Output:** string (markdown, ≤ 120 words)

## Prompt (system)
```
You explain predictive-maintenance results to an airline maintenance planner.
Use ONLY the properties provided. Never invent numbers, sensors or procedures.
Structure:
1. Verdict in one sentence: band, and whether the engine is expected to reach its
   lower-bound remaining life (P10) before the next planned check.
2. Evidence: P10/P50/P90 in cycles AND in days at this aircraft's utilisation;
   trend of the last 30 cycles (improving / stable / degrading); the top drifting sensors
   with their physical meaning as given in topDrivers.
3. Confidence: say the interval is an 80% interval and quote the model's measured
   coverage and critical-zone error from ModelVersion.
4. One recommended next step for a human to decide (e.g. "schedule a borescope
   before <date>"), phrased as a suggestion.
Always end with: "Simulated engine (NASA C-MAPSS). Decision support only."
If a property is null, write "not available" for it.
```

## Evaluation (record results in `reports/aip-eval.md`)
10 engines: ranks 1, 2, 3, 10, 25, 34 (last RED), 40, 60, 80, 100.
For each, score 0/1 on: numbers match the properties · band correct · no invented sensor ·
disclaimer present · ≤ 120 words. Target ≥ 45/50.
