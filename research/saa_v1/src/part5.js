const fs = require('fs');
const h = require('./build_report.js');
const { H1, H2, H3, P, Bullet, Caption, imgParagraph, cell, Paragraph, AlignmentType,
  Table, TableRow, TableCell, WidthType, VerticalAlign, PageBreak } = h;
const { simpleTable } = require('./part4.js');

const FIGDIR = 'figs/';

const section4 = [
  H1('4. Implementation and Results'),

  H2('4.1 Exploratory data analysis'),
  P('Before modeling, the 21 raw sensors were examined for informativeness. Figure 1 shows the trajectories of nine representative sensors for the first five engines of the training set. Several sensors (e.g. sensor 11, sensor 4, sensor 7) show a clear, visually identifiable drift as the engine approaches failure, while others remain essentially flat and were confirmed statistically to have near-zero variance — these correspond exactly to the six sensors excluded in Section 3.2.1.'),
  imgParagraph(FIGDIR + 'fig1_sensor_trajectories.png', 560, 405),
  Caption('Figure 1 — Sensor readings vs operating cycle, engines 1 to 5 (FD001 training set). Several sensors show a clear degradation trend as engines approach end-of-life; others (e.g. sensors 1, 5) are flat and uninformative under this single operating condition.'),

  P('Figure 2 shows the distribution of engine lifetimes across the 100 training engines, confirming substantial variability (min 128, max 362, mean ≈ 206 cycles) — a reminder that "normal" wear varies significantly between nominally identical units, which is precisely the variability predictive maintenance aims to account for individually rather than through a fixed schedule.'),
  imgParagraph(FIGDIR + 'fig2_lifetime_distribution.png', 420, 278),
  Caption('Figure 2 — Distribution of engine lifetimes (cycles until failure), FD001 training set, n = 100 engines.'),

  P('Figure 3 ranks the 15 informative sensors by their Pearson correlation with RUL. Sensor 11 shows the strongest (negative) correlation, followed by sensors 4, 15, 2 and 17, while sensors 7, 12, 20 and 21 show strong positive correlation — meaning these sensor values rise as the engine degrades. This ranking is consistent with published C-MAPSS analyses and is confirmed independently by the Random Forest feature importance in Section 4.4.'),
  imgParagraph(FIGDIR + 'fig3_sensor_rul_correlation.png', 420, 349),
  Caption('Figure 3 — Pearson correlation of each informative sensor with Remaining Useful Life.'),

  H2('4.2 Baseline models: Linear Regression, Random Forest, Gradient Boosting'),
  P('The three tabular baselines were trained on the 80-engine training split and evaluated on the 20-engine validation split and on the 100-engine test set (last cycle per engine). Results are summarized in Table 2.'),
  simpleTable(
    ['Model', 'Validation RMSE', 'Test RMSE', 'Test NASA score', 'Training time (s)'],
    [
      ['Linear Regression', '20.21', '21.88', '1307.6', '0.01'],
      ['Random Forest', '17.01', '18.08', '912.6', '28.68'],
      ['Gradient Boosting', '17.00', '18.37', '1047.7', '13.72'],
    ],
    [3000, 2400, 2200, 2400, 2400],
  ),
  new Paragraph({ text: '', spacing: { after: 200 } }),
  Caption('Table 2 — Baseline model performance on FD001 (validation: 20 held-out engines; test: 100 test engines, last cycle each).'),
  P('Both ensemble methods substantially outperform plain linear regression (roughly 17% lower test RMSE, and 22–30% lower NASA score), confirming that the relationship between sensor readings and RUL is meaningfully non-linear. Random Forest and Gradient Boosting perform similarly on RMSE, but Random Forest achieves a notably better (lower) NASA score, meaning its errors are, on average, less skewed toward the dangerous late-prediction side — likely a consequence of Random Forest\'s prediction-averaging behavior, which tends to smooth out extreme optimistic outliers more than boosting\'s sequential error-correction.'),

  H2('4.3 Deep learning model: LSTM'),
  P('The LSTM model (two stacked LSTM layers of 64 and 32 units, with dropout regularization, followed by two dense layers) was trained on 30-cycle sliding windows built at the engine level, using early stopping on validation loss to avoid overfitting. Training converged after 21 epochs (out of a maximum of 60), reaching a validation RMSE of 12.44 cycles — substantially lower than any tabular baseline. Figure 4 (training curves) shows the loss dropping sharply around epoch 9-10 as the model transitions from an early plateau to effectively learning the degradation pattern, then stabilizing.'),
  imgParagraph(FIGDIR + 'fig8_lstm_training_curve.png', 460, 283),
  Caption('Figure 4 — LSTM training and validation loss (MSE) across training epochs, with early stopping.'),

  H2('4.4 Comparative results'),
  simpleTable(
    ['Model', 'Validation RMSE', 'Test RMSE', 'Test NASA score', 'Training time (s)'],
    [
      ['Linear Regression', '20.21', '21.88', '1307.6', '0.01'],
      ['Gradient Boosting', '17.00', '18.37', '1047.7', '13.72'],
      ['Random Forest', '17.01', '18.08', '912.6', '28.68'],
      ['LSTM', '12.44', '15.41', '423.3', '219.37'],
    ],
    [3000, 2400, 2200, 2400, 2400],
  ),
  new Paragraph({ text: '', spacing: { after: 200 } }),
  Caption('Table 3 — Full model comparison on the FD001 test set (100 engines, last cycle each).'),
  imgParagraph(FIGDIR + 'fig4_rmse_comparison.png', 460, 283),
  Caption('Figure 5 — Test RMSE by model (lower is better).'),
  imgParagraph(FIGDIR + 'fig5_nasa_score_comparison.png', 460, 283),
  Caption('Figure 6 — Test NASA asymmetric score by model (lower is better).'),
  P('The LSTM model outperforms every tabular baseline on both metrics: a 14.7% lower RMSE than the best tabular model (Random Forest), and, more strikingly, a 53.6% lower NASA score — meaning that beyond simply being more accurate on average, the LSTM\'s errors are also far less skewed toward the dangerous, overly-optimistic side. This is consistent with the state-of-the-art findings discussed in Section 2.3.2: exploiting the temporal degradation trajectory, rather than treating each cycle as an independent snapshot, provides a real and substantial advantage for this problem.'),
  P('Figure 7 shows the LSTM\'s predicted RUL against the true RUL for all 100 test engines, sorted by true RUL. The model tracks the true degradation trend closely for low-to-medium RUL values (the operationally critical region, where maintenance decisions matter most), with visibly larger scatter for engines with high true RUL (i.e. engines observed early in their life, before degradation is strongly expressed in the sensors) — an expected and, from a safety standpoint, acceptable pattern: the model is most accurate exactly where accuracy matters most.'),
  imgParagraph(FIGDIR + 'fig6_true_vs_pred_lstm.png', 460, 349),
  Caption('Figure 7 — LSTM: true vs predicted RUL for all 100 FD001 test engines, sorted by true RUL.'),
  P('For direct visual contrast, Figure 10 shows the same true-vs-predicted view for the two tabular baselines. Both Random Forest and Gradient Boosting exhibit visibly more scatter throughout the RUL range, and in particular fail to track the steep drop in true RUL for the lowest-RUL engines as tightly as the LSTM — a visual confirmation of the quantitative critical-zone gap quantified in Section 4.6.'),
  imgParagraph(FIGDIR + 'fig10_baseline_true_vs_pred.png', 480, 211),
  Caption('Figure 10 — Random Forest and Gradient Boosting: true vs predicted RUL, FD001 test set (for direct visual comparison with Figure 7).'),

  H2('4.5 Feature importance and discussion'),
  P('Figure 8 shows the Random Forest feature importance ranking. Sensor 11 alone accounts for roughly 65% of total importance, with sensor 9 (14%) and sensor 4 (8%) as secondary contributors — a striking concentration that echoes the correlation ranking of Section 4.1 and is consistent with published C-MAPSS analyses, where sensor 11 (commonly identified as a static-pressure-related measurement at the High-Pressure Compressor outlet) is repeatedly reported as the single most predictive channel for this fault mode, which affects the HPC directly.'),
  imgParagraph(FIGDIR + 'fig7_feature_importance.png', 460, 349),
  Caption('Figure 8 — Top 12 features by Random Forest importance (Gini importance).'),
  P('Two practical observations follow from this result. First, this concentration of signal in a small number of sensors suggests that a lighter, cheaper sensing setup could, in principle, capture most of the predictive information for this specific fault mode — a relevant consideration for real-world instrumentation cost. Second, and more importantly for model choice, it shows that the LSTM\'s advantage over the tabular models is not primarily about discovering hidden relevant sensors (the same sensors dominate importance in both cases), but about how it uses the temporal evolution of those sensors — i.e. the shape and rate of change of the degradation curve, not just its current value — which a snapshot-based tabular model cannot represent by construction.'),
  P('Overall, these results validate the central hypothesis of this study (Section 1.3): machine learning, and sequence-aware deep learning in particular, can predict RUL from raw multivariate sensor data with a level of accuracy (RMSE of roughly 15 cycles, on engines with typical lifetimes of 128–362 cycles) that is directly actionable for scheduling maintenance meaningfully ahead of failure, while the NASA score confirms this is achieved without a dangerous bias toward late, overly optimistic predictions.'),

  H2('4.6 Error analysis by operational criticality zone'),
  P('Aggregate RMSE (Section 4.4) can mask an important operational nuance: not all prediction errors matter equally. An engine with a true RUL of 200 cycles being predicted at 180 cycles is a minor discrepancy; an engine with a true RUL of 10 cycles being predicted at 30 is a maintenance-scheduling near-miss. To examine this, the test set was split into a "critical" zone (true RUL below 50 cycles — where a maintenance decision is operationally urgent) and a "non-critical" zone (true RUL of 50 cycles or more), and RMSE was recomputed within each zone for all three best-performing models.'),
  imgParagraph(FIGDIR + 'fig9_error_by_zone.png', 460, 296),
  Caption('Figure 9 — Prediction error (RMSE) by operational criticality zone, FD001 test set.'),
  new Table({
    width: { size: 9200, type: WidthType.DXA },
    rows: [
      new TableRow({ tableHeader: true, children: [
        cell('Zone', { bold: true, shade: 'D9D9D9', width: 3400 }),
        cell('Engines (n)', { bold: true, shade: 'D9D9D9', width: 1800 }),
        cell('RF RMSE', { bold: true, shade: 'D9D9D9', width: 1500 }),
        cell('GB RMSE', { bold: true, shade: 'D9D9D9', width: 1500 }),
        cell('LSTM RMSE', { bold: true, shade: 'D9D9D9', width: 1500 }),
      ]}),
      new TableRow({ children: [
        cell('Critical (RUL < 50)', { width: 3400 }),
        cell('30', { width: 1800 }),
        cell('16.47', { width: 1500 }),
        cell('16.49', { width: 1500 }),
        cell('6.14', { width: 1500 }),
      ]}),
      new TableRow({ children: [
        cell('Non-critical (RUL ≥ 50)', { width: 3400 }),
        cell('70', { width: 1800 }),
        cell('18.73', { width: 1800 }),
        cell('19.13', { width: 1500 }),
        cell('17.98', { width: 1500 }),
      ]}),
    ],
  }),
  new Paragraph({ text: '', spacing: { after: 200 } }),
  Caption('Table 4 — Prediction error (RMSE) by operational criticality zone.'),
  P('This breakdown reveals the LSTM\'s advantage is far larger than the aggregate numbers suggest: in the critical zone, its RMSE (6.14 cycles) is roughly 2.7 times lower than either tabular baseline (16.47–16.49 cycles), while in the non-critical zone the three models perform much more similarly (17.98–19.13 cycles). In other words, the LSTM\'s temporal-sequence advantage concentrates almost entirely in exactly the region where it matters most operationally: engines nearing failure, where an accurate RUL estimate directly determines whether maintenance is scheduled in time. This is, from an engineering standpoint, a substantially stronger result than the aggregate RMSE comparison alone conveys, and it directly reinforces the recommendation, developed further in Section 5, to prioritize sequence-aware models for any operational deployment of this approach.'),

  H2('4.7 Cross-check against the literature'),
  P('The ordering of model families observed here — tabular baselines within a similar range of each other, LSTM as a clear improvement — is consistent with the qualitative literature positioning summarized in Table 1 (Section 2.4), which found LSTM to be reported as a strong improvement over classical regression and plain RNN baselines, with 1D-CNN architectures reported as a further potential improvement. This consistency gives reasonable confidence that the experimental pipeline built for this study (feature selection, RUL capping, train/validation split by engine, evaluation protocol) is methodologically sound, even though this study does not replicate exact published numbers, for the preprocessing-comparability reasons noted in Section 2.4.'),

  H2('4.8 Threats to validity'),
  P('In the interest of scientific rigor, three categories of threats to the validity of the results above are made explicit here, in addition to the broader limitations discussed in Section 6.2.'),
  H3('4.8.1 Internal validity'),
  P('The engine-level train/validation split (Section 3.2.4) and the strict train-only fitting of the normalization scaler (Section 3.2.3) were specifically designed to prevent data leakage, which is the most common internal-validity threat in time-series prognostics studies. The single fixed random seed (42) used throughout means the exact numerical results reported are not subject to run-to-run variance in this report; however, this also means the results represent one draw of the train/validation split rather than an average over several — a limitation partially mitigated by the fact that the test set (used for all headline comparisons in Section 4.4) is fixed by the dataset\'s official train/test partition and never touched during model selection.'),
  H3('4.8.2 External validity'),
  P('As emphasized throughout (Sections 1.4, 2.5, 6.2), external validity beyond the FD001 simulation — to real engines, other fault modes, or multi-condition operation — is the most significant open question raised by this study, and is explicitly not claimed to be resolved here.'),
  H3('4.8.3 Construct validity'),
  P('The RMSE and NASA score metrics (Section 3.4) are standard in the literature and were adopted deliberately for comparability (Section 4.7), but they remain proxies for the real quantity of interest — the safety and economic outcome of a maintenance decision informed by the model — rather than a direct measurement of it; Section 5\'s discussion of operational implications is, in part, an attempt to bridge that gap explicitly rather than treat the statistical metrics as self-sufficient evidence of real-world value.'),
  new Paragraph({ children: [new PageBreak()] }),
];

module.exports = { section4 };
