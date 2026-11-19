const fs = require('fs');
const h = require('./build_report.js');
const {
  H1, H2, H3, P, Bullet, Caption, imgParagraph, cell,
  Paragraph, TextRun, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, VerticalAlign,
  PageBreak, YELLOW,
} = h;

function simpleTable(headers, rows, widths) {
  const headerRow = new TableRow({
    children: headers.map((t, i) => cell(t, { bold: true, shade: 'D9D9D9', width: widths[i], align: AlignmentType.CENTER })),
    tableHeader: true,
  });
  const dataRows = rows.map(r => new TableRow({
    children: r.map((t, i) => cell(String(t), { width: widths[i], align: i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER })),
  }));
  return new Table({ rows: [headerRow, ...dataRows], width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA } });
}

const section3 = [
  H1('3. Proposed Methodology'),

  H2('3.1 Dataset presentation'),
  P('The FD001 subset of the C-MAPSS dataset contains 100 training engines and 100 test engines, all operating under a single flight condition (sea level) and developing a single fault mode (High-Pressure Compressor degradation). Each row of raw data corresponds to one operational cycle of one engine and contains: an engine identifier, the cycle number, three operational settings, and 21 sensor measurements (temperatures, pressures, fan speed, etc.). In the training set, each engine\'s time series runs until failure, giving a natural ground-truth RUL for every cycle (computed as the number of remaining cycles until the engine\'s last recorded cycle). In the test set, each series is truncated at an arbitrary point before failure, and the true RUL at that cutoff is provided separately — this mirrors the real operational situation, where an engine is observed as it currently is, with its true remaining life obviously unknown.'),
  P('Data loading and RUL-label construction were verified against the dataset documentation: the loaded training set contains 20,631 rows across 100 engines with individual lifetimes ranging from 128 to 362 cycles (mean 206.3 cycles), consistent with the published dataset description.'),

  H2('3.2 Data preparation'),
  H3('3.2.1 Feature selection'),
  P('An exploratory analysis of sensor variance (Section 4.1) showed that 6 of the 21 raw sensors (sensors 1, 5, 10, 16, 18 and 19) are near-constant under the single operating condition of FD001 and therefore carry no useful signal for this subset; they were excluded, leaving 15 informative sensors plus the 3 operational settings as candidate features (18 features total).'),
  H3('3.2.2 RUL capping (piecewise-linear target)'),
  P('A well-known issue in RUL regression is that, at the start of an engine\'s life, degradation has not yet begun to manifest in the sensor data, so the true (linear) RUL label is effectively unlearnable from the input at that point and only adds noise to training. Following standard practice in the literature (e.g. Heimes 2008), the training RUL target was capped at 125 cycles: cycles further than 125 from failure are all labeled with RUL = 125, on the assumption that degradation is not yet meaningfully observable before that point. This piecewise-linear RUL target is applied to the training labels only; the true (uncapped) RUL is used for test-set evaluation, since that is the real quantity of interest.'),
  H3('3.2.3 Normalization'),
  P('All features were rescaled to the [0, 1] range using min-max normalization, with scaling parameters fitted exclusively on the training set and then applied unchanged to the validation and test sets, to avoid information leakage from the evaluation data into preprocessing.'),
  H3('3.2.4 Train / validation split'),
  P('To obtain a validation set for model selection and hyperparameter checks, 20 of the 100 training engines were held out as a validation set, with the split performed at the engine level (not the row level): all cycles of a given engine belong entirely to either the training or the validation subset. A row-level random split would let the model see cycles from the same engine\'s trajectory in both sets, artificially inflating validation performance — a data-leakage pitfall this study explicitly avoids.'),

  H2('3.3 Candidate models and selection criteria'),
  P('Four model families were selected to cover a representative and complementary range of complexity, interpretability and computational cost, each justified against the following criteria: predictive accuracy, training/inference cost, interpretability, and ability to exploit temporal structure.'),
  simpleTable(
    ['Model', 'Type', 'Exploits time order?', 'Interpretability', 'Rationale'],
    [
      ['Linear Regression', 'Classical, tabular', 'No', 'High', 'Simple interpretable baseline; establishes a lower performance bound'],
      ['Random Forest', 'Tree ensemble, tabular', 'No', 'Medium (feature importance)', 'Robust, handles non-linearities, widely used industrial baseline'],
      ['Gradient Boosting', 'Tree ensemble, tabular', 'No', 'Medium', 'Often outperforms Random Forest on tabular data; second ensemble baseline'],
      ['LSTM', 'Recurrent deep learning', 'Yes', 'Low', 'Literature shows sequence models best exploit degradation trajectories'],
    ],
    [2200, 2200, 2000, 2600, 3400],
  ),
  new Paragraph({ text: '', spacing: { after: 200 } }),
  P('For the tabular models (Linear Regression, Random Forest, Gradient Boosting), each row (one engine-cycle) is used as an independent training example. For the LSTM, the input is instead a sliding window of 30 consecutive cycles per engine (a sequence length chosen as a common value in the literature, balancing enough temporal context against the shorter engine lifetimes present in the dataset), and the model predicts the RUL at the end of that window.'),

  H2('3.4 Evaluation protocol'),
  P('Two complementary metrics were used to evaluate all models on the held-out test set:'),
  Bullet('Root Mean Squared Error (RMSE): the standard regression metric, measuring the average magnitude of prediction error in cycles, penalizing large errors more than small ones, but treating early and late errors symmetrically.'),
  Bullet('NASA scoring function: the asymmetric scoring function introduced with the original PHM08 challenge, defined as S = Σ(exp(−d/13) − 1) for d < 0, and S = Σ(exp(d/10) − 1) for d ≥ 0, where d = predicted RUL − true RUL. This function penalizes late predictions (d > 0, i.e. the model predicts the engine will last longer than it actually does) roughly 30% more steeply than early predictions of the same magnitude, directly reflecting the real safety asymmetry of the problem: an overly optimistic prediction risks an in-flight failure, while an overly conservative one merely costs an early, safe maintenance action.'),
  P('Following the standard C-MAPSS evaluation protocol, test-set performance is computed on the last available cycle of each of the 100 test engines only (i.e. the most recent, most informative observation for each engine), matching how the model would be used operationally: to answer "what is this engine\'s remaining life right now?".'),

  H2('3.5 Hyperparameter selection'),
  P('Given the scope of a single-student SAA project, hyperparameters were set using established literature defaults and light manual tuning against the validation set, rather than an exhaustive grid or Bayesian search — a deliberate simplification flagged here for transparency, and identified as a direction for future work in Section 6.3. For the tree-based ensembles, tree count (300) and depth/leaf constraints were chosen to balance bias and variance without excessive training time; for the LSTM, layer sizes (64, 32 units) and dropout (0.2) follow common configurations reported in the RUL-prediction literature (Section 2.3.2), and the sequence length (30 cycles) was chosen to provide meaningful temporal context while remaining shorter than the majority of engine lifetimes in the dataset (minimum 128 cycles). Early stopping on validation loss (patience of 8 epochs) was used in place of a fixed epoch budget, to avoid both under- and over-fitting without manual trial and error on the number of epochs.'),

  H2('3.6 Computational environment'),
  P('All experiments were run on CPU (no GPU acceleration was required given the dataset size), using Python 3 with scikit-learn for the classical models and TensorFlow/Keras for the LSTM. Exact training times are reported in Section 4.4 and are relevant to the discussion of model choice trade-offs in Section 5.'),

  H2('3.7 Data quality checks'),
  P('Before any modeling, the loaded dataset was systematically checked for common data-quality issues that could otherwise silently bias the results: missing values, duplicate rows, and inconsistent unit/cycle indexing. All three checks passed cleanly — zero missing values were found across both the training (20,631 rows) and test (13,096 rows) sets, zero duplicate rows were found, and every engine unit\'s cycle count began at 1 and increased monotonically with no gaps, confirming the dataset\'s internal consistency prior to feature engineering. This is expected given the dataset\'s origin as a controlled simulation rather than field-collected telemetry, but the check is nonetheless reported here as standard due diligence, and would become considerably more important — and more likely to surface real issues — if this methodology were ever applied to real fleet data (Section 6.2).'),
  new Paragraph({ children: [new PageBreak()] }),
];

module.exports = { section3, simpleTable };
