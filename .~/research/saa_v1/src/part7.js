const fs = require('fs');
const h = require('./build_report.js');
const { H1, H2, H3, P, Bullet, Caption, Paragraph, PageBreak,
  Table, TableRow, TableCell, WidthType, cell } = h;

const section5 = [
  H1('5. Discussion: Operational Implications'),

  H2('5.1 From model accuracy to maintenance decisions'),
  P('A predictive model is only useful if its output can be translated into an actionable maintenance decision. A typical deployment would define a decision threshold (e.g. "schedule inspection when predicted RUL falls below 30 cycles") rather than acting on the raw regression output directly. The results of Section 4.6 are directly relevant here: because the LSTM\'s accuracy advantage concentrates in the low-RUL region, it is precisely in the region close to such a threshold that its predictions can be trusted the most, which is the opposite of what one might fear from a more complex, less interpretable model — here, complexity buys accuracy exactly where it is needed.'),

  H2('5.2 Illustrative cost-benefit example'),
  P('To make the economic stakes discussed in Section 1.5 concrete, consider a simplified, illustrative example (using representative order-of-magnitude figures, not sourced airline data, purely to demonstrate the reasoning a real deployment study would need to formalize with actual cost data). Assume a fleet of 50 engines, each currently maintained on a fixed schedule that discards components with an estimated 15% of remaining useful life still available, and assume a representative overhaul cost per engine. Table 5 illustrates, at an order-of-magnitude level, how a modest reduction in wasted useful life compounds across a fleet.'),
  new Table({
    width: { size: 9200, type: WidthType.DXA },
    rows: [
      new TableRow({ tableHeader: true, children: [
        cell('Scenario', { bold: true, shade: 'D9D9D9', width: 3600 }),
        cell('Assumed wasted useful life per overhaul', { bold: true, shade: 'D9D9D9', width: 3200 }),
        cell('Relative fleet-wide maintenance cost', { bold: true, shade: 'D9D9D9', width: 2400 }),
      ]}),
      new TableRow({ children: [
        cell('Current fixed-schedule preventive maintenance', { width: 3600 }),
        cell('~15% (illustrative)', { width: 3200 }),
        cell('Baseline (100%)', { width: 2400 }),
      ]}),
      new TableRow({ children: [
        cell('Predictive maintenance (model-informed scheduling)', { width: 3600 }),
        cell('~5% (illustrative, reflecting residual model uncertainty)', { width: 3200 }),
        cell('Reduced (illustrative order of magnitude only)', { width: 2400 }),
      ]}),
    ],
  }),
  new Paragraph({ text: '', spacing: { after: 200 } }),
  Caption('Table 5 — Illustrative, order-of-magnitude cost-benefit comparison of maintenance strategies (assumed figures for demonstration purposes; a real deployment would require validated cost and reliability data from the operator).'),
  P('This example is deliberately illustrative rather than a real cost projection: an actual business case would require validated MRO cost data, fleet-specific failure statistics, and a formal reliability engineering study, all of which are outside the scope of this SAA project. Its purpose here is only to make explicit the mechanism by which even a partial reduction in wasted component life — which the model comparison in Section 4 suggests is achievable — compounds into a fleet-wide economic effect, which is the socio-economic stake originally framed in Section 1.5.'),

  H2('5.3 Sketch of an operational deployment architecture'),
  P('Moving from this study\'s offline, historical-data evaluation to an operational system would require, at minimum, the following components, sketched here at a conceptual level rather than implemented (which would exceed the scope of a single SAA project):'),
  Bullet('Data ingestion: a pipeline collecting sensor telemetry after each flight cycle (or continuously, depending on the aircraft\'s data-link capability), replacing this study\'s static, pre-collected dataset.'),
  Bullet('Feature computation: reproducing the normalization and feature-selection steps of Section 3.2 on live data, using statistics frozen from a training reference period rather than recomputed on the fly, to preserve the guarantees discussed in Section 3.2.3.'),
  Bullet('Inference service: the trained LSTM model (or a periodically retrained version of it) scoring each engine\'s latest window of cycles to produce an updated RUL estimate.'),
  Bullet('Alerting and decision support: translating the RUL estimate and an associated confidence/uncertainty signal (identified as a limitation in Section 6.2 and a perspective in Section 6.3) into a maintenance recommendation surfaced to human planners — not a fully automated maintenance trigger, given the safety-critical nature of the decision.'),
  Bullet('Monitoring and retraining: tracking prediction accuracy against realized failures over time, and retraining the model periodically as new run-to-failure data becomes available, to guard against distribution drift (e.g. new engine variants, changed operating patterns).'),
  P('This sketch highlights that the machine learning model evaluated in this report, while central, is only one component of a larger system; the human-in-the-loop decision support framing is deliberate, reflecting the safety-critical context established in Section 1.4.'),

  H2('5.4 Risk considerations'),
  P('Two risk categories deserve explicit mention. First, model risk: a model trained on simulated data (Section 6.2) could behave unpredictably on real sensor distributions it has not seen, which is why any real deployment would require an extensive validation phase against real fleet data before being used to inform actual maintenance decisions, rather than being deployed directly from this study\'s results. Second, organizational risk: introducing a data-driven maintenance recommendation changes established MRO workflows and requires buy-in from maintenance planners and regulators; the NASA scoring function\'s emphasis on avoiding late predictions (Section 3.4) is one way of aligning the model\'s optimization target with the risk tolerance such stakeholders would reasonably require, but is not by itself a substitute for a formal safety case.'),

  H2('5.5 Accountability and environmental considerations'),
  P('Beyond technical and organizational risk, introducing an algorithmic recommendation into a safety-critical maintenance decision raises a genuine question of accountability: if a model-informed decision to defer maintenance is later followed by an in-flight incident, responsibility cannot reasonably be attributed to the model itself — it must remain with the human decision-maker and the organization\'s safety processes that decided how much weight to give the model\'s output. This is precisely why Section 5.3 frames the model as a decision-support input rather than an autonomous trigger, and why aviation regulators (e.g. EASA, FAA) require any such tool to sit within a certified safety management system rather than operate as a standalone black box.'),
  P('A secondary, but genuinely relevant, stake is environmental: avoiding premature replacement of engine components (Section 1.5) reduces the manufacturing footprint associated with spare-parts production — raw material extraction, machining, and transport — for each component whose full useful life is realized rather than discarded early. This does not compete with the safety case for predictive maintenance; rather, it reinforces it, since the same accuracy improvement that allows safe deferral of unnecessary maintenance also reduces the industry\'s material and carbon footprint per flight-hour, a secondary co-benefit worth naming explicitly given the aeronautics sector\'s broader sustainability pressures.'),

  H2('5.6 Alignment with broader industry trends'),
  P('The approach studied here fits within a wider movement, sometimes labeled Industry 4.0 in the manufacturing and MRO literature, toward instrumenting physical assets with sensors and using data-driven models to optimize their operation and upkeep. Aircraft engines are a particularly mature case for this trend: they already carry extensive sensor suites for engine control purposes, meaning the marginal cost of also using that data for prognostics is comparatively low compared to retrofitting sensors onto legacy industrial equipment purely for predictive maintenance purposes. This context suggests that the results of this study, while obtained on a simulated benchmark, address a problem for which the underlying data infrastructure is, in large part, already in place in modern fleets — the primary remaining gap being the analytics layer this study contributes to, and the organizational and regulatory integration discussed in Section 5.4 and 5.5.'),
  new Paragraph({ children: [new PageBreak()] }),
];

module.exports = { section5 };
