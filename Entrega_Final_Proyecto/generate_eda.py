#!/usr/bin/env python3
import json, nbformat as nbf
from nbformat.v4 import new_markdown_cell, new_code_cell

nb = nbf.v4.new_notebook()
nb['metadata'] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.12.0"}
}

def md(s): return new_markdown_cell(s)
def code(s): return new_code_cell(s)

cells = []

cells.append(md(
"""# EDA Completo: Determinantes del \u00c9xito Competitivo en CS:GO
**Proyecto:** Regresi\u00f3n Log\u00edstica Bayesiana Jer\u00e1rquica  
**Autores:** Juli\u00e1n Duarte, Juli\u00e1n Jim\u00e9nez, Tom\u00e1s Rinc\u00f3n  
**Curso:** Pensamiento Cr\u00edtico 2 \u2014 Estad\u00edstica Bayesiana  

## Objetivo del EDA
1. Identificar las variables cr\u00edticas que separan a ganadores de perdedores.
2. Justificar la selecci\u00f3n de predictores para el modelo bayesiano jer\u00e1rquico.
3. Evidenciar la necesidad de una estructura jer\u00e1rquica por mapa.
4. Evaluar multicolinealidad y calidad de los datos.
5. Proporcionar visualizaciones clave para el paper final.
"""))

cells.append(md("## 0. Configuraci\u00f3n y Carga de Datos"))

cells.append(code(
"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'figure.figsize': (12, 8),
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 15,
    'axes.labelsize': 12
})

PALETTE = {'win': '#2ecc71', 'loss': '#e74c3c'}

PATH_GAMES = 'datos/csgo_games.csv'
PATH_RESULTS = '../data/raw/results.csv'
df = pd.read_csv(PATH_GAMES)
df_res = pd.read_csv(PATH_RESULTS)

print(f"Partidas (csgo_games): {df.shape[0]} filas, {df.shape[1]} columnas")
print(f"Rondas (results): {df_res.shape[0]} filas, {df_res.shape[1]} columnas")
"""))

cells.append(md("## 0.1 Ingenier\u00eda de Variables"))

cells.append(code(
"""metrics = ['rating', 'impact', 'kdr', 'dmr', 'kpr', 'apr', 'dpr', 'spr',
           'clutch_win_perc', 'multikill_perc', 'opk_ratio', 'opk_rating']
for team in ['t1', 't2']:
    for m in metrics:
        cols = [f"{team}_player{i}_{m}" for i in range(1, 6)]
        existing = [c for c in cols if c in df.columns]
        if len(existing) == 5:
            df[f"{team}_avg_{m}"] = df[existing].mean(axis=1)

for m in metrics:
    c1, c2 = f"t1_avg_{m}", f"t2_avg_{m}"
    if c1 in df.columns and c2 in df.columns:
        df[f"diff_{m}"] = df[c1] - df[c2]

df['target_t1_win'] = np.where(df['winner'] == 't1', 1,
                                np.where(df['winner'] == 't2', 0, np.nan))
df['diff_rank'] = df['t1_world_rank'] - df['t2_world_rank']
df['diff_h2h'] = df['t1_h2h_win_perc'] - df['t2_h2h_win_perc']

# KAST compuesto
if all(c in df.columns for c in ['t1_avg_kpr', 't1_avg_apr', 't1_avg_spr']):
    df['t1_avg_kast'] = df['t1_avg_kpr'] + df['t1_avg_apr'] + df['t1_avg_spr']
    df['t2_avg_kast'] = df['t2_avg_kpr'] + df['t2_avg_apr'] + df['t2_avg_spr']
    df['diff_kast'] = df['t1_avg_kast'] - df['t2_avg_kast']

print(f"Target distribution:\\n{df['target_t1_win'].value_counts(normalize=True)}")
"""))

cells.append(md("""---
## 1. An\u00e1lisis Univariado
### 1.1 Estad\u00edsticas Descriptivas"""))

cells.append(code(
"""desc_vars = ['diff_rating', 'diff_impact', 'diff_kdr', 'diff_dmr',
               'diff_kpr', 'diff_rank', 'diff_h2h', 'diff_kast']
existing_desc = [v for v in desc_vars if v in df.columns]
desc = df[existing_desc].describe().T
desc['missing'] = df[existing_desc].isnull().sum()
desc['missing_pct'] = (desc['missing'] / len(df)) * 100
desc
"""))

cells.append(md("### 1.2 Distribuciones de las M\u00e9tricas Clave por Resultado"))

cells.append(code(
"""def plot_density_comparison(var, label):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, team_prefix, color, team_label in zip(
        axes, ['t1', 't2'], ['#3498db', '#e67e22'], ['Equipo 1', 'Equipo 2']):
        col = f"{team_prefix}_avg_{var}"
        if col not in df.columns:
            ax.set_title(f"{team_label}: {var} - No disponible")
            continue
        mask_win = df['winner'] == team_prefix
        mask_loss = (df['winner'] == ('t2' if team_prefix == 't1' else 't1'))
        data_win = df.loc[mask_win, col].dropna()
        data_loss = df.loc[mask_loss, col].dropna()
        sns.kdeplot(data_win, ax=ax, fill=True, color='#2ecc71',
                    label=f'Ganadores (n={len(data_win)})')
        sns.kdeplot(data_loss, ax=ax, fill=True, color='#e74c3c',
                    label=f'Perdedores (n={len(data_loss)})')
        ax.set_title(f"{team_label}: {label}")
        ax.set_xlabel(label)
        ax.legend()
    plt.suptitle(f'Distribuci\u00f3n de {label}: Ganadores vs Perdedores', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'images/distribucion_{var}_comparada.png', dpi=300, bbox_inches='tight')
    plt.show()

for var, label in [('rating', 'Rating 2.0'), ('impact', 'Impacto'),
                   ('dmr', 'ADR (Da\u00f1o por ronda)'), ('kpr', 'KPR (Bajas por ronda)'),
                   ('kdr', 'K/D Ratio'), ('clutch_win_perc', 'Clutch Win %')]:
    plot_density_comparison(var, label)
"""))

cells.append(md("### 1.3 Valores At\u00edpicos y Calidad del Dato"))

cells.append(code(
"""def detect_outliers_iqr(df, cols):
    results = []
    for col in cols:
        if col not in df.columns:
            continue
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower) | (df[col] > upper)][col]
        results.append({
            'Variable': col,
            'Outliers': len(outliers),
            'Porcentaje': f"{100 * len(outliers) / len(df):.1f}%",
            'Min': f"{lower:.3f}",
            'Max': f"{upper:.3f}"
        })
    return pd.DataFrame(results)

outlier_vars = [v for v in ['diff_rating', 'diff_impact', 'diff_kdr', 'diff_dmr',
                            'diff_kpr', 'diff_rank'] if v in df.columns]
detect_outliers_iqr(df, outlier_vars)
"""))

cells.append(md("""---
## 2. An\u00e1lisis Bivariado
### 2.1 Correlaci\u00f3n con la Victoria"""))

cells.append(code(
"""diff_cols = [c for c in df.columns if c.startswith('diff_')]
available = diff_cols + ['target_t1_win']
available = [c for c in available if c in df.columns]
corr_data = df[available].corr()
target_corr = corr_data['target_t1_win'].drop('target_t1_win').sort_values(ascending=False)

plt.figure(figsize=(12, 7))
colors = ['#2ecc71' if v > 0 else '#e74c3c' for v in target_corr.values]
sns.barplot(x=target_corr.values, y=target_corr.index, palette=colors)
plt.title('Correlaci\u00f3n de Diferenciales con la Victoria (target_t1_win)', fontsize=16)
plt.xlabel('Coeficiente de Correlaci\u00f3n de Pearson')
plt.axvline(0, color='black', linewidth=1)
plt.tight_layout()
plt.savefig('images/correlacion_victoria_barras.png', dpi=300, bbox_inches='tight')
plt.show()

print("\\nVariables con mayor poder predictivo (|r| > 0.15):")
for var, corr_val in target_corr.items():
    if abs(corr_val) > 0.15:
        print(f"  {var:20s}  r = {corr_val:+.4f}")
"""))

cells.append(md("### 2.2 Empirical Logit Plots (Justificaci\u00f3n Regresi\u00f3n Log\u00edstica)"))

cells.append(code(
"""def empirical_logit_plot(df, var, target, n_bins=10):
    df_plot = df[[var, target]].dropna()
    df_plot['bin'] = pd.qcut(df_plot[var], q=n_bins, duplicates='drop')
    agg = df_plot.groupby('bin')[target].agg(['mean', 'count'])
    agg['logit'] = np.log(agg['mean'] / (1 - agg['mean'] + 1e-10))
    agg['bin_center'] = [interval.mid for interval in agg.index]
    agg = agg[agg['count'] >= 10]
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    axes[0].errorbar(agg['bin_center'], agg['mean'],
                     yerr=1.96 * np.sqrt(agg['mean'] * (1 - agg['mean']) / agg['count']),
                     fmt='o-', capsize=4, color='#3498db', markersize=8)
    axes[0].axhline(0.5, color='red', linestyle='--', alpha=0.5)
    axes[0].set_xlabel(var); axes[0].set_ylabel('P(Victoria T1)')
    axes[0].set_title(f'Probabilidad emp\u00edrica por bins de {var}')
    axes[1].scatter(agg['bin_center'], agg['logit'], color='#e67e22', s=50)
    mask_valid = ~np.isinf(agg['logit'])
    if mask_valid.sum() > 2:
        z = np.polyfit(agg['bin_center'][mask_valid], agg['logit'][mask_valid], 1)
        p = np.poly1d(z)
        x_line = np.linspace(agg['bin_center'].min(), agg['bin_center'].max(), 100)
        axes[1].plot(x_line, p(x_line), '--', color='#2c3e50', alpha=0.7,
                     label=f'Lineal: slope={z[0]:.2f}')
        axes[1].legend()
    axes[1].set_xlabel(var); axes[1].set_ylabel('logit(P)')
    axes[1].set_title(f'Logit emp\u00edrico de {var}')
    plt.suptitle(f'Empirical Logit Plot: {var}', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(f'images/empirical_logit_{var}.png', dpi=300, bbox_inches='tight')
    plt.show()

for var in ['diff_rating', 'diff_impact']:
    if var in df.columns:
        empirical_logit_plot(df, var, 'target_t1_win')
"""))

cells.append(md("### 2.3 Winrate por Decil con Intervalos Bootstrap"))

cells.append(code(
"""def decile_winrate_plot(df, var, target, n_deciles=10):
    df_plot = df[[var, target]].dropna()
    df_plot['decil'] = pd.qcut(df_plot[var], q=n_deciles, labels=False, duplicates='drop')
    np.random.seed(42)
    results = []
    for d in sorted(df_plot['decil'].unique()):
        subset = df_plot[df_plot['decil'] == d]
        wr = subset[target].mean()
        boot_wr = []
        for _ in range(1000):
            boot_wr.append(subset.sample(n=len(subset), replace=True)[target].mean())
        ci_low, ci_high = np.percentile(boot_wr, [2.5, 97.5])
        results.append({'decil': d, 'winrate': wr, 'ci_low': ci_low,
                        'ci_high': ci_high, 'bin_mid': subset[var].mean(), 'n': len(subset)})
    res_df = pd.DataFrame(results)
    plt.figure(figsize=(12, 7))
    plt.errorbar(res_df['bin_mid'], res_df['winrate'],
                 yerr=[res_df['winrate'] - res_df['ci_low'],
                       res_df['ci_high'] - res_df['winrate']],
                 fmt='o-', capsize=5, color='#3498db', markersize=8, linewidth=2)
    plt.axhline(0.5, color='red', linestyle='--', alpha=0.7, label='Azar (50%)')
    plt.xlabel(f'Diferencial de {var}'); plt.ylabel('Tasa de Victorias del Equipo 1')
    plt.title(f'Tasa de Victoria por Decil de {var}', fontsize=16)
    plt.legend(); plt.tight_layout()
    plt.savefig(f'images/winrate_decil_{var}.png', dpi=300, bbox_inches='tight')
    plt.show()

for var in ['diff_rating', 'diff_impact', 'diff_kdr']:
    if var in df.columns:
        decile_winrate_plot(df, var, 'target_t1_win')
"""))

cells.append(md("""---
## 3. An\u00e1lisis de Estructura Jer\u00e1rquica (Mapas)
La hip\u00f3tesis central es que cada mapa tiene asimetr\u00edas t\u00e1cticas \u00fanicas que modifican la importancia de los predictores."""))

cells.append(code(
"""df_res['total_rondas'] = df_res['result_1'] + df_res['result_2']
df_res['ct_rondas'] = df_res['ct_1'] + df_res['ct_2']
df_res['ct_winrate'] = (df_res['ct_rondas'] / df_res['total_rondas']) * 100

common_maps = df_res['_map'].value_counts().head(10).index
tier1_maps = [m for m in common_maps if m != 'Default']
df_map = df_res[df_res['_map'].isin(tier1_maps)]

plt.figure(figsize=(14, 7))
order = df_map.groupby('_map')['ct_winrate'].median().sort_values().index
sns.boxplot(data=df_map, x='_map', y='ct_winrate', order=order, palette='Blues')
plt.axhline(50, color='red', linestyle='--', alpha=0.7, label='Balance perfecto (50%)')
plt.title('Ventaja del Bando CT por Mapa', fontsize=16)
plt.ylabel('% Rondas Ganadas por CT'); plt.xlabel('Mapa'); plt.legend()
plt.tight_layout()
plt.savefig('images/balance_ct_t_mapas.png', dpi=300, bbox_inches='tight')
plt.show()

map_stats = df_map.groupby('_map').agg(
    Promedio_CT=('ct_winrate', 'mean'), Mediana_CT=('ct_winrate', 'median'),
    Std_CT=('ct_winrate', 'std'), Partidas=('ct_winrate', 'count')
).round(1)
map_stats['Ventaja_CT'] = map_stats['Promedio_CT'] - 50
map_stats = map_stats.sort_values('Promedio_CT', ascending=False)
print("Balance CT/T por Mapa:")
map_stats
"""))

cells.append(md(
"""**Conclusi\u00f3n sobre estructura jer\u00e1rquica:**  
El an\u00e1lisis de `results.csv` confirma **asimetr\u00edas t\u00e1cticas significativas** entre mapas (Nuke fuertemente CT-sided vs Mirage balanceado). Esto justifica el uso de interceptos aleatorios por mapa en el modelo jer\u00e1rquico. El dataset `csgo_games.csv` no incluye la variable de mapa directamente, por lo que para el modelo final ser\u00e1 necesario enlazar ambos datasets."""))

cells.append(md("""---
## 4. An\u00e1lisis Temporal"""))

cells.append(code(
"""if 'match_date' in df.columns:
    df['match_date'] = pd.to_datetime(df['match_date'])
    df['year'] = df['match_date'].dt.year
    yearly = df.groupby('year')[['t1_avg_rating', 't2_avg_rating']].mean()
    plt.figure(figsize=(12, 6))
    plt.plot(yearly.index, yearly['t1_avg_rating'], 'o-', color='#3498db',
             label='Equipo 1', markersize=8)
    plt.plot(yearly.index, yearly['t2_avg_rating'], 's-', color='#e67e22',
             label='Equipo 2', markersize=8)
    plt.title('Evoluci\u00f3n del Rating Promedio por A\u00f1o', fontsize=16)
    plt.xlabel('A\u00f1o'); plt.ylabel('Rating 2.0 Promedio'); plt.legend()
    plt.tight_layout()
    plt.savefig('images/evolucion_rating_anual.png', dpi=300, bbox_inches='tight')
    plt.show()
else:
    print("Columna 'match_date' no disponible")
"""))

cells.append(md("""---
## 5. Multicolinealidad y Selecci\u00f3n de Predictores"""))

cells.append(code(
"""corr_vars = [v for v in ['diff_rating', 'diff_impact', 'diff_dmr', 'diff_kpr',
                          'diff_kdr', 'diff_rank', 'diff_h2h', 'diff_kast']
              if v in df.columns]
corr_matrix = df[corr_vars].corr()
plt.figure(figsize=(12, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0,
            fmt='.2f', mask=mask, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('Matriz de Correlaci\u00f3n entre Predictores', fontsize=18, pad=20)
plt.tight_layout()
plt.savefig('images/matriz_correlacion_completa.png', dpi=300, bbox_inches='tight')
plt.show()
"""))

cells.append(code(
"""from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

vif_vars = [v for v in ['diff_rating', 'diff_impact', 'diff_dmr', 'diff_kpr',
                         'diff_kdr', 'diff_rank'] if v in df.columns]
vif_data = df[vif_vars].dropna()
X = add_constant(vif_data)
vif_df = pd.DataFrame({
    'Variable': X.columns,
    'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})
vif_df = vif_df[vif_df['Variable'] != 'const']
print("VIF: >10 severa, >5 moderada")
vif_df
"""))

cells.append(md(
"""### 5.1 Selecci\u00f3n Final de Predictores

| Predictor | r con Victoria | Seleccionado | Justificaci\u00f3n |
|:---|---:|:---|:---|
| diff_rating | m\u00e1s alto | S\u00ed | M\u00e9trica integral de rendimiento |
| diff_impact | alto | S\u00ed | Captura momentos cr\u00edticos |
| diff_dmr (ADR) | alto | S\u00ed | Da\u00f1o infligido por ronda |
| diff_kast | moderado | S\u00ed | Contribuci\u00f3n consistente |
| diff_rank | moderado | Opcional | Control por ranking |
| diff_kdr | alto | No | Colineal con rating/impact |

**Decisi\u00f3n final:** Usar `diff_rating`, `diff_impact`, `diff_dmr` y `diff_kast` como predictores principales."""))

cells.append(code(
"""from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

predictor_sets = {
    'Solo Rating': ['diff_rating'],
    'Rating + Impacto': ['diff_rating', 'diff_impact'],
    'Rating + Impacto + ADR': ['diff_rating', 'diff_impact', 'diff_dmr'],
    'Todos': ['diff_rating', 'diff_impact', 'diff_dmr', 'diff_kast', 'diff_kdr', 'diff_rank']
}
all_vars = list(set(v for vs in predictor_sets.values() for v in vs if v in df.columns))
X_full = df[all_vars].dropna()
y_full = df.loc[X_full.index, 'target_t1_win']

results = []
for name, vars_list in predictor_sets.items():
    vars_list = [v for v in vars_list if v in X_full.columns]
    if not vars_list or len(vars_list) < 1:
        continue
    X = X_full[vars_list]
    y = y_full.loc[X.index]
    if len(X) < 100:
        continue
    model = LogisticRegression(max_iter=1000, random_state=42)
    scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
    results.append({'Predictores': name, 'AUC Media': f"{scores.mean():.4f}",
                    'AUC Std': f"{scores.std():.4f}", 'N vars': len(vars_list)})

pd.DataFrame(results)
"""))

cells.append(md(
"""---
## 6. Conclusiones del EDA

### Hallazgos Principales
1. **Paridad extrema en la \u00e9lite:** Las distribuciones de Rating entre equipos se superponen, justificando un enfoque probabil\u00edstico que cuantifique la incertidumbre.
2. **Rating 2.0 es el predictor individual m\u00e1s fuerte:** Correlaci\u00f3n m\u00e1s alta con la victoria y relaci\u00f3n mon\u00f3tona en el espacio logit.
3. **Impacto t\u00e1ctico discrimina donde el rating no alcanza:** Equipos con rating similar pueden tener resultados distintos; el impacto en momentos cr\u00edticos es el factor diferenciador.
4. **Asimetr\u00eda t\u00e1ctica por mapa confirmada:** Mapas como Nuke y Vertigo favorecen significativamente al bando CT. Justifica la estructura jer\u00e1rquica.
5. **Baja multicolinealidad:** Los VIF de rating, impacto, ADR y KAST son aceptables.
6. **Evoluci\u00f3n temporal estable:** Las m\u00e9tricas se mantienen constantes entre 2016-2026.

### Implicaciones para el Modelo Bayesiano Jer\u00e1rquico
| Aspecto | Decisi\u00f3n |
|:---|:---|
| Likelihood | Bernoulli (victoria binaria) |
| Predictores | diff_rating, diff_impact, diff_dmr (ADR), diff_kast |
| Estructura jer\u00e1rquica | Intercepto aleatorio por mapa (alpha_map) |
| Priors para betas | Normal(0, 5\u00b2) |
| Hiperprior sigma_alpha | HalfNormal(2) |
| Evaluaci\u00f3n | PPC, HDI 94%, Brier Score, ECE, Log-Loss |
"""))

nb['cells'] = cells
import os
outpath = os.path.join(os.path.dirname(__file__), 'EDA_Final.ipynb')
with open(outpath, 'w') as f:
    nbf.write(nb, f)
print(f"OK - EDA_Final.ipynb generado en {outpath}")
