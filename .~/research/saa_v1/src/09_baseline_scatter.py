import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 9

base = pd.read_csv('data/baseline_test_predictions.csv').sort_values('RUL')
x = np.arange(len(base))

fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.2), sharey=True)
for ax, col, name, color in zip(axes, ['pred_RF', 'pred_GB'], ['Random Forest', 'Gradient Boosting'], ['#2c6e91', '#e67e22']):
    ax.plot(x, base['RUL'], color='black', linewidth=1.2, label='True RUL')
    ax.scatter(x, base[col], color=color, s=12, alpha=0.75, label=f'{name} predicted')
    ax.set_title(name, fontsize=10)
    ax.set_xlabel('Test engine (sorted by true RUL)')
    ax.legend(fontsize=8)
axes[0].set_ylabel('Remaining Useful Life (cycles)')
fig.suptitle('Baseline models: true vs predicted RUL — FD001 test set', fontsize=11)
fig.tight_layout()
fig.savefig('figs/fig10_baseline_true_vs_pred.png', bbox_inches='tight')
plt.close(fig)
print("Saved fig10.")
