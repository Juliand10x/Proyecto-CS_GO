import pandas as pd
import numpy as np
import os

# Configuración de rutas
DATA_RAW = "data/raw/"
OUTPUT_PATH = "entregable_4/reporte_eda.md"

def load_dataset(filename):
    path = os.path.join(DATA_RAW, filename)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

def main():
    report = []
    report.append("# Reporte de Análisis Exploratorio de Datos (EDA) - Entregable 4\n")

    # 1. RESULTS
    results = load_dataset("results.csv")
    if results is not None:
        report.append("## 1. resultados.csv (Match Level)")
        report.append(f"- **Registros:** {results.shape[0]}")
        report.append(f"- **Columnas:** {results.shape[1]}")
        
        # Calcular victoria del team 1
        results['t1_win'] = (results['result_1'] > results['result_2']).astype(int)
        win_rate_t1 = results['t1_win'].mean()
        report.append(f"- **Win Rate Team 1 (Sesgo de datos):** {win_rate_t1:.2%}")
        
        # Rankings (Si el rank menor es mejor)
        avg_rank_diff = (results['rank_1'] - results['rank_2']).mean()
        report.append(f"- **Diferencia promedio de Ranking (T1-T2):** {avg_rank_diff:.2f}")
        report.append("\n")

    # 2. PICKS
    picks = load_dataset("picks.csv")
    if picks is not None:
        report.append("## 2. picks.csv (Map Veto)")
        map_cols = ['t1_picked_1', 't2_picked_1', 'left_over']
        all_maps = pd.concat([picks[col] for col in map_cols if col in picks.columns])
        # Filtrar valores no válidos (como '0' o '0.0' si existen)
        all_maps = all_maps[~all_maps.isin(['0', '0.0', 0, 0.0])]
        top_maps = all_maps.value_counts().head(7)
        report.append("- **Top 7 Mapas más frecuentes en picks/decider:**")
        for m, count in top_maps.items():
            report.append(f"  - {m}: {count}")
        report.append("\n")

    # 3. CS2 COMBINED (El dataset procesado más útil)
    cs2 = load_dataset("cs2_newestcombinedmatches.csv")
    if cs2 is not None:
        report.append("## 3. cs2_newestcombinedmatches.csv (Features pre-procesadas)")
        report.append(f"- **Registros filtrados CS2:** {cs2.shape[0]}")
        
        # Correlaciones clave para el modelo Bayesiano
        cs2['winner_t1'] = (cs2['winner'] == 'team1').astype(int)
        features = ['rating_diff', 'adr_diff', 'kpr_diff', 'ct_rating_diff', 't_rating_diff']
        # Asegurarse de que las columnas existan
        available_features = [f for f in features if f in cs2.columns]
        if available_features:
            corr = cs2[available_features + ['winner_t1']].corr()['winner_t1'].sort_values(ascending=False)
            report.append("- **Correlación de variables con la victoria del Team 1:**")
            for feat, value in corr.items():
                if feat != 'winner_t1':
                    report.append(f"  - {feat}: {value:.4f}")
        report.append("\n")

    # Guardar reporte
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    
    print(f"EDA completado. Reporte guardado en {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
