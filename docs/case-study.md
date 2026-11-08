# Case study (fill at M11)

Write it for a reliability engineer or a Skywise product manager who has 5 minutes. Answer first.

## 1. The question
*Which engines should we inspect first, why, and what happens if we wait?* One paragraph on why the question matters: unscheduled removals, aircraft on ground, the value of turning unscheduled maintenance into scheduled maintenance. Use sourced figures only, with links.

## 2. The users
- Reliability / powerplant engineer: wants the ranking and the reason
- Maintenance planner / MCC: wants to act (schedule) and see the effect
- Data team: wants pipelines that don't break silently

## 3. The data
Public sources, what is real (flights, airframes, airports) and what is simulated (engines). Limits.

## 4. The approach
Pipeline → ontology → models with intervals → utilization → risk ranking → action → copilot. One diagram.

## 5. The results
- Model comparison (from `reports/evaluation.md`)
- Interval coverage
- Example: one engine's ranking explained
- Copilot eval score (from `reports/copilot-eval.md`)

## 6. What I'd do with real airline data
Bullet list (see [skywise-foundry-mapping.md](skywise-foundry-mapping.md)).

## 7. What I learned
Three honest lessons.
