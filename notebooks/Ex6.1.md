🟢 < Module 6.1 > Data Cleaning & Imputation — Advanced Survey Non-Response Codes & Imputation Strategies

##### 🎯 Context & Objectives

In survey data engineering (such as the European Social Survey), failing to distinguish between **systematic non-response codes** (`66`, `77`, `88`, `99`) and **legitimate extreme scale values** (`0` and `10`) introduces catastrophic bias into machine learning models. Treating a valid response of `0` ("No trust at all") as a missing value deletes extreme opinions and artificially compresses the variance towards the mean.

In this exercise, you will build an automated, auditable data cleaning and imputation pipeline in Python. You will systematically convert ESS missing codes to standard `NaN`s, preserve valid scale boundaries, and compare single-variable/grouped imputation with multivariate algorithms (`IterativeImputer` / MICE).

##### 📑 Exercise Instructions

###### 1. Syntactic / Algorithmic Level (Systematic Missing Code Handling)

Create a Python notebook (`notebooks/06_1_data_cleaning_imputation.ipynb`) that implements the following technical workflow:

- **Explicit Code Mapping (Avoiding Heuristic Pitfalls):**
    
    - Define a explicit dictionary structure mapping specific ESS missing value codes (`66` = Not applicable, `77` = Refusal, `88` = Don't know, `99` = No answer, `999` = Not available) to `np.nan`.
        
    - **Crucial Rule:** Ensure that legitimate scale endpoints (`0` and `10`) for 11-point Likert variables (such as `ppltrst`, `stfdem`, `lrscale`, `happy`, `rlgdgr`) are **strictly preserved** and NEVER converted to `NaN`.
        
- **Missingness Diagnosis (MCAR vs. MAR vs. MNAR):**
    
    - Calculate and display missing data percentages per column across the dataset.
        
    - Filter and inspect rows where non-response occurs to determine whether missingness is completely random or correlated with demographics (e.g., age or education level).
        

###### 2. Applied / Data Level (Grouped vs. Multivariate Imputation)

Apply these transformations to your merged master dataset (`master_country_features` or `surveys`):

- **Grouped Baseline Imputation:**
    
    - Impute missing values in ordinal survey variables (e.g., `trstlgl`, `stfdem`, `polintr`) using country-level or regional-cluster medians (`cntgrp_fc`) using Pandas `.groupby().transform()`.
        
- **Multivariate Imputation (`IterativeImputer` / MICE):**
    
    - Utilize `sklearn.impute.IterativeImputer` (enabling experimental features via `from sklearn.experimental import enable_iterative_imputer`) to model missing features as a function of other respondent answers.
        
- **Distributional Audit & Impact Assessment:**
    
    - Compare the summary statistics (mean, standard deviation, median, IQR) and probability density plots (KDE) of key variables before and after imputation.
        
    - Verify that the proportion of extreme responses (`0`s and `10`s) remains intact after cleaning.
        

##### 🌐 Official References & Documentation

- **European Social Survey Methodology:** [ESS Data Documentation Report — Missing Values Guide](https://www.google.com/search?q=https://www.europeansocialsurvey.org/methodology)
    
- **Scikit-Learn Imputation Guide:** [Imputing Missing Values (`IterativeImputer`)](https://www.google.com/search?q=https://scikit-learn.org/stable/modules/impute.html%23multivariate-feature-imputation)
    
- **Pandas Missing Data Guide:** [Working with Missing Data in Pandas](https://pandas.pydata.org/docs/user_guide/missing_data.html)
    

##### 📚 Recommended Manuals & CheatSheets

- **Scikit-Learn Imputation Cheat Sheet:** [DataCamp Scikit-Learn Missing Value Handling](https://www.google.com/search?q=https://www.datacamp.com/cheat-sheet/scikit-learn-cheat-sheet-python)
    
- **Rubin's Missing Data Theory:** [Little & Rubin — Statistical Analysis with Missing Data Overview](https://www.wiley.com/)
    

💻 **Tu Desafío:** Crea el cuaderno `notebooks/06_1_data_cleaning_imputation.ipynb` en tu entorno local. Implementa el mapeo explícito de códigos (`77`, `88`, `99` $\rightarrow$ `NaN`) respetando los extremos válidos `0` y `10`, aplica `IterativeImputer` y compara las distribuciones resultantes[cite: 4, 6, 7].


```python
# 1. Syntactic / Algorithmic Level (Systematic Missing Code Handling):
# A: Explicit Code Mapping (Avoiding Heuristic Pitfalls): We must to create a mask filter to check unique values count of every columm, and decide wich of those values
# corresponds to missing value codes from ESS.
# We must follow the data missing protocol from https://www.europeansocialsurvey.org/sites/default/files/2023-06/ESS9_data_protocol_e01_4.pdf
# Also a md, with columm variable collection located in ./DataScienceCourse/data/raw/VariablesESS.md
# Our vectorized mask will be done on the read process of duckdb sql, so we will save memory and will be cleaner. for these we need to prepare the query,
# Predefining the filter dictionaries:
import os
import duckdb
from dotenv import load_dotenv
load_dotenv()
# Conexión a tu servidor PostgreSQL
con = duckdb.connect()
attach_query = f"""
ATTACH 'dbname={os.getenv("PGDATABASE")} 
        user={os.getenv("PGUSER")} 
        password={os.getenv("PGPASSWORD")} 
        host={os.getenv("PGHOST")} 
        port={os.getenv("PGPORT")}' 
AS db (TYPE postgres);
"""
con.execute(attach_query)


# Lets creat vectori
con.execute("""
    CREATE OR REPLACE MACRO clean_ess_1d(x) AS 
        CASE WHEN x IN (6, 7, 8, 9) THEN NULL ELSE x END;
        
    CREATE OR REPLACE MACRO clean_ess_2d(x) AS 
        CASE WHEN x IN (66, 77, 88, 99) THEN NULL ELSE x END;
        
    CREATE OR REPLACE MACRO clean_ess_3d(x) AS 
        CASE WHEN x IN (666, 777, 888, 999) THEN NULL ELSE x END;
        
    CREATE OR REPLACE MACRO clean_ess_5d(x) AS 
        CASE WHEN x IN (66666, 77777, 88888, 99999) THEN NULL ELSE x END;
""")

```




    <_duckdb.DuckDBPyConnection at 0x7f26d01482b0>




```python
# Listas de variables según su formato del ESS
ESS_1D = ['clsprty', 'gincdif', 'brncntr', 'ctzcntr', 'domicil', 'emplrel', 'polintr', 'gndr']
ESS_2D = [
    'ppltrst', 'trstlgl', 'trstplc', 'trstplt', 'trstprl', 'trstprt', 'trstep', 'trstsci', 'trtsci_pnd',
    'stfdem', 'stfeco', 'stfgov', 'lrscale', 'happy', 'rlgdgr', 'pplfair', 'pplhlp', 'imbgeco', 
    'imwbcnt', 'atcherp', 'atchctr', 'health', 'mnactic', 'edulvlb'
]
ESS_3D = ['wkhtot', 'agea', 'hhmmb']
ESS_5D = ['emplno', 'isco08']

def build_duckdb_clean_select(table_columns: list, table_alias: str = 'e') -> str:
    """
    Genera dinámicamente las cláusulas SELECT aplicando las macros de DuckDB
    según la tipología de cada columna encontrada en la tabla.
    """
    select_clauses = []
    
    for col in table_columns:
        col_ref = f"{table_alias}.{col}" if table_alias else col
        
        if col in ESS_1D:
            select_clauses.append(f"clean_ess_1d({col_ref}) AS {col}")
        elif col in ESS_2D:
            select_clauses.append(f"clean_ess_2d({col_ref}) AS {col}")
        elif col in ESS_3D:
            select_clauses.append(f"clean_ess_3d({col_ref}) AS {col}")
        elif col in ESS_5D:
            select_clauses.append(f"clean_ess_5d({col_ref}) AS {col}")
        else:
            # Columnas identificativas o métricas continuas (cntry, essround, OBS_VALUE, etc.)
            select_clauses.append(f"{col_ref} AS {col}")
            
    return ",\n    ".join(select_clauses)
```


```python
build_duckdb_clean_select(ESS_1D)
```




    'clean_ess_1d(e.clsprty) AS clsprty,\n    clean_ess_1d(e.gincdif) AS gincdif,\n    clean_ess_1d(e.brncntr) AS brncntr,\n    clean_ess_1d(e.ctzcntr) AS ctzcntr,\n    clean_ess_1d(e.domicil) AS domicil,\n    clean_ess_1d(e.emplrel) AS emplrel,\n    clean_ess_1d(e.polintr) AS polintr,\n    clean_ess_1d(e.gndr) AS gndr'




```python

```
