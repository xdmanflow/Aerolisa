import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import json, time

def nasa_score(y_true, y_pred):
    """PHM08/NASA asymmetric scoring function: penalizes late predictions
    (predicted RUL > true RUL, i.e. predicting the engine lasts longer than
    it really does) more heavily than early ones, reflecting real safety priorities."""
    d = y_pred - y_true
    s = np.where(d < 0, np.exp(-d / 13) - 1, np.exp(d / 10) - 1)
    return np.sum(s)

def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

with open('data/feature_cols.txt') as f:
    feature_cols = f.read().split(',')

train_set = pd.read_parquet('data/train_split.parquet')
val_set = pd.read_parquet('data/val_split.parquet')
test_set = pd.read_parquet('data/test_split.parquet')

# For test set: NASA convention evaluates on the LAST cycle of each engine only
test_last = test_set.sort_values('cycle').groupby('unit').tail(1).reset_index(drop=True)

Xtr, ytr = train_set[feature_cols], train_set['RUL_capped']
Xval, yval = val_set[feature_cols], val_set['RUL'].clip(upper=125)
Xtest, ytest = test_last[feature_cols], test_last['RUL']

results = {}

models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=300, max_depth=10, min_samples_leaf=5,
                                            random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=300, max_depth=3, learning_rate=0.05,
                                                    random_state=42),
}

for name, model in models.items():
    t0 = time.time()
    model.fit(Xtr, ytr)
    train_time = time.time() - t0

    val_pred = np.clip(model.predict(Xval), 0, None)
    test_pred = np.clip(model.predict(Xtest), 0, None)

    results[name] = {
        'val_rmse': round(rmse(yval, val_pred), 2),
        'test_rmse': round(rmse(ytest, test_pred), 2),
        'test_nasa_score': round(float(nasa_score(ytest.values, test_pred)), 1),
        'train_time_s': round(train_time, 2),
    }
    print(name, results[name])

# Feature importance from Random Forest for the report
rf = models['Random Forest']
importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
importances.to_csv('data/rf_feature_importance.csv')

# Save test predictions for RF (best baseline candidate) for the true-vs-predicted plot
test_last['pred_RF'] = np.clip(models['Random Forest'].predict(Xtest), 0, None)
test_last['pred_GB'] = np.clip(models['Gradient Boosting'].predict(Xtest), 0, None)
test_last[['unit', 'RUL', 'pred_RF', 'pred_GB']].to_csv('data/baseline_test_predictions.csv', index=False)

with open('data/baseline_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(json.dumps(results, indent=2))
