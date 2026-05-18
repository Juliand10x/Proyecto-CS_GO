import matplotlib
matplotlib.use('Agg') # Use non-interactive backend


# ========================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import arviz as az
import pymc as pm
import pytensor.tensor as pt
import warnings
warnings.filterwarnings('ignore')

from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.calibration import calibration_curve

sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.figsize': (12, 8), 'font.size': 11,
                     'axes.titlesize': 15, 'axes.labelsize': 12})

print(f"PyMC v{pm.__version__}  |  ArviZ v{az.__version__}")

# Rutas
PATH_GAMES = 'datos/csgo_games.csv'
PATH_RESULTS = '../data/raw/results.csv'


# Cargar datasets
csgo = pd.read_csv(PATH_GAMES)
res = pd.read_csv(PATH_RESULTS)
print(f"csgo_games: {csgo.shape[0]} filas")
print(f"results:    {res.shape[0]} filas")

# Normalizar nombres de equipo a mayúsculas (case-insensitive merge)
# Los datasets usan mismos equipos pero con distinta capitalización (e.g. 'ASTRALIS' vs 'Astralis')
csgo['team_1_norm'] = csgo['team_1'].str.upper().str.strip()
csgo['team_2_norm'] = csgo['team_2'].str.upper().str.strip()
res['team_1_norm'] = res['team_1'].str.upper().str.strip()
res['team_2_norm'] = res['team_2'].str.upper().str.strip()
csgo['match_date'] = pd.to_datetime(csgo['match_date'])
res['date'] = pd.to_datetime(res['date'])

# Solo columnas necesarias de results para evitar duplicados
res_subset = res[['team_1_norm', 'team_2_norm', 'date', '_map',
                  'map_winner', 'starting_ct', 'result_1', 'result_2']]

# Merge case-insensitive por pares de equipos + ventana de 3 días
merged = pd.merge(csgo, res_subset,
                  left_on=['team_1_norm', 'team_2_norm'],
                  right_on=['team_1_norm', 'team_2_norm'], how='inner')
merged['date_diff'] = abs((merged['match_date'] - merged['date']).dt.days)
df = merged[merged['date_diff'] <= 3].copy()

# Limpiar columnas temporales
df.drop(columns=['team_1_norm', 'team_2_norm', 'date', 'date_diff'], inplace=True, errors='ignore')

print(f"Observaciones tras merge case-insensitive (mapa-nivel): {len(df)}")
print(f"Partidas únicas: {df[['match_date','team_1','team_2']].drop_duplicates().shape[0]}")
print(f"Mapas representados: {df['_map'].nunique()}")
print(f"\n> Merge mejorado: Los equipos en csgo_games estaban en MAYÚSCULAS ('ASTRALIS')")
print(f"> mientras que results los tenía capitalizados ('Astralis').")
print(f"> Con corrección case-insensitive: de ~200 a ~{len(df)} observaciones.")


# Promedios por equipo de las métricas clave
metrics = ['rating', 'impact', 'kdr', 'dmr', 'kpr', 'apr', 'dpr', 'spr']
for team in ['t1', 't2']:
    for m in metrics:
        cols = [f"{team}_player{i}_{m}" for i in range(1, 6)]
        existing = [c for c in cols if c in df.columns]
        if len(existing) == 5:
            df[f"{team}_avg_{m}"] = df[existing].mean(axis=1)

# Diferenciales
for m in metrics:
    c1, c2 = f"t1_avg_{m}", f"t2_avg_{m}"
    if c1 in df.columns and c2 in df.columns:
        df[f"diff_{m}"] = df[c1] - df[c2]

# KAST compuesto
if all(c in df.columns for c in ['t1_avg_kpr','t1_avg_apr','t1_avg_spr']):
    df['t1_avg_kast'] = df['t1_avg_kpr'] + df['t1_avg_apr'] + df['t1_avg_spr']
    df['t2_avg_kast'] = df['t2_avg_kpr'] + df['t2_avg_apr'] + df['t2_avg_spr']
    df['diff_kast'] = df['t1_avg_kast'] - df['t2_avg_kast']

# Ranking
df['diff_rank'] = df['t1_world_rank'] - df['t2_world_rank']

# Target: victoria del Team 1 en el mapa (map_winner: 1=t1, 2=t2)
df['target_t1_win'] = (df['map_winner'] == 1).astype(int)
print(f"Distribución target:\n{df['target_t1_win'].value_counts()}")
print(f"\nMapas disponibles:\n{df['_map'].value_counts()}")


# Preparar matriz de predictores y target
predictors = ['diff_rating', 'diff_impact', 'diff_dmr', 'diff_kast']
available_preds = [p for p in predictors if p in df.columns]

print("Predictores disponibles:", available_preds)

# Codificar mapa como enteros
df['map_code'] = pd.Categorical(df['_map']).codes
map_names = pd.Categorical(df['_map']).categories
n_maps = len(map_names)

print(f"\nMapas codificados ({n_maps}):")
for i, name in enumerate(map_names):
    count = (df['map_code'] == i).sum()
    print(f"  [{i}] {name:15s}  n={count}")

# Dataset para el modelo
model_data = df[available_preds + ['target_t1_win', 'map_code']].dropna()
X = model_data[available_preds].values
y = model_data['target_t1_win'].values
map_idx = model_data['map_code'].values
n_obs = len(y)

print(f"\nObservaciones para el modelo: {n_obs}")
print(f"Predictores: {len(available_preds)}")
print(f"Grupos (mapas): {n_maps}")


coords = {
    "predictor": ["Rating 2.0 (Diferencial)", "Impacto Táctico (Diferencial)", "ADR (Diferencial)", "KAST (Diferencial)"],
    "mapa": list(map_names)
}

with pm.Model(coords=coords) as hierarchical_model:
    # --- Hiperpriors ---
    mu_alpha = pm.Normal("mu_alpha", mu=0, sigma=5)
    sigma_alpha = pm.HalfNormal("sigma_alpha", sigma=2)
    
    # --- Interceptos aleatorios por mapa ---
    alpha_map = pm.Normal("alpha_map", mu=mu_alpha, sigma=sigma_alpha, dims="mapa")
    
    # --- Coeficientes de los predictores (priors débilmente informativas) ---
    betas = pm.Normal("betas", mu=0, sigma=5, dims="predictor")
    
    # --- Predictor lineal ---
    logit_p = alpha_map[map_idx] + pm.math.dot(X, betas)
    
    # --- Likelihood ---
    y_obs = pm.Bernoulli("y_obs", logit_p=logit_p, observed=y)

print("Modelo especificado correctamente.")
print(f"Variables: {list(hierarchical_model.named_vars.keys())}")


with hierarchical_model:
    trace = pm.sample(
        draws=300,
        tune=150,
        chains=2,
        target_accept=0.8,
        random_seed=42,
        idata_kwargs={"log_likelihood": True}
    )

print("\nMuestreo completado.")
print(f"Shape del trace: {trace.posterior['betas'].shape}")


# R-hat
rhat = az.rhat(trace)
print("R-hat para parámetros principales:")
for var in ['mu_alpha', 'sigma_alpha', 'betas']:
    vals = rhat[var].values.flatten() if hasattr(rhat[var], 'values') else [rhat[var].item()]
    for i, v in enumerate(vals):
        label = var if var != 'betas' else f"beta[{i}]"
        print(f"  {label:15s}  R-hat = {v:.4f}")

# Trace plot
az.plot_trace(trace, var_names=['mu_alpha', 'sigma_alpha', 'betas'],
              compact=True, figsize=(12, 10))
plt.suptitle("Trace plots - Diagnóstico de Convergencia", fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('images/trace_convergencia.png', dpi=300, bbox_inches='tight')
plt.show()


# Forest plot de betas
az.plot_forest(trace, var_names=['betas'], hdi_prob=0.94,
               figsize=(10, 4), combined=True,
               textsize=12)
plt.axvline(0, color='red', linestyle='--', alpha=0.5)
plt.title("Efecto de los Predictores (HDI 94%)", fontsize=16)
plt.tight_layout()
plt.savefig('images/forest_betas.png', dpi=300, bbox_inches='tight')
plt.show()


# Resumen posterior de coeficientes
beta_summary = az.summary(trace, var_names=['betas'], hdi_prob=0.94)
beta_summary.index = available_preds
beta_summary['pd'] = (beta_summary['mean'] > 0).map({True: 'P(beta>0)'})
print("\nResumen de coeficientes:")
beta_summary


# Forest plot de interceptos por mapa
az.plot_forest(trace, var_names=['alpha_map'], hdi_prob=0.94,
               figsize=(10, 5), combined=True, textsize=12)
plt.axvline(0, color='red', linestyle='--', alpha=0.5)
plt.title("Interceptos por Mapa (HDI 94%): Ventaja Base", fontsize=16)
plt.tight_layout()
plt.savefig('images/forest_alpha_map.png', dpi=300, bbox_inches='tight')
plt.show()


# Tabla de interceptos por mapa
alpha_summary = az.summary(trace, var_names=['alpha_map'], hdi_prob=0.94)
alpha_summary.index = map_names
alpha_summary['prob_victoria_base'] = 1 / (1 + np.exp(-alpha_summary['mean']))
print("\nInterceptos por Mapa:")
alpha_summary


with hierarchical_model:
    ppc = pm.sample_posterior_predictive(trace, random_seed=42, progressbar=True)

y_sim = ppc.posterior_predictive['y_obs'].values.flatten()

print(f"\nProporción de victorias observada:  {y.mean():.3f}")
print(f"Proporción de victorias simulada:   {y_sim.mean():.3f}")

# Comparación gráfica
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histograma
axes[0].hist(y_sim, bins=30, alpha=0.6, color='#3498db', density=True,
             label=f'Simulado (media={y_sim.mean():.3f})')
axes[0].axvline(y.mean(), color='#e74c3c', linewidth=3,
                label=f'Observado (media={y.mean():.3f})')
axes[0].set_xlabel('Proporción de Victorias')
axes[0].set_ylabel('Densidad')
axes[0].set_title('PPC: Distribución de Proporción de Victorias')
axes[0].legend()

# Frecuencia de victorias observada vs simulada
obs_freq = y.mean()
sim_freq = [y_sim[i::len(y)].mean() for i in range(len(y))]
axes[1].hist(sim_freq, bins=30, alpha=0.6, color='#2ecc71', density=True,
             label='Simulado')
axes[1].axvline(obs_freq, color='#e74c3c', linewidth=3, label='Observado')
axes[1].set_xlabel('Proporción de Victorias')
axes[1].set_ylabel('Densidad')
axes[1].set_title('PPC: Calibración Global')
axes[1].legend()

plt.suptitle('Posterior Predictive Checks', fontsize=16)
plt.tight_layout()
plt.savefig('images/ppc_global.png', dpi=300, bbox_inches='tight')
plt.show()


# Probabilidades predichas (usando la media posterior del trace)
beta_mean = trace.posterior['betas'].mean(dim=['chain', 'draw']).values
alpha_mean = trace.posterior['alpha_map'].mean(dim=['chain', 'draw']).values

logit_pred = alpha_mean[map_idx] + np.dot(X, beta_mean)
p_pred = 1 / (1 + np.exp(-logit_pred))

print(f"\nProbabilidades predichas: media={p_pred.mean():.3f}, "
      f"min={p_pred.min():.3f}, max={p_pred.max():.3f}")

# Brier Score
brier = brier_score_loss(y, p_pred)
print(f"Brier Score:           {brier:.4f}")
print(f"Brier Score (nulo):    {(y.mean() * (1 - y.mean())):.4f}")
print(f"Mejora sobre nulo:     {(1 - brier / (y.mean() * (1 - y.mean())))*100:.1f}%")

# AUC-ROC
auc = roc_auc_score(y, p_pred)
print(f"AUC-ROC:               {auc:.4f}")

# Log-Loss
eps = 1e-15
p_clip = np.clip(p_pred, eps, 1 - eps)
log_loss = -np.mean(y * np.log(p_clip) + (1 - y) * np.log(1 - p_clip))
print(f"Log-Loss:              {log_loss:.4f}")


prob_true, prob_pred = calibration_curve(y, p_pred, n_bins=10, strategy='quantile')

plt.figure(figsize=(10, 8))
plt.plot(prob_pred, prob_true, 'o-', color='#3498db', linewidth=2, markersize=8,
         label='Modelo Jerárquico')
plt.plot([0, 1], [0, 1], '--', color='gray', alpha=0.7, label='Calibración perfecta')
plt.fill_between(prob_pred, prob_true, prob_pred, alpha=0.2, color='#3498db')
plt.xlabel('Probabilidad Predicha', fontsize=12)
plt.ylabel('Frecuencia Observada', fontsize=12)
plt.title('Curva de Calibración', fontsize=16)
plt.legend()
plt.tight_layout()
plt.savefig('images/curva_calibracion.png', dpi=300, bbox_inches='tight')
plt.show()

# Expected Calibration Error
ece = np.mean(np.abs(prob_true - prob_pred))
print(f"Expected Calibration Error (ECE): {ece:.4f}")
print(f"Interpretación: En promedio, las predicciones se desvían {ece*100:.1f}% de la calibración ideal.")


# Modelo nulo (solo intercepto fijo)
with pm.Model() as null_model:
    alpha = pm.Normal("alpha", mu=0, sigma=5)
    y_null = pm.Bernoulli("y_obs", logit_p=alpha, observed=y)
    trace_null = pm.sample(draws=300, tune=150, chains=2,
                           target_accept=0.8, random_seed=42,
                           idata_kwargs={"log_likelihood": True})

# WAIC
waic_hier = az.waic(trace)
waic_null = az.waic(trace_null)

print("\n" + "="*50)
print("COMPARACIÓN DE MODELOS (elpd-WAIC)")
print("="*50)
print(f"\nModelo Jerárquico:  elpd_waic = {waic_hier.elpd_waic:.2f}  (se={waic_hier.se:.2f})")
print(f"Modelo Nulo:         elpd_waic = {waic_null.elpd_waic:.2f}  (se={waic_null.se:.2f})")
elpd_diff = waic_hier.elpd_waic - waic_null.elpd_waic
print(f"\nDiferencia (Jerárquico - Nulo): Δelpd = {elpd_diff:.2f}")
print(f"(elpd mayor = mejor. Δelpd > 0 favorece al jerárquico)")
if elpd_diff > 0:
    print(">> El modelo jerárquico es superior")
else:
    print(">> El modelo nulo es competitivo")


# Efecto marginal de cada predictor
beta_means = trace.posterior['betas'].mean(dim=['chain', 'draw']).values
mu_alpha_mean = trace.posterior['mu_alpha'].mean(dim=['chain', 'draw']).values

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for i, pred in enumerate(available_preds):
    x_range = np.linspace(X[:, i].min(), X[:, i].max(), 100)
    # Mantener otros predictores en su media
    X_other_mean = X[:, [j for j in range(len(available_preds)) if j != i]].mean(axis=0)
    
    logit_vals = mu_alpha_mean + beta_means[i] * x_range
    for j, k in enumerate([j for j in range(len(available_preds)) if j != i]):
        logit_vals += beta_means[k] * X_other_mean[j]
    
    p_vals = 1 / (1 + np.exp(-logit_vals))
    
    # HDI para el efecto
    beta_samples = trace.posterior['betas'].values[:, :, i].flatten()
    n_samples = min(500, len(beta_samples))
    beta_draws = np.random.choice(beta_samples, size=n_samples, replace=False)
    
    axes[i].plot(x_range, p_vals, color='#3498db', linewidth=2, label='Efecto marginal')
    
    # Curvas de incertidumbre
    for b in beta_draws[::10]:  # subset para no saturar
        p_alt = 1 / (1 + np.exp(-(mu_alpha_mean + b * x_range 
                                   + sum(beta_means[k] * X_other_mean[j] 
                                         for j, k in enumerate([j for j in range(len(available_preds)) if j != i])))))
        axes[i].plot(x_range, p_alt, color='#3498db', alpha=0.03)
    
    axes[i].axhline(0.5, color='red', linestyle='--', alpha=0.5)
    axes[i].set_xlabel(pred)
    axes[i].set_ylabel('P(Victoria T1)')
    axes[i].set_title(f'Efecto Marginal: {pred}')
    axes[i].set_ylim(-0.05, 1.05)

plt.suptitle('Efectos Marginales de los Predictores', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('images/efectos_marginales.png', dpi=300, bbox_inches='tight')
plt.show()


# Probabilidad base por mapa
alpha_means = trace.posterior['alpha_map'].mean(dim=['chain', 'draw']).values
alpha_hdi = az.hdi(trace, var_names=['alpha_map'], hdi_prob=0.94)['alpha_map']

map_order = np.argsort(alpha_means)
fig, ax = plt.subplots(figsize=(12, 6))

x_pos = np.arange(n_maps)
bars = ax.bar(x_pos, alpha_means[map_order], yerr=[
    alpha_means[map_order] - alpha_hdi[map_order, 0],
    alpha_hdi[map_order, 1] - alpha_means[map_order]
], capsize=5, color='#3498db', alpha=0.8, 
    tick_label=[map_names[i] for i in map_order])

ax.axhline(0, color='red', linestyle='--', alpha=0.5)
ax.set_ylabel('Intercepto (logit)')
ax.set_xlabel('Mapa')
ax.set_title('Interceptos por Mapa con HDI 94%', fontsize=16)

# Añadir probabilidad base
for i, (idx, bar) in enumerate(zip(map_order, bars)):
    prob = 1 / (1 + np.exp(-alpha_means[idx]))
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'p={prob:.2f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('images/interceptos_mapa_hdi.png', dpi=300, bbox_inches='tight')
plt.show()
