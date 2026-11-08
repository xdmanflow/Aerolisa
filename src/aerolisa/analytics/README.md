# Analytics

> The data-analyst proof: KPIs, SQL analyses, a dashboard and an insight memo on European air-traffic performance (Eurocontrol) and Airbus orders & deliveries.

**Milestone:** M8
**May import:** `aerolisa.core`
**Learn:** Renaissance 02, 11

## Why
Many Airbus data apprenticeships are analyst roles: collect data, define KPIs, build dashboards, explain results to stakeholders. This module shows that skill set on aviation data, separate from the ML work.

## KPI dictionary (fill at M8)

| KPI | Definition | Formula | Grain | Caveats |
|---|---|---|---|---|
| Arrival delay per flight | | | airport × month | |
| Delay share by cause | | | airport × month × cause | |
| Year-over-year delay change | | | airport × month | |
| Monthly deliveries by family | | | family × month | |
| Rolling 12-month deliveries | | | family × month | |
| Delivery rate vs prior year | | | family × year | |

## Steps
1. [ ] `silver/delays` and `silver/deliveries` from the pipelines (M8 steps 1–2)
2. [ ] KPI dictionary above, complete
3. [ ] 10 SQL analyses in [`sql/`](../../../sql/README.md), each with its business question
4. [ ] Gold aggregates for the app (`gold/analytics_*`)
5. [ ] Streamlit Analytics page and/or Power BI report (screenshots in `reports/analytics/`)
6. [ ] Memo `reports/analytics/memo.md`: answer first, 3 findings, 1 recommendation, limits
7. [ ] 3-minute recorded presentation

## Definition of done
- [ ] Every chart has a one-line takeaway
- [ ] Every number in the memo traces back to a query in `sql/`

## Results
_Added at M8._
