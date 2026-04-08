import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración de rutas
DATA_RAW = "data/raw/"
OUTPUT_DIR = "entregable_4"

def load_dataset(filename):
    path = os.path.join(DATA_RAW, filename)
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        print(f"Advertencia: No se encontró {filename}")
        return None

def main():
    print("--- Iniciando EDA para Entregable 4 ---")
    
    # 1. Análisis de RESULTS
    results = load_dataset("results.csv")
    if results is not None:
        print("\n[results.csv]")
        print(f"Forma: {results.shape}")
        print(f"Nulos:\n{results.isnull().sum()[results.isnull().sum() > 0]}")
        # Analizar distribución de victorias
        results['winner'] = results.apply(lambda x: x['team_1'] if x['result_1'] > x['result_2'] else x['team_2'], axis=1)
        print("Muestra de ganadores procesada.")

    # 2. Análisis de PICKS
    picks = load_dataset("picks.csv")
    if picks is not None:
        print("\n[picks.csv]")
        print(f"Forma: {picks.shape}")
        print("Top 5 mapas más jugados (picks):")
        print(picks['map'].value_counts().head())

    # 3. Análisis de PLAYERS (Solo una muestra por tamaño)
    players = load_dataset("players.csv")
    if players is not None:
        print("\n[players.csv]")
        print(f"Forma: {players.shape}")
        print("Media de Rating por jugador (muestra):")
        print(players['rating'].describe())

    # 4. Análisis de CS2 COMBINED (El más relevante para el modelo)
    cs2 = load_dataset("cs2_newestcombinedmatches.csv")
    if cs2 is not None:
        print("\n[cs2_newestcombinedmatches.csv]")
        print(f"Forma: {cs2.shape}")
        # Correlación entre rating_diff y victoria del team1
        # Asumiendo winner='team1' si ganó el equipo 1
        cs2['team1_win'] = (cs2['winner'] == 'team1').astype(int)
        correlation = cs2[['rating_diff', 'adr_diff', 'kpr_diff', 'team1_win']].corr()
        print("Correlación con la victoria (Team 1):")
        print(correlation['team1_win'])

if __name__ == "__main__":
    main()
