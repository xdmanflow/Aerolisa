const fs = require('fs');
const h = require('./build_report.js');
const {
  H1, H2, H3, P, Bullet, Caption, imgParagraph, cell,
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  TableOfContents, PageBreak, PageNumber, Footer, Header,
  convertInchesToTwip, VerticalAlign, YELLOW, DARKBLUE, GREY,
} = h;

const FIGDIR = 'figs/';

// ---------- COVER PAGE ----------
// Title kept <= 60 characters (incl. spaces) per CESI writing guide (Section 1, "Remarques concernant le titre")
const cover = [
  new Paragraph({ spacing: { before: 1000 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'CESI École d\'Ingénieurs — Toulouse', bold: true, size: 28, color: DARKBLUE })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 100 },
    children: [new TextRun({ text: 'Application de la Démarche Scientifique (ADS) — Scientific Approach Application (SAA)', size: 22, color: GREY })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60 },
    children: [new TextRun({ text: '4th Year Report — Program: CS Engineer, AI & Data Science track', size: 20, color: GREY, italics: true })],
  }),
  new Paragraph({ spacing: { before: 700 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({
      text: 'Predictive Maintenance of Turbofan Engines',
      bold: true, size: 40,
    })],
  }),
  new Paragraph({ spacing: { before: 150 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'Estimating Remaining Useful Life from Multivariate Sensor Data: a Comparison of Machine Learning and Deep Learning Approaches on NASA C-MAPSS', italics: true, size: 24 })],
  }),
  new Paragraph({ spacing: { before: 1100 }, children: [] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'Author: [Student First Name LAST NAME]', size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60 }, children: [new TextRun({ text: 'Document type: Scientific Approach Application (SAA) report', size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60 }, children: [new TextRun({ text: 'Date: [Submission date]', size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60 }, children: [new TextRun({ text: 'School: CESI École d\'Ingénieurs, Toulouse campus — Promotion 2026–2027', size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60 }, children: [new TextRun({ text: 'Academic tutor: [Tutor Name]', size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60 }, children: [new TextRun({ text: 'Host organization: none — independent research project using public open datasets', size: 22 })] }),
  new Paragraph({ spacing: { before: 1200 }, children: [] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'Confidentiality: none — this study uses exclusively public, open-access datasets', size: 18, color: GREY, italics: true })] }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- CONFIDENTIALITY SHEET ----------
const confidentiality = [
  H1('Confidentiality Notice'),
  P('This report is the result of an independent academic research project (Application de la Démarche Scientifique / Scientific Approach Application) carried out as part of the 4th-year curriculum at CESI École d\'Ingénieurs.'),
  P('The study relies exclusively on public, open-access data — NASA\'s C-MAPSS Turbofan Engine Degradation Simulation Dataset (FD001 subset) — and does not involve any proprietary, confidential, or company-owned data, systems, or processes.'),
  P('Consequently, no confidentiality restriction applies to this report. It may be freely consulted, reproduced for academic evaluation purposes, and archived by CESI École d\'Ingénieurs.'),
  new Paragraph({ spacing: { before: 900 }, children: [] }),
  new Paragraph({ children: [new TextRun({ text: 'Student signature:', bold: true })], spacing: { after: 600 } }),
  new Paragraph({ children: [new TextRun({ text: 'Academic tutor signature:', bold: true })], spacing: { after: 200 } }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- ACKNOWLEDGMENTS ----------
const acknowledgments = [
  H1('Acknowledgments'),
  P('I would like to thank my academic tutor at CESI École d\'Ingénieurs for their guidance and feedback throughout this Scientific Approach Application project, and for helping frame the initial problem into a well-scoped, feasible research question.'),
  P('I also gratefully acknowledge NASA\'s Prognostics Center of Excellence for making the C-MAPSS dataset publicly available, which made this comparative study possible without requiring access to proprietary industrial data.'),
  P('Finally, I thank my peers for the discussions that helped sharpen the interpretation of the results presented in this report.'),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- ABSTRACT (EN) ----------
const abstractEN = [
  H1('Abstract'),
  P('Unplanned turbofan engine failures are safety-critical and economically damaging for airlines, while conventional schedule-based preventive maintenance often replaces components well before the end of their useful life, generating unnecessary cost. Predictive maintenance, which anticipates failure from real-time sensor data, offers a middle path but requires models able to accurately estimate a component\'s Remaining Useful Life (RUL) from noisy, multivariate, time-series sensor readings.'),
  P('This study investigates and compares classical machine learning models (Linear Regression, Random Forest, Gradient Boosting) and a deep learning sequence model (LSTM) for RUL prediction, using the FD001 subset of NASA\'s C-MAPSS (Commercial Modular Aero-Propulsion System Simulation) turbofan degradation dataset, a widely used benchmark in prognostics and health management (PHM) research.'),
  P('Following a rigorous scientific approach, the problem is first framed in terms of its safety and economic stakes; the state of the art in RUL prediction is then reviewed; candidate models are selected, implemented and evaluated using RMSE and the NASA asymmetric scoring function, which penalizes late (optimistic) predictions more heavily than early ones. Results show that the LSTM model achieves the best performance (test RMSE = 15.41 cycles, NASA score = 423.3), clearly outperforming Random Forest (RMSE = 18.08, score = 912.6), Gradient Boosting (RMSE = 18.37, score = 1047.7) and Linear Regression (RMSE = 21.88, score = 1307.6), confirming the value of modeling engine degradation as a temporal sequence rather than as independent snapshots.'),
  P('The study concludes with a discussion of the operational relevance of these results, their limitations (notably the simulation-to-reality gap and the use of a single operating condition), and perspectives for future work, including multi-condition generalization, uncertainty quantification, and real-world deployment considerations.'),
  P('Keywords: Predictive maintenance, Remaining Useful Life (RUL), Machine Learning, LSTM, Turbofan engines, C-MAPSS, Prognostics and Health Management.'),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- RÉSUMÉ (FR) ----------
const resumeFR = [
  H1('Résumé'),
  P('Les pannes non planifiées de moteurs d\'avion présentent un enjeu critique pour la sécurité et un coût économique important pour les compagnies aériennes, tandis que la maintenance préventive classique, basée sur un calendrier fixe, remplace souvent des composants avant la fin réelle de leur durée de vie utile, générant un surcoût inutile. La maintenance prédictive, qui anticipe la panne à partir de données capteurs en temps réel, propose une voie intermédiaire, mais nécessite des modèles capables d\'estimer avec précision la durée de vie résiduelle (Remaining Useful Life, RUL) d\'un composant à partir de mesures capteurs multivariées, bruitées et temporelles.'),
  P('Cette étude examine et compare des modèles de machine learning classiques (régression linéaire, forêt aléatoire, gradient boosting) et un modèle d\'apprentissage profond séquentiel (LSTM) pour la prédiction de la RUL, en utilisant le sous-ensemble FD001 du jeu de données C-MAPSS de la NASA, une référence largement utilisée dans la recherche en pronostic et gestion de la santé des systèmes (PHM).'),
  P('En suivant une démarche scientifique rigoureuse, le problème est d\'abord posé en termes d\'enjeux sécuritaires et économiques ; l\'état de l\'art de la prédiction de RUL est ensuite analysé ; des modèles candidats sont sélectionnés, implémentés et évalués à l\'aide de la RMSE et de la fonction de score asymétrique de la NASA, qui pénalise davantage les prédictions tardives (optimistes) que les prédictions précoces. Les résultats montrent que le modèle LSTM obtient la meilleure performance (RMSE test = 15,41 cycles, score NASA = 423,3), surpassant nettement la forêt aléatoire (RMSE = 18,08, score = 912,6), le gradient boosting (RMSE = 18,37, score = 1047,7) et la régression linéaire (RMSE = 21,88, score = 1307,6), confirmant l\'intérêt de modéliser la dégradation moteur comme une séquence temporelle plutôt que comme des instantanés indépendants.'),
  P('L\'étude se conclut par une discussion sur la pertinence opérationnelle de ces résultats, leurs limites (notamment l\'écart simulation-réalité et l\'utilisation d\'une seule condition opérationnelle), et des perspectives de travaux futurs, incluant la généralisation multi-conditions, la quantification de l\'incertitude et les enjeux de déploiement en conditions réelles.'),
  P('Mots-clés : Maintenance prédictive, Durée de vie résiduelle (RUL), Machine Learning, LSTM, Moteurs turbofan, C-MAPSS, Pronostic et gestion de la santé des systèmes.'),
  new Paragraph({ children: [new PageBreak()] }),
];

fs.writeFileSync('/tmp/section_status.txt', 'part1 done');
module.exports = { cover, confidentiality, acknowledgments, abstractEN, resumeFR };
