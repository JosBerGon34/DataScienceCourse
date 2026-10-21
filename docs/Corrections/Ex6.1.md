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

# 1. Syntactic / Algorithmic Level (Systematic Missing Code Handling):
# A: Explicit Code Mapping (Avoiding Heuristic Pitfalls): We must to create a mask filter to check unique values count of some different columms, and decide wich of those values
# corresponds to missing value codes from ESS.
# We must follow the data missing protocol from https://www.europeansocialsurvey.org/sites/default/files/2023-06/ESS9_data_protocol_e01_4.pdf
# Also a md, with columm variable collection located in ./DataScienceCourse/data/raw/VariablesESS.md
# Our vectorized mask will be done on the read process of duckdb sql, so we will save memory and will be cleaner. for these we need to prepare the query,
# Predefining the filter dictionaries.
# Also we will make our own cluster or group variable from zero.
# Our testing variables are in the next cell:

### -edulvlb — Highest level of education

**Question:** What is the highest level of education you have successfully completed?

**ESS rounds:** ESS5, ESS6, ESS7, ESS8, ESS9, ESS10, ESS10SC, ESS11

#### Code list

| Value | Category |
|-------|----------|
| 0 | Not completed ISCED level 1 |
| 113 | ISCED 1, completed primary education |
| 129 | Vocational ISCED 2C < 2 years, no access ISCED 3 |
| 212 | General/pre-vocational ISCED 2A/2B, access ISCED 3 vocational |
| 213 | General ISCED 2A, access ISCED 3A general/all 3 |
| 221 | Vocational ISCED 2C >= 2 years, no access ISCED 3 |
| 222 | Vocational ISCED 2A/2B, access ISCED 3 vocational |
| 223 | Vocational ISCED 2, access ISCED 3 general/all |
| 229 | Vocational ISCED 3C < 2 years, no access ISCED 5 |
| 311 | General ISCED 3 >=2 years, no access ISCED 5 |
| 312 | General ISCED 3A/3B, access ISCED 5B/lower tier 5A |
| 313 | General ISCED 3A, access upper tier ISCED 5A/all 5 |
| 321 | Vocational ISCED 3C >= 2 years, no access ISCED 5 |
| 322 | Vocational ISCED 3A, access ISCED 5B/lower tier 5A |
| 323 | Vocational ISCED 3A, access upper tier ISCED 5A/all 5 |
| 412 | General ISCED 4A/4B, access ISCED 5B/lower tier 5A |
| 413 | General ISCED 4A, access upper tier ISCED 5A/all 5 |
| 421 | ISCED 4 programmes without access ISCED 5 |
| 422 | Vocational ISCED 4A/4B, access ISCED 5B/lower tier 5A |
| 423 | Vocational ISCED 4A, access upper tier ISCED 5A/all 5 |
| 510 | ISCED 5A short, intermediate/academic/general tertiary below bachelor |
| 520 | ISCED 5B short, advanced vocational qualifications |
| 610 | ISCED 5A medium, bachelor/equivalent from lower tier tertiary |
| 620 | ISCED 5A medium, bachelor/equivalent from upper/single tier tertiary |
| 710 | ISCED 5A long, master/equivalent from lower tier tertiary |
| 720 | ISCED 5A long, master/equivalent from upper/single tier tertiary |
| 800 | ISCED 6, doctoral degree |
| 5555 | Other |
| 7777 | Refusal* |
| 8888 | Don't know* |
| 9999 | No answer* |

\* Missing Value

---

### -emplno — Number of employees respondent has/had

**Question:** How many employees (if any) do/did you have?

**ESS rounds:** ESS1, ESS2, ESS3, ESS4, ESS5, ESS6, ESS7, ESS8, ESS9, ESS10, ESS10SC, ESS11

#### Code list

| Value | Category |
|-------|----------|
| 66666 | Not applicable* |
| 77777 | Refusal* |
| 88888 | Don't know* |
| 99999 | No answer* |

\* Missing Value

---

### -emplrel — Employment relation

**Question:** In your main job are/were you...

**ESS rounds:** ESS1, ESS2, ESS3, ESS4, ESS5, ESS6, ESS7, ESS8, ESS9, ESS10, ESS10SC, ESS11

#### Code list

| Value | Category |
|-------|----------|
| 1 | Employee |
| 2 | Self-employed |
| 3 | Working for own family business |
| 6 | Not applicable* |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value   


```python
# 1. Define filter dictionary and extract it the results via duckdb queries.
import os
import numpy as np
import pandas as pd
import duckdb as db
from dotenv import load_dotenv

load_dotenv()

# Initialize DuckDB connection
con = db.connect()
con.execute("INSTALL postgres; LOAD postgres;")

attach_query = f"""
ATTACH IF NOT EXISTS 'dbname={os.getenv("PGDATABASE")} 
        user={os.getenv("PGUSER")} 
        password={os.getenv("PGPASSWORD")} 
        host={os.getenv("PGHOST")} 
        port={os.getenv("PGPORT")}' 
AS db (TYPE postgres);
"""
con.execute(attach_query)

# A. Register updated DuckDB filters (preserving code 6 as a structural valid category)
con.execute("""
    -- 1-digit macro: preserves code 6 (Not applicable), maps 7, 8, 9 to NULL
    CREATE OR REPLACE MACRO clean_ess_1d(x) AS 
        CASE 
            WHEN x IN (7, 8, 9) THEN NULL 
            ELSE x 
        END;
        
    -- 4-digit macro for education levels
    CREATE OR REPLACE MACRO clean_ess_4d(x) AS 
        CASE WHEN x IN (7777, 8888, 9999) THEN NULL ELSE x END;
        
    -- 5-digit macro for employee counts
    CREATE OR REPLACE MACRO clean_ess_5d(x) AS 
        CASE WHEN x IN (66666, 77777, 88888, 99999) THEN NULL ELSE x END;
""")

# B. Build and execute the query for our variables
query_custom_3vars = """
CREATE OR REPLACE TABLE surveys_sample_3v AS
SELECT 
    s.cntry,
    s.essround,
    s.emplrel AS emplrel_raw,  -- Keep raw emplrel for tracking routing vs missing
    clean_ess_1d(s.emplrel) AS emplrel,  -- Cleaned 1D (code 6 is preserved, 7-9 mapped to NULL)
    clean_ess_4d(s.edulvlb) AS edulvlb,  -- Cleaned 4D
    clean_ess_5d(s.emplno)  AS emplno    -- Cleaned 5D
FROM db.surveys s
WHERE s.cntry IS NOT NULL;
"""
con.execute(query_custom_3vars)

# C. Extract results to Pandas DataFrame
df_sample_3v = con.sql("SELECT * FROM surveys_sample_3v").df()

# D. Feature Engineering: Create 'EmployType' 
# Value 1: Employee (Wage earner)
# Value 2: Self-employed or family business (Self Employers / Businessmen)
# Value 3: Inactive, unemployed, or non-applicable population (Default)
df_sample_3v['EmployType'] = 3  # Set default value first
df_sample_3v.loc[df_sample_3v['emplrel'] == 1, 'EmployType'] = 1
df_sample_3v.loc[df_sample_3v['emplrel'].isin([2, 3]), 'EmployType'] = 2

# E. Structural assignment for emplno: 
# If the respondent is a wage employee (EmployType == 1), 
# their number of employees is structurally 0, not a missing value to impute.
df_sample_3v.loc[df_sample_3v['EmployType'] == 1, 'emplno'] = df_sample_3v['emplno'].fillna(0)

print(f"✅ ¡Sample dataframe successfully processed with proper routing separation!")
print(f"📊 Final dimensions: {df_sample_3v.shape}")
print("\nDistribution of 'EmployType' (1: Employee, 2: Self-employed, 3: Inactive/Not applicable):")
print(df_sample_3v['EmployType'].value_counts(sort=False))

print("\nFirst lines with clean results and new feature:")
print(df_sample_3v[['cntry', 'emplrel', 'EmployType', 'emplno', 'edulvlb']].head(10))
```

    ✅ ¡Sample dataframe successfully processed with proper routing separation!
    📊 Final dimensions: (41702, 7)
    
    Distribution of 'EmployType' (1: Employee, 2: Self-employed, 3: Inactive/Not applicable):
    EmployType
    3     4186
    1    32137
    2     5379
    Name: count, dtype: int64
    
    First lines with clean results and new feature:
      cntry  emplrel  EmployType  emplno  edulvlb
    0    AT        6           3    <NA>      322
    1    AT        1           1       0      423
    2    AT        1           1       0      610
    3    AT        1           1       0      422
    4    AT        1           1       0      322
    5    AT        1           1       0      313
    6    AT        1           1       0      212
    7    AT        1           1       0      720
    8    AT        1           1       0      422
    9    AT        1           1       0      212



```python
# As we can see on the data, the surveys aplies "not applicated, code 66666" to all employed worker.
# Lets make a boolean mask to fill those samples with 0 value.
#D check the percentage of NAN values for every columm:
#E the nan counts from emplrel and emplno decreases when we asume the group with unique value == 6 on emplrel has 0 workers on emplno
print(df_sample_3v.isna().mean().mul(100).round(2).sort_values(ascending=False))
df_sample_3v.info()
```

    emplno         12.05
    emplrel         0.49
    edulvlb         0.35
    emplrel_raw     0.00
    essround        0.00
    cntry           0.00
    EmployType      0.00
    dtype: float64
    <class 'pandas.DataFrame'>
    RangeIndex: 41702 entries, 0 to 41701
    Data columns (total 7 columns):
     #   Column       Non-Null Count  Dtype
    ---  ------       --------------  -----
     0   cntry        41702 non-null  str  
     1   essround     41702 non-null  int64
     2   emplrel_raw  41702 non-null  int64
     3   emplrel      41496 non-null  Int64
     4   edulvlb      41557 non-null  Int64
     5   emplno       36677 non-null  Int64
     6   EmployType   41702 non-null  int64
    dtypes: Int64(3), int64(3), str(1)
    memory usage: 2.4 MB



```python
#2. Applied / Data Level (Grouped vs. Multivariate Imputation)

#A Impute missing values in ordinal survey variables (e.g., trstlgl, stfdem, polintr) using country-level or regional-cluster medians (cntgrp_fc) using Pandas .groupby().transform().
# Multivariate Imputation (IterativeImputer / MICE):
# Utilize sklearn.impute.IterativeImputer (enabling experimental features via from sklearn.experimental import enable_iterative_imputer) to model missing features as a function of other respondent answers.
import numpy as np
import pandas as pd
import duckdb as db

#A.1 Lets load our region-economic table and check the data:
con.execute(attach_query)
df_clusters = con.sql("""SELECT * FROM db.macro_features_matrix_2015_2025""").df()
#Lets verify the data:
print(df_clusters.shape)
print(df_clusters[['geo', 'countries']].head())
print(df_clusters.isna().sum())  # Check where are the nulls.
```

    (39, 13)
      geo      countries
    0  AT        Austria
    1  LI  Liechtenstein
    2  SI       Slovenia
    3  SM     San Marino
    4  IT          Italy
    geo                               0
    countries                         0
    regions                           1
    offilang                          0
    reglang                          27
    demographypct_2015_2025           5
    unemploymentpct_2015_2025        10
    govdebtgdpabspct_2015_2025       14
    povertypct_2015_2025             12
    ginicoefpct_2015_2025            12
    gdpcapitapct_2015_2025            7
    disposableincomepct_2015_2025    13
    inflationpct_2015_2025           11
    dtype: int64



```python
#Lets see wich countries has those NA values on economic columms:

econ_cols = [
    'demographypct_2015_2025', 'unemploymentpct_2015_2025',
    'govdebtgdpabspct_2015_2025', 'povertypct_2015_2025',
    'ginicoefpct_2015_2025', 'gdpcapitapct_2015_2025',
    'disposableincomepct_2015_2025', 'inflationpct_2015_2025'
]
print(f"\nCountries with some Nulls on economic columms:")
print(df_clusters[df_clusters[econ_cols].isna().any(axis=1)][['geo', 'countries']])   

```

    
    Countries with some Nulls on economic columms:
       geo               countries
    1   LI           Liechtenstein
    3   SM              San Marino
    8   IS                 Iceland
    9   MK         North Macedonia
    10  BG                Bulgaria
    12  RS                  Serbia
    14  AL                 Albania
    16  ME              Montenegro
    17  GR                  Greece
    23  UA                 Ukraine
    24  BA  Bosnia and Herzegovina
    27  NO                  Norway
    28  AD                 Andorra
    36  MC                  Monaco
    38  BY                 Belarus



```python
#Lets verify wich countries we must fill null values, according on unique values
#coincidence with our main ESS dataset:
ess_countries = set(df_sample_3v['cntry'])
mask = df_clusters['geo'].isin(ess_countries) & df_clusters[econ_cols].isna().any(axis=1)

print(df_clusters.loc[mask, ['geo', 'countries']]
      .assign(nulls=df_clusters.loc[mask, econ_cols].isna().sum(axis=1)))
```

       geo countries  nulls
    10  BG  Bulgaria      1
    12  RS    Serbia      2
    17  GR    Greece      8
    27  NO    Norway      2



```python
#Now we need to know wich columns are with null values for each coincident country
#unique value:
df_clusters.loc[mask, ['geo', 'countries'] + econ_cols].T   
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>10</th>
      <th>12</th>
      <th>17</th>
      <th>27</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>geo</th>
      <td>BG</td>
      <td>RS</td>
      <td>GR</td>
      <td>NO</td>
    </tr>
    <tr>
      <th>countries</th>
      <td>Bulgaria</td>
      <td>Serbia</td>
      <td>Greece</td>
      <td>Norway</td>
    </tr>
    <tr>
      <th>demographypct_2015_2025</th>
      <td>-8.43</td>
      <td>-7.68</td>
      <td>NaN</td>
      <td>8.11</td>
    </tr>
    <tr>
      <th>unemploymentpct_2015_2025</th>
      <td>-68.25</td>
      <td>-52.28</td>
      <td>NaN</td>
      <td>3.82</td>
    </tr>
    <tr>
      <th>govdebtgdpabspct_2015_2025</th>
      <td>15.44</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>povertypct_2015_2025</th>
      <td>-33.03</td>
      <td>-43.41</td>
      <td>NaN</td>
      <td>9.52</td>
    </tr>
    <tr>
      <th>ginicoefpct_2015_2025</th>
      <td>1.89</td>
      <td>-20.0</td>
      <td>NaN</td>
      <td>-0.84</td>
    </tr>
    <tr>
      <th>gdpcapitapct_2015_2025</th>
      <td>38.78</td>
      <td>30.0</td>
      <td>NaN</td>
      <td>-1.85</td>
    </tr>
    <tr>
      <th>disposableincomepct_2015_2025</th>
      <td>NaN</td>
      <td>72.61</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>inflationpct_2015_2025</th>
      <td>42.5</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>39.14</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Lets use eurostat library to download and update our region-economic table
#filling those null values using a temporary dictionary with columm variables, adapting the values from eurostat to pct on 10 years(2015-2025)
#to ours, the idea is fill maximum of Null values from our main target countries of ESS surveys analisis.
#The rest of them we will use later KMeans to calculate the main 3 economic clusters of Europe Union, then, those
#Null will be fullfilled with the means of the specific cluster.
import eurostat
import pandas as pd
import numpy as np

# ═══════════════════════════════════════════════════════════════════════
# 2.A) Main eurostat function, data extraction on wide(extended on
#  columm cuantity) dataframe format.
# ═══════════════════════════════════════════════════════════════════════
def get_pct_change(dataset, geo, start='2015', end='2025', **filters):
    """
    The data is downloaded thanks to eurostat library,
    the values are download year by year with the next function, the
    main target is calculate pct's via start/end method for every
    related variable  and skip failures if there is no data
    (pct, v_start, v_end, ok).
    ok=False  if the year window is not complete (fallback)
    """
    try:
        all_filters = {'startPeriod': start, 'endPeriod': end, 'geo': geo, **filters}
        df = eurostat.get_data_df(dataset, filter_pars=all_filters)
    except Exception as e:
        print(f"   ❌ {geo}/{dataset}: {type(e).__name__} → keep it NaN")
        return np.nan, np.nan, np.nan, False

    year_cols = sorted([c for c in df.columns if str(c).strip().isdigit()])
    geo_col = [c for c in df.columns if 'geo' in c.lower()][0]
    df = df[df[geo_col] == geo]

    if df.empty:
        return np.nan, np.nan, np.nan, False

    for c in year_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    available = [c for c in year_cols if df[c].notna().any()]
    if not available:
        return np.nan, np.nan, np.nan, False

    start_col = start if start in available else available[0]
    end_col   = end   if end   in available else available[-1]

    if end_col != end:
        print(f"   ⚠️  {geo}/{dataset}: last value {end_col} (no {end}) → keep it NaN")
        return np.nan, np.nan, np.nan, False

    v_start = df[start_col].mean()
    v_end   = df[end_col].mean()

    if pd.isna(v_start) or pd.isna(v_end) or v_start == 0:
        return np.nan, v_start, v_end, False

    return (v_end - v_start) / v_start * 100, v_start, v_end, True


# ═══════════════════════════════════════════════════════════════════════
# 2.A). Df bridge dictionary. Is the place our eurostat function will save
# the formated data.
# ═══════════════════════════════════════════════════════════════════════
todo = [
    # (geo(country code 2digits), dataset, filters, destination column)
    ('BG', 'tec00113',       {'na_item':'B7G', 'sector':'S14_S15', 'unit':'PPS_EU27_2020_HAB'}, 'disposableincomepct_2015_2025'),
    ('EL', 'demo_pjan', {'indic':'PTOT', 'sex':'T', 'age':'TOTAL'}, 'demographypct_2015_2025'),
    ('EL', 'une_rt_a', {'age':'Y15-74', 'sex':'T', 'unit':'PC_ACT'}, 'unemploymentpct_2015_2025'),
    ('EL', 'gov_10dd_edpt1', {'na_item':'GD', 'sector':'S13', 'unit':'PC_GDP'}, 'govdebtgdpabspct_2015_2025'),
    ('EL', 'ilc_peps01n', {'age': 'TOTAL', 'sex': 'T'}, 'povertypct_2015_2025'),
    ('EL', 'ilc_di12', {'age': 'TOTAL', 'indic': 'GINI_HND'}, 'ginicoefpct_2015_2025'),
    ('EL', 'nama_10_pc', {'na_item': 'B1GQ', 'unit': 'CP_EUR_HAB'}, 'gdpcapitapct_2015_2025'),
    ('EL', 'tec00113',  {'na_item':'B7G', 'sector':'S14_S15', 'unit':'PPS_EU27_2020_HAB'}, 'disposableincomepct_2015_2025'),
    ('EL', 'prc_hicp_ainr', {'coicop18': 'AP', 'unit': 'INX_A_AVG'}, 'inflationpct_2015_2025'),         
    ('NO', 'gov_10dd_edpt1', {'na_item':'GD', 'sector':'S13', 'unit':'PC_GDP'},                  'govdebtgdpabspct_2015_2025'),
    ('NO', 'tec00113',       {'na_item':'B7G', 'sector':'S14_S15', 'unit':'PPS_EU27_2020_HAB'},  'disposableincomepct_2015_2025'),
]

# ═══════════════════════════════════════════════════════════════════════
# 2.A) LOOP: execute and prepare the bridge:
# We save the data in a csv with coincidental columm names with our
# original dataset wich must be filled in order to quit Null values.
# ═══════════════════════════════════════════════════════════════════════
bridge_rows = []

for geo, dataset, filters, col in todo:
    pct, v1, v2, ok = get_pct_change(dataset, geo, **filters)
    if ok:
        bridge_rows.append({'geo': geo, 'col': col, 'value': pct,
                            'raw_2015': v1, 'raw_2025': v2})
        print(f"  ✅ {geo} | {col[:25]:25s} | {v1:>10.2f} → {v2:>10.2f} | {pct:+.2f}%")
    else:
        print(f"  ❌ {geo} | {col[:25]:25s} → se deja NaN")

bridge = pd.DataFrame(bridge_rows)
bridge.to_csv('bridge_eurostat.csv', index=False)

# ═══════════════════════════════════════════════════════════════════════
# 2.A). Dumping data to the original
# ═══════════════════════════════════════════════════════════════════════
# Eurostat uses EL referring to Greece, our dataset uses GR.
# Lets change the value with a category dict.
eurostat_to_geo = {'EL': 'GR'}

for _, row in bridge.iterrows():
    geo_target = eurostat_to_geo.get(row['geo'], row['geo'])
    df_clusters.loc[df_clusters['geo'] == geo_target, row['col']] = row['value']

# Check the data dumping.
print("\n✅ Verificación final:")
print(df_clusters[df_clusters['geo'].isin(['BG','GR','NO'])][['geo'] + econ_cols])   
```

       ⚠️  BG/tec00113: last value 2022 (no 2025) → keep it NaN
      ❌ BG | disposableincomepct_2015_ → se deja NaN
      ✅ EL | demographypct_2015_2025   | 10818041.00 → 10372335.00 | -4.12%
      ✅ EL | unemploymentpct_2015_2025 |      25.00 →       8.90 | -64.40%
      ✅ EL | govdebtgdpabspct_2015_202 |     179.60 →     145.40 | -19.04%
      ✅ EL | povertypct_2015_2025      |    1751.20 →    1412.25 | -19.36%
      ✅ EL | ginicoefpct_2015_2025     |      34.20 →      31.60 | -7.60%
      ✅ EL | gdpcapitapct_2015_2025    |   16280.00 →   24080.00 | +47.91%
       ⚠️  EL/tec00113: last value 2024 (no 2025) → keep it NaN
      ❌ EL | disposableincomepct_2015_ → se deja NaN
      ✅ EL | inflationpct_2015_2025    |      85.16 →     100.00 | +17.43%
    faultcode: 150
    faultstring: INVALID_QUERY_DIMENSION_VALUE: Query is invalid as per its structure's definition. The following values for dimension are not allowed: GEO=NO.
       ❌ NO/gov_10dd_edpt1: HTTPError → keep it NaN
      ❌ NO | govdebtgdpabspct_2015_202 → se deja NaN
       ⚠️  NO/tec00113: last value 2022 (no 2025) → keep it NaN
      ❌ NO | disposableincomepct_2015_ → se deja NaN
    
    ✅ Verificación final:
       geo  demographypct_2015_2025  unemploymentpct_2015_2025  \
    10  BG                -8.430000                     -68.25   
    17  GR                -4.120025                     -64.40   
    27  NO                 8.110000                       3.82   
    
        govdebtgdpabspct_2015_2025  povertypct_2015_2025  ginicoefpct_2015_2025  \
    10                   15.440000            -33.030000               1.890000   
    17                  -19.042316            -19.355299              -7.602339   
    27                         NaN              9.520000              -0.840000   
    
        gdpcapitapct_2015_2025  disposableincomepct_2015_2025  \
    10               38.780000                            NaN   
    17               47.911548                            NaN   
    27               -1.850000                            NaN   
    
        inflationpct_2015_2025  
    10               42.500000  
    17               17.426022  
    27               39.140000  



```python
df_clusters.loc[mask, ['geo', 'countries'] + econ_cols].T   
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>10</th>
      <th>12</th>
      <th>17</th>
      <th>27</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>geo</th>
      <td>BG</td>
      <td>RS</td>
      <td>GR</td>
      <td>NO</td>
    </tr>
    <tr>
      <th>countries</th>
      <td>Bulgaria</td>
      <td>Serbia</td>
      <td>Greece</td>
      <td>Norway</td>
    </tr>
    <tr>
      <th>demographypct_2015_2025</th>
      <td>-8.43</td>
      <td>-7.68</td>
      <td>-4.120025</td>
      <td>8.11</td>
    </tr>
    <tr>
      <th>unemploymentpct_2015_2025</th>
      <td>-68.25</td>
      <td>-52.28</td>
      <td>-64.4</td>
      <td>3.82</td>
    </tr>
    <tr>
      <th>govdebtgdpabspct_2015_2025</th>
      <td>15.44</td>
      <td>NaN</td>
      <td>-19.042316</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>povertypct_2015_2025</th>
      <td>-33.03</td>
      <td>-43.41</td>
      <td>-19.355299</td>
      <td>9.52</td>
    </tr>
    <tr>
      <th>ginicoefpct_2015_2025</th>
      <td>1.89</td>
      <td>-20.0</td>
      <td>-7.602339</td>
      <td>-0.84</td>
    </tr>
    <tr>
      <th>gdpcapitapct_2015_2025</th>
      <td>38.78</td>
      <td>30.0</td>
      <td>47.911548</td>
      <td>-1.85</td>
    </tr>
    <tr>
      <th>disposableincomepct_2015_2025</th>
      <td>NaN</td>
      <td>72.61</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>inflationpct_2015_2025</th>
      <td>42.5</td>
      <td>NaN</td>
      <td>17.426022</td>
      <td>39.14</td>
    </tr>
  </tbody>
</table>
</div>




```python
# 2.B) Now that we have established the criteria to build our own country
# cluster groups (geographically, economically, or hybrid) and the
# alternative of using multivariate imputation (MICE / IterativeImputer),
# we have also covered the full spectrum of imputation methods — from the
# simplest (statistical mean, mode, median) to the most accurate and
# complex. It is time to demonstrate their effectiveness on real survey
# data with structured missing patterns.
# ═══════════════════════════════════════════════════════════════════════
# A. Loading data.
# ═══════════════════════════════════════════════════════════════════════
econ_cols = [
    'demographypct_2015_2025', 'unemploymentpct_2015_2025',
    'govdebtgdpabspct_2015_2025', 'povertypct_2015_2025',
    'ginicoefpct_2015_2025', 'gdpcapitapct_2015_2025',
    'disposableincomepct_2015_2025', 'inflationpct_2015_2025'
]
# We just need our country data from ESS. Some of the countries of our economical
# Data set will be omitted
ess_codes = set(df_sample_3v['cntry'])
df_clusters = df_clusters[df_clusters['geo'].isin(ess_codes)].reset_index(drop=True)


```


```python
#2.B 
# ═══════════════════════════════════════════════════════════════════════
# B. Regional Grouping. First region as key.
# To watch it properly, render df_cluster and watch Regions columm.
# This method witll strip the string and will get the firs region as valid.
# ═══════════════════════════════════════════════════════════════════════
df_clusters['region_1'] = df_clusters['regions'].apply(
    lambda x: x.split(" & ")[0].strip("' ") if pd.notna(x) else 'Unassigned')

print("Regiones y países:")
print(df_clusters.groupby('region_1')['geo'].apply(list).to_string())


```

    Regiones y países:
    region_1
    Alpine countries                                      [AT, SI]
    Apennine Peninsula (Italian Peninsula)                    [IT]
    Atlantic Europe                                   [IE, BE, NL]
    Balkans region                            [BG, HU, RS, HR, GR]
    Baltic Rim region                                     [EE, PL]
    Carpathian states                                         [SK]
    Fennoscandian Peninsula                           [FI, SE, NO]
    Iberian Peninsula                                 [FR, PT, ES]
    Jutland Peninsula                                         [DE]



```python
# Regional clustering based on the first geographic label produces 3 groups from a single country and 2 assignment errors (FR→Iberian, DE→Jutland), 
# making regional median imputation unviable for 12.5% of the sample. 
# Economic clustering (KMeans, K=3) solves both problems: all groups have ≥7 countries and cohesion is based on trajectory, not label.
# It will not fullfill all null values also is a bad grouping.
# We could do a generic region clustering instead and also proving
# this criteria will be worse than economic or even with the iterative imputer.
# ═══════════════════════════════════════════════════════════════════════
# B. Regional Grouping.
# ═══════════════════════════════════════════════════════════════════════
standard_region = {
    'AT': 'Western', 'BE': 'Western', 'DE': 'Western', 'FR': 'Western',
    'IE': 'Western', 'NL': 'Western', 'SE': 'Western', 'FI': 'Western',
    'NO': 'Western', 'CH': 'Western', 'GB': 'Western',
    'ES': 'Southern', 'IT': 'Southern', 'PT': 'Southern', 'GR': 'Southern',
    'HR': 'Southern',
    'BG': 'Eastern', 'EE': 'Eastern', 'HU': 'Eastern', 'PL': 'Eastern',
    'RO': 'Eastern', 'SK': 'Eastern', 'SI': 'Eastern',
    'IL': 'Western', 'RS': 'Eastern',
}
#We digitaly put Israel as western(IL), and serbia as Eastern(RS)
df_sample_3v['std_region'] = df_sample_3v['cntry'].map(standard_region)
```


```python
# Prefulfill audit score "df_sample_3v"
# This will be our reference point to watch 
# wich method is better for imputation.
# Lets load our audit statistical function:
def quick_audit(df, cols, label):
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")
    print(df[cols].describe().T[['mean','std','50%','min','max']])
    
    # IQR
    iqr = df[cols].quantile(0.75) - df[cols].quantile(0.25)
    print(f"\nIQR:\n{iqr}")
    
    # Extremes (adapted to our variables)
    for col in cols:
        valid = df[col].dropna()
        if col == 'emplno':
            ext = ((valid == 0).sum() + (valid > 100).sum()) / len(valid) * 100
        elif col == 'emplrel':
            ext = valid.isin([1, 3]).mean() * 100
        else:
            ext = ((valid == 0).sum() + (valid == 800).sum()) / len(valid) * 100
        print(f"  {col}: extremes = {ext:.2f}%")
    
    # NaNs
    print(f"\nNaNs:\n{df[cols].isna().sum()}")

# Pre
imp_cols = ['emplrel', 'edulvlb', 'emplno']
quick_audit(df_sample_3v, imp_cols, "before (pre-fulfill)")
```

    
    ==================================================
      before (pre-fulfill)
    ==================================================
                   mean        std    50%  min     max
    emplrel    1.627603   1.479476    1.0  1.0     6.0
    edulvlb  418.662632  367.11207  322.0  0.0  5555.0
    emplno     0.319492   4.073616    0.0  0.0   400.0
    
    IQR:
    emplrel      0
    edulvlb    297
    emplno       0
    dtype: Int64
      emplrel: extremes = 79.29%
      edulvlb: extremes = 2.04%
      emplno: extremes = 94.63%
    
    NaNs:
    emplrel     206
    edulvlb     145
    emplno     5025
    dtype: int64



```python
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
# ═══════════════════════════════════════════════════════════════════════
# B. Regional Grouping.
# ═══════════════════════════════════════════════════════════════════════
# Now lets fulfill null values and store the data with this criteria in a sample.
# Auditing scores to compare it with the other 2 criterias.
# Also checking the null values still on after imputation.
df_reg = df_sample_3v.copy()
for col in imp_cols:
    df_reg[col] = df_reg[col].fillna(
        df_reg.groupby('std_region')[col].transform('median')
    )
quick_audit(df_reg, imp_cols, "after (std regional clustering)")
print(df_reg[df_reg['std_region'].isna()]['cntry'].value_counts())
df_reg.to_csv(DATA_TABLES/'ex6.1regional.csv')
del df_reg,
```

    
    ==================================================
      after (std regional clustering)
    ==================================================
                   mean         std    50%  min     max
    emplrel    1.624502    1.476473    1.0  1.0     6.0
    edulvlb  418.323294  366.518364  322.0  0.0  5555.0
    emplno     0.280994    3.821719    0.0  0.0   400.0
    
    IQR:
    emplrel      0.0
    edulvlb    297.0
    emplno       0.0
    dtype: Float64
      emplrel: extremes = 79.39%
      edulvlb: extremes = 2.03%
      emplno: extremes = 95.27%
    
    NaNs:
    emplrel    0
    edulvlb    0
    emplno     0
    dtype: int64
    Series([], Name: count, dtype: int64)


The standard regional median imputation does not produce significant distributional distortion. 
The maximum change observed is a 6.2% reduction in the emplno standard deviation, attributable to the injection of modal values (0) into a variable with an extremely biased distribution.
The proportion of extreme responses varies < 1pp in all variables.


```python
# ═══════════════════════════════════════════════════════════════════════
# C. Economic Grouping (KMeans on 10-year trends)
# ═══════════════════════════════════════════════════════════════════════
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

#Lets calculate the node clustering:

X_raw = df_clusters[econ_cols].fillna(df_clusters[econ_cols].median())
X_scaled = StandardScaler().fit_transform(X_raw)
sils = []
for k in range(2, 6):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    sils.append(silhouette_score(X_scaled, labels))

best_k = sils.index(max(sils)) + 2
km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df_clusters['cluster'] = km.fit_predict(X_scaled)

print(f"K = {best_k} (silhouette = {max(sils):.3f})")
print(df_clusters.groupby('cluster')['geo'].apply(list))

# Country maping → cluster
geo_to_cluster = dict(zip(df_clusters['geo'], df_clusters['cluster']))

# Countries without eco data (IL, RS,'GB','CH') → autoassing to closest cluster
geo_to_cluster['IL'] = geo_to_cluster.get('DE', 0)  # ≈ Western
geo_to_cluster['RS'] = geo_to_cluster.get('BG', 1)  # ≈ Eastern
geo_to_cluster['GB'] = geo_to_cluster.get('DE', 4)  # ≈ Western/Northern
geo_to_cluster['CH'] = geo_to_cluster.get('AT', 4)  # ≈ Western/Northern

# Impute
df_eco = df_sample_3v.copy()
df_eco['econ_cluster'] = df_eco['cntry'].map(geo_to_cluster)

for col in imp_cols:
    df_eco[col] = df_eco[col].fillna(
        df_eco.groupby('econ_cluster')[col].transform('median')
    )

quick_audit(df_eco, imp_cols, "after (economic clustering)")
print(df_eco[df_eco['econ_cluster'].isna()]['cntry'].value_counts())
df_eco.to_csv(DATA_TABLES / 'ex6.1economic.csv')
del df_eco
```

    K = 5 (silhouette = 0.262)
    cluster
    0    [SI, IT, IE, BE, NL, SK, PT, ES]
    1                [BG, RS, HR, GR, PL]
    2                                [EE]
    3                                [HU]
    4            [AT, FI, SE, NO, FR, DE]
    Name: geo, dtype: object
    
    ==================================================
      after (economic clustering)
    ==================================================
                   mean         std    50%  min     max
    emplrel    1.624502    1.476473    1.0  1.0     6.0
    edulvlb  418.331927  366.516689  322.0  0.0  5555.0
    emplno     0.280994    3.821719    0.0  0.0   400.0
    
    IQR:
    emplrel      0.0
    edulvlb    297.0
    emplno       0.0
    dtype: Float64
      emplrel: extremes = 79.39%
      edulvlb: extremes = 2.03%
      emplno: extremes = 95.27%
    
    NaNs:
    emplrel    0
    edulvlb    0
    emplno     0
    dtype: int64
    Series([], Name: count, dtype: int64)



```python
# ═══════════════════════════════════════════════════════════════════════
# D. Multivariate IMputation (MICE / IterativeImputer)
# ═══════════════════════════════════════════════════════════════════════
# Now lets use another Imputation feature, MICE.

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

mice_cols = imp_cols + ['EmployType']  # predictive features

df_mice = df_sample_3v.copy()

imp = IterativeImputer(
    max_iter=30,
    random_state=42,
    tol=1e-3,
    sample_posterior=False  # deterministic: predicts the most probable value
)

df_mice[mice_cols] = imp.fit_transform(df_mice[mice_cols])

# Round to integer (they are ordinal/discrete variables)
df_mice[imp_cols] = df_mice[imp_cols].round().astype('Int64')

quick_audit(df_mice, imp_cols, "after (MICE / IterativeImputer)")
print(df_mice[imp_cols].isna().sum())
df_mice.to_csv(DATA_TABLES / 'ex6.1mice.csv')
del df_mice
```

    
    ==================================================
      after (MICE / IterativeImputer)
    ==================================================
                   mean         std    50%  min     max
    emplrel    1.644262    1.494638    1.0  1.0     6.0
    edulvlb  418.558127  366.490495  322.0  0.0  5555.0
    emplno     1.259148    4.633982    0.0  0.0   400.0
    
    IQR:
    emplrel      0.0
    edulvlb    297.0
    emplno       0.0
    dtype: Float64
      emplrel: extremes = 78.90%
      edulvlb: extremes = 2.03%
      emplno: extremes = 83.22%
    
    NaNs:
    emplrel    0
    edulvlb    0
    emplno     0
    dtype: int64
    emplrel    0
    edulvlb    0
    emplno     0
    dtype: int64


IterativeImputer (linear regression, sample_posterior=False) distorts emplno by not modeling the point mass at 0. It is reported as a limitation of the method: multivariate imputation assumes continuous distributions and does not capture discrete structures with high concentration in a modal value. In contexts where all variables are continuous ordinals (trstlgl, stfdem, polintr — scales 0-10), this artifact does not occur
--------------------------------------------------------------------------------
In conclusion, I will not recommend one method over another. 
The appropriate choice depends on the dataset structure, and the distributional audit will reveal it. 
In cases where variables are discrete with high modal concentration (e.g., emplno),
a simple group median is sufficient and robust.
In contexts where all variables are continuous ordinals (e.g., trstlgl, stfdem, polintr — 0–10 scales), multivariate imputation (MICE) can leverage inter-variable correlations without introducing distributional artifacts. 
The audit, not the method name, is the decision criterion.
