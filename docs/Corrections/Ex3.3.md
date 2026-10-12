First of all lets install via bash terminal in the root of
repository all the libraries or enviroment needs to connect
to our practice database in lan mode:
'''bash
[***@cachyos-***DataScienceCourse]$ source .venv-core/bin/activate
[***@cachyos-*** DataScienceCourse]$ pip install psycopg2-binary sqlalchemy ipython-sql
Collecting...
'''
#Part1.1 and Part1.2: Lets connect to our database, i suggest to use a paralel viewer and editor of sql db's. i recomend tabularis, very good client, it includes mcp services, to connect AI apis.
#This is our main workflow we must follow:


CSV / Parquet          PostgreSQL (lectura)
     │                       │
     └──────────┬────────────┘
                ▼
             DuckDB
      (ATTACH postgres + JOIN
       between sources)
                │
          first filter / clean
          aggregate
                │
                ▼
           DataFrame(numpy & pandas operations)
                │
                ▼
          SQLAlchemy
                │
                ▼
          PostgreSQL (writing on db)


```python
%load_ext sql
%config SqlMagic.style = 'MARKDOWN'  # O 'SIMPLE', 'MSWORD_FRIENDLY'
```

    /home/josu/Documentos/DataScienceCourse/.venv-core/lib/python3.13/site-packages/pyspark/sql/connect/utils.py:41: FutureWarning: PySpark does not yet fully support pandas >= 3.0.0. Some features may not work correctly. It is recommended to use pandas < 3.0.0 for now.
      require_minimum_pandas_version()
    /home/josu/Documentos/DataScienceCourse/.venv-core/lib/python3.13/site-packages/pyspark/testing/utils.py:127: FutureWarning: PySpark does not yet fully support pandas >= 3.0.0. Some features may not work correctly. It is recommended to use pandas < 3.0.0 for now.
      require_minimum_pandas_version()



```python
%sql postgresql+psycopg2://Practice:12345@localhost:5432/DataScienceCourse
```


<span style="None">Connecting to &#x27;postgresql+psycopg2://Practice:***@localhost:5432/DataScienceCourse&#x27;</span>



```python
%sql SELECT current_user, current_database();
```


<span style="None">Running query in &#x27;postgresql+psycopg2://Practice:***@localhost:5432/DataScienceCourse&#x27;</span>



<span style="color: green">1 rows affected.</span>





<table>
    <thead>
        <tr>
            <th>current_user</th>
            <th>current_database</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Practice</td>
            <td>DataScienceCourse</td>
        </tr>
    </tbody>
</table>




```python
%sql SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```


<span style="None">Running query in &#x27;postgresql+psycopg2://Practice:***@localhost:5432/DataScienceCourse&#x27;</span>





<table>
    <thead>
        <tr>
            <th>table_name</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
</table>




```python
%sql SHOW TABLES;
%sql DESCRIBE nombre_tabla;
```


<span style="None">Running query in &#x27;postgresql+psycopg2://Practice:***@localhost:5432/DataScienceCourse&#x27;</span>


    RuntimeError: (psycopg2.errors.UndefinedObject) unrecognized configuration parameter "tables"
    
    [SQL: SHOW TABLES;]
    (Background on this error at: https://sqlalche.me/e/20/f405)



```python
#The previous cell gives an error because we dont have
#Any table on DataScienceCourse database.
from pathlib import Path
import os
import pandas as pd
import random
#PATHING SCRIPT FOR EVERY EXCERSISE - PROJECT - WORKSPACE
# 1.Literal definition of route pathings(Every user of remote repository must config this pathing in order to find the local repository of his computer)
# My case:
ROOT = Path("/home/josu/Documentos/DataScienceCourse")

# We verify the existence before continue
if not ROOT.exists():
    raise FileNotFoundError(f"❌ The route {ROOT} doesn't exist. Check it.")

# 2. Fix the workspace
os.chdir(ROOT)
print(f"✅ Worskspace enabled!: {os.getcwd()}")

# 3. Define relative pathings to work properly
DATA_TABLES = ROOT / "data" / "raw" / "Tables"

# Let's verify our table folder:
if not DATA_TABLES.exists():
    # If it fails, monitorize the issue: 
    data_dir = ROOT / "data"
    if data_dir.exists():
        print(f"⚠️ the folder 'data' exists but it doesn't have any 'Tables'. 'data' content: {os.listdir(data_dir)}")
    else:
        print(f"⚠️ The folder 'data' doesn't exist on ROOT workspace: {os.listdir(ROOT)}")
    raise FileNotFoundError(f"❌ The tables route {DATA_TABLES} is missing.")

print(f"📂 Tables route detected: {DATA_TABLES}")
```

    ✅ Worskspace enabled!: /home/josu/Documentos/DataScienceCourse
    📂 Tables route detected: /home/josu/Documentos/DataScienceCourse/data/raw/Tables



```python


print(Path.cwd())
```

    /home/josu/Documentos/DataScienceCourse



```python

import duckdb

csv_path = Path("data/raw/Tables/CambioDemografico.csv")

print(csv_path.exists())
print(csv_path.resolve())
```

    True
    /home/josu/Documentos/DataScienceCourse/data/raw/Tables/CambioDemografico.csv



```python
#Part 1.3, DataIngestion:
#lETS CHECK EUROSTAT DATABASES, filter every1 by the range of years (2015-2025)
#The idea is unify the dataframes using vectorized operations, first filtering with duckdb in to the csv files.
csv_path  = DATA_TABLES / "CambioDemografico.csv"
csv_path1 = DATA_TABLES / "DesempleoEU.csv"  
csv_path2 = DATA_TABLES / "DeudaBrutaGoviernosEu.csv"
csv_path3 = DATA_TABLES / "ExclusionSocialPobreza.csv"
csv_path4 = DATA_TABLES / "GiniCoefEU.csv"   
csv_path5 = DATA_TABLES / "PIBperCapitaEuropa.csv"
csv_path6 = DATA_TABLES / "RentaDisponibleBrutaHogares.csv"
csv_path7 = DATA_TABLES / "IPC-Inflation.csv"
csv_path8 = DATA_TABLES / "EuInfo.csv"
print("=== TEMPORAL AUDIT FOR EUROSTAT DATASETS ===")
con = duckdb.connect()
datasets_audit = {
    "Demography (csv_path)": csv_path,
    "Unemployment (csv_path1)": csv_path1,
    "Gov Debt (csv_path2)": csv_path2,
    "Poverty (csv_path3)": csv_path3,
    "Gini Coefficient (csv_path4)": csv_path4,
    "GDP per Capita (csv_path5)": csv_path5,
    "Household Income (csv_path6)": csv_path6,
    "Inflation / HICP (csv_path7)": csv_path7
}

for name, path in datasets_audit.items():
    try:
        # Para el IPC mensual extraemos los primeros 4 caracteres como año
        if "Inflation" in name:
            audit_query = f"""
                SELECT 
                    MIN(SUBSTRING(TIME_PERIOD, 1, 4)) AS min_year, 
                    MAX(SUBSTRING(TIME_PERIOD, 1, 4)) AS max_year,
                    COUNT(DISTINCT SUBSTRING(TIME_PERIOD, 1, 4)) AS unique_years_count
                FROM read_csv_auto('{path}')
            """
        else:
            audit_query = f"""
                SELECT 
                    MIN(TIME_PERIOD) AS min_year, 
                    MAX(TIME_PERIOD) AS max_year,
                    COUNT(DISTINCT TIME_PERIOD) AS unique_years_count
                FROM read_csv_auto('{path}')
            """
        
        res = con.execute(audit_query).df()
        print(f"{name:<30} -> Min Year: {res['min_year'][0]} | Max Year: {res['max_year'][0]} | Total Years: {res['unique_years_count'][0]}")
    except Exception as e:
        print(f"Error auditing {name}: {e}")

```

    === TEMPORAL AUDIT FOR EUROSTAT DATASETS ===
    Demography (csv_path)          -> Min Year: 1960 | Max Year: 2026 | Total Years: 67
    Unemployment (csv_path1)       -> Min Year: 2003 | Max Year: 2025 | Total Years: 23
    Gov Debt (csv_path2)           -> Min Year: 2025 | Max Year: 2025 | Total Years: 1
    Poverty (csv_path3)            -> Min Year: 2003 | Max Year: 2020 | Total Years: 18
    Gini Coefficient (csv_path4)   -> Min Year: 2014 | Max Year: 2025 | Total Years: 12
    GDP per Capita (csv_path5)     -> Min Year: 2014 | Max Year: 2025 | Total Years: 12
    Household Income (csv_path6)   -> Min Year: 2014 | Max Year: 2025 | Total Years: 12
    Inflation / HICP (csv_path7)   -> Min Year: 2025 | Max Year: 2025 | Total Years: 1



```python
#As we can see we have a lack of data for Gov Debt, Poverty and inflation, lets search the complete dataset in Eurostat gain
#lets recheck with the new datasets:
csv_path2 = DATA_TABLES / "GovermentGrossDebtV2.csv"
csv_path3 = DATA_TABLES / "PovertyV2.csv"
csv_path7 = DATA_TABLES / "IPC-Inflationv2.csv"
datasets_audit = {
    "Demography (csv_path)": csv_path,
    "Unemployment (csv_path1)": csv_path1,
    "Gov Debt (csv_path2)": csv_path2,
    "Poverty (csv_path3)": csv_path3,
    "Gini Coefficient (csv_path4)": csv_path4,
    "GDP per Capita (csv_path5)": csv_path5,
    "Household Income (csv_path6)": csv_path6,
    "Inflation / HICP (csv_path7)": csv_path7
}

for name, path in datasets_audit.items():
    try:
        # Para el IPC mensual extraemos los primeros 4 caracteres como año
        if "Inflation" in name:
            audit_query = f"""
                SELECT 
                    MIN(SUBSTRING(TIME_PERIOD, 1, 4)) AS min_year, 
                    MAX(SUBSTRING(TIME_PERIOD, 1, 4)) AS max_year,
                    COUNT(DISTINCT SUBSTRING(TIME_PERIOD, 1, 4)) AS unique_years_count
                FROM read_csv_auto('{path}')
            """
        else:
            audit_query = f"""
                SELECT 
                    MIN(TIME_PERIOD) AS min_year, 
                    MAX(TIME_PERIOD) AS max_year,
                    COUNT(DISTINCT TIME_PERIOD) AS unique_years_count
                FROM read_csv_auto('{path}')
            """
        
        res = con.execute(audit_query).df()
        print(f"{name:<30} -> Min Year: {res['min_year'][0]} | Max Year: {res['max_year'][0]} | Total Years: {res['unique_years_count'][0]}")
    except Exception as e:
        print(f"Error auditing {name}: {e}")

```

    Demography (csv_path)          -> Min Year: 1960 | Max Year: 2026 | Total Years: 67
    Unemployment (csv_path1)       -> Min Year: 2003 | Max Year: 2025 | Total Years: 23
    Gov Debt (csv_path2)           -> Min Year: 2014 | Max Year: 2025 | Total Years: 12
    Poverty (csv_path3)            -> Min Year: 2015 | Max Year: 2025 | Total Years: 11
    Gini Coefficient (csv_path4)   -> Min Year: 2014 | Max Year: 2025 | Total Years: 12
    GDP per Capita (csv_path5)     -> Min Year: 2014 | Max Year: 2025 | Total Years: 12
    Household Income (csv_path6)   -> Min Year: 2014 | Max Year: 2025 | Total Years: 12
    Inflation / HICP (csv_path7)   -> Min Year: 2015 | Max Year: 2025 | Total Years: 11



```python
import duckdb

# 1. Create temporary views calculating 10-year variation metrics for ALL datasets
con.execute(f"""
    -- 1. Demography (Relative Variation 2015-2025)
    CREATE OR REPLACE VIEW view_demo AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS DemographyPct_2015_2025
    FROM read_csv_auto('{csv_path}') WHERE TIME_PERIOD IN (2015, 2025) GROUP BY geo;

    -- 2. Unemployment (Relative Variation 2015-2025 for age group Y15-74)
    CREATE OR REPLACE VIEW view_unemp AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS UnemploymentPct_2015_2025
    FROM read_csv_auto('{csv_path1}') WHERE TIME_PERIOD IN (2015, 2025) AND age = 'Y15-74' GROUP BY geo;

    -- 3. Government Debt (RESTORED: Relative Variation 2015-2025 using the new dataset)
    CREATE OR REPLACE VIEW view_debt AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS GovDebtGDPAbsPct_2015_2025
    FROM read_csv_auto('{csv_path2}') WHERE TIME_PERIOD IN (2015, 2025) GROUP BY geo;

    -- 4. Poverty Risk (RESTORED: Relative Variation 2015-2025 using the new dataset)
    CREATE OR REPLACE VIEW view_poverty AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS PovertyPct_2015_2025
    FROM read_csv_auto('{csv_path3}') WHERE TIME_PERIOD IN (2015, 2025) AND unit = 'PC' AND age = 'TOTAL' AND sex = 'T' GROUP BY geo;

    -- 5. Gini Coefficient (Relative Variation 2015-2025)
    CREATE OR REPLACE VIEW view_gini AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS GiniCoefPct_2015_2025
    FROM read_csv_auto('{csv_path4}') WHERE TIME_PERIOD IN (2015, 2025) AND age = 'TOTAL' AND statinfo = 'GINI_HND' GROUP BY geo;

    -- 6. GDP per Capita (Relative Variation 2015-2025)
    CREATE OR REPLACE VIEW view_gdp AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS GDPCapitaPct_2015_2025
    FROM read_csv_auto('{csv_path5}') WHERE TIME_PERIOD IN (2015, 2025) AND ppp_cat18 = 'GDP' AND indic_ppp = 'VI_PPS_EU27_2020_HAB' GROUP BY geo;

    -- 7. Household Income (Relative Variation 2015-2025/2024 using COALESCE)
    CREATE OR REPLACE VIEW view_income AS 
    SELECT geo, ROUND(((COALESCE(MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END), MAX(CASE WHEN TIME_PERIOD = 2024 THEN OBS_VALUE END)) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS DisposableIncomePct_2015_2025
    FROM read_csv_auto('{csv_path6}') WHERE TIME_PERIOD IN (2015, 2024, 2025) AND unit = 'PPS_EU27_2020_HAB' AND na_item = 'B7G' AND sector = 'S14_S15' GROUP BY geo;

    -- 8. Inflation (Net change between 2015 and 2025 annual averages using LIKE for monthly logs)
    CREATE OR REPLACE VIEW view_inflation AS 
    SELECT geo, ROUND(AVG(CASE WHEN TIME_PERIOD LIKE '2025-%' THEN OBS_VALUE END) - AVG(CASE WHEN TIME_PERIOD LIKE '2015-%' THEN OBS_VALUE END), 2) AS InflationPressureChange_2015_2025
    FROM read_csv_auto('{csv_path7}') WHERE (TIME_PERIOD LIKE '2015-%' OR TIME_PERIOD LIKE '2025-%') AND unit = 'RCH_A' AND coicop = 'AP' GROUP BY geo;
""")

con.execute(f"""
    CREATE OR REPLACE VIEW view_eu_info AS 
    SELECT 
        "Código" AS geo,
        "Countries" AS Countries,  
        "Regions" AS Regions,
        "Official language(s)" AS OffiLang,  
        "Regional language(s)" AS RegLang
    FROM read_csv_auto('{csv_path8}');
""")

# 2. Master JOIN combining all homogeneous macroeconomic variations
matriz_macro_final = con.execute("""
    SELECT 
        info.geo,
        info.Countries,
        info.Regions,
        info.OffiLang,                        
        info.RegLang,
        d.DemographyPct_2015_2025,            
        u.UnemploymentPct_2015_2025,          
        deb.GovDebtGDPAbsPct_2015_2025,       -- Successfully restored to 10-year variation pct
        p.PovertyPct_2015_2025,               -- Successfully restored to 10-year variation pct
        g.GiniCoefPct_2015_2025,              
        pib.GDPCapitaPct_2015_2025,           
        i.DisposableIncomePct_2015_2025,      
        inf.InflationPressureChange_2015_2025 
    FROM view_eu_info info
    LEFT JOIN view_demo d      ON info.geo = d.geo
    LEFT JOIN view_unemp u     ON info.geo = u.geo
    LEFT JOIN view_debt deb    ON info.geo = deb.geo
    LEFT JOIN view_poverty p   ON info.geo = p.geo
    LEFT JOIN view_gini g      ON info.geo = g.geo
    LEFT JOIN view_gdp pib     ON info.geo = pib.geo
    LEFT JOIN view_income i    ON info.geo = i.geo
    LEFT JOIN view_inflation inf ON info.geo = inf.geo
    ORDER BY info.Regions, info.geo           
""").df()

print("Homogeneous Macroeconomic Feature Matrix (2015-2025) successfully compiled!")

```

    Homogeneous Macroeconomic Feature Matrix (2015-2025) successfully compiled!



```python
matriz_macro_final.info()
```

    <class 'pandas.DataFrame'>
    RangeIndex: 39 entries, 0 to 38
    Data columns (total 13 columns):
     #   Column                             Non-Null Count  Dtype  
    ---  ------                             --------------  -----  
     0   geo                                39 non-null     str    
     1   Countries                          39 non-null     str    
     2   Regions                            38 non-null     str    
     3   OffiLang                           39 non-null     str    
     4   RegLang                            12 non-null     str    
     5   DemographyPct_2015_2025            34 non-null     float64
     6   UnemploymentPct_2015_2025          29 non-null     float64
     7   GovDebtGDPAbsPct_2015_2025         25 non-null     float64
     8   PovertyPct_2015_2025               27 non-null     float64
     9   GiniCoefPct_2015_2025              27 non-null     float64
     10  GDPCapitaPct_2015_2025             32 non-null     float64
     11  DisposableIncomePct_2015_2025      26 non-null     float64
     12  InflationPressureChange_2015_2025  0 non-null      float64
    dtypes: float64(8), str(5)
    memory usage: 7.9 KB



```python
#We still have NaN values, its because some countries doesnt report his stats
#So often, also some of the columns ID changes between similar tables. lets check the headers
#from the conflictive columns.

print("=== COLUMNS AND FIRST ROWS ===")
print(con.execute(f"SELECT * FROM read_csv_auto('{csv_path7}') LIMIT 3").df().T)


print("\n=== UNIQUE UNITS ===")
print(con.execute(f"SELECT DISTINCT unit FROM read_csv_auto('{csv_path7}') LIMIT 5").df())

print("\n=== UNIQUE COICOP CODES ===")
print(con.execute(f"SELECT DISTINCT coicop FROM read_csv_auto('{csv_path7}') LIMIT 5").df())



```

    === COLUMNS AND FIRST ROWS ===
                                                                                              0  \
    STRUCTURE                                                                          dataflow   
    STRUCTURE_ID                                                       ESTAT:PRC_HICP_MIDX(1.0)   
    STRUCTURE_NAME                                      HICP - monthly data (index) (1996-2025)   
    freq                                                                                      M   
    Time frequency                                                                      Monthly   
    unit                                                                                    I05   
    Unit of measure                                                             Index, 2005=100   
    coicop                                                                                 CP00   
    Classification of individual consumption by pur...                           All-items HICP   
    geo                                                                                      AT   
    Geopolitical entity (reporting)                                                     Austria   
    TIME_PERIOD                                                                         2015-01   
    Time                                                                                   None   
    OBS_VALUE                                                                            119.66   
    Observation value                                                                      None   
    OBS_FLAG                                                                               None   
    Observation status (Flag) V2 structure                                                 None   
    CONF_STATUS                                                                            None   
    Confidentiality status (flag)                                                          None   
    
                                                                                              1  \
    STRUCTURE                                                                          dataflow   
    STRUCTURE_ID                                                       ESTAT:PRC_HICP_MIDX(1.0)   
    STRUCTURE_NAME                                      HICP - monthly data (index) (1996-2025)   
    freq                                                                                      M   
    Time frequency                                                                      Monthly   
    unit                                                                                    I05   
    Unit of measure                                                             Index, 2005=100   
    coicop                                                                                 CP00   
    Classification of individual consumption by pur...                           All-items HICP   
    geo                                                                                      AT   
    Geopolitical entity (reporting)                                                     Austria   
    TIME_PERIOD                                                                         2015-02   
    Time                                                                                   None   
    OBS_VALUE                                                                            119.99   
    Observation value                                                                      None   
    OBS_FLAG                                                                               None   
    Observation status (Flag) V2 structure                                                 None   
    CONF_STATUS                                                                            None   
    Confidentiality status (flag)                                                          None   
    
                                                                                              2  
    STRUCTURE                                                                          dataflow  
    STRUCTURE_ID                                                       ESTAT:PRC_HICP_MIDX(1.0)  
    STRUCTURE_NAME                                      HICP - monthly data (index) (1996-2025)  
    freq                                                                                      M  
    Time frequency                                                                      Monthly  
    unit                                                                                    I05  
    Unit of measure                                                             Index, 2005=100  
    coicop                                                                                 CP00  
    Classification of individual consumption by pur...                           All-items HICP  
    geo                                                                                      AT  
    Geopolitical entity (reporting)                                                     Austria  
    TIME_PERIOD                                                                         2015-03  
    Time                                                                                   None  
    OBS_VALUE                                                                            121.68  
    Observation value                                                                      None  
    OBS_FLAG                                                                               None  
    Observation status (Flag) V2 structure                                                 None  
    CONF_STATUS                                                                            None  
    Confidentiality status (flag)                                                          None  
    
    === UNIQUE UNITS ===
      unit
    0  I05
    1  I15
    2  I96
    
    === UNIQUE COICOP CODES ===
        coicop
    0     CP00
    1     CP01
    2   CP0111
    3    CP011
    4  CP01111



```python
import duckdb
#Part 2.1 Relational Query Execution:
# 1. Re-create temporary views matching the new Index (I05) structure
con.execute(f"""
    CREATE OR REPLACE VIEW view_demo AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS DemographyPct_2015_2025
    FROM read_csv_auto('{csv_path}') WHERE TIME_PERIOD IN (2015, 2025) GROUP BY geo;

    CREATE OR REPLACE VIEW view_unemp AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS UnemploymentPct_2015_2025
    FROM read_csv_auto('{csv_path1}') WHERE TIME_PERIOD IN (2015, 2025) AND age = 'Y15-74' GROUP BY geo;

    CREATE OR REPLACE VIEW view_debt AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS GovDebtGDPAbsPct_2015_2025
    FROM read_csv_auto('{csv_path2}') WHERE TIME_PERIOD IN (2015, 2025) GROUP BY geo;

    CREATE OR REPLACE VIEW view_poverty AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS PovertyPct_2015_2025
    FROM read_csv_auto('{csv_path3}') WHERE TIME_PERIOD IN (2015, 2025) AND unit = 'PC' AND age = 'TOTAL' AND sex = 'T' GROUP BY geo;

    CREATE OR REPLACE VIEW view_gini AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS GiniCoefPct_2015_2025
    FROM read_csv_auto('{csv_path4}') WHERE TIME_PERIOD IN (2015, 2025) AND age = 'TOTAL' AND statinfo = 'GINI_HND' GROUP BY geo;

    CREATE OR REPLACE VIEW view_gdp AS 
    SELECT geo, ROUND(((MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS GDPCapitaPct_2015_2025
    FROM read_csv_auto('{csv_path5}') WHERE TIME_PERIOD IN (2015, 2025) AND ppp_cat18 = 'GDP' AND indic_ppp = 'VI_PPS_EU27_2020_HAB' GROUP BY geo;

    CREATE OR REPLACE VIEW view_income AS 
    SELECT geo, ROUND(((COALESCE(MAX(CASE WHEN TIME_PERIOD = 2025 THEN OBS_VALUE END), MAX(CASE WHEN TIME_PERIOD = 2024 THEN OBS_VALUE END)) - MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) / MAX(CASE WHEN TIME_PERIOD = 2015 THEN OBS_VALUE END)) * 100, 2) AS DisposableIncomePct_2015_2025
    FROM read_csv_auto('{csv_path6}') WHERE TIME_PERIOD IN (2015, 2024, 2025) AND unit = 'PPS_EU27_2020_HAB' AND na_item = 'B7G' AND sector = 'S14_S15' GROUP BY geo;

    -- FIXED INFLATION VIEW: Calculates the 10-year cumulative Inflation Rate (%) using Index Base 2005
    CREATE OR REPLACE VIEW view_inflation AS 
    WITH annual_cpi AS (
        SELECT geo,
               AVG(CASE WHEN TIME_PERIOD LIKE '2015-%' THEN OBS_VALUE END) AS cpi_2015,
               AVG(CASE WHEN TIME_PERIOD LIKE '2025-%' THEN OBS_VALUE END) AS cpi_2025
        FROM read_csv_auto('{csv_path7}')
        WHERE (TIME_PERIOD LIKE '2015-%' OR TIME_PERIOD LIKE '2025-%')
          AND coicop = 'CP00'  -- All-items HICP (Confirmed)
          AND unit = 'I05'     -- Index, 2005=100 (Confirmed)
        GROUP BY geo
    )
    SELECT geo,
           ROUND(((cpi_2025 - cpi_2015) / cpi_2015) * 100, 2) AS InflationPct_2015_2025
    FROM annual_cpi
    WHERE cpi_2015 IS NOT NULL AND cpi_2025 IS NOT NULL;
""")

con.execute(f"""
    CREATE OR REPLACE VIEW view_eu_info AS 
    SELECT "Código" AS geo, "Countries" AS Countries, "Regions" AS Regions, "Official language(s)" AS OffiLang, "Regional language(s)" AS RegLang
    FROM read_csv_auto('{csv_path8}');
""")

# 2. Final JOIN pipeline producing the homogeneous matrix
matriz_macro_finalv2 = con.execute("""
    SELECT 
        info.geo, info.Countries, info.Regions, info.OffiLang, info.RegLang,
        d.DemographyPct_2015_2025,            
        u.UnemploymentPct_2015_2025,          
        deb.GovDebtGDPAbsPct_2015_2025,       
        p.PovertyPct_2015_2025,               
        g.GiniCoefPct_2015_2025,              
        pib.GDPCapitaPct_2015_2025,           
        i.DisposableIncomePct_2015_2025,      
        inf.InflationPct_2015_2025 -- Mapped to the new cumulative inflation percentage column
    FROM view_eu_info info
    LEFT JOIN view_demo d      ON info.geo = d.geo
    LEFT JOIN view_unemp u     ON info.geo = u.geo
    LEFT JOIN view_debt deb    ON info.geo = deb.geo
    LEFT JOIN view_poverty p   ON info.geo = p.geo
    LEFT JOIN view_gini g      ON info.geo = g.geo
    LEFT JOIN view_gdp pib     ON info.geo = pib.geo
    LEFT JOIN view_income i    ON info.geo = i.geo
    LEFT JOIN view_inflation inf ON info.geo = inf.geo
    ORDER BY info.Regions, info.geo           
""").df()

print("Unified homogeneous feature matrix successfully updated!")

```

    Unified homogeneous feature matrix successfully updated!



```python
#Lets delete the old matrix dataframe and check the new one.
del matriz_macro_final
matriz_macro_finalv2.info()
```

    <class 'pandas.DataFrame'>
    RangeIndex: 39 entries, 0 to 38
    Data columns (total 13 columns):
     #   Column                         Non-Null Count  Dtype  
    ---  ------                         --------------  -----  
     0   geo                            39 non-null     str    
     1   Countries                      39 non-null     str    
     2   Regions                        38 non-null     str    
     3   OffiLang                       39 non-null     str    
     4   RegLang                        12 non-null     str    
     5   DemographyPct_2015_2025        34 non-null     float64
     6   UnemploymentPct_2015_2025      29 non-null     float64
     7   GovDebtGDPAbsPct_2015_2025     25 non-null     float64
     8   PovertyPct_2015_2025           27 non-null     float64
     9   GiniCoefPct_2015_2025          27 non-null     float64
     10  GDPCapitaPct_2015_2025         32 non-null     float64
     11  DisposableIncomePct_2015_2025  26 non-null     float64
     12  InflationPct_2015_2025         28 non-null     float64
    dtypes: float64(8), str(5)
    memory usage: 7.9 KB



```python
#As we can see , we still need more data cleaning and preparating, but this will be in
#the final proyect, in order to get an economic reference, linked with EssSurvey dataset.
#Part 2.2: Data extraction and download to our localhost DataBase.
import duckdb
from sqlalchemy import create_engine

# Ensure your master DataFrame from the previous step is updated
# matriz_macro_finalv2 = matriz_macro_final.copy()

# 1. Define the PostgreSQL connection string using SQLAlchemy
connection_string = "postgresql+psycopg2://Practice:12345@localhost:5432/DataScienceCourse"

# 2. Create the SQLAlchemy engine instance
engine = create_engine(connection_string)

print("Connecting to PostgreSQL database...")

try:
    # 3. Upload the DataFrame to a SQL table named 'macro_features_matrix_2015_2025'
    # 'if_exists="replace"' ensures that if the table already exists, it is updated cleanly
    # 'index=False' prevents Pandas from uploading the row numbers as a separate column
    matriz_macro_finalv2.to_sql(
        name='macro_features_matrix_2015_2025', 
        con=engine, 
        if_exists='replace', 
        index=False
    )
    print("Database upload successful! Data transferred from memory to PostgreSQL.")
except Exception as e:
    print(f"Database connection or upload failed: {e}")

```

    Connecting to PostgreSQL database...
    Database upload successful! Data transferred from memory to PostgreSQL.



```python
# 1. Conservas tu DataFrame intacto con tus mayúsculas
matriz_macro_finalv3 = matriz_macro_finalv2.copy()

# 2. TRUCO: Clonamos el DataFrame y pasamos sus columnas a minúsculas solo para SQL
df_to_upload = matriz_macro_finalv2.copy()
df_to_upload.columns = df_to_upload.columns.str.lower()

# 3. Lo subes a PostgreSQL de forma segura
df_to_upload.to_sql(
    name='macro_features_matrix_2015_2025', 
    con=engine, 
    if_exists='replace', 
    index=False
)
print("¡Subido con éxito! Las columnas ahora son seguras para PostgreSQL.")

```

    ¡Subido con éxito! Las columnas ahora son seguras para PostgreSQL.



```python
#We already verify via Tabularies client but lets check the table with a SQL query in the 
#Notebook.

# Load the SQL extension in Jupyter (if not already loaded)
%reload_ext sql

# Establish the interactive connection
%sql postgresql+psycopg2://Practice:12345@localhost:5432/DataScienceCourse

# Query the first 5 records of the newly created production table
%sql SELECT geo, Countries, Regions, DemographyPct_2015_2025, InflationPct_2015_2025 FROM macro_features_matrix_2015_2025 LIMIT 5;


```


<span style="None">Connecting and switching to connection &#x27;postgresql+psycopg2://Practice:***@localhost:5432/DataScienceCourse&#x27;</span>



<span style="None">Running query in &#x27;postgresql+psycopg2://Practice:***@localhost:5432/DataScienceCourse&#x27;</span>



<span style="color: green">5 rows affected.</span>





<table>
    <thead>
        <tr>
            <th>geo</th>
            <th>countries</th>
            <th>regions</th>
            <th>demographypct_2015_2025</th>
            <th>inflationpct_2015_2025</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>AT</td>
            <td>Austria</td>
            <td>'Alpine countries'</td>
            <td>6.52</td>
            <td>39.01</td>
        </tr>
        <tr>
            <td>LI</td>
            <td>Liechtenstein</td>
            <td>'Alpine countries'</td>
            <td>9.5</td>
            <td>None</td>
        </tr>
        <tr>
            <td>SI</td>
            <td>Slovenia</td>
            <td>'Alpine countries' & 'Balkans region' & 'Dinaric Alps' & 'Mediterranean countries'</td>
            <td>3.37</td>
            <td>31.04</td>
        </tr>
        <tr>
            <td>SM</td>
            <td>San Marino</td>
            <td>'Apennine Peninsula (Italian Peninsula)'</td>
            <td>None</td>
            <td>None</td>
        </tr>
        <tr>
            <td>IT</td>
            <td>Italy</td>
            <td>'Apennine Peninsula (Italian Peninsula)' & 'Alpine countries' & 'Mediterranean countries'</td>
            <td>-2.24</td>
            <td>24.28</td>
        </tr>
    </tbody>
</table>


