import os
import requests
import pandas as pd
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN DE DATASETS
# =============================================================================
DATASETS = {
    "csgo_match_results": "https://raw.githubusercontent.com/hojlund123/csgo-dataset/master/csgoresults.csv",
}

DATA_RAW_DIR = os.path.join(os.getcwd(), "data", "raw")

def setup_directories():
    """Asegura que la estructura de carpetas de datos exista."""
    if not os.path.exists(DATA_RAW_DIR):
        os.makedirs(DATA_RAW_DIR)
        print(f"✅ Carpeta creada: {DATA_RAW_DIR}")

def download_datasets():
    """Descarga los archivos configurados en DATASETS."""
    for name, url in DATASETS.items():
        target_path = os.path.join(DATA_RAW_DIR, f"{name}.csv")
        print(f"🚀 Iniciando descarga de: {name}...")
        
        try:
            # Nota: Para archivos grandes o APIs (como PandasScore), 
            # aquí implementaríamos lógica de autenticación o fragmentación.
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Si la respuesta es CSV, lo guardamos vía pandas para asegurar formato
            # Si es binario (como el placeholder), lo guardamos directo
            with open(target_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✔️ Archivo guardado satisfactoriamente en: {target_path}")
            
        except Exception as e:
            print(f"❌ Error al descargar {name}: {e}")

def create_audit_log():
    """Genera un archivo de registro para control de versiones de datos."""
    log_path = os.path.join(DATA_RAW_DIR, "data_version.txt")
    with open(log_path, "w") as f:
        f.write(f"Dataset Version Control\n")
        f.write(f"----------------------\n")
        f.write(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Responsable: Automatización del Proyecto\n")
    print(f"📝 Registro de auditoría actualizado en: {log_path}")

if __name__ == "__main__":
    print("--- INICIANDO CAPTURA DE DATOS PARA PROYECTO CS:GO ---")
    setup_directories()
    download_datasets()
    create_audit_log()
    print("--- PROCESO FINALIZADO ---")
