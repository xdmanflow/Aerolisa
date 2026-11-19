import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib

RUL_CAP = 125  # standard piecewise-linear RUL cap used in C-MAPSS literature (Heimes 2008)

train = pd.read_parquet('data/train_FD001_rul.parquet')
test = pd.read_parquet('data/test_FD001_rul.parquet')
with open('data/informative_sensors.txt') as f:
    sensors = f.read().split(',')

feature_cols = ['op1', 'op2', 'op3'] + sensors

# Apply piecewise-linear RUL cap (train only — standard practice, avoids penalizing
# the model for early-life cycles where degradation is not yet observable)
train['RUL_capped'] = train['RUL'].clip(upper=RUL_CAP)

# Normalize features using train statistics only
scaler = MinMaxScaler()
train[feature_cols] = scaler.fit_transform(train[feature_cols])
test[feature_cols] = scaler.transform(test[feature_cols])
joblib.dump(scaler, 'data/scaler.pkl')

# Held-out validation split BY ENGINE (not by row) to avoid leakage across cycles
# of the same engine between train and validation
rng = np.random.RandomState(42)
units = train['unit'].unique()
val_units = rng.choice(units, size=20, replace=False)
train_units = np.setdiff1d(units, val_units)

train_set = train[train['unit'].isin(train_units)].copy()
val_set = train[train['unit'].isin(val_units)].copy()

train_set.to_parquet('data/train_split.parquet')
val_set.to_parquet('data/val_split.parquet')
test.to_parquet('data/test_split.parquet')

with open('data/feature_cols.txt', 'w') as f:
    f.write(','.join(feature_cols))

print("Feature columns:", feature_cols)
print("Train rows:", len(train_set), "| Val rows:", len(val_set), "| Test rows:", len(test))
print("Train engines:", len(train_units), "| Val engines:", len(val_units))
