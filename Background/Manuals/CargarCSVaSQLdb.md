Script Python Configurado con Variables de Entorno (.env)
Crea un archivo llamado cargar_db.py en tu directorio de trabajo (y asegúrate de que .env y .venv/ estén listados en tu .gitignore):

Python
import os
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv

# 1. Cargar las variables de entorno desde el archivo .env oculto
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# 2. Construir la URI de conexión de forma segura
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def main():
    # 3. Inicializar el motor SQLAlchemy (Traductor de sintaxis SQL/Python)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    
    # Ruta al archivo CSV (usando rutas relativas limpias)
    csv_path = "./data/raw/Tables/EuInfo.csv"
    
    print(f"🔄 Leyendo archivo: {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # 4. Volcado a la base de datos (idempotente con if_exists='replace')
    table_name = "EuInfo"
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    
    print(f"✅ ¡Tabla '{table_name}' cargada con éxito en PostgreSQL desde la terminal Bash!")

if __name__ == "__main__":
    main()
Archivo de Configuración Oculto (.env)
En la raíz de tu proyecto, crea este archivo (recuerda añadirlo al .gitignore para que no se suba a GitHub):

Fragmento de código
DB_USER=Practice
DB_PASSWORD=12345
DB_HOST=localhost
DB_PORT=5432
DB_NAME=DataScienceCourse
Ejecución desde la Terminal Bash (con el entorno virtual activo)
Para disparar el script utilizando el intérprete de tu entorno virtual (.venv) directamente desde la línea de comandos de tu terminal de JupyterLab o Bash:

Bash
python cargar_db.py
Manual en Markdown para la carpeta background/
Guarda el siguiente contenido en un archivo markdown dentro de tu carpeta de documentación de fondo (por ejemplo, background/manual_env_bash_postgresql.md):

Markdown
# 📘 Manual Técnico: Ingestión Automatizada a PostgreSQL con Python-Dotenv y Terminal Bash

## 1. Object & Scope
Este procedimiento establece el estándar de ingeniería para conectar de forma segura scripts de Python con una base de datos PostgreSQL local o en red LAN, utilizando variables de entorno protegidas (`.dotenv`) y ejecución directa por línea de comandos CLI en entornos CachyOS/Linux.

---

## 2. Configuración de Seguridad y Credenciales (.env)
Las credenciales sensibles de acceso a la base de datos nunca deben hardcodearse en el código fuente. Se externalizan en un archivo `.env` ubicado en la raíz del proyecto y excluido mediante `.gitignore`:

1. Crear el archivo `.env`:
   ```env
   DB_USER=tu_usuario
   DB_PASSWORD=tu_contraseña
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=nombre_base_datos
Asegurar que .env y el entorno virtual (.venv/) estén registrados en el archivo .gitignore.

3. Estructura del Script de Ingestión (cargar_db.py)
El script combina tres librerías esenciales del pipeline:

python-dotenv: Carga las variables de entorno de forma dinámica.

pandas: Maneja la lectura eficiente del archivo CSV plano.

SQLAlchemy: Actúa como el motor abstracto de traducción entre los DataFrames de Python y el servidor SQL relacional.

4. Ejecución en Producción Local (Terminal Bash)
Para garantizar que se utilicen las dependencias correctas del entorno virtual configurado en JupyterLab/CachyOS:

Bash
# Activar el entorno virtual (si procede)
source .venv/bin/activate

# Ejecutar el script de carga
python cargar_db.py

¡Con esto ya tienes documentado, automatizado y blindado el flujo de carga mediante variables de entorno y terminal Bash para tu portfolio! 🚀🐘