# Workshop app: "Aerolisa · Inspection Queue"

Users: maintenance planner / MCC (acts), powerplant reliability engineer (understands why).
Question the app answers: **which engines should we inspect first, why, and what happens if we wait?**

## Page 1 · Fleet overview
| Widget | Config |
|---|---|
| Metric cards (4) | Engines in RED / AMBER / GREEN (object set Engine filtered by `band`), aircraft with ≥1 RED engine (`enginesInRed > 0`) |
| Chart: bar | Function `fleetBandCounts(Engine all)` → engines per band (status colours + labels) |
| Object table: Aircraft | registration, model, cyclesPerDay, nextCheckDate, worstEngineRisk (sorted desc), enginesInRed |
| Banner | "Engines are NASA C-MAPSS simulations assigned to a simulated fleet. Not real maintenance data." |

Variables: `selectedAircraft` (from table selection) → navigates to page 2 filtered.

## Page 2 · Inspection queue (main page)
| Widget | Config |
|---|---|
| Filter list | band, tailId, alert, status |
| Object table: InspectionRecommendation | rank, engineId, tailId, position, band (icon+label), rulP10 / rulP50 / rulP90, daysP10, daysToNextCheck, riskBeforeCheck (as %), status; default sort `rank` asc; filter status ≠ SCHEDULED |
| Text (markdown) | `reason` of the selected row |
| Numeric input | `delayDays` (0–30, default 7) |
| Metric card | Function `riskIfDelayed(selectedRecommendation, delayDays)` → "Risk if delayed by {delayDays} days" |
| Button group | **Schedule inspection** (action ScheduleInspection, prefilled: rec = selection, createdBy = current user), **Acknowledge** (AcknowledgeRecommendation) |

Variables: `selectedRecommendation` (table selection), `delayDays` (numeric input).

## Page 3 · Engine detail (opened from a row)
| Widget | Config |
|---|---|
| Object properties card | Engine: engineModel, position, currentCycle, healthIndex, anomalyScore, modelVersion, topDrivers |
| Chart (time series / XY) | linked EngineHealthSnapshot: x = cycle; series rulP10, rulP50, rulP90 (band area) |
| Chart | linked EngineHealthSnapshot: healthIndex and anomalyScore vs cycle (two separate charts, never a dual axis) |
| Chart | ps30Mean, t50Mean vs cycle (top physical drivers) |
| Object table | linked WorkOrder (status, plannedDate, finding) + action **Close work order** |
| AIP Logic panel | function "Explain this engine's risk" (step 14) |

## Design rules
- Colour = band only, always with an icon and a label (accessible, never colour alone).
- Every number shown with its unit (cycles, days, %).
- `rulTruthSimulationOnly` never shown in this app (it exists only to evaluate the model).
