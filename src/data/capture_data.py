import os
import requests
import pandas as pd
from datetime import datetime
import zipfile
import shutil

# Intentar importar las librerías de Kaggle
try:
    import kagglehub
    KAGGLEHUB_AVAILABLE = True
except ImportError:
    KAGGLEHUB_AVAILABLE = False

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
    KAGGLE_API_AVAILABLE = True
except ImportError:
    KAGGLE_API_AVAILABLE = False

# =============================================================================
# CONFIGURACIÓN DE DATASETS
# =============================================================================
# Fuentes directas (GitHub/URLs)
DATASETS_URL = {
    "csgo_match_results": "https://raw.githubusercontent.com/hojlund123/csgo-dataset/master/csgoresults.csv",
}

# Fuentes de Kaggle (Slug del dataset)
KAGGLE_DATASETS = [
    "mateusdmachado/csgo-professional-matches", # El más completo (Economy, Picks, Players)
    "griffindesroches/cs2-hltv-professional-match-statistics-dataset" # Datos CS2 2024-2025
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
    """Descarga datasets usando kagglehub (método recomendado) o Kaggle API."""
    for dataset_slug in KAGGLE_DATASETS:
        print(f"🚀 Intentando descargar desde Kaggle: {dataset_slug}...")
        
        # Primero intentamos con kagglehub (no requiere kaggle.json para datasets públicos)
        if KAGGLEHUB_AVAILABLE:
            try:
                download_path = kagglehub.dataset_download(dataset_slug)
                print(f"📦 Archivos descargados en caché: {download_path}")
                
                # Movemos los archivos a nuestra carpeta local data/raw
                for item in os.listdir(download_path):
                    s = os.path.join(download_path, item)
                    d = os.path.join(DATA_RAW_DIR, item)
                    if os.path.isdir(s):
                        if os.path.exists(d): shutil.rmtree(d)
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)
                print(f"✔️ Dataset [{dataset_slug}] movido a {DATA_RAW_DIR}")
                continue # Si funciona, pasamos al siguiente dataset
            except Exception as e:
                print(f"⚠️ Falló kagglehub para {dataset_slug}: {e}. Intentando con API...")

        # Si falla o no está disponible, intentamos con la API tradicional (requiere kaggle.json)
        if KAGGLE_API_AVAILABLE:
            try:
                api = KaggleApi()
                api.authenticate()
                api.dataset_download_files(dataset_slug, path=DATA_RAW_DIR, unzip=True)
                print(f"✔️ Dataset [{dataset_slug}] descargado vía API en {DATA_RAW_DIR}")
            except Exception as e:
                print(f"❌ Error total para {dataset_slug}: {e}")

def create_audit_log():
    """Genera un archivo de registro para control de versiones de datos."""
    log_path = os.path.join(DATA_RAW_DIR, "data_version.txt")
    with open(log_path, "w") as f:
        f.write(f"Dataset Version Control\n")
        f.write(f"----------------------\n")
        f.write(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Método: kagglehub + requests\n")
    print(f"📝 Registro de auditoría actualizado.")

if __name__ == "__main__":
    print("--- INICIANDO CAPTURA DE DATOS PARA PROYECTO CS:GO ---")
    setup_directories()
    download_from_url()
    download_from_kaggle()
    create_audit_log()
    print("--- PROCESO FINALIZADO ---")
