DataScienceCourse/
├── notebooks/
│   ├── 00_template.ipynb           # Template, for copying and having relative paths functional.
│   ├── 01_limpieza_grupo1.ipynb
│   └── 05_eda_analisis.ipynb
├── src/
│   ├── __init__.py
│   ├── paths.py                    # Pathing Setup script
│   └── descriptive_tools.py        # Script datascience ds3on1, vartype, statsgroup
└── main.py                         # Entry point for the scripts./
        "ROOT": ROOT_DIR,
        "DATA": DATA_DIR,
        "TABLES": TABLES_DIR,
        "PROCESSED": PROCESSED_DATA_DIR

```python
%load_ext autoreload
%autoreload 2

import sys
from pathlib import Path
import os

ROOT_DIR = Path.cwd().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src import setup_workspace, query_to_df, ds3on1

# 1. Inicializar workspace y rutas
paths = setup_workspace()

# 2. Consultar directamente a PostgreSQL (vía DuckDB ATTACH)
#df = query_to_df("SELECT * FROM db.surveys;")

# 3. Análisis univariable 3-en-1
#ds3on1(df, 'happy', Desc=True, Stat=True, Graph=True)
```

    ✅ Workspace anclado en: /home/josu/Documentos/DataScienceCourse
    📂 Ruta de tablas verificada: /home/josu/Documentos/DataScienceCourse/data/raw/Tables


🟢 < Module 8.1 > Feature Engineering, PCA & Calibrated Resampling (SMOTE):
##### 🎯 Context & Objectives

Data cannot be fed into a Machine Learning model exactly as it comes out of an Exploratory Data Analysis. In this module, you will finalize the feature matrix by applying deterministic transformations (replacing any stochastic binning to ensure reproducibility), reducing dimensionality for highly correlated blocks, and preparing the mathematical groundwork for handling imbalanced classes using **SMOTE** (Synthetic Minority Over-sampling Technique). A critical objective is to understand **when** and **how** to apply SMOTE without causing _data leakage_ or generating mathematically impossible synthetic records (like continuous decimals for categorical countries).

##### 📑 Exercise Instructions

###### 1. Syntactic / Algorithmic Level (Feature Engineering & Transformation)

Create a Python notebook (`notebooks/08_1_feature_engineering_resampling.ipynb`) that implements the following steps on your cleaned dataset:

- **Deterministic Thresholding (Fixing Stochastic Binning):**
    
    - Review any custom binning functions you planned to use (e.g., separating `happy` or `lrscale` into binary classes). If you previously used stochastic or weighted random approaches (like a custom `BinarizePond` function), replace them with **strict, deterministic threshold rules** (e.g., `value >= median` or `value >= 7`). Document why introducing randomness when constructing a target variable reduces the theoretical maximum achievable accuracy (Label Noise).
        
- **Dimensionality Reduction (The Institutional Trust Block):**
    
    - In Module 7, you discovered that `trstprl` (trust in parliament) and `trstlgl` (trust in the legal system) are highly correlated (ρ = 0.628).
        
    - Implement **PCA (Principal Component Analysis)** with `n_components=1` (using `sklearn.decomposition.PCA`) on these two variables to create a single `institutional_trust_index`. Briefly compare the explained variance of this component versus calculating a simple arithmetic mean.
        
- **Categorical Encoding:**
    
    - Apply `pd.get_dummies(drop_first=True)` to your nominal variables (e.g., macro-regions) to prevent perfect multicollinearity in linear models, as agreed upon during the EDA phase.
        

###### 2. Applied / Data Level (Calibrated Resampling with SMOTE)

Imbalanced classes require resampling, but executing it at the wrong time ruins the validity of the experiment.

- **The Golden Rule of Resampling:**
    
    - Define a function that accepts `X_train` and `y_train` and applies `imblearn.over_sampling.SMOTE` to balance the target classes.
        
    - **Crucial Conceptual Task:** Explain in your notebook why SMOTE must **never** be applied to the entire dataset before making the validation split. What happens to the test set and the _data leakage_ if you oversample before splitting?
        
- **Auditing Synthetic Generation (The Substrate Bias):**
    
    - Generate a test `X_train_resampled` by applying your SMOTE function.
        
    - Analyze the generated synthetic rows. Since SMOTE interpolates mathematically (calculating Euclidean distances) between neighboring points, what happens to discrete or ordinal variables (like the ISCED educational level or an economic cluster `0, 1, 2`)? Do they become continuous decimals (e.g., `cluster = 1.45`)?
        
    - Apply a post-processing function (iterative rounding) to the synthetic data to force these features back into valid discrete values.
        

##### 🌐 Official References & Documentation

- **Imbalanced-Learn (SMOTE):** [SMOTE Documentation](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html)
    
- **Scikit-Learn PCA:** [PCA Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
    

##### 📚 Recommended Manuals & CheatSheets

- **Handling Imbalanced Datasets:** [SMOTE for Imbalanced Classification with Python](https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/)
    
- **Feature Engineering:** _Feature Engineering for Machine Learning (Alice Zheng & Amanda Casari)_ — Dimensionality Reduction.
    

💻 **Your Challenge:** Create the notebook `notebooks/08_1_feature_engineering_resampling.ipynb`. Implement deterministic binning, extract the institutional trust PCA index, configure the SMOTE function (with rounding logic for ordinal values), and draft the explanation of why SMOTE is strictly a _post-split_ operation. Share your code when ready! 🚀📊



```python
# Step 1: Prepare the dataset with the target variables to work on. (lrscale,happy ,trstprl , trstlgl, cntry)
df81 = query_to_df("SELECT lrscale, happy, trstprl, trstlgl, cntry  FROM db.surveys WHERE COLUMNS (*) IS NOT NULL")
# You can check the function on ./src/db.py
df81.head(6)
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
      <th>lrscale</th>
      <th>happy</th>
      <th>trstprl</th>
      <th>trstlgl</th>
      <th>cntry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3</td>
      <td>7</td>
      <td>2</td>
      <td>2</td>
      <td>GR</td>
    </tr>
    <tr>
      <th>1</th>
      <td>8</td>
      <td>5</td>
      <td>1</td>
      <td>4</td>
      <td>IT</td>
    </tr>
    <tr>
      <th>2</th>
      <td>5</td>
      <td>6</td>
      <td>6</td>
      <td>3</td>
      <td>BE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5</td>
      <td>8</td>
      <td>0</td>
      <td>4</td>
      <td>HU</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3</td>
      <td>6</td>
      <td>1</td>
      <td>3</td>
      <td>GR</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>10</td>
      <td>7</td>
      <td>8</td>
      <td>RS</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Step 1.1, first of all we declare  our functions non respondent values and hot-deck imputation after applying smote on train group, preventing the data leekage on test group.
# Our future model will have to train with the synthetic minority clases train group, assigning properly the variables for avoid data leekage.

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE

# 0. Global reproducibility seed
SEED = 42

# 1. Declare deterministic cleaning & row-level counter function (no randomness)
def clean_and_count(df: pd.DataFrame):
    df = df.copy()
    df["n_nonresp"] = 0
    CODE_GROUPS = [
        [99999, 88888, 77777, 66666],
        [9999,  8888,  7777,  6666],
        [999,   888,   777,   666],
        [99,    88,    77,    66],
    ]
    for col in df.columns:
        if col == "n_nonresp" or not pd.api.types.is_numeric_dtype(df[col]):
            continue
        unique = set(df[col].dropna().unique())
        codes_found = next(([c for c in g if c in unique] for g in CODE_GROUPS if any(c in unique for c in g)), None)
        if codes_found:
            mask = df[col].isin(codes_found)
            df.loc[mask, "n_nonresp"] += 1
            df.loc[mask, col] = np.nan
    df["has_nonresp"] = (df["n_nonresp"] > 0).astype(int)
    return df

# 2. Declare asymmetric Hot-deck imputation using isolated Generator (PCG64)[cite: 7]
def hot_deck_impute_split(X_train: pd.DataFrame, X_test: pd.DataFrame, seed: int = SEED):
    rng = np.random.default_rng(seed)
    X_tr, X_te = X_train.copy(), X_test.copy()
    protected = {"n_nonresp", "has_nonresp"}

    for col in X_tr.columns:
        if col in protected or not pd.api.types.is_numeric_dtype(X_tr[col]):
            continue
        valid_tr = X_tr[col].dropna()
        if valid_tr.empty:
            continue
        weights = valid_tr.value_counts(normalize=True)
        cats, probs = weights.index.to_numpy(), weights.to_numpy()

        mask_tr, mask_te = X_tr[col].isna(), X_te[col].isna()
        if mask_tr.any():
            X_tr.loc[mask_tr, col] = rng.choice(cats, size=int(mask_tr.sum()), p=probs)
        if mask_te.any():
            X_te.loc[mask_te, col] = rng.choice(cats, size=int(mask_te.sum()), p=probs)

    return X_tr, X_te
```


```python
# Step 1.2,After non respondent cleaning, we must create or dummy target variable , in our  case we will create happy_high, every row with happy == 7 or higher will be 1 in this variable,
# also we will delete from the split train/test happy variable to avoid data leekage.
df81c = clean_and_count(df81)
df81c.info()
```

    <class 'pandas.DataFrame'>
    RangeIndex: 37499 entries, 0 to 37498
    Data columns (total 7 columns):
     #   Column       Non-Null Count  Dtype  
    ---  ------       --------------  -----  
     0   lrscale      33057 non-null  float64
     1   happy        37389 non-null  float64
     2   trstprl      36805 non-null  float64
     3   trstlgl      36843 non-null  float64
     4   cntry        37499 non-null  str    
     5   n_nonresp    37499 non-null  int64  
     6   has_nonresp  37499 non-null  int64  
    dtypes: float64(4), int64(2), str(1)
    memory usage: 2.1 MB



```python
# Step 1.2, dummy creation ['happy_high'] (0-1, No-Yes)
df81c['happy_high']=(df81c['happy'] >= 7).astype(int)
df81c['happy_high'].describe()
```




    count    37499.000000
    mean         0.761647
    std          0.426082
    min          0.000000
    25%          1.000000
    50%          1.000000
    75%          1.000000
    max          1.000000
    Name: happy_high, dtype: float64




```python
del df81
```


```python
# Step 1.2, Lets declare the variable groups for a clean split train/test function.

groups= df81c["cntry"]
X= df81c[["lrscale", "trstprl", "trstlgl", "n_nonresp", "has_nonresp"]].copy()
y= df81c["happy_high"].copy()
```


```python
# Step 1.2, before dimensionality reduction and artifically sampled by smote our train group, we will have to hot-deck impute on our X train test  data, filling NAN values
# Group train/test split by country
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups=groups))

X_train, X_test = X.iloc[train_idx].copy(), X.iloc[test_idx].copy()
y_train, y_test = y.iloc[train_idx].copy(), y.iloc[test_idx].copy()

# Anti-leakage Hot-deck imputation (fit weights on X_train, fill both), calling our second function.
X_train_imp, X_test_imp, = hot_deck_impute_split(X_train, X_test, seed=42)
```


```python
# Step 1.3: Apply PCA (Principal Component Analysis) to fuse features that measure
# the same underlying construct (institutional trust) and show strong collinearity
# (e.g., |r| >= 0.7), condensing their shared variance into a single continuous index
# fitted strictly on X_train to prevent data leakage.

# Dimensionality reduction on institutional trust block (fit on train only)
trust_cols = ["trstprl", "trstlgl"]
scaler = StandardScaler()
pca = PCA(n_components=1, random_state=42)

X_train_imp["institutional_trust_index"] = pca.fit_transform(
    scaler.fit_transform(X_train_imp[trust_cols])
)
X_test_imp["institutional_trust_index"] = pca.transform(
    scaler.transform(X_test_imp[trust_cols])
)

print(f"Explained variance by PC1: {pca.explained_variance_ratio_[0]:.2%}")

# Drop raw trust features after combining
X_train_final = X_train_imp.drop(columns=trust_cols)
X_test_final = X_test_imp.drop(columns=trust_cols)

print(X_train_final.head(),'\n', X_test_final.head())
```

    Explained variance by PC1: 81.28%
       lrscale  n_nonresp  has_nonresp  institutional_trust_index
    0      3.0          0            0                  -1.599663
    1      8.0          0            0                  -1.332600
    2      5.0          0            0                  -0.292122
    3      5.0          0            0                  -1.593491
    4      3.0          0            0                  -1.596577 
         lrscale  n_nonresp  has_nonresp  institutional_trust_index
    13     10.0          0            0                   0.238918
    17      5.0          0            0                  -2.649398
    21      9.0          0            0                  -1.338772
    32      5.0          0            0                  -1.599663
    42      3.0          0            0                  -1.599663



```python
# Step 2, generating train data using SMOTE technique, in our case we wont  use any macro region or economic clustering, just calculating euclidian distances
# with our cntry variable.
# Calibrated SMOTE oversampling (strictly on training set)

# 1. Classify numeric cols and cntry group categorical col for SMOTE processing
X_train_numeric = X_train_final.drop(columns=["cntry"], errors="ignore") if "cntry" in X_train_final.columns else X_train_final.copy()
train_countries_orig = X_train_final["cntry"].values if "cntry" in X_train_final.columns else df81c.iloc[train_idx]["cntry"].values

# 2. Apply Smote on numeric cols.
smote = SMOTE(random_state=42)
X_train_res_num, y_train_res = smote.fit_resample(X_train_numeric, y_train)

# 3. Rounding values on discrete vars
discrete_cols = ["lrscale", "n_nonresp", "has_nonresp"]
for col in discrete_cols:
    if col in X_train_res_num.columns:
        X_train_res_num[col] = X_train_res_num[col].round().astype(int)

# 4. Unify train, test tagging the rows wich are train , test and original or synthetic.
n_orig = len(X_train_numeric)
n_total = len(X_train_res_num)
n_synth = n_total - n_orig

df_train_sql = X_train_res_num.copy()
df_train_sql["happy_high"] = y_train_res.values

# Banderas de auditoría independientes
df_train_sql["is_test"] = 0
df_train_sql["is_synthetic"] = ([0] * n_orig) + ([1] * n_synth)

# Inherit the country: the originals preserve their country; Synthetics inherit the country from the first n_orig records (or a neighbor mapping)
# (For synthetic ones you can repeat the country of the base neighbor or assign them the country of origin directly)
synthetic_countries = train_countries_orig[:n_synth] # or a neighbor allocation strategy
df_train_sql["cntry"] = list(train_countries_orig) + list(synthetic_countries)

# 5. Prepare the Test block intact
df_test_sql = X_test_final.drop(columns=["cntry"], errors="ignore") if "cntry" in X_test_final.columns else X_test_final.copy()
df_test_sql["happy_high"] = y_test.values
df_test_sql["is_test"] = 1
df_test_sql["is_synthetic"] = 0
df_test_sql["cntry"] = df81c.iloc[test_idx]["cntry"].values

# 6. Unify in the master table
df_split_master = pd.concat([df_train_sql, df_test_sql], ignore_index=True)
```


```python
# Lets compare our main columns, before and after with easy check of our statistical shape.
# for example in the feature 'lrscale'
print('Before Smote dataframe:',df81c['lrscale'].describe(),'\n','Post Smote dataframe:',df_split_master['lrscale'].describe(),'\n Before Smote dataframe:',df81c.info(),'\n Post Smote dataframe:',df_split_master.info())
```

    <class 'pandas.DataFrame'>
    RangeIndex: 37499 entries, 0 to 37498
    Data columns (total 8 columns):
     #   Column       Non-Null Count  Dtype  
    ---  ------       --------------  -----  
     0   lrscale      33057 non-null  float64
     1   happy        37389 non-null  float64
     2   trstprl      36805 non-null  float64
     3   trstlgl      36843 non-null  float64
     4   cntry        37499 non-null  str    
     5   n_nonresp    37499 non-null  int64  
     6   has_nonresp  37499 non-null  int64  
     7   happy_high   37499 non-null  int64  
    dtypes: float64(4), int64(3), str(1)
    memory usage: 2.4 MB
    <class 'pandas.DataFrame'>
    RangeIndex: 52058 entries, 0 to 52057
    Data columns (total 8 columns):
     #   Column                     Non-Null Count  Dtype  
    ---  ------                     --------------  -----  
     0   lrscale                    52058 non-null  float64
     1   n_nonresp                  52058 non-null  int64  
     2   has_nonresp                52058 non-null  int64  
     3   institutional_trust_index  52058 non-null  float64
     4   happy_high                 52058 non-null  int64  
     5   is_test                    52058 non-null  int64  
     6   is_synthetic               52058 non-null  int64  
     7   cntry                      52058 non-null  str    
    dtypes: float64(2), int64(5), str(1)
    memory usage: 3.3 MB
    Before Smote dataframe: count    33057.000000
    mean         5.063073
    std          2.248181
    min          0.000000
    25%          4.000000
    50%          5.000000
    75%          7.000000
    max         10.000000
    Name: lrscale, dtype: float64 
     Post Smote dataframe: count    52058.000000
    mean         5.007645
    std          2.256915
    min          0.000000
    25%          4.000000
    50%          5.000000
    75%          6.000000
    max         10.000000
    Name: lrscale, dtype: float64 
     Before Smote dataframe: None 
     Post Smote dataframe: None



```python
#Lets prepare the data, converting again the split function(series data) in to dataframe. Making 2 different study blocks, pre Smote and post Smote.
import os
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()
db_uri = (
    f"postgresql+psycopg2://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}"
    f"@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
)
engine = sqlalchemy.create_engine(db_uri)

table_name = "ess_ex81_smote_split"
df_split_master.to_sql(table_name, con=engine, if_exists="replace", index=False)

print(f"✅ Tabla '{table_name}' persistida en PostgreSQL ({len(df_split_master)} filas).")


```

    ✅ Tabla 'ess_ex81_smote_split' persistida en PostgreSQL (52058 filas).



```python
# In conclusion, this asymetric method of sinthetically create more samples of our minority classes, help us to capture better the intervariable relations we need to
# balance our data before applying machine learning. its important to remember that the synth data cant be in our test split, thats why we tagged them with audit variables.
```
