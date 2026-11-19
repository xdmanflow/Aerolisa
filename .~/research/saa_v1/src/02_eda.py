import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 9

train = pd.read_parquet('data/train_FD001_rul.parquet')
sensor_cols = [c for c in train.columns if c.startswith('sensor_')]

# 1. Identify constant / non-informative sensors
stds = train[sensor_cols].std()
constant_sensors = stds[stds < 1e-4].index.tolist()
print("Near-constant sensors (to drop):", constant_sensors)
informative_sensors = [c for c in sensor_cols if c not in constant_sensors]
print(f"Informative sensors: {len(informative_sensors)} / {len(sensor_cols)}")

# 2. Plot sensor trajectories for 5 example engines
fig, axes = plt.subplots(3, 3, figsize=(11, 8))
example_sensors = ['sensor_2', 'sensor_3', 'sensor_4', 'sensor_7', 'sensor_11',
                    'sensor_12', 'sensor_15', 'sensor_17', 'sensor_20']
for ax, sensor in zip(axes.flat, example_sensors):
    for unit in [1, 2, 3, 4, 5]:
        d = train[train['unit'] == unit]
        ax.plot(d['cycle'], d[sensor], alpha=0.7, linewidth=0.9)
    ax.set_title(sensor, fontsize=9)
    ax.set_xlabel('Cycle', fontsize=7)
    ax.tick_params(labelsize=7)
fig.suptitle('Sensor readings vs operating cycle — engines 1 to 5 (FD001)', fontsize=11)
fig.tight_layout()
fig.savefig('figs/fig1_sensor_trajectories.png', bbox_inches='tight')
plt.close(fig)

# 3. RUL distribution
fig, ax = plt.subplots(figsize=(6, 4))
max_cycles = train.groupby('unit')['cycle'].max()
ax.hist(max_cycles, bins=20, color='#2c6e91', edgecolor='white')
ax.set_xlabel('Engine life (cycles until failure)')
ax.set_ylabel('Number of engines')
ax.set_title('Distribution of engine lifetimes — FD001 training set (n=100)')
fig.tight_layout()
fig.savefig('figs/fig2_lifetime_distribution.png', bbox_inches='tight')
plt.close(fig)

# 4. Sensor correlation with RUL (informative subset)
corrs = train[informative_sensors + ['RUL']].corr()['RUL'].drop('RUL').sort_values()
fig, ax = plt.subplots(figsize=(6, 5))
colors = ['#c0392b' if v < 0 else '#2c6e91' for v in corrs.values]
ax.barh(corrs.index, corrs.values, color=colors)
ax.set_xlabel('Pearson correlation with RUL')
ax.set_title('Sensor correlation with Remaining Useful Life')
fig.tight_layout()
fig.savefig('figs/fig3_sensor_rul_correlation.png', bbox_inches='tight')
plt.close(fig)

with open('data/informative_sensors.txt', 'w') as f:
    f.write(','.join(informative_sensors))

print("EDA figures saved.")
print(corrs)
