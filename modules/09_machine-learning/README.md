# Module 09 · Machine learning

**Roles:** DS · AI · **Size:** 3 weekends · **Priority:** P0 · **Builds:** Aerolisa M6 (engine health v2)

## Why this matters
Airbus data scientist apprenticeships name the methods directly ("random forest, GBT, linear regression") and Skywise data scientist roles apply them to operational use cases. Interviews test understanding more than libraries: leakage, validation, metric choice, explaining a model to an engineer.

## 🎯 Apprenticeship level (must)
**Math, only what ML uses**
- [ ] Vectors, dot product, matrices, matrix × vector as a transformation; norms and distances
- [ ] Eigenvectors intuition; PCA as finding directions of maximal variance
- [ ] Derivatives, partial derivatives, gradient, chain rule; gradient descent and learning rate

**Machine learning**
- [ ] Supervised vs unsupervised; regression vs classification; bias–variance trade-off
- [ ] Train / validation / test; cross-validation; **GroupKFold** (never split one engine across train and test); time-aware splits; data leakage patterns
- [ ] Linear regression (implemented once from scratch with gradient descent), regularization (L1, L2)
- [ ] Logistic regression, decision boundary, probability calibration
- [ ] Decision trees, random forest, gradient boosting (XGBoost / LightGBM): how they work, key hyperparameters
- [ ] kNN, k-means, PCA
- [ ] Metrics: MAE, RMSE, R²; precision, recall, F1, ROC-AUC, PR-AUC; confusion matrix; choosing a threshold by cost
- [ ] Feature engineering: scaling, encoding, rolling and lag features, interactions; scikit-learn `Pipeline` and `ColumnTransformer`
- [ ] Hyperparameter tuning (grid, random, early stopping)
- [ ] Explainability: permutation importance, SHAP values, partial dependence; explaining one prediction to a non-data person
- [ ] Baselines first; honest comparison tables

## 🚀 Pro level
- [ ] Gradient boosting internals (residual fitting), bagging vs boosting variance
- [ ] Imbalanced data: class weights, resampling, focal loss concept
- [ ] Optuna for tuning
- [ ] Model monitoring: data drift, concept drift

## Steps
**Weekend 1: math + linear models**
1. Learn: 3Blue1Brown *Essence of Linear Algebra* (episodes 1–4, 7, 9, 14) on the commute; ISLP chapters 2–3 (statistical learning, linear regression).
2. Practice: gradient descent linear regression from scratch in NumPy; compare with scikit-learn on C-MAPSS FD001 RUL.
3. Apply: Aerolisa M6, leak-free validation setup (GroupKFold by unit) + baseline + linear model.

**Weekend 2: trees and boosting**
4. Learn: ISLP chapter 8 (trees), XGBoost docs intro; StatQuest on random forest and gradient boosting.
5. Practice: random forest and LightGBM/XGBoost on C-MAPSS with tuned hyperparameters; comparison table.
6. Apply: Aerolisa M6, model comparison and MLflow tracking.

**Weekend 3: classification, metrics, explainability**
7. Learn: ISLP chapter 4 (classification); SHAP docs.
8. Practice: reframe as "fails within 30 cycles?" classification; ROC/PR curves; choose a threshold from a cost table (missed failure vs unnecessary inspection); SHAP for one engine.
9. Apply: Aerolisa M6, alert model + explanations stored on `EngineHealthSnapshot`.

## Exit test (90 min, no AI, docs allowed)
Raw CSV → leak-free validated model → comparison against a baseline → one SHAP explanation → a 5-line written conclusion. Then explain, out loud, why random splitting would have lied.

## Resources
- ISLP (free) · scikit-learn user guide · *Mathematics for Machine Learning* (free) · 3Blue1Brown · StatQuest

## Gaps found
-

## Notes
-

## Work
[`work/`](work)
