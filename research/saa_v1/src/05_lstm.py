import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import mean_squared_error
import json, time

tf.random.set_seed(42)
np.random.seed(42)

SEQ_LEN = 30

with open('data/feature_cols.txt') as f:
    feature_cols = f.read().split(',')

train_set = pd.read_parquet('data/train_split.parquet')
val_set = pd.read_parquet('data/val_split.parquet')
test_set = pd.read_parquet('data/test_split.parquet')

def build_sequences(df, feature_cols, seq_len, label_col='RUL_capped', is_test=False):
    X, y, unit_ids = [], [], []
    for unit, g in df.groupby('unit'):
        g = g.sort_values('cycle')
        vals = g[feature_cols].values
        labels = g[label_col].values if label_col in g.columns else g['RUL'].clip(upper=125).values
        n = len(g)
        if is_test:
            # For test: take the LAST seq_len cycles (pad with first row if engine history is shorter)
            if n >= seq_len:
                seq = vals[-seq_len:]
            else:
                pad = np.repeat(vals[0:1], seq_len - n, axis=0)
                seq = np.vstack([pad, vals])
            X.append(seq)
            y.append(labels[-1])
            unit_ids.append(unit)
        else:
            if n < seq_len:
                continue
            for i in range(n - seq_len + 1):
                X.append(vals[i:i+seq_len])
                y.append(labels[i+seq_len-1])
    return np.array(X), np.array(y), unit_ids

Xtr, ytr, _ = build_sequences(train_set, feature_cols, SEQ_LEN)
Xval, yval, _ = build_sequences(val_set, feature_cols, SEQ_LEN)
test_last = test_set.sort_values('cycle').groupby('unit').tail(1)[['unit', 'RUL']].reset_index(drop=True)
Xtest, ytest, test_units = build_sequences(test_set, feature_cols, SEQ_LEN, is_test=True)
ytest = test_last.set_index('unit').loc[test_units]['RUL'].values

print("Train sequences:", Xtr.shape, "Val sequences:", Xval.shape, "Test sequences:", Xtest.shape)

n_features = len(feature_cols)

model = keras.Sequential([
    layers.Input(shape=(SEQ_LEN, n_features)),
    layers.LSTM(64, return_sequences=True),
    layers.Dropout(0.2),
    layers.LSTM(32),
    layers.Dropout(0.2),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='relu'),
])
model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-3), loss='mse', metrics=['mae'])
model.summary()

t0 = time.time()
history = model.fit(
    Xtr, ytr,
    validation_data=(Xval, yval),
    epochs=60,
    batch_size=64,
    callbacks=[keras.callbacks.EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)],
    verbose=2,
)
train_time = time.time() - t0

def rmse(a, b):
    return np.sqrt(mean_squared_error(a, b))

def nasa_score(y_true, y_pred):
    d = y_pred - y_true
    s = np.where(d < 0, np.exp(-d / 13) - 1, np.exp(d / 10) - 1)
    return np.sum(s)

val_pred = np.clip(model.predict(Xval, verbose=0).flatten(), 0, None)
test_pred = np.clip(model.predict(Xtest, verbose=0).flatten(), 0, None)

results = {
    'val_rmse': round(float(rmse(yval, val_pred)), 2),
    'test_rmse': round(float(rmse(ytest, test_pred)), 2),
    'test_nasa_score': round(float(nasa_score(ytest, test_pred)), 1),
    'train_time_s': round(train_time, 2),
    'epochs_trained': len(history.history['loss']),
}
print(json.dumps(results, indent=2))

with open('data/lstm_results.json', 'w') as f:
    json.dump(results, f, indent=2)

pd.DataFrame({'loss': history.history['loss'], 'val_loss': history.history['val_loss']}).to_csv('data/lstm_history.csv', index=False)
pd.DataFrame({'unit': test_units, 'RUL': ytest, 'pred_LSTM': test_pred}).to_csv('data/lstm_test_predictions.csv', index=False)

model.save('data/lstm_model.keras')
