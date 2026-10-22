# src/db.py
import os
import duckdb
import pandas as pd
from dotenv import load_dotenv
from src.paths import ROOT_DIR

# 1. Cargar las variables de entorno de forma silenciosa y segura
ENV_PATH = ROOT_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)

def get_duckdb_pg_conn():
    """
    Inicia una instancia de DuckDB en memoria, carga la extensión de PostgreSQL 
    y adjunta la base de datos externa usando credenciales del archivo .env.
    """
    # Recolectar variables con un fallback seguro por si el .env falla temporalmente
    pg_db = os.getenv("PGDATABASE")
    pg_user = os.getenv("PGUSER")
    pg_pass = os.getenv("PGPASSWORD")
    pg_host = os.getenv("PGHOST")
    pg_port = os.getenv("PGPORT")

    # Iniciar DuckDB (en memoria, sin generar archivos locales)
    conn = duckdb.connect()
    
    # Instalar (si no existe) y cargar el conector nativo de PostgreSQL
    conn.execute("INSTALL postgres; LOAD postgres;")
    
    # Construir el puente ATTACH inyectando las variables de entorno
    attach_query = f"""
    ATTACH IF NOT EXISTS 'dbname={pg_db} user={pg_user} password={pg_pass} host={pg_host} port={pg_port}' 
    AS db (TYPE postgres);
    """
    
    # Ejecutar el puente
    conn.execute(attach_query)
    
    return conn

def query_to_df(query: str) -> pd.DataFrame:
    """
    Ejecuta una consulta SQL en DuckDB (apuntando al alias 'db') 
    y extrae el resultado directamente a un DataFrame de Pandas.
    """
    conn = get_duckdb_pg_conn()
    try:
        # La API de DuckDB convierte a Pandas de forma nativa y vectorizada
        df = conn.execute(query).df()
        return df
    finally:
        # Garantizar que la conexión se cierra para liberar memoria
        conn.close()