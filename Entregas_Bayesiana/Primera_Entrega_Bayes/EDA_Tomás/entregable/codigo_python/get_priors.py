import pandas as pd
import statsmodels.api as sm
import os

# Carga de datos
path = 'Entregas_Bayesiana/Primera_Entrega_Bayes/EDA_Tomás/data/csgo_games.csv'
df = pd.read_csv(path)

# Ingeniería mínima
metrics = ['rating', 'impact']
for team in ['t1', 't2']:
    for m in metrics:
        cols = [f"{team}_player{i}_{m}" for i in range(1, 6)]
        df[f"{team}_avg_{m}"] = df[cols].mean(axis=1)

for m in metrics:
    df[f"diff_{m}"] = df[f"t1_avg_{m}"] - df[f"t2_avg_{m}"]

df['target_t1_win'] = (df['winner'] == 't1').astype(int)

# Regresión Logística
X = sm.add_constant(df[['diff_rating', 'diff_impact']])
model = sm.Logit(df['target_t1_win'], X).fit()
print(model.summary())
print("\nVALORES PRECISOS PARA PRIORS:")
print(model.params)
