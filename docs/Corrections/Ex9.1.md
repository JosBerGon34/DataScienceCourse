```python
----------------------------------------------------------------------------------------------
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
----------------------------------------------------------------------------------------------
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

## 2. Consultar directamente a PostgreSQL (vía DuckDB ATTACH)
#df = query_to_df("SELECT * FROM db.EuInfo;")

# 3. Análisis univariable 3-en-1
# ds3on1(df, 'happy', Desc=True, Stat=True, Graph=True)
```

    ✅ Workspace anclado en: /home/josu/Documentos/DataScienceCourse
    📂 Ruta de tablas verificada: /home/josu/Documentos/DataScienceCourse/data/raw/Tables


🟢 < Module 9.1 > Predictive Modeling, Ablation Study & Country-Grouped Cross-Validation (GroupKFold):

##### 🎯 Context & Objectives

In hierarchical socio-economic datasets—where individual survey respondents (ESS) are nested within countries and macroeconomic clusters (Eurostat)—standard random cross-validation (`KFold` or `StratifiedKFold`) violates the independent and identically distributed (**i.i.d.**) assumption. Mixing citizens from the same country across training and validation folds allows models to memorize national baselines ("country leakage"), yielding artificially inflated evaluation scores.

In this module, you will build a leakage-free predictive modeling pipeline using **country-grouped cross-validation (`GroupKFold`)** and execute a controlled **Feature Ablation Study**. By keeping the algorithm and cross-validation splits fixed while varying the input feature blocks (Individual Microdata vs. Macroeconomic Clusters vs. Combined Hybrid), you will scientifically test whether macro-regional economic indicators provide statistically meaningful predictive power on unseen countries.

---

##### 📑 Exercise Instructions

###### 1. Syntactic / Algorithmic Level (Leakage-Free GroupKFold Pipeline)

Create a Python notebook (`notebooks/09_1_predictive_modeling_groupkfold.ipynb`) that implements the following architectural steps:

- **SQL Ingestion & Clean Data Retrieval:**
    - Connect to your local PostgreSQL instance via DuckDB (`src/db.py`) and load the cleaned survey microdata merged with the macroeconomic country features (`cntry`, individual attitudes/demographics, and macro indicators/clusters).
    - Ensure raw rows are used prior to global oversampling so that `GroupKFold` can isolate complete countries (`groups = df['cntry']`) without synthetic cross-border contamination.

- **Inside-the-Fold Asymmetric Preprocessing (`imblearn.pipeline.Pipeline`):**
    - Configure `GroupKFold(n_splits=5)` using `cntry` as the grouping vector.
    - Encapsulate your preprocessing transformations (`StandardScaler`, `PCA(n_components=1)` on institutional trust, and calibrated `SMOTE(random_state=42)` + post-synthesis discrete rounding) **strictly inside each training fold** so that validation folds remain 100% untouched real respondents.

---

###### 2. Applied / Data Level (Controlled Ablation Study & Bayesian Baseline)

Evaluate whether macroeconomic context improves out-of-country generalization compared to individual-level predictors alone:

- **Four-Tier Feature Ablation Experiment:**
    - Train and evaluate the same baseline classifier (e.g., `LogisticRegression` or `HistGradientBoostingClassifier`) across four controlled feature configurations under identical `GroupKFold` splits:
        1. **Tier 0 — Null Baseline (`DummyClassifier`):** Majority-class baseline establishing the random-guess floor.
        2. **Tier 1 — Individual Microdata Only ($X_{\text{micro}}$):** Only respondent-level variables (`lrscale`, `institutional_trust_index`, `n_nonresp`, `has_nonresp`, demographics).
        3. **Tier 2 — Macroeconomic Context Only ($X_{\text{macro}}$):** Only country-level macroeconomic metrics and structural clusters (GDP, inflation, unemployment, economic cluster dummies).
        4. **Tier 3 — Hybrid Model ($X_{\text{micro}} + X_{\text{macro}}$):** Full feature matrix combining individual microdata and macroeconomic context.

- **Probabilistic / Bayesian Comparison & Error Analysis:**
    - Compare your discriminative classifier against a probabilistic Bayesian baseline (`GaussianNB` or Bayesian Logistic Regression) on the Hybrid feature set.
    - Report **ROC-AUC**, **Macro F1-Score**, and **Balanced Accuracy** (mean $\pm$ std across the 5 country folds) in a summary comparison table.
    - **Conceptual Conclusion:** Based on the delta between Tier 1 ($X_{\text{micro}}$) and Tier 3 ($X_{\text{hybrid}}$), state formally whether you reject or fail to reject the null hypothesis ($H_0$) regarding the predictive power of macroeconomic clusters on unseen countries, discussing the role of unobserved individual latent factors.

---

##### 🌐 Official References & Documentation

- **Scikit-Learn GroupKFold:** [GroupKFold Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html)
- **Scikit-Learn Cross-Validation on Grouped Data:** [Group CV Guide](https://scikit-learn.org/stable/modules/cross_validation.html#group-cv)
- **Imbalanced-Learn Pipeline:** [imblearn.pipeline.Pipeline Documentation](https://imbalanced-learn.org/stable/references/generated/imblearn.pipeline.Pipeline.html)

---

##### 📚 Recommended Manuals & CheatSheets

- **Multilevel & Hierarchical Modeling:** *Data Analysis Using Regression and Multilevel/Hierarchical Models (Andrew Gelman & Jennifer Hill)* — Chapter 11–12 (Nested/Clustered Survey Data).
- **Model Evaluation & Ablation:** *Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow (Aurélien Géron)* — Chapter 3 (Classification Metrics: ROC-AUC vs. F1).

💻 **Your Challenge:** Create `notebooks/09_1_predictive_modeling_groupkfold.ipynb` (or `notebooks/Ex9.1.ipynb`), implement the 5-fold `GroupKFold` pipeline with inside-the-fold `SMOTE`, run the 4-tier ablation comparison (`Dummy` vs. `Micro` vs. `Macro` vs. `Hybrid` + `GaussianNB`), and share your cross-validation metrics table to audit the scientific conclusion! 🚀📊


```python
# Step 1: Lets create our study table, we must stratify the sample to not lose or intoxicate the statistics shape.
# We must merge using key value from 'cntry' column of "ess_ex81_smote_split" table, and key values from 'geo' column of "macro_panel" table, just data from 2024, 
# the table of last exercise, has in purpose audit variables as "is_test" and "is_synthetic"
# We must use random seed for determinism results.
import pandas as db
import numpy as np
import pandas as pd
import random


# Extract the stratified samples between "cntry"-"happy_high" values with the macroeconomic clustering.
# We will select 250 samples per combination. Will be enought for this exercise.
df91 = query_to_df("""
    WITH joined_data AS (
        SELECT 
            a.cntry,
            a.lrscale,
            a.institutional_trust_index,
            a.happy_high,
            a.is_test,
            a.is_synthetic,
            b.* EXCLUDE (geo),
            ROW_NUMBER() OVER (
                PARTITION BY a.cntry, a.happy_high
                ORDER BY hash(a.cntry, a.lrscale, a.institutional_trust_index, 42)
            ) AS rn
        FROM db.ess_ex81_smote_split a
        INNER JOIN db.macro_panel b 
            ON a.cntry = b.geo
        WHERE b.year = 2024
    )
    SELECT * EXCLUDE (rn)
    FROM joined_data
    WHERE rn <= 250;
""")

print(f"✅ Stratified Dataset: {df91.shape}")
print(df91.groupby(["cntry", "happy_high"]).size().unstack(fill_value=0))   
```

    ✅ Stratified Dataset: (7391, 13)
    happy_high    0    1
    cntry               
    AT          250  250
    BE          250  250
    DE          250  250
    EE          250  250
    ES          250  250
    FI          250  250
    FR          250  250
    GB          250  250
    HU          250  250
    IE          250  250
    NL          141  250
    NO          250  250
    PL          250  250
    PT          250  250
    SE          250  250



```python
#Lets check how many different values, check the list of unique values, and the frecuency of each one.
print(df91['cntry'].nunique()) 
print(df91['cntry'].unique())         
print(df91['cntry'].value_counts())
```

    15
    <ArrowStringArray>
    ['PL', 'FR', 'IE', 'BE', 'HU', 'NO', 'DE', 'EE', 'FI', 'AT', 'SE', 'PT', 'GB',
     'ES', 'NL']
    Length: 15, dtype: str
    cntry
    PL    500
    FR    500
    IE    500
    BE    500
    HU    500
    NO    500
    DE    500
    EE    500
    FI    500
    AT    500
    SE    500
    PT    500
    GB    500
    ES    500
    NL    391
    Name: count, dtype: int64



```python
----------------------------------------------------------------------------------------------
# Remember that our macroregion and economic clustering doesnt have all european countries, just the most relevant for our study.
# NL"netherlands" has a bit less of representation than the others, just a 22% less, it wont be a problem for our training model.
----------------------------------------------------------------------------------------------
```


```python
# Step 1.2: asymethric preprocessing using "cntry" as group vector.
# Our table/dataframe is ready thanks to the previous exercise with audit variables that indicates us wich rows are train  data and test data, including synthetic rows for the training data.
# Our variable trust index must be tranformed to ordinal discrete variable.
# A lot of regresion/clasification models internaly reduces the dimensionality of variables, passing from  integers to float between 0 and 1(MinMaxScaler)
# Other ones passes the data in to Normal standarization (Standard Scaler, 0 is the mean, negative values are close to the minimum range value, and positive close to maximum, important to take a look
# on outliers to prepare the data before.)
# We can manually do the  transformation.
# After this consideration we have only to create GroupKFolds grouping by cntry and then using StandardScale to give the correct format to data, we can include the factorization of Categorical values.
# Step 1.3, variable transformation "institutional_trust_index", from continuos to discrete ordinal lickert variable.
df91['trust'] = (
    (df91['institutional_trust_index'] - df91['institutional_trust_index'].min())
    / (df91['institutional_trust_index'].max() - df91['institutional_trust_index'].min())
    * 10
).round().clip(0, 10).astype(int)

df91['trust'].describe()


```




    count    7391.000000
    mean        5.146259
    std         2.372112
    min         0.000000
    25%         4.000000
    50%         5.000000
    75%         7.000000
    max        10.000000
    Name: trust, dtype: float64




```python
# ============================================================
# Step 1.4: Split train/test using boolean masks (no pipeline)
# ============================================================
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import MinMaxScaler

feature_cols = ["lrscale", "trust"]
y_col = "happy_high"
group_col = "cntry"

# Boolean masks: test = real rows only (no synthetics)
mask_test  = (df91["is_test"] == 1) & (df91["is_synthetic"] == 0)
mask_train = (df91["is_test"] == 0)

# Extract train (originals + synthetics) and test (real only)
X_train = df91.loc[mask_train, feature_cols].copy()
y_train = df91.loc[mask_train, y_col].copy()
X_test  = df91.loc[mask_test,  feature_cols].copy()
y_test  = df91.loc[mask_test,  y_col].copy()
groups  = df91.loc[mask_train, group_col].copy()

# MinMax 0-10 + round: fit ONLY on train, transform on both
scaler = MinMaxScaler(feature_range=(0, 10))
X_train[feature_cols] = scaler.fit_transform(X_train[feature_cols])
X_test[feature_cols]  = scaler.transform(X_test[feature_cols])

for col in feature_cols:
    X_train[col] = X_train[col].round().clip(0, 10).astype(int)
    X_test[col]  = X_test[col].round().clip(0, 10).astype(int)

print(f"Train: {X_train.shape} | Test: {X_test.shape}")
print(f"Train class balance:\n{y_train.value_counts(normalize=True)}")

# ============================================================
# Step 1.5: Logistic Regression (no pipeline, manual fit/predict)
# ============================================================
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"\nAccuracy (test): {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred, target_names=["happy_low", "happy_high"]))

# ============================================================
# Step 1.6: GroupKFold cross-validation (optional, for variance estimate)
# ============================================================
gkf = GroupKFold(n_splits=5)  # 15 countries / 5 folds = 3 countries per fold
cv_scores = []

for fold, (tr_idx, te_idx) in enumerate(gkf.split(X_train, y_train, groups)):
    X_tr, X_te = X_train.iloc[tr_idx], X_train.iloc[te_idx]  # BUG FIX: use scaled data
    y_tr, y_te = y_train.iloc[tr_idx], y_train.iloc[te_idx]

    m = LogisticRegression(random_state=42)
    m.fit(X_tr, y_tr)
    score = accuracy_score(y_te, m.predict(X_te))
    cv_scores.append(score)
    print(f"  Fold {fold+1}: acc={score:.4f} | test countries={sorted(groups.iloc[te_idx].unique())}")

print(f"\nCV: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")   
```

    Train: (5500, 2) | Test: (1891, 2)
    Train class balance:
    happy_high
    1    0.5
    0    0.5
    Name: proportion, dtype: float64
    
    Accuracy (test): 0.5743
                  precision    recall  f1-score   support
    
       happy_low       0.54      0.63      0.58       891
      happy_high       0.61      0.52      0.56      1000
    
        accuracy                           0.57      1891
       macro avg       0.58      0.58      0.57      1891
    weighted avg       0.58      0.57      0.57      1891
    
      Fold 1: acc=0.5887 | test countries=['BE', 'GB', 'SE']
      Fold 2: acc=0.5890 | test countries=['FI', 'PT']
      Fold 3: acc=0.5470 | test countries=['ES', 'NO']
      Fold 4: acc=0.5800 | test countries=['EE', 'IE']
      Fold 5: acc=0.5890 | test countries=['DE', 'HU']
    
    CV: 0.5787 ± 0.0162


> With only 2 weak predictors (`lrscale`, `trust`), ~58% accuracy is expected.
> The low CV variance (±0.016) confirms stable generalization across country groups.
> Additional macroeconomic features (Module 9.2) will provide incremental signal.   

## Step 2: Implementing imblearn Pipeline

As you can see, the process above dirties our memory and mutates the original DataFrame.
In production environments, this entire process is encapsulated in pipeline functions.
The foundation is `imblearn.pipeline`, but you can also build a custom wrapper
that depends on the specific data transformation needs.

I'll explain why pipelines are used below:

1. **Immutability of the original DataFrame**
   `df91` is never mutated. Each transformation operates on an internal copy within
   the pipeline. The pristine DataFrame remains available at all times for auditing
   or re-execution.

2. **Reproducibility**
   The process consists of a sequence of pure functions:
   `input + spec → output`. If you change the spec, the result changes; otherwise,
   it remains the same. There is no hidden state carried over from previous cells.

3. **Portability**
   The `PipelineOutput` and `DatasetSpec` are serializable (e.g., as JSON or a
   dataclass). The same pipeline can be applied to a different dataset simply by
   updating the spec—no need to rewrite the underlying logic.

4. **Structural prevention of data leakage**
   The `fit`/`transform` operations are applied in the correct order by design—
   `fit` on the training set and `transform` on the test set—rather than relying
   on the programmer's discipline. The pipeline guarantees this.   

In our next document we will implement this method . Starting on step 2(tier 2, tier 3 and bayesian model) of the statement.
[[Ex9.12.ipynb]]
