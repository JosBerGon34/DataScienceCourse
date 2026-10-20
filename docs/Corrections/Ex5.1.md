🟢 < Module 5.1 > NumPy & Pandas — High-Performance Data Ingestion, Merging & Reshaping

#### 🎯 Context & Objectives

In real-world data science pipelines, analytical data arrives fragmented across multiple sources (macroeconomic files from Eurostat, individual survey microdata waves from the European Social Survey, and scraped categorical attributes). To feed downstream machine learning models without introducing memory leaks or data corruption, a Data Scientist must master vectorized data manipulation, memory-efficient type casting, and relational merging using NumPy and Pandas.

In this exercise, you will build an optimized ingestion pipeline that merges multi-source datasets, restructures data shapes using pivot/melt operations, and handles complex multi-index groupings.

#### 📑 Exercise Instructions

##### 1. Syntactic / Algorithmic Level (Vectorized Operations & Reshaping)

Create a Python notebook or script (`notebooks/05_1_numpy_pandas_operations.ipynb`) that implements the following technical steps:

- **Vectorized Array Operations**:
    
    - Perform high-performance vectorized calculations on NumPy arrays (e.g., calculating standardized z-scores across multi-dimensional macro matrices without explicit Python `for` loops).
        
- **Data Reshaping (Wide vs. Long Formats)**:
    
    - Take a wide Eurostat macroeconomic table (where years are represented as individual columns) and transform it into a clean long-format tidy dataset using `pd.melt()`.
        
    - Reconstruct the wide matrix back using `pd.pivot_table()`, ensuring multi-level column indexing is properly flattened and cleaned.
        

##### 2. Applied / Data Level (Multi-Source Relational Merging)

Apply advanced Pandas joining techniques to your project datasets:

- **Relational Merging & Key Alignment**:
    
    - Load your cleaned CSV/DuckDB exports for country metadata (`GlobalCountriesLang.csv`), macroeconomic features, and ESS survey summaries.
        
    - Perform inner and outer joins (`pd.merge()`) using compound keys (e.g., country code `cntry` / `geo` and survey year/round) to prevent row explosion or silent data loss.
        
- **Hierarchical Groupings & Aggregations**:
    
    - Group the merged master dataset by macro-economic region clusters (`cntgrp_fc`) and compute multi-metric aggregated summaries (mean, median, IQR) for institutional trust variables.
        

#### 🌐 Official References for Documentation

- **Pandas Merging / Joining Guide**: [Pandas Merge, Join, and Concatenate Documentation](https://pandas.pydata.org/docs/user_guide/merging.html)
    
- **Pandas Reshaping Guide**: [Reshaping and Pivot Tables Documentation](https://pandas.pydata.org/docs/user_guide/reshaping.html)
    

#### 📚 Recommended Manuals & CheatSheets

- **Pandas Cheat Sheet**: [DataCamp Pandas Cheat Sheet (PDF)](https://www.google.com/search?q=https://www.datacamp.com/cheat-sheet/pandas-cheat-sheet)
    

💻 **Your Challenge:** Crea el cuaderno `notebooks/05_1_numpy_pandas_operations.ipynb` en tu entorno local, ejecuta las transformaciones y fusiones de alto rendimiento con tus datasets, y pásame tu código o resultados cuando estés listo para avanzar al Módulo 6 (Data Cleaning & Imputation).


```python
# I will focus this excersise to practice this vectorized methods, but aswell, to link indirectly , different dataframes using variables that will create different classes. We cant invent or
# simulate clases, we will use some variables related between dataframes to make indirectly different clases with a dense meaning. For example age, number of sons, how many
# people lives in his home, etc. For this i upload the whole csv to my database via python on a code cell or a bash terminal from activated venv with required libraries.
import duckdb as db
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()  # search .env on the directory
con = db.connect()
con.execute("ATTACH '' AS db (TYPE postgres, SCHEMA 'public')")
```




    <_duckdb.DuckDBPyConnection at 0x7f82d975a470>




```python
#Let's inspect how is the format of our csv's located in the sql databaseÑ
schema_info = con.sql("DESCRIBE db.PobrezaEU").df()
print(schema_info)
```

                                   column_name column_type null   key default  \
    0                                STRUCTURE     VARCHAR  YES  None    None   
    1                             STRUCTURE_ID     VARCHAR  YES  None    None   
    2                           STRUCTURE_NAME     VARCHAR  YES  None    None   
    3                                     freq     VARCHAR  YES  None    None   
    4                           Time frequency     VARCHAR  YES  None    None   
    5                                     unit     VARCHAR  YES  None    None   
    6                          Unit of measure     VARCHAR  YES  None    None   
    7                                      age     VARCHAR  YES  None    None   
    8                                Age class     VARCHAR  YES  None    None   
    9                                      sex     VARCHAR  YES  None    None   
    10                                   Sex_1     VARCHAR  YES  None    None   
    11                                     geo     VARCHAR  YES  None    None   
    12         Geopolitical entity (reporting)     VARCHAR  YES  None    None   
    13                             TIME_PERIOD      BIGINT  YES  None    None   
    14                                    Time      DOUBLE  YES  None    None   
    15                               OBS_VALUE      DOUBLE  YES  None    None   
    16                       Observation value      DOUBLE  YES  None    None   
    17                                OBS_FLAG     VARCHAR  YES  None    None   
    18  Observation status (Flag) V2 structure     VARCHAR  YES  None    None   
    19                             CONF_STATUS      DOUBLE  YES  None    None   
    20           Confidentiality status (flag)      DOUBLE  YES  None    None   
    
       extra  
    0   None  
    1   None  
    2   None  
    3   None  
    4   None  
    5   None  
    6   None  
    7   None  
    8   None  
    9   None  
    10  None  
    11  None  
    12  None  
    13  None  
    14  None  
    15  None  
    16  None  
    17  None  
    18  None  
    19  None  
    20  None  



```python
import numpy as np
#1 lets get z-score from PobrezaEu.csv located in our local database.
# A. Lets define the query sentence.
query = """
    SELECT TIME_PERIOD, OBS_VALUE, geo 
    FROM db.pobrezaeu
    WHERE OBS_VALUE IS NOT NULL AND TIME_PERIOD >= 2015
"""
df_filtered = con.sql(query).df()

# B. Direct conversion to Numpy arrais for the vectorized computing.
time_arr = df_filtered['TIME_PERIOD'].to_numpy(dtype=int)
obs_arr = df_filtered['OBS_VALUE'].to_numpy(dtype=float)
geo_arr = df_filtered['geo'].to_numpy(dtype=str)

# C. Vectorized calculation using Numpy Z-scores
mean_obs = np.mean(obs_arr)
std_obs = np.std(obs_arr)

z_scores = (obs_arr - mean_obs) / std_obs

print(f"✅ Succesfull arrays exctracted via DuckDB:")
print(f" - Computed Samples: {len(obs_arr)}")
print(f" - Array mean: {mean_obs:.4f}")
print(f" - First 5 z-score results: {z_scores[:5]}")
```

    ✅ Succesfull arrays exctracted via DuckDB:
     - Computed Samples: 87720
     - Array mean: 1419.7538
     - First 5 z-score results: [-0.21022835 -0.2109397  -0.21138817 -0.21211498 -0.2120222 ]



```python
#Let's inspect how is the format of our csv's located in the sql databaseÑ
schema_info = con.sql("DESCRIBE db.Surveys").df()
print(schema_info)
```

       column_name column_type null   key default extra
    0         name     VARCHAR  YES  None    None  None
    1     essround      BIGINT  YES  None    None  None
    2      edition      DOUBLE  YES  None    None  None
    3     proddate     VARCHAR  YES  None    None  None
    4         idno      BIGINT  YES  None    None  None
    5        cntry     VARCHAR  YES  None    None  None
    6      dweight      DOUBLE  YES  None    None  None
    7      pspwght      DOUBLE  YES  None    None  None
    8      pweight      DOUBLE  YES  None    None  None
    9     anweight      DOUBLE  YES  None    None  None
    10    netusoft      BIGINT  YES  None    None  None
    11     ppltrst      BIGINT  YES  None    None  None
    12     trstprl      BIGINT  YES  None    None  None
    13     trstlgl      BIGINT  YES  None    None  None
    14      trstun      BIGINT  YES  None    None  None
    15     clsprty      BIGINT  YES  None    None  None
    16     lrscale      BIGINT  YES  None    None  None
    17     gincdif      BIGINT  YES  None    None  None
    18     imbgeco      BIGINT  YES  None    None  None
    19       happy      BIGINT  YES  None    None  None
    20      health      BIGINT  YES  None    None  None
    21     atchctr      BIGINT  YES  None    None  None
    22     atcherp      BIGINT  YES  None    None  None
    23      rlgdnm      BIGINT  YES  None    None  None
    24      rlgdgr      BIGINT  YES  None    None  None
    25     ctzcntr      BIGINT  YES  None    None  None
    26     brncntr      BIGINT  YES  None    None  None
    27       hhmmb      BIGINT  YES  None    None  None
    28        gndr      BIGINT  YES  None    None  None
    29        agea      BIGINT  YES  None    None  None
    30     domicil      BIGINT  YES  None    None  None
    31     edulvlb      BIGINT  YES  None    None  None
    32     mnactic      BIGINT  YES  None    None  None
    33     emplrel      BIGINT  YES  None    None  None
    34      emplno      BIGINT  YES  None    None  None
    35      wkhtot      BIGINT  YES  None    None  None
    36     tporgwk      BIGINT  YES  None    None  None
    37    impricha      BIGINT  YES  None    None  None
    38    impfreea      BIGINT  YES  None    None  None
    39    iphlppla      BIGINT  YES  None    None  None
    40    imptrada      BIGINT  YES  None    None  None
    41        prob      DOUBLE  YES  None    None  None
    42     stratum      BIGINT  YES  None    None  None
    43         psu      BIGINT  YES  None    None  None



```python

schema_info = con.sql("DESCRIBE db.macro_features_matrix_2015_2025").df()
print(schema_info)
```

                          column_name column_type null   key default extra
    0                             geo     VARCHAR  YES  None    None  None
    1                       countries     VARCHAR  YES  None    None  None
    2                         regions     VARCHAR  YES  None    None  None
    3                        offilang     VARCHAR  YES  None    None  None
    4                         reglang     VARCHAR  YES  None    None  None
    5         demographypct_2015_2025      DOUBLE  YES  None    None  None
    6       unemploymentpct_2015_2025      DOUBLE  YES  None    None  None
    7      govdebtgdpabspct_2015_2025      DOUBLE  YES  None    None  None
    8            povertypct_2015_2025      DOUBLE  YES  None    None  None
    9           ginicoefpct_2015_2025      DOUBLE  YES  None    None  None
    10         gdpcapitapct_2015_2025      DOUBLE  YES  None    None  None
    11  disposableincomepct_2015_2025      DOUBLE  YES  None    None  None
    12         inflationpct_2015_2025      DOUBLE  YES  None    None  None



```python
#2. Applied / Data Level (Multi-Source Relational Merging) using unique key values from common columms of our different datablocks.
# We will use our Surveys DF and our matrix economic and regional features we did exercises ago.
# We use a query on sql via duckdb to make an easy filtering, it saves memory instead to load the whole dataframe or partial df just with the columns we need and then
#filter it via pandas library.
import os
import duckdb
from dotenv import load_dotenv

# A. We load the start credentials stored in .env
load_dotenv()

# B. Initialize DuckDB
con = duckdb.connect()

# C. Load and install postgresql on duckdb
con.execute("INSTALL postgres;")
con.execute("LOAD postgres;")

# D. We get the inner variables from the .env
attach_query = f"""
ATTACH 'dbname={os.getenv("PGDATABASE")} 
        user={os.getenv("PGUSER")} 
        password={os.getenv("PGPASSWORD")} 
        host={os.getenv("PGHOST")} 
        port={os.getenv("PGPORT")}' 
AS db (TYPE postgres);
"""
con.execute(attach_query)

# 4. Query the tables to get only our desired columns and merge them via unique values mask.
query = """
    CREATE OR REPLACE TABLE master_country_features AS
    SELECT 
        e.cntry AS country_code,
        e.essround,
        e.happy,
        e.trstlgl,
        e.lrscale,
        m.geo AS macro_geo,
        m.unemploymentpct_2015_2025 AS macro_unemployment,
        m.povertypct_2015_2025 AS macro_poverty
    FROM db.surveys e
    LEFT JOIN db.macro_features_matrix_2015_2025 m
        ON e.cntry = m.geo
    WHERE e.cntry IS NOT NULL AND m.unemploymentpct_2015_2025 IS NOT NULL;
"""

con.execute(query)

# 5. Checking the results
df_result = con.sql("SELECT * FROM master_country_features LIMIT 5").df()
print("✅ ¡Succesfull relational merge in DuckDB!")
print(df_result)

```

    ✅ ¡Succesfull relational merge in DuckDB!
      country_code  essround  happy  trstlgl  lrscale macro_geo  \
    0           AT        11      8        9        5        AT   
    1           AT        11      9        6        0        AT   
    2           AT        11      9        5        3        AT   
    3           AT        11      7        6        5        AT   
    4           AT        11      9        8        2        AT   
    
       macro_unemployment  macro_poverty  
    0               -0.37          10.06  
    1               -0.37          10.06  
    2               -0.37          10.06  
    3               -0.37          10.06  
    4               -0.37          10.06  



```python

```
