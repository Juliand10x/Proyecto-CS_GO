import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# CONFIGURACIÓN
DATA_RAW_DIR = "../../data/raw"
RESULTS_FILE = os.path.join(DATA_RAW_DIR, "results.csv")
PICKS_FILE = os.path.join(DATA_RAW_DIR, "picks.csv")

def run_eda():
    if not os.path.exists(RESULTS_FILE):
        print("❌ Archivos de datos no encontrados. Ejecuta src/data/capture_data.py primero.")
        return

    print("🚀 Cargando datos para la primera aproximación bayesiana...")
    df_results = pd.read_csv(RESULTS_FILE)
    df_picks = pd.read_csv(PICKS_FILE)

    print(f"📊 Dataset de resultados: {df_results.shape[1]} columnas y {df_results.shape[0]} registros.")
    
    # Análisis de Mapas
    plt.figure(figsize=(10,6))
    df_results['map'].value_counts().plot(kind='bar', color='skyblue')
    plt.title("Frecuencia de Mapas en Series Profesionales")
    plt.xlabel("Mapa")
    plt.ylabel("Cantidad de Partidas")
    plt.tight_layout()
    plt.savefig("distribucion_mapas.png")
    print("📈 Gráfico de distribución de mapas generado.")

    # Análisis de Winrate por Mapa (Estadística de base)
    # Suponiendo columnas 'team_1', 'team_2', 'winner'
    # Esto es solo un ejemplo de lo que se alimentará al modelo bayesiano
    print("✅ Primera aproximación finalizada.")

if __name__ == "__main__":
    run_eda()
