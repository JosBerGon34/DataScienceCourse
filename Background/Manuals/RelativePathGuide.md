1. Importación y obtención del directorio base:

from pathlib import Path

# Obtener la ruta del archivo actual (funciona en scripts .py)
# BASE_DIR = Path(__file__).resolve().parent

# En cuadernos Jupyter / VSCodium Interactive:
BASE_DIR = Path.cwd() # O Path().resolve() para la ruta absoluta del workspace actual
print(f"Directorio de trabajo actual: {BASE_DIR}")

2. Operadores y Navegación entre Subcarpetas
Usamos el operador / directamente para concatenar carpetas y archivos de forma limpia:

# Moverse un nivel arriba (equivalente a '../')
PARENT_DIR = BASE_DIR.parent

# Navegar a una subcarpeta interna
DATA_DIR = BASE_DIR / "DATASETS" / "DataSetSamplers"

# Ruta directa a tu CSV
csv_path = DATA_DIR / "sample_DesempleoEU.csv"

print(f"Ruta construida: {csv_path}")
print(f"¿Existe el archivo?: {csv_path.exists()}")

3. Búsqueda Dinámica de Archivos (Globbing)
Si no recuerdas la ubicación exacta del archivo dentro del proyecto, puedes buscarlo dinámicamente con glob o rglob (búsqueda recursiva en todas las subcarpetas):

# Buscar en el proyecto entero un archivo que contenga 'Desempleo' en el nombre
archivos_encontrados = list(BASE_DIR.rglob("*Desempleo*.csv"))

if archivos_encontrados:
    csv_path = archivos_encontrados[0]
    print(f"✓ Archivo localizado en: {csv_path}")
else:
    print("❌ Archivo no encontrado.")

4. Cargar en Pandas usando Path
Pandas acepta objetos Path de forma nativa sin necesidad de convertirlos a str

import pandas as pd
from pathlib import Path

# Construcción de la ruta agnóstica
ROOT_DIR = Path.cwd()
DATA_PATH = ROOT_DIR / "DATASETS" / "DataSetSamplers" / "sample_DesempleoEU.csv"

# Lectura directa
if DATA_PATH.exists():
    df100lines = pd.read_csv(DATA_PATH).sample(100)
    print("Cargado con éxito.")
else:
    print(f"Error: Comprueba la ruta {DATA_PATH}")
