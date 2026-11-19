const fs = require('fs');
const h = require('./build_report.js');
const { H1, H2, H3, P, Bullet, Caption, Paragraph, PageBreak,
  Table, TableRow, TableCell, WidthType, cell } = h;

const section2 = [
  H1('2. State of the Art'),

  H2('2.1 Maintenance strategies: from reactive to predictive'),
  P('Industrial maintenance strategies are generally classified into three categories. Reactive (corrective) maintenance intervenes after failure; it is simple but unacceptable for safety-critical systems. Preventive maintenance intervenes at fixed intervals, based on statistical failure distributions across a fleet, regardless of the actual condition of a specific unit; it is the dominant strategy in aviation today, but is known to be conservative and cost-inefficient. Predictive maintenance, sometimes called condition-based maintenance, uses real-time or near-real-time sensor data to estimate the actual health state of a specific unit and intervene only when needed. This third strategy is the object of a large and active research field known as Prognostics and Health Management (PHM), which combines signal processing, reliability engineering, and, increasingly, machine learning.'),

  H2('2.2 The C-MAPSS benchmark'),
  P('The dataset used in this study originates from a NASA-run simulation of turbofan engine degradation, first introduced by Saxena, Goebel, Simon and Eklund at the 2008 International Conference on Prognostics and Health Management (PHM08), and has since become the most widely used public benchmark in RUL-prediction research. It simulates engines of the same type, each starting with a different (unknown) degree of initial wear, operating under one or more flight conditions, and developing one or two fault modes until failure. Because ground truth RUL is known by construction (the simulation is run to failure), it allows supervised learning approaches to be trained and rigorously evaluated — a rare property in reliability engineering, where real failure data is scarce, expensive, and often incomplete.'),
  P('The dataset\'s broad adoption over more than a decade also means that a large body of published results is available for comparison, which is a deliberate advantage exploited in this study: it allows the results obtained here to be sanity-checked against the literature (see Section 4.5) rather than evaluated in isolation.'),

  H2('2.3 Machine learning approaches for RUL estimation'),
  H3('2.3.1 Classical machine learning and regression'),
  P('Early approaches to RUL estimation on C-MAPSS-like data used classical regression techniques — linear regression, support vector regression, and later tree-based ensembles such as Random Forest and Gradient Boosting. These methods treat each sensor reading (or a rolling-window feature derived from it) as an independent tabular observation, and are attractive for their simplicity, speed, and interpretability (e.g. feature importance rankings). Their main limitation is that they discard the temporal ordering of the data: two engines at the same degradation level but arrived at through a different history are treated identically, even though the trajectory of degradation itself often carries predictive signal.'),

  H3('2.3.2 Recurrent neural networks: LSTM and GRU'),
  P('To exploit the temporal structure of the data, several works have applied recurrent neural networks. Heimes (2008), one of the first PHM08 challenge participants, used a recurrent neural network directly on the raw sensor sequences and achieved competitive results, establishing early on that sequence modeling was a natural fit for this problem. Later, Zheng, Ristovski, Farahat and Gupta (2017) demonstrated that Long Short-Term Memory (LSTM) networks — a recurrent architecture designed to mitigate the vanishing-gradient problem of plain RNNs and better capture long-range dependencies — outperformed classical regression and plain RNN baselines on the C-MAPSS benchmark, establishing LSTM as a strong and now-standard baseline for RUL prediction.'),

  H3('2.3.3 Convolutional and hybrid architectures'),
  P('More recent work has explored one-dimensional Convolutional Neural Networks (CNNs) as an alternative to recurrent architectures. Babu, Zhao and Li (2016) proposed a CNN-based regression approach treating the multivariate sensor window as an image-like input, exploiting local temporal patterns through convolution rather than recurrence. Li, Ding and Sun (2018) extended this direction with deeper convolutional architectures and reported improved accuracy over LSTM baselines on several C-MAPSS subsets, while also being faster to train due to the parallelizable nature of convolution compared to the inherently sequential computation of recurrent networks. More recent literature (post-2020) has also explored attention-based and Transformer architectures, following their success in natural language processing, though these typically require larger training sets to outperform LSTM/CNN baselines and add architectural complexity that is not always justified for a dataset of this size.'),

  H3('2.3.4 Feature engineering and health indicator construction'),
  P('A parallel strand of the literature focuses less on model architecture and more on how the raw sensor signal is transformed before being fed to any model. Two recurring ideas are relevant to this study\'s methodology (Section 3.2): first, dropping or down-weighting sensors that show negligible variance under a given operating condition, which several authors report as both simplifying the model and, counter-intuitively, sometimes improving accuracy by removing pure noise dimensions; second, constructing a single scalar "health indicator" from multiple raw sensors (via, e.g., principal component analysis or an autoencoder\'s reconstruction error) as an intermediate representation, rather than feeding all raw sensors directly into the RUL model. This study adopts the first idea directly (Section 3.2.1) but not the second, favoring the simpler and more interpretable route of feeding the filtered raw sensors themselves into each model — a deliberate scope choice, flagged as a possible extension in Section 6.3.'),

  H2('2.4 Comparative overview of published results'),
  P('Table 1 summarizes, at a qualitative and approximate level, how the main model families discussed above have been reported to perform on the FD001 subset across the literature cited. These figures should be read with caution: different papers use different feature engineering pipelines, RUL-capping values, and train/validation splits, so results are not strictly comparable across studies — they are shown here only to establish the broad ordering of model families that motivates this study\'s design, and are cross-checked against the results independently obtained in Section 4.'),
  new Table({
    width: { size: 9200, type: WidthType.DXA },
    rows: [
      new TableRow({ tableHeader: true, children: [
        cell('Model family', { bold: true, shade: 'D9D9D9', width: 2600 }),
        cell('Representative work', { bold: true, shade: 'D9D9D9', width: 3200 }),
        cell('Approximate reported RMSE range (FD001)', { bold: true, shade: 'D9D9D9', width: 3400 }),
      ]}),
      new TableRow({ children: [
        cell('Classical regression / tabular ML', { width: 2600 }),
        cell('Various (baseline comparisons in RUL literature)', { width: 3200 }),
        cell('Typically higher error; used as baseline reference', { width: 3400 }),
      ]}),
      new TableRow({ children: [
        cell('Plain RNN', { width: 2600 }),
        cell('Heimes (2008)', { width: 3200 }),
        cell('Competitive for its time; superseded by LSTM/GRU', { width: 3400 }),
      ]}),
      new TableRow({ children: [
        cell('LSTM', { width: 2600 }),
        cell('Zheng et al. (2017)', { width: 3200 }),
        cell('Reported as a strong improvement over RNN/regression baselines', { width: 3400 }),
      ]}),
      new TableRow({ children: [
        cell('1D-CNN', { width: 2600 }),
        cell('Babu et al. (2016); Li et al. (2018)', { width: 3200 }),
        cell('Reported as competitive with or superior to LSTM, at lower training cost', { width: 3400 }),
      ]}),
    ],
  }),
  new Paragraph({ text: '', spacing: { after: 200 } }),
  Caption('Table 1 — Qualitative positioning of model families reported in the RUL-prediction literature on C-MAPSS/FD001 (approximate, illustrative ordering only — see caveat above).'),

  H2('2.5 Physics-based vs data-driven prognostics'),
  P('It is worth situating the data-driven approach adopted in this study (and in the majority of the literature reviewed above) against an alternative, older paradigm in prognostics: physics-of-failure models, which simulate the underlying degradation mechanism (e.g. crack growth, thermal fatigue) from first-principles engineering models of the specific failure mode, as reviewed by Pecht and Gu (2009) in the broader context of electronic systems. Physics-based models have the advantage of remaining interpretable and physically grounded even with very little historical failure data, since they do not need to learn the degradation pattern from examples — they encode it directly from engineering knowledge of the failure mechanism. Their disadvantage is that they require a detailed, mechanism-specific model to be developed and validated for every failure mode of interest, which is costly and does not transfer easily across engine types or fault modes.'),
  P('Data-driven approaches, including all model families discussed above, invert this trade-off: they require comparatively little domain-specific engineering effort to set up (the same LSTM architecture, for instance, could in principle be retrained on a different fault mode or engine type given sufficient run-to-failure data), but they depend entirely on the availability of representative historical degradation data to learn from, and offer comparatively little physical interpretability of why a given prediction was made. The C-MAPSS dataset used in this study is itself a physics-based simulation used to generate data for a data-driven study — a hybrid use of both paradigms that is increasingly common in the literature, since it sidesteps the practical difficulty of collecting enough real run-to-failure data for a purely data-driven study, while still allowing the resulting method to be as domain-agnostic as any other data-driven approach once real data becomes available. This framing directly motivates the simulation-to-reality gap discussed as a limitation in Section 6.2: this study\'s data-driven models were trained on data itself generated by a physics-based model, one further remove from real fleet telemetry than a purely field-collected dataset would be.'),

  H2('2.6 Synthesis and positioning of this study'),
  P('Across the literature, three findings recur consistently and directly motivate the methodology adopted in this report: (1) recurrent architectures, and LSTM in particular, reliably outperform classical tabular regression on this task because they exploit the temporal degradation trajectory rather than treating each cycle independently; (2) evaluation should not rely on RMSE alone, since it treats early and late prediction errors symmetrically, whereas in a safety-critical maintenance context a late (overly optimistic) prediction is far more dangerous than an early one — this motivates the use of the NASA asymmetric scoring function introduced with the original PHM08 challenge, in addition to RMSE; and (3) feature selection and normalization matter significantly, since several of the 21 raw sensors in C-MAPSS are near-constant under a single operating condition and contribute noise rather than signal.'),
  P('This study is positioned as a comparative, reproducible study rather than a novel-architecture contribution: it implements and rigorously compares a classical baseline (linear regression), two tree-based ensembles (Random Forest, Gradient Boosting) and a recurrent deep learning model (LSTM) on the FD001 subset, following the evaluation practices established in the literature (RMSE and NASA score, train/validation split by engine to avoid leakage), in order to draw sound, evidence-based conclusions about the trade-offs between model complexity, interpretability, and predictive accuracy for this problem.'),
  new Paragraph({ children: [new PageBreak()] }),
];

module.exports = { section2 };
