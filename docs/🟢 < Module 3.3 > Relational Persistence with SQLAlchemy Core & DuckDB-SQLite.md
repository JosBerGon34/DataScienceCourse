🟢 < MODULE 3.3 > Relational Persistence with SQLAlchemy Core & DuckDB-SQLite


### 🎯 Context & Objectives

In real-world Data Science environments, production data does not live in static CSV files. It is stored across enterprise relational databases (e.g., PostgreSQL, Snowflake) accessed programmatically via database engines.

In this exercise, you will construct a database ingestion pipeline using **SQLAlchemy** (Core abstraction layer) paired with an embedded relational engine (**DuckDB** or **SQLite**). You will programmatically create database schemas, ingest raw CSV artifacts (`GlobalCountriesLang.csv`, `EuRegions.csv`), execute relational joins via SQL / SQLAlchemy expressions, and extract the unified master dataset.


### 📑 Exercise Instructions

#### 1. Syntactic Level (SQLAlchemy Engine & Schema Definition)

In your local script or notebook (`notebooks/Ex3.3.ipynb`), implement the following pipeline:

1. **Engine & Connection Setup**:
    
    - Create an isolated database connection using SQLAlchemy:
        
        Python
        
		
        
2. **Schema Declarations & DDL**:
    
    - Programmatically drop existing tables to guarantee pipeline idempotency (`DROP TABLE IF EXISTS ...`).
        
    - Create target tables using raw SQL via `engine.connect()` and `text()`, or using SQLAlchemy `Table` / `MetaData` constructs.
        
3. **Data Ingestion**:
    
    - Read your local CSVs (`GlobalCountriesLang.csv`, `EuRegions.csv`, and sample Eurostat data) into Pandas DataFrames.
        
    - Persist the DataFrames into database tables using Pandas' `.to_sql()` method linked directly to your SQLAlchemy `engine` (`index=False`, `if_exists='replace'`).


```Python
#1) Engine & Connection:
from sqlalchemy import create_engine, text
# For DuckDB: create_engine("duckdb:///data/processed/datascience.duckdb")
# For SQLite: create_engine("sqlite:///data/processed/datascience.db")
engine = create_engine("duckdb:///data/processed/datascience.duckdb")
```
#### 2. Applied Data Science Level (Relational Master Query & Export)

Consolidate the multi-source dataset into a master feature table for downstream modules:

1. **Relational Query Execution**:
    
    - Write an SQL `JOIN` query via SQLAlchemy to merge the country metadata, geographical region classifications, and economic indicators on the country code key (`geo` / `country_code`).
        
    - Include aggregation (`AVG()`, `COUNT()`) and a `HAVING` clause to filter countries missing critical observations.
        
2. **DataFrame Extraction & Integrity Checks**:
    
    - Read the query result into a DataFrame using `pd.read_sql_query(sql_query, con=engine)`.
        
    - Export the unified DataFrame to `data/processed/master_country_features.csv`.
        
    - Verify schema types and confirm zero unintended missing values in primary key columns.
        

### 🌐 Official References for Documentation

- **SQLAlchemy Official Documentation**: [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
    
- **DuckDB SQLAlchemy Integration**: [DuckDB SQLAlchemy Engine Docs](https://www.google.com/search?q=https://duckdb.org/docs/api/python/sqlalchemy)
    

### 📚 Recommended Manuals & CheatSheets

- **SQLAlchemy Core Cheat Sheet**: [DataCamp SQLAlchemy Cheat Sheet (PDF)](https://www.google.com/search?q=https://www.datacamp.com/cheat-sheet/sqlalchemy-cheat-sheet)
    

¿Prefieres continuar con esta versión que integra **SQLAlchemy Core** para simular la conexión estandarizada a la BD?