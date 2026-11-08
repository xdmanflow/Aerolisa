# Fleet

> Real flight activity from the OpenSky Network turned into cycles and flight hours per airframe, and the link between real aircraft and simulated engines.

**Milestone:** M5
**May import:** `aerolisa.core`
**Learn:** Renaissance 02 (gaps-and-islands), 04, 05, 08

## Why
Cycles and hours are what wear engines out. Utilization converts "cycles left" into "days left", so an aircraft flown harder rises in the inspection queue. It is the link between operations and maintenance, and it's real data.

## Outputs
- `gold/aircraft_utilization_daily`: airframe, date, cycles, flight hours
- `gold/engine_assignment`: engine id, airframe, position, C-MAPSS dataset/unit, start cycle, `simulated = true`

## Steps
1. [ ] Choose one operator's A320-family airframes from the aircraft registry; document why and how many
2. [ ] Utilization: cycles and hours per airframe per day from `silver/flights`; robust to missing days
3. [ ] Statistics: distribution of daily cycles per airframe, mean with confidence interval, outliers
4. [ ] Engine assignment: two C-MAPSS engines per airframe, reproducible (seeded), documented
5. [ ] Current simulated cycle of each engine = start cycle + real cycles since assignment
6. [ ] Tests on synthetic flight samples (never real OpenSky data in Git)

## Definition of done
- [ ] Utilization validated by hand on 3 airframes
- [ ] Planner consumes cycles per day
- [ ] "Simulated" label visible wherever an engine is shown

## Results
_Added at M5._
