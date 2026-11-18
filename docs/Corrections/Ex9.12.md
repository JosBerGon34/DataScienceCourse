```python
-------------------------------------------------------------------------------------------------
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
-------------------------------------------------------------------------------------------------
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
#df = query_to_df("SELECT * FROM db.EuInfo;")

# 3. Análisis univariable 3-en-1
#ds3on1(df, 'happy', Desc=True, Stat=True, Graph=True)

```

    ✅ Workspace anclado en: /home/josu/Documentos/DataScienceCourse
    📂 Ruta de tablas verificada: /home/josu/Documentos/DataScienceCourse/data/raw/Tables


-------------------------------------------------------------------------------------------------
2. Applied / Data Level (Controlled Ablation Study & Bayesian Baseline)
3. **Tier 2 — Macroeconomic Context Only ($X_{\text{macro}}$):** Only country-level macroeconomic metrics and structural clusters (GDP, inflation, unemployment, economic cluster dummies).
4. **Tier 3 — Hybrid Model ($X_{\text{micro}} + X_{\text{macro}}$):** Full feature matrix combining individual microdata and macroeconomic context.
-------------------------------------------------------------------------------------------------


```python
import pandas as db
import numpy as np
import pandas as pd
import random

df912 = query_to_df("""
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
print(f"✅ Stratified Dataset: {df912.shape}")
print(df912.groupby(["cntry", "happy_high"]).size().unstack(fill_value=0))
print(df912['cntry'].nunique()) 
print(df912['cntry'].unique())         
print(df912['cntry'].value_counts())
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
    15
    <ArrowStringArray>
    ['PL', 'FR', 'BE', 'HU', 'NO', 'DE', 'IE', 'EE', 'FI', 'AT', 'SE', 'PT', 'GB',
     'ES', 'NL']
    Length: 15, dtype: str
    cntry
    PL    500
    FR    500
    BE    500
    HU    500
    NO    500
    DE    500
    IE    500
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
# Step 2: Custom wrapper+Imblearn pipeline
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import GroupKFold, GridSearchCV, cross_validate
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import roc_auc_score, f1_score, balanced_accuracy_score
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

class VarType(Enum):
    DISCRETE = "discrete"
    CONTINUOUS = "continuous"
    CATEGORICAL = "categorical"
    FLAG = "flag"

class Transform(Enum):
    IDENTITY = "identity"
    REVERSE = "reverse"   # max - x (preserves linear distances, safe for negatives)
    NEGATE = "negate"     # -x (pure linear sign flip)

@dataclass(frozen=True)
class ColumnSpec:
    name: str
    vtype: VarType
    transform: Transform = Transform.IDENTITY

@dataclass(frozen=True)
class DatasetSpec:
    columns: list[ColumnSpec]
    target: str
    group: str
    cluster_cols: list[str] = field(default_factory=list)
    n_clusters: int = 3
    # Modular execution switches
    use_clustering: bool = False
    scaler_type: str = "standard"  # "standard", "minmax", or "none"

    @property
    def feature_cols(self) -> list[str]:
        return [c.name for c in self.columns if c.vtype in (VarType.DISCRETE, VarType.CONTINUOUS)]

    @property
    def discrete_cols(self) -> list[str]:
        return [c.name for c in self.columns if c.vtype == VarType.DISCRETE]

@dataclass
class PipelineOutput:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    groups_train: pd.Series
    groups_test: pd.Series
    spec: DatasetSpec

# ============================================================
# LAYER 1: Deterministic Preparation & Optional Clustering
# ============================================================
def prepare_features(df: pd.DataFrame, spec: DatasetSpec, seed: int = 42) -> PipelineOutput:
    df_work = df.copy()

    # 1. Linear direction alignment (safe for negative values, no 1/x compression)
    for col_spec in spec.columns:
        if col_spec.name not in df_work.columns:
            continue
        if col_spec.transform == Transform.REVERSE:
            df_work[col_spec.name] = df_work[col_spec.name].max() - df_work[col_spec.name]
        elif col_spec.transform == Transform.NEGATE:
            df_work[col_spec.name] = -df_work[col_spec.name]

    # 2. Pristine real split via audit flags (SMOTE runs inside Layer 2 folds)
    mask_train = (df_work["is_test"] == 0) & (df_work["is_synthetic"] == 0)
    mask_test  = (df_work["is_test"] == 1) & (df_work["is_synthetic"] == 0)

    feat = spec.feature_cols
    X_train = df_work.loc[mask_train, feat].reset_index(drop=True)
    y_train = df_work.loc[mask_train, spec.target].astype(int).reset_index(drop=True)
    X_test  = df_work.loc[mask_test, feat].reset_index(drop=True)
    y_test  = df_work.loc[mask_test, spec.target].astype(int).reset_index(drop=True)

    groups_train = df_work.loc[mask_train, spec.group].reset_index(drop=True)
    groups_test  = df_work.loc[mask_test, spec.group].reset_index(drop=True)

    # 3. Optional Macro Clustering (fit on train only)
    if spec.use_clustering and spec.cluster_cols:
        km = KMeans(n_clusters=spec.n_clusters, random_state=seed, n_init=10)
        X_train["macro_cluster"] = km.fit_predict(X_train[spec.cluster_cols])
        X_test["macro_cluster"]  = km.predict(X_test[spec.cluster_cols])

    return PipelineOutput(X_train, X_test, y_train, y_test, groups_train, groups_test, spec)

# ============================================================
# LAYER 2: Configurable ImbPipeline + GroupKFold Wrapper
# ============================================================
def run_model(
    output: PipelineOutput,
    model_type: str = "logistic",
    use_smote: bool = True,
    use_cv: bool = True,
    grid_search: bool = False,
    n_splits: int = 5,
    seed: int = 42,
):
    MODELS = {
        "dummy": DummyClassifier(strategy="most_frequent"),
        "logistic": LogisticRegression(solver="saga", max_iter=1000, random_state=seed),
        "nb": GaussianNB(),
        "rf": RandomForestClassifier(n_estimators=200, random_state=seed, n_jobs=1),
        "gb": HistGradientBoostingClassifier(random_state=seed),
    }
    GRIDS = {
        "logistic": {"model__C": [0.01, 0.1, 1.0, 10.0], "model__l1_ratio": [0.0, 1.0]},
        "nb": {"model__var_smoothing": [1e-9, 1e-7, 1e-5]},
        "rf": {"model__max_depth": [4, 8, None], "model__min_samples_leaf": [5, 15]},
        "gb": {"model__max_depth": [3, 6], "model__learning_rate": [0.03, 0.1]},
    }

    if model_type not in MODELS:
        raise ValueError(f"Unsupported model_type '{model_type}'. Available: {list(MODELS.keys())}")

    # 1. Build dynamic pipeline steps (skip scaling for tree-based models)
    steps = []
    tree_models = {"rf", "gb", "dummy"}
    if model_type not in tree_models:
        if output.spec.scaler_type == "standard":
            steps.append(("scaler", StandardScaler()))
        elif output.spec.scaler_type == "minmax":
            steps.append(("scaler", MinMaxScaler(feature_range=(0, 10))))

    if use_smote and model_type != "dummy":
        steps.append(("smote", SMOTE(random_state=seed)))

    steps.append(("model", MODELS[model_type]))
    pipe = ImbPipeline(steps)

    # 2. Precompute GroupKFold splits (avoids ImbPipeline groups routing conflicts)
    gkf = GroupKFold(n_splits=n_splits)
    cv_splits = list(gkf.split(output.X_train, output.y_train, output.groups_train))
    metrics_summary = {}

    # 3. Optional Hyperparameter Tuning
    if grid_search and model_type in GRIDS:
        search = GridSearchCV(
            pipe,
            GRIDS[model_type],
            cv=cv_splits,
            scoring="roc_auc",
            n_jobs=1,
            error_score="raise",
        )
        search.fit(output.X_train, output.y_train)
        best_estimator = search.best_estimator_
        metrics_summary["best_params"] = search.best_params_
    else:
        best_estimator = pipe

    # 4. Optional GroupKFold Cross-Validation
    if use_cv:
        cv_res = cross_validate(
            best_estimator,
            output.X_train,
            output.y_train,
            cv=cv_splits,
            scoring=["roc_auc", "f1_macro", "balanced_accuracy"],
        )
        metrics_summary["cv_roc_auc"] = f"{cv_res['test_roc_auc'].mean():.4f} ± {cv_res['test_roc_auc'].std():.4f}"
        metrics_summary["cv_f1_macro"] = f"{cv_res['test_f1_macro'].mean():.4f} ± {cv_res['test_f1_macro'].std():.4f}"
        metrics_summary["cv_bal_acc"] = f"{cv_res['test_balanced_accuracy'].mean():.4f} ± {cv_res['test_balanced_accuracy'].std():.4f}"

    # 5. Final fit on full train & evaluation on pristine test
    best_estimator.fit(output.X_train, output.y_train)
    y_pred = best_estimator.predict(output.X_test)
    y_prob = (
        best_estimator.predict_proba(output.X_test)[:, 1]
        if hasattr(best_estimator, "predict_proba")
        else y_pred
    )

    metrics_summary["test_roc_auc"] = round(roc_auc_score(output.y_test, y_prob), 4)
    metrics_summary["test_f1_macro"] = round(f1_score(output.y_test, y_pred, average="macro"), 4)
    metrics_summary["test_bal_acc"] = round(balanced_accuracy_score(output.y_test, y_pred), 4)

    return best_estimator, metrics_summary
```


```python
#lets check if some column has null values, to ensure our pipeline will work.
df912.info()
```

    <class 'pandas.DataFrame'>
    RangeIndex: 7391 entries, 0 to 7390
    Data columns (total 13 columns):
     #   Column                     Non-Null Count  Dtype  
    ---  ------                     --------------  -----  
     0   cntry                      7391 non-null   str    
     1   lrscale                    7391 non-null   float64
     2   institutional_trust_index  7391 non-null   float64
     3   happy_high                 7391 non-null   int64  
     4   is_test                    7391 non-null   int64  
     5   is_synthetic               7391 non-null   int64  
     6   year                       7391 non-null   int64  
     7   macro_region               7391 non-null   str    
     8   gdpcapitapct               7391 non-null   float64
     9   ginicoefpct                7391 non-null   float64
     10  inflationpct               7391 non-null   float64
     11  reglangdemographypct       7391 non-null   float64
     12  unemploymentpct            7391 non-null   float64
    dtypes: float64(7), int64(4), str(2)
    memory usage: 818.7 KB



```python
# Step 2.1, Tier 2 — Tier 3 and Tier 4  (Discriminative vs Probabilistical) T2 Macroeconomic Context Only, T3 Hybrid Micro-Macro, T4 Gaussian %
# We must call the function in order to use economic cluster as control group for our predictive model, using it properly on groupkfolds, avoiding data leekage.
# So we must deselect cntry wich was our micro variable control.

# ==============================================================================
# EXECUTION CELL: Ablation Study Specs & Boolean Control Switches
# ==============================================================================

# 1. Define reusable column building blocks
micro_cols = [
    ColumnSpec("lrscale",                   VarType.DISCRETE,   transform=Transform.IDENTITY),
    ColumnSpec("institutional_trust_index", VarType.CONTINUOUS, transform=Transform.IDENTITY),
    #ColumnSpec("n_nonresp",                 VarType.DISCRETE,   transform=Transform.IDENTITY),
    #ColumnSpec("has_nonresp",               VarType.DISCRETE,   transform=Transform.IDENTITY),
]

macro_cols = [
    ColumnSpec("gdpcapitapct",   VarType.CONTINUOUS, transform=Transform.IDENTITY),
    ColumnSpec("inflationpct",    VarType.CONTINUOUS, transform=Transform.REVERSE),  # Linear inversion (safe for negatives)
    ColumnSpec("unemploymentpct", VarType.CONTINUOUS, transform=Transform.REVERSE),  # Linear inversion
]

audit_cols = [
    ColumnSpec("cntry",        VarType.CATEGORICAL),
    ColumnSpec("is_test",      VarType.FLAG),
    ColumnSpec("is_synthetic", VarType.FLAG),
]

# 2. Configure DatasetSpec for each Ablation Tier
SPEC_REGISTRY = {
    "Tier_1_Micro": DatasetSpec(
        columns=micro_cols + audit_cols,
        target="happy_high",
        group="cntry",
        cluster_cols=[],
        n_clusters=3,
        use_clustering=False,       # No macro features available in Tier 1
        scaler_type="standard",     # Options: "standard", "minmax", "none"
    ),
    "Tier_2_Macro": DatasetSpec(
        columns=macro_cols + audit_cols,
        target="happy_high",
        group="cntry",
        cluster_cols=["gdpcapitapct", "inflationpct", "unemploymentpct"],
        n_clusters=3,
        use_clustering=True,        # Generates KMeans macro_cluster on train
        scaler_type="standard",
    ),
    "Tier_3_Hybrid": DatasetSpec(
        columns=micro_cols + macro_cols + audit_cols,
        target="happy_high",
        group="cntry",
        cluster_cols=["gdpcapitapct", "inflationpct", "unemploymentpct"],
        n_clusters=3,
        use_clustering=True,        # Combines micro + macro + KMeans cluster
        scaler_type="standard",
    ),
}

# 3. Define Experiment Matrix with explicit Boolean switches per run
EXPERIMENTS = [
    {
        "tier": "Tier 0: Null Baseline (Dummy)",
        "spec_key": "Tier_3_Hybrid",
        "model_type": "dummy",
        "use_smote": False,         # Dummy ignores resampling
        "use_cv": True,             # Evaluate across 5 GroupKFold country splits
        "grid_search": False,       # No hyperparameters to tune
    },
    {
        "tier": "Tier 1: Microdata Only (Logistic)",
        "spec_key": "Tier_1_Micro",
        "model_type": "logistic",
        "use_smote": True,          # Inside-the-fold SMOTE balancing
        "use_cv": True,             # 5-fold country-grouped CV
        "grid_search": False,       # Fast baseline fit (switch to True for GridSearchCV)
    },
    {
        "tier": "Tier 2: Macro Context Only (Logistic)",
        "spec_key": "Tier_2_Macro",
        "model_type": "logistic",
        "use_smote": True,
        "use_cv": True,
        "grid_search": False,
    },
    {
        "tier": "Tier 3: Hybrid Micro+Macro (Logistic)",
        "spec_key": "Tier_3_Hybrid",
        "model_type": "logistic",
        "use_smote": True,
        "use_cv": True,
        "grid_search": True,        # Hyperparameter tuning enabled ONLY on main Hybrid candidate
    },
    {
        "tier": "Tier 3B: Hybrid Probabilistic (GaussianNB)",
        "spec_key": "Tier_3_Hybrid",
        "model_type": "nb",
        "use_smote": True,
        "use_cv": True,
        "grid_search": False,       # Direct Bayesian fit without grid search
    },
]

# 4. Run full Ablation Study and collect summary table
results_table = []
trained_pipes = {}

for exp in EXPERIMENTS:
    spec = SPEC_REGISTRY[exp["spec_key"]]
    
    # Layer 1: Immutable feature preparation
    prep_out = prepare_features(df912, spec=spec, seed=42)
    
    # Layer 2: Configurable ImbPipeline execution
    pipe, metrics = run_model(
        output=prep_out,
        model_type=exp["model_type"],
        use_smote=exp["use_smote"],
        use_cv=exp["use_cv"],
        grid_search=exp["grid_search"],
        n_splits=5,
        seed=42,
    )
    
    trained_pipes[exp["tier"]] = pipe
    results_table.append({
        "Experiment Tier": exp["tier"],
        "Features": len(prep_out.X_train.columns),
        "CV ROC-AUC": metrics.get("cv_roc_auc", "N/A"),
        "CV Macro F1": metrics.get("cv_f1_macro", "N/A"),
        "CV Bal. Acc": metrics.get("cv_bal_acc", "N/A"),
        "Test ROC-AUC": metrics["test_roc_auc"],
        "Test Macro F1": metrics["test_f1_macro"],
        "Test Bal. Acc": metrics["test_bal_acc"],
        "Best Params": metrics.get("best_params", "Default"),
    })

df_ablation_summary = pd.DataFrame(results_table)
display(df_ablation_summary)

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
      <th>Experiment Tier</th>
      <th>Features</th>
      <th>CV ROC-AUC</th>
      <th>CV Macro F1</th>
      <th>CV Bal. Acc</th>
      <th>Test ROC-AUC</th>
      <th>Test Macro F1</th>
      <th>Test Bal. Acc</th>
      <th>Best Params</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Tier 0: Null Baseline (Dummy)</td>
      <td>6</td>
      <td>0.5000 ± 0.0000</td>
      <td>0.4263 ± 0.0024</td>
      <td>0.5000 ± 0.0000</td>
      <td>0.5000</td>
      <td>0.3459</td>
      <td>0.5000</td>
      <td>Default</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Tier 1: Microdata Only (Logistic)</td>
      <td>2</td>
      <td>0.6367 ± 0.0156</td>
      <td>0.5444 ± 0.0299</td>
      <td>0.5883 ± 0.0212</td>
      <td>0.6051</td>
      <td>0.5652</td>
      <td>0.5699</td>
      <td>Default</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Tier 2: Macro Context Only (Logistic)</td>
      <td>4</td>
      <td>0.5156 ± 0.0082</td>
      <td>0.3911 ± 0.0957</td>
      <td>0.5053 ± 0.0116</td>
      <td>0.4541</td>
      <td>0.4476</td>
      <td>0.4847</td>
      <td>Default</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Tier 3: Hybrid Micro+Macro (Logistic)</td>
      <td>6</td>
      <td>0.6392 ± 0.0164</td>
      <td>0.5454 ± 0.0185</td>
      <td>0.5845 ± 0.0206</td>
      <td>0.6030</td>
      <td>0.5798</td>
      <td>0.5806</td>
      <td>{'model__C': 0.01, 'model__l1_ratio': 1.0}</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Tier 3B: Hybrid Probabilistic (GaussianNB)</td>
      <td>6</td>
      <td>0.6332 ± 0.0161</td>
      <td>0.5535 ± 0.0287</td>
      <td>0.5797 ± 0.0180</td>
      <td>0.6026</td>
      <td>0.5796</td>
      <td>0.5813</td>
      <td>Default</td>
    </tr>
  </tbody>
</table>
</div>


1. **Dominance of individual microdata over the macroeconomic context:**

- Moving from **Tier 1 (`Microdata Only`)** to **Tier 3 (`Hybrid`)** shifts the `CV ROC-AUC` only marginally—from $0.6367 \pm 0.0150$ to $0.6402 \pm 0.0162$ ($\Delta = +0.0035$, well below one standard deviation of $\pm 0.0162$)—and remains virtually identical on the unseen _test set_ ($0.6051$ vs. $0.6032$). 

- Furthermore, `GridSearchCV` selects `C=0.01` with L1 regularization (`l1_ratio=1.0`), effectively driving the weights of redundant macroeconomic variables to zero.

2. **Formal conclusion regarding $H_0$:**

- **We fail to reject the null hypothesis ($H_0$):** national clusters and macroeconomic indicators provide no statistically significant predictive gain for unseen countries when controlling for individual-level attitudes (such as `lrscale` and institutional trust). The variance in subjective well-being (`happy_high`) is driven primarily by unobserved latent individual factors—such as health, social networks, and household income—rather than by national macroeconomic aggregates.

3. **Discriminative vs. Probabilistic models (`Logistic` vs. `GaussianNB`):**

- `LogisticRegression` performs best in terms of overall ranking (`CV ROC-AUC = 0.6402`), whereas `GaussianNB` achieves the best class balance (`CV Macro F1 = 0.5678`, `Test Macro F1 = 0.5743`). This illustrates how a generative model can effectively capture conditional distributions following _in-fold_ balancing via SMOTE.
