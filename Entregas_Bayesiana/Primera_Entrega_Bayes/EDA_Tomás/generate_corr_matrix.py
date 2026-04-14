import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.figsize': (12, 10), 'font.family': 'sans-serif'})

path = 'data/csgo_games.csv'
df = pd.read_csv(path)

metrics = ['rating', 'impact', 'kdr', 'dmr', 'kpr', 'clutch_win_perc']
for team in ['t1', 't2']:
    for m in metrics:
        cols = [f"{team}_player{i}_{m}" for i in range(1, 6)]
        df[f"{team}_avg_{m}"] = df[cols].mean(axis=1)

for m in metrics:
    df[f"diff_{m}"] = df[f"t1_avg_{m}"] - df[f"t2_avg_{m}"]

df['target_t1_win'] = (df['winner'] == 't1').astype(int)
df['diff_rank'] = df['t1_world_rank'] - df['t2_world_rank']

# Select variables for correlation matrix
corr_vars = [
    'target_t1_win', 
    'diff_rating', 
    'diff_impact', 
    'diff_rank',
    'diff_dmr',
    'diff_kpr',
    'diff_kdr',
    'diff_clutch_win_perc'
]

corr_data = df[corr_vars].corr()

# Rename columns for better visualization
rename_map = {
    'target_t1_win': 'Victoria T1',
    'diff_rating': 'Diferencia Rating (Prior)',
    'diff_impact': 'Diferencia Impacto (Prior)',
    'diff_rank': 'Diferencia Ranking',
    'diff_dmr': 'Diferencia Daño (DMR)',
    'diff_kpr': 'Diferencia Bajas (KPR)',
    'diff_kdr': 'Diferencia K/D Ratio',
    'diff_clutch_win_perc': 'Diferencia Clutch %'
}
corr_data = corr_data.rename(columns=rename_map, index=rename_map)

# Generate Heatmap
plt.figure(figsize=(14, 12))
mask = np.triu(np.ones_like(corr_data, dtype=bool))
sns.heatmap(corr_data, annot=True, cmap='RdBu_r', center=0, fmt='.2f', 
            mask=mask, square=True, linewidths=.5, cbar_kws={"shrink": .8})
plt.title('Matriz de Correlación Completa: Variables de Victoria', fontsize=18, pad=20)
plt.tight_layout()
plt.savefig('overleaf/matriz_correlacion_completa.png', dpi=300)
print("Matriz de correlación generada y guardada.")
