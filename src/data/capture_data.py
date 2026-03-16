import os
import requests
import pandas as pd
from datetime import datetime
import zipfile

# Intentar importar la API de Kaggle
try:
    from kaggle.api.kaggle_api_extended import KaggleApi
    KAGGLE_AVAILABLE = True
except ImportError:
    KAGGLE_AVAILABLE = False

# =============================================================================
# CONFIGURACIÓN DE DATASETS
# =============================================================================
# Fuentes directas (GitHub/URLs)
DATASETS_URL = {
    "csgo_match_results": "https://raw.githubusercontent.com/hojlund123/csgo-dataset/master/csgoresults.csv",
}

# Fuentes de Kaggle (Slug del dataset)
# Usaremos datasets balanceados entre CS:GO histórico y CS2 reciente
KAGGLE_DATASETS = [
    "mateusmachado/hltv-csgo-match-stats",  # Stats de mapas y equipos (CS:GO)
    "griffindesroches/cs2-hltv-professional-match-statistics-dataset" # Datos CS2 (Nuevos)
]

DATA_RAW_DIR = os.path.join(os.getcwd(), "data", "raw")

def setup_directories():
    """Asegura que la estructura de carpetas de datos exista."""
    if not os.path.exists(DATA_RAW_DIR):
        os.makedirs(DATA_RAW_DIR, exist_ok=True)
        print(f"✅ Carpeta creada: {DATA_RAW_DIR}")

def download_from_url():
    """Descarga los archivos configurados en DATASETS_URL."""
    for name, url in DATASETS_URL.items():
        target_path = os.path.join(DATA_RAW_DIR, f"{name}.csv")
        print(f"🚀 Descargando desde URL: {name}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(target_path, 'wb') as f:
                f.write(response.content)
            print(f"✔️ Guardado: {target_path}")
        except Exception as e:
            print(f"❌ Error en URL {name}: {e}")

def download_from_kaggle():
    """Descarga datasets usando la API de Kaggle."""
    if not KAGGLE_AVAILABLE:
        print("⚠️ Librería 'kaggle' no instalada. Ejecuta: pip install kaggle")
        return

    try:
        api = KaggleApi()
        api.authenticate()
        
        for dataset in KAGGLE_DATASETS:
            print(f"🚀 Descargando desde Kaggle: {dataset}...")
            # Descargar archivos (vienen en ZIP generalmente)
            api.dataset_download_files(dataset, path=DATA_RAW_DIR, unzip=True)
            print(f"✔️ Dataset [{dataset}] extraído con éxito en {DATA_RAW_DIR}")
            
    except Exception as e:
        print(f"❌ Error con la API de Kaggle: {e}")
        print("💡 TIP: Asegúrate de tener tu archivo 'kaggle.json' en la carpeta correcta (~/.kaggle/ en Linux o .config/kaggle/ en otros casos).")

def create_audit_log():
    """Genera un archivo de registro para control de versiones de datos."""
    log_path = os.path.join(DATA_RAW_DIR, "data_version.txt")
    with open(log_path, "w") as f:
        f.write(f"Dataset Version Control\n")
        f.write(f"----------------------\n")
        f.write(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Datasets: GitHub (Histórico) + Kaggle (Táctico & CS2)\n")
    print(f"📝 Registro de auditoría actualizado.")

if __name__ == "__main__":
    print("--- INICIANDO CAPTURA DE DATOS PARA PROYECTO CS:GO ---")
    setup_directories()
    download_from_url()
    download_from_kaggle()
    create_audit_log()
    print("--- PROCESO FINALIZADO ---")
