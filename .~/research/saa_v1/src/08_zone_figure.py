import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 9

df = pd.read_csv('data/error_by_zone.csv')

fig, ax = plt.subplots(figsize=(6.5, 4.2))
x = np.arange(len(df))
width = 0.25
ax.bar(x - width, df['RF_rmse'], width, label='Random Forest', color='#2c6e91')
ax.bar(x, df['GB_rmse'], width, label='Gradient Boosting', color='#e67e22')
ax.bar(x + width, df['LSTM_rmse'], width, label='LSTM', color='#c0392b')
ax.set_xticks(x)
ax.set_xticklabels(df['zone'])
ax.set_ylabel('RMSE (cycles)')
ax.set_title('Prediction error by operational zone (FD001 test set)')
ax.legend()
for i, row in df.iterrows():
    ax.text(i - width, row['RF_rmse'] + 0.3, f"{row['RF_rmse']:.1f}", ha='center', fontsize=8)
    ax.text(i, row['GB_rmse'] + 0.3, f"{row['GB_rmse']:.1f}", ha='center', fontsize=8)
    ax.text(i + width, row['LSTM_rmse'] + 0.3, f"{row['LSTM_rmse']:.1f}", ha='center', fontsize=8)
fig.tight_layout()
fig.savefig('figs/fig9_error_by_zone.png', bbox_inches='tight')
plt.close(fig)
print("Saved fig9.")
