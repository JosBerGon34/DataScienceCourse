# src/paths.py
import os
from pathlib import Path

# 1. Detección dinámica de la raíz del proyecto
# Como paths.py está en la carpeta 'src/', el padre del padre (.parent.parent) es siempre la raíz del repo.
ROOT_DIR = Path(__file__).resolve().parent.parent

# 2. Definición de rutas estandarizadas
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
TABLES_DIR = RAW_DATA_DIR / "Tables"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = ROOT_DIR / "models"

def setup_workspace():
    """
    Configura el directorio de trabajo activo y verifica la integridad 
    de las carpetas de datos principales. Retorna un diccionario con las rutas.
    """
    if not ROOT_DIR.exists():
        raise FileNotFoundError(f"❌ No se pudo localizar la raíz del proyecto en {ROOT_DIR}")

    # Fijar el workspace
    os.chdir(ROOT_DIR)
    print(f"✅ Workspace anclado en: {os.getcwd()}")

    # Verificar existencia de la carpeta de tablas crudas
    if not TABLES_DIR.exists():
        if DATA_DIR.exists():
            print(f"⚠️ La carpeta 'data' existe pero falta 'Tables'. Contenido: {os.listdir(DATA_DIR)}")
        else:
            print(f"⚠️ La carpeta 'data' no existe en la raíz: {os.listdir(ROOT_DIR)}")
        raise FileNotFoundError(f"❌ Falta la ruta de tablas: {TABLES_DIR}")

    print(f"📂 Ruta de tablas verificada: {TABLES_DIR}")
    
    # Retornamos las variables para usarlas fácilmente en el notebook
    return {
        "ROOT": ROOT_DIR,
        "DATA": DATA_DIR,
        "TABLES": TABLES_DIR,
        "PROCESSED": PROCESSED_DATA_DIR
    }
    