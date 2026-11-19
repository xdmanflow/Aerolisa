import pandas as pd
import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 9

with open('data/baseline_results.json') as f:
    baseline = json.load(f)
with open('data/lstm_results.json') as f:
    lstm = json.load(f)

all_results = dict(baseline)
all_results['LSTM'] = {k: v for k, v in lstm.items() if k in ['val_rmse', 'test_rmse', 'test_nasa_score', 'train_time_s']}

df = pd.DataFrame(all_results).T
df.to_csv('data/all_results_table.csv')
print(df)

# --- Fig 4: RMSE comparison bar chart ---
fig, ax = plt.subplots(figsize=(6.5, 4))
order = ['Linear Regression', 'Gradient Boosting', 'Random Forest', 'LSTM']
vals = [all_results[m]['test_rmse'] for m in order]
colors = ['#95a5a6', '#e67e22', '#2c6e91', '#c0392b']
bars = ax.bar(order, vals, color=colors)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + 0.3, f'{v:.1f}', ha='center', fontsize=9)
ax.set_ylabel('Test RMSE (cycles)')
ax.set_title('Model comparison — RUL prediction error on FD001 test set')
fig.tight_layout()
fig.savefig('figs/fig4_rmse_comparison.png', bbox_inches='tight')
plt.close(fig)

# --- Fig 5: NASA score comparison ---
fig, ax = plt.subplots(figsize=(6.5, 4))
vals2 = [all_results[m]['test_nasa_score'] for m in order]
bars = ax.bar(order, vals2, color=colors)
for b, v in zip(bars, vals2):
    ax.text(b.get_x() + b.get_width()/2, v + 15, f'{v:.0f}', ha='center', fontsize=9)
ax.set_ylabel('NASA scoring function (lower = better)')
ax.set_title('Model comparison — asymmetric NASA score (penalizes late predictions)')
fig.tight_layout()
fig.savefig('figs/fig5_nasa_score_comparison.png', bbox_inches='tight')
plt.close(fig)

# --- Fig 6: True vs Predicted RUL (LSTM, best model) ---
lstm_pred = pd.read_csv('data/lstm_test_predictions.csv').sort_values('RUL')
fig, ax = plt.subplots(figsize=(6.5, 5))
x = np.arange(len(lstm_pred))
ax.plot(x, lstm_pred['RUL'], label='True RUL', color='black', linewidth=1.3)
ax.scatter(x, lstm_pred['pred_LSTM'], label='LSTM predicted RUL', color='#c0392b', s=14, alpha=0.75)
ax.set_xlabel('Test engine (sorted by true RUL)')
ax.set_ylabel('Remaining Useful Life (cycles)')
ax.set_title('LSTM: true vs predicted RUL — FD001 test set (100 engines)')
ax.legend()
fig.tight_layout()
fig.savefig('figs/fig6_true_vs_pred_lstm.png', bbox_inches='tight')
plt.close(fig)

# --- Fig 7: Random Forest feature importance ---
imp = pd.read_csv('data/rf_feature_importance.csv', index_col=0).squeeze('columns').sort_values()
fig, ax = plt.subplots(figsize=(6.5, 5))
ax.barh(imp.index[-12:], imp.values[-12:], color='#2c6e91')
ax.set_xlabel('Feature importance (Random Forest, Gini)')
ax.set_title('Top predictive features for RUL estimation')
fig.tight_layout()
fig.savefig('figs/fig7_feature_importance.png', bbox_inches='tight')
plt.close(fig)

# --- Fig 8: LSTM training curves ---
hist = pd.read_csv('data/lstm_history.csv')
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(hist['loss'], label='Training loss (MSE)')
ax.plot(hist['val_loss'], label='Validation loss (MSE)')
ax.set_xlabel('Epoch')
ax.set_ylabel('MSE loss')
ax.set_title('LSTM training curves (early stopping at best validation loss)')
ax.legend()
fig.tight_layout()
fig.savefig('figs/fig8_lstm_training_curve.png', bbox_inches='tight')
plt.close(fig)

print("All results figures generated.")
