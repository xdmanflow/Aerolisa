const fs = require('fs');
const h = require('./build_report.js');
const {
  H1, H2, H3, P, Bullet, Caption, imgParagraph, cell,
  Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType,
  TableOfContents, PageBreak, VerticalAlign,
} = h;

const toc = [
  H1('Table of Contents'),
  new TableOfContents('Table of Contents', { hyperlink: true, headingStyleRange: '1-3' }),
  new Paragraph({ children: [new PageBreak()] }),
];

const tableOfIllustrations = [
  H1('Table of Illustrations'),
  H2('Figures'),
  Bullet('Figure 1 — Sensor readings vs operating cycle, engines 1 to 5 (FD001 training set)'),
  Bullet('Figure 2 — Distribution of engine lifetimes, FD001 training set'),
  Bullet('Figure 3 — Pearson correlation of each informative sensor with Remaining Useful Life'),
  Bullet('Figure 4 — LSTM training and validation loss across training epochs'),
  Bullet('Figure 5 — Test RMSE by model'),
  Bullet('Figure 6 — Test NASA asymmetric score by model'),
  Bullet('Figure 7 — LSTM: true vs predicted RUL for all 100 FD001 test engines'),
  Bullet('Figure 8 — Top 12 features by Random Forest importance'),
  Bullet('Figure 9 — Prediction error by operational zone (critical vs non-critical)'),
  Bullet('Figure 10 — Random Forest and Gradient Boosting: true vs predicted RUL'),
  H2('Tables'),
  Bullet('Table 1 — Candidate model families and selection rationale'),
  Bullet('Table 2 — Baseline model performance on FD001'),
  Bullet('Table 3 — Full model comparison on the FD001 test set'),
  Bullet('Table 4 — Prediction error by operational criticality zone'),
  Bullet('Table 5 — Illustrative cost-benefit comparison of maintenance strategies'),
  Bullet('Table 6 — Model hyperparameters'),
  Bullet('Table 7 — Full Random Forest feature importance'),
  Bullet('Table 8 — Full C-MAPSS sensor list and description'),
  new Paragraph({ children: [new PageBreak()] }),
];

const introduction = [
  H1('Introduction'),
  P('The engineering profession requires the ability to pose and solve complex problems efficiently, using a rigorous and well-reasoned approach grounded in scientific method. This report applies that method to a real problem in the aeronautics industry: predicting when an aircraft engine will require maintenance, based on the data it produces while operating.'),
  P('Aircraft engine maintenance today relies primarily on two strategies. The first, reactive maintenance, repairs or replaces a component only after it fails — acceptable for non-critical parts, but unacceptable for a jet engine, where failure in flight is a safety event. The second, preventive maintenance, replaces components on a fixed schedule regardless of their actual condition. This is safe, but wasteful: a component removed after 80% of its useful life still had 20% of value left on the table, multiplied across a fleet of thousands of engines.'),
  P('Predictive maintenance proposes a third way: use the engine\'s own sensor data — temperature, pressure, rotational speed, and more — to estimate how much operational life remains, and schedule maintenance exactly when needed, no earlier and no later. This is fundamentally a data science and machine learning problem: given a time series of noisy multivariate sensor readings, estimate a single number, the Remaining Useful Life (RUL), as accurately and as reliably as possible.'),
  P('This report investigates that problem using NASA\'s C-MAPSS dataset, a public benchmark that simulates turbofan engines operated from a healthy state to failure. It compares several families of machine learning models — from simple linear regression to a Long Short-Term Memory (LSTM) recurrent neural network — following the CESI scientific method: precisely framing the problem and its stakes, reviewing the state of the art, proposing and justifying candidate solutions, implementing and validating them experimentally, and concluding on their relevance and limitations.'),
  P('The report is structured as follows. Section 1 defines the problem, its context, scope and socio-economic stakes. Section 2 reviews the state of the art in predictive maintenance and RUL estimation. Section 3 details the proposed methodology: dataset, feature engineering, candidate models, and evaluation protocol. Section 4 presents and discusses the experimental results. Section 5 discusses the operational implications of these results — how a model output becomes a maintenance decision, an illustrative cost-benefit view, a sketch of a deployment architecture, and the risk and accountability considerations that come with it. Section 6 concludes on the initial problem and outlines perspectives for future work.'),
  P('Throughout, the report follows the scientific method promoted by CESI\'s Application de la Démarche Scientifique framework: every claim is either derived directly from an experiment run for this study, or explicitly attributed to and cross-checked against the published literature, with the two kept clearly distinguishable (Section 2.4 and Section 4.7 make this cross-check explicit). Where a limitation or a simplifying assumption was made for feasibility reasons — as any bounded student project must — it is flagged at the point it is introduced rather than left implicit, and revisited comprehensively in Section 6.2.'),
  new Paragraph({ children: [new PageBreak()] }),
];

// ================= SECTION 1: PROBLEM DEFINITION =================
const section1 = [
  H1('1. Problem Definition and Context'),

  H2('1.1 Comparison of maintenance strategies'),
  P('The three maintenance strategies introduced above are compared in Table 1 below across the dimensions that matter most operationally: safety exposure, cost efficiency, and the technical maturity required to implement each strategy.'),
  new Table({
    width: { size: 9200, type: WidthType.DXA },
    rows: [
      new TableRow({ tableHeader: true, children: [
        cell('Strategy', { bold: true, shade: 'D9D9D9', width: 2400 }),
        cell('Trigger for intervention', { bold: true, shade: 'D9D9D9', width: 2800 }),
        cell('Safety exposure', { bold: true, shade: 'D9D9D9', width: 2000 }),
        cell('Cost efficiency', { bold: true, shade: 'D9D9D9', width: 2000 }),
      ]}),
      new TableRow({ children: [
        cell('Reactive (corrective)', { width: 2400 }),
        cell('Failure has already occurred', { width: 2800 }),
        cell('High risk', { width: 2000 }),
        cell('Low (unplanned downtime)', { width: 2000 }),
      ]}),
      new TableRow({ children: [
        cell('Preventive (scheduled)', { width: 2400 }),
        cell('Fixed calendar / flight-hour interval', { width: 2800 }),
        cell('Low risk', { width: 2000 }),
        cell('Medium (parts replaced early)', { width: 2000 }),
      ]}),
      new TableRow({ children: [
        cell('Predictive (condition-based)', { width: 2400 }),
        cell('Estimated Remaining Useful Life crosses a threshold', { width: 2800 }),
        cell('Low risk (if model is reliable)', { width: 2000 }),
        cell('High (parts used near full life)', { width: 2000 }),
      ]}),
    ],
  }),
  new Paragraph({ text: '', spacing: { after: 200 } }),
  Caption('Table 1 — Comparison of the three principal aircraft engine maintenance strategies.'),

  H2('1.2 Industrial context'),
  P('Commercial aviation operates under extremely strict safety and reliability requirements. Engine manufacturers (CFM International, Rolls-Royce, GE Aerospace, Safran, Pratt & Whitney) and maintenance, repair and overhaul (MRO) providers must guarantee that engines are serviced before any critical degradation occurs, while minimizing unnecessary downtime and part replacement. An Aircraft-On-Ground (AOG) event — where an aircraft cannot fly due to an unplanned technical issue — can cost an airline tens of thousands of euros per day in lost revenue, passenger compensation, and logistics, in addition to the reputational cost.'),
  P('At the same time, over-conservative preventive maintenance directly inflates Maintenance, Repair and Overhaul (MRO) costs, which represent a significant share of an airline\'s total operating expenses. The digitalization of aircraft engines — modern turbofans carry hundreds of sensors recording temperature, pressure, vibration, and rotational speed at each flight cycle — creates an opportunity to move from calendar-based to condition-based and ultimately predictive maintenance, provided the data can be turned into a reliable estimate of remaining engine life.'),
  P('Table 1bis maps the principal stakeholders in this problem and what each of them would need from a predictive maintenance system for it to be trustworthy and adopted in practice — a useful discipline before proposing any technical solution, since a model that is accurate but ignores what its users actually need (e.g. interpretability for a regulator, or a simple threshold for a maintenance planner) is unlikely to be adopted regardless of its RMSE.'),
  new Table({
    width: { size: 9200, type: WidthType.DXA },
    rows: [
      new TableRow({ tableHeader: true, children: [
        cell('Stakeholder', { bold: true, shade: 'D9D9D9', width: 2600 }),
        cell('Primary concern', { bold: true, shade: 'D9D9D9', width: 3600 }),
        cell('Requirement from the model', { bold: true, shade: 'D9D9D9', width: 3000 }),
      ]}),
      new TableRow({ children: [
        cell('Airline / MRO operator', { width: 2600 }),
        cell('Minimizing cost while avoiding AOG events', { width: 3600 }),
        cell('Accurate RUL estimate, actionable ahead of failure', { width: 3000 }),
      ]}),
      new TableRow({ children: [
        cell('Maintenance planner (end user)', { width: 2600 }),
        cell('Trusting and acting on the recommendation', { width: 3600 }),
        cell('Clear output, ideally with a confidence indicator', { width: 3000 }),
      ]}),
      new TableRow({ children: [
        cell('Regulator (e.g. EASA, FAA)', { width: 2600 }),
        cell('Ensuring the tool does not compromise safety', { width: 3600 }),
        cell('Auditability; human-in-the-loop decision process', { width: 3000 }),
      ]}),
      new TableRow({ children: [
        cell('Passengers / public', { width: 2600 }),
        cell('Flight safety', { width: 3600 }),
        cell('Indirect: relies on the above being satisfied', { width: 3000 }),
      ]}),
    ],
  }),
  new Paragraph({ text: '', spacing: { after: 200 } }),
  Caption('Table 1bis — Stakeholder mapping for a predictive maintenance system in commercial aviation.'),

  H2('1.3 Problem statement'),
  P('The central question addressed in this study is the following: can machine learning models predict a turbofan engine\'s Remaining Useful Life (RUL) from multivariate sensor data accurately enough to support a shift from scheduled to predictive maintenance?'),
  P('This decomposes into three sub-questions that structure the rest of this report:'),
  Bullet('What features of the raw sensor data are actually informative for estimating degradation, and which are noise or redundant?'),
  Bullet('Which model family — classical tabular machine learning or sequence-aware deep learning — is best suited to this kind of temporal, multivariate degradation data?'),
  Bullet('How should model quality be measured in a way that reflects the real, asymmetric cost of prediction errors in a safety-critical context (an overly optimistic prediction is far more dangerous than an overly conservative one)?'),

  H2('1.4 Scope and constraints'),
  P('Given the constraints of a student research project (limited time, no access to proprietary airline or manufacturer data), the scope of this study is deliberately bounded:'),
  Bullet('Data source: the FD001 subset of NASA\'s public C-MAPSS dataset is used — engines operating under a single flight condition (sea level) with a single fault mode (High-Pressure Compressor degradation). This keeps the problem well-posed and comparable to a large body of published research, while more complex subsets (FD002–FD004, with multiple operating conditions and fault modes) are left for future work (see Section 6.3).'),
  Bullet('Modeling scope: the study compares three families of models — linear regression (interpretable baseline), tree-based ensembles (Random Forest, Gradient Boosting), and a recurrent deep learning model (LSTM) — rather than attempting an exhaustive survey of all possible architectures (e.g. Transformers, CNNs, hybrid models), which is discussed but not implemented, for feasibility within the available time budget.'),
  Bullet('Deployment scope: this study evaluates model accuracy on historical/simulated data; it does not implement a live monitoring system, nor does it address sensor fusion across an entire aircraft, which would fall outside a single SAA project.'),

  H2('1.5 Socio-economic stakes'),
  P('The stakes of accurate RUL prediction operate at three levels:'),
  Bullet('Safety: reducing the risk of in-flight or on-ground failure by catching degradation early, which is the primary justification for any change to maintenance practice in aviation.'),
  Bullet('Economic: MRO costs represent a major and recurring expense for airlines and engine manufacturers; even a modest improvement in maintenance timing, applied across a large fleet over years of operation, translates into meaningful savings and less unplanned downtime.'),
  Bullet('Environmental: better-maintained engines operate closer to their design efficiency, and avoiding premature part replacement reduces the material and manufacturing footprint associated with spare parts production — a secondary but increasingly relevant stake in aeronautics.'),
  H2('1.6 Synthesis: research questions'),
  P('To make the problem statement of Section 1.3 directly testable, it is restated here as three concrete, individually answerable research questions, each of which is picked back up explicitly in the results (Section 4) and conclusion (Section 6):'),
  Bullet('RQ1 (feature relevance): Which of the 21 raw C-MAPSS sensors carry genuine predictive signal for RUL under a single operating condition, and can uninformative sensors be identified and safely excluded without hurting model accuracy? Answered in Sections 4.1 and 4.5.'),
  Bullet('RQ2 (model family): Does modeling engine degradation as an ordered temporal sequence (via a recurrent architecture) meaningfully outperform treating each engine-cycle as an independent snapshot (via classical tabular regression), and if so, by how much, and where in the RUL range does the advantage concentrate? Answered in Sections 4.4 and 4.6.'),
  Bullet('RQ3 (evaluation validity): Does the choice of evaluation metric (symmetric RMSE vs the asymmetric, safety-weighted NASA score) change the practical conclusion about which model is "best" for this safety-critical use case? Answered in Section 4.4.'),
  P('Framing the problem this way — as falsifiable, individually testable sub-questions rather than a single vague objective — is itself an application of the rigorous, structured approach this SAA project is meant to demonstrate (see the CESI SAA framework\'s objectives, which call explicitly for precisely identifying the issue before analyzing it).'),
  new Paragraph({ children: [new PageBreak()] }),
];

module.exports = { toc, tableOfIllustrations, introduction, section1 };
