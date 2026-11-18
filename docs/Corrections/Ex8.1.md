```python
-----------------------------------------------------------------------------
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
-----------------------------------------------------------------------------
```


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
# df = query_to_df("SELECT * FROM db.EuInfo;")

# 3. Análisis univariable 3-en-1
# ds3on1(df, 'happy', Desc=True, Stat=True, Graph=True)
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

# 2. Declare asymmetric Hot-deck imputation using isolated Generator (PCG64)
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
trust_cols = ["trstprl", "trstlgl"]

# --- Fit the scaler ONLY ONCE in train ---
scaler = StandardScaler()
X_tr_scaled = scaler.fit_transform(X_train_imp[trust_cols])
X_te_scaled = scaler.transform(X_test_imp[trust_cols])

# --- PCA (fit only in train) ---
pca = PCA(n_components=1, random_state=42)
X_train_imp["institutional_trust_index"] = pca.fit_transform(X_tr_scaled)
X_test_imp["institutional_trust_index"] = pca.transform(X_te_scaled)

# --- Arithmetic mean (same standardized basis) ---
X_train_imp["trust_mean"] = X_tr_scaled.mean(axis=1)
X_test_imp["trust_mean"] = X_te_scaled.mean(axis=1)

# --- Comparison of variance explained ---
var_total = X_tr_scaled.var(axis=0).sum() # ← axis=0 (per column)

var_pca = pca.explained_variance_ratio_[0] * var_total
var_mean = X_tr_scaled.mean(axis=1).var()

print(f"Total block variance: {var_total:.4f}")
print(f"Variance explained by PCA (PC1): {var_pca:.4f} ({var_pca/var_total:.2%})")
print(f"Variance explained by mean: {var_mean:.4f} ({var_mean/var_total:.2%})")
print(f"Difference: PCA captures {(var_pca-var_mean)/var_total:.2%} more than average")

# --- Drop raw features + trust_mean, keep only the PCA index ---
X_train_final = X_train_imp.drop(columns=trust_cols + ["trust_mean"])
X_test_final = X_test_imp.drop(columns=trust_cols + ["trust_mean"])
```

    Total block variance: 2.0000
    Variance explained by PCA (PC1): 1.6256 (81.28%)
    Variance explained by mean: 0.8128 (40.64%)
    Difference: PCA captures 40.64% more than average



```python
-----------------------------------------------------------------------------
# As we can see, our method using PCA1, normalizing with standard scaler for our new variable is way better than doing the mean.
# Also hot-deck helped us to not deviate our statistical shape, it take count about the original distribution.
-----------------------------------------------------------------------------
```


```python
# Step 2: Calibrated SMOTE oversampling (strictly on training set)
# SMOTENC is used, which adapts to these types of datasets: 
# it interpolates numerical features using Euclidean distance 
# and assigns the categorical value (cntry) as the mode of the k nearest neighbors."

from imblearn.over_sampling import SMOTENC

# 1. Re-attach cntry to the features DataFrame (only for SMOTENC)
X_train_with_cntry = X_train_final.copy()
X_train_with_cntry["cntry"] = df81c.iloc[train_idx]["cntry"].values

#2. SMOTENC: cntry is the last column (index -1 or its position)
categorical_idx = list(X_train_with_cntry.columns).index("cntry")
smote_nc = SMOTENC(categorical_features=[categorical_idx], random_state=42)
X_train_res, y_train_res = smote_nc.fit_resample(X_train_with_cntry, y_train)

#3. Rounding of discrete variables
discrete_cols = ["lrscale", "n_nonresp", "has_nonresp"]
for col in discrete_cols:
    if col in X_train_res.columns:
        X_train_res[col] = X_train_res[col].round().astype(int)

# 4. Separate cntry from features (not predictor, only audit)
train_countries_res = X_train_res.pop("cntry") # removes and returns the column

#5. Audit flags
n_orig = len(X_train_final)
n_synth = len(X_train_res) - n_orig

df_train_sql = X_train_res.copy()
df_train_sql["happy_high"] = y_train_res.values
df_train_sql["is_test"] = 0
df_train_sql["is_synthetic"] = ([0] * n_orig) + ([1] * n_synth)
df_train_sql["cntry"] = train_countries_res.values

#6. Test intact
df_test_sql = X_test_final.copy()
df_test_sql["happy_high"] = y_test.values
df_test_sql["is_test"] = 1
df_test_sql["is_synthetic"] = 0
df_test_sql["cntry"] = df81c.iloc[test_idx]["cntry"].values

#7. Unify
df_split_master = pd.concat([df_train_sql, df_test_sql], ignore_index=True)   
```


```python
#Lets check how many NAN values has the cntry variable when is_synthethic is 1.

print("NaN in cntry (synthetic rows):", df_split_master.loc[df_split_master["is_synthetic"] == 1, "cntry"].isna().sum())  
```

    NaN in cntry (synthetic rows): 0



```python
-----------------------------------------------------------------------------
# In conclusion, this asymetric method of sinthetically create more samples of our minority classes, help us to capture better the intervariable relations we need to
# balance our data before applying machine learning. its important to remember that the synth data cant be in our test split, thats why we tagged them with audit variables.
# Now let's store this table in to local sql server.
-----------------------------------------------------------------------------
```


```python
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

```
