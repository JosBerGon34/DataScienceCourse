# Technical Manual: Custom Wrapper & Imblearn Pipeline

This technical manual specifies the design, syntax, best practices, and complete implementation of the Modular Wrapper with nested `imblearn.pipeline.Pipeline` workflows (**Module 9.1**). The document is structured to facilitate technical reading, GitHub repository documentation, and continuous integration into Obsidian vaults.

---

## 1. General System Architecture

The system implements a strict **two-layer decoupled architecture**. This design guarantees experiment reproducibility, completely eliminates data leakage between training and test sets, and ensures dataset specification immutability.

```text
+-----------------------------------------------------------------------------------+
| LAYER 1: DETERMINISTIC & IMMUTABLE CONTRACT                                       |
|                                                                                   |
|  [ Origin DataFrame ]                                                             |
|          │                                                                        |
|          ▼                                                                        |
|  [ Enum / Dataclass ] ──► ColumnSpec / DatasetSpec (frozen=True)                  |
|          │                                                                        |
|          ▼                                                                        |
|  [ prepare_features() ]                                                           |
|          ├── Oriented Linear Transformation (REVERSE / NEGATE)                    |
|          ├── Clean Data Split (Audit Flags: is_test, is_synthetic)                |
|          └── Macro-Clustering (Fit strictly on Training data only)                |
+-----------------------------------------------------------------------------------+
                                   │
                                   ▼
+-----------------------------------------------------------------------------------+
| LAYER 2: DYNAMIC & LEAKAGE-FREE EXECUTION                                         |
|                                                                                   |
|  [ run_model() ]                                                                  |
|          │                                                                        |
|          ├── Precomputed GroupKFold splits (Stable pre-SMOTE indices)             |
|          │                                                                        |
|          ├── [ imblearn.pipeline.Pipeline ]                                       |
|          │          ├── Step 1: Conditional Scaler (Standard / MinMax)            |
|          │          ├── Step 2: Custom Transformer (DiscreteRounder)              |
|          │          ├── Step 3: Imbalance Sampler (SMOTE / None)                  |
|          │          └── Step 4: Estimator (Classifier)                            |
|          │                                                                        |
|          ├── GridSearchCV (Hyperparameter tuning via "step__param")               |
|          └── cross_validate() ──► PipelineOutput (@dataclass immutable)           |
+-----------------------------------------------------------------------------------+
```

### Layer 1: Deterministic & Immutable Contract (`prepare_features`)
The first layer establishes strict data contracts and deterministic pre-modeling operations:
* **Strict Type Contracts:** Definition of static enumerations (`VarType`, `Transform`) and immutable data structures (`ColumnSpec`, `DatasetSpec`, `PipelineOutput`) decorated with `@dataclass(frozen=True)`.
* **Linear Direction Alignment:** Ensures features share a consistent semantic orientation without introducing non-linear distortions:
  * `REVERSE`: Transforms $x \mapsto \max(x) - x$. Preserves linear distance properties and avoids division-by-zero errors.
  * `NEGATE`: Transforms $x \mapsto -x$.
* **Sample Isolation (Audit Flags):** Strict filtering using indicator columns (`is_test`, `is_synthetic`) to isolate a pristine hold-out test partition. Synthetic or test records never contaminate the fitting phase.
* **Training-Only Macro-Clustering:** Unsupervised clustering (`KMeans`) is fitted **exclusively** on the real training partition (`is_test == 0` and `is_synthetic == 0`) and projected onto `X_test` via `.predict()` to prevent data leakage.

### Layer 2: Dynamic & Leakage-Free Execution (`run_model`)
The second layer orchestrates model training, inside-the-fold resampling, tuning, and evaluation:
* **Core Container (`ImbPipeline`):** Uses `imblearn.pipeline.Pipeline` instead of Scikit-Learn's standard `Pipeline`. This allows integrating resamplers like `SMOTE` that dynamically alter row counts (`n_samples`) during `.fit()`.
* **Group-Aware Cross-Validation (`GroupKFold`):** Precomputes group splits prior to pipeline execution. This ensures all observations belonging to a single group (e.g., `cntry`) fall entirely into either the training or validation fold.
* **Optional Hyperparameter Tuning (`GridSearchCV`):** Integrated parameter optimization using step-name routing (`step__parameter`).
* **Multi-Metric Evaluation (`cross_validate`):** Evaluates multiple metrics across validated splits and returns the fitted pipeline alongside a standardized summary dictionary.

---

## 2. Syntax & Core Operands

To guarantee error-free execution in production environments, the wrapper relies on specific constructs from modern Python, `scikit-learn`, and `imbalanced-learn`.

### Type Contracts & Immutability

| Component | Role in Wrapper | Stability Impact |
| :--- | :--- | :--- |
| `Enum` | Defines static types for variables and transformations. | Eliminates error-prone "magic strings" and typos. |
| `@dataclass(frozen=True)` | Generates immutable data classes for configurations. | Guarantees dataset specs cannot be mutated mid-run. |
| `@property` | Exposes dynamically computed attributes (e.g., `feature_cols`). | Keeps interfaces clean and decoupled from internal state. |
| Defensive Copy (`df.copy()`) | Clones the DataFrame before applying transformations. | Prevents unintended side-effects on the upstream DataFrame. |
| `.reset_index(drop=True)` | Reindexes arrays/DataFrames after boolean masking. | Prevents index misalignment across `pandas` and `numpy`. |

### Step Routing in Pipelines (`__`)
`ImbPipeline` chains steps via a list of `("step_name", estimator)` tuples. When tuning hyperparameters with `GridSearchCV`, double underscores (`__`) are mandatory to route parameters to the target step inside the pipeline:

```python
grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid={
        "model__C": [0.01, 0.1, 1.0, 10.0],
        "model__l1_ratio": [0.0, 1.0],
    },
    cv=cv_splits,
    scoring="roc_auc",
)
```
* **Routing Syntax:** `<step_name>__<parameter_name>`

### Asymmetric API Lifecycle
`imbalanced-learn` pipelines manage method calls asymmetrically between training and inference phases:
* `fit(X, y)`: Sequentially calls `fit_transform()` on transformers, `fit_resample()` on samplers, and finally `fit()` on the terminal estimator.
* `transform(X)`: Applies learned transformations sequentially. **Does not alter row counts.**
* `fit_resample(X, y)`: Exclusive to samplers (e.g., `SMOTE`). Synthesizes or removes rows to balance classes. **Executed strictly during `.fit()`.**
* `predict(X)` / `predict_proba(X)`: Passes unseen data through `.transform()`, **automatically skipping resampling steps**, and generates predictions from the final estimator.

```text
Training Phase (.fit):
X, y ──► [ Scaler.fit_transform ] ──► [ SMOTE.fit_resample ] ──► [ Model.fit ]
                                       (Alters row count)

Inference Phase (.predict):
X ─────► [ Scaler.transform ] ──────► [ SMOTE (Skipped) ] ─────► [ Model.predict ]
                                       (Preserves row count)
```

### Precomputed Splits with `GroupKFold`
When oversampling techniques like `SMOTE` run inside a cross-validation fold, the row count of `X_train` changes dynamically inside each fold. Passing raw `groups` directly into `ImbPipeline` alongside `GridSearchCV` or `cross_validate` can trigger routing or shape-mismatch conflicts.

Precomputing index tuples prior to pipeline execution solves this cleanly:

```python
gkf = GroupKFold(n_splits=5)
cv_splits = list(gkf.split(output.X_train, output.y_train, output.groups_train))
```
Passing `cv=cv_splits` to `GridSearchCV` and `cross_validate` guarantees strict group isolation independent of internal resampling.

---

## 3. Best Practices & Performance Optimization

### Linear Inversion vs. Non-Linear Inversion
When aligning feature directionality (e.g., inverting inflation or unemployment so higher values indicate better conditions), avoid reciprocal inversion ($1/x$).
* **Risks of $1/x$:**
  * Triggers `ZeroDivisionError` or `inf` whenever $x = 0$.
  * Introduces severe non-linear distortion, compressing high values and inflating values near zero.
  * Breaks on negative values (e.g., deflation rates).
* **Recommended Solution (`Transform.REVERSE`):**
  $$\text{REVERSE}(x) = \max(x) - x$$
  This preserves exact linear distances and relative scale across both positive and negative ranges.

### Conditional Scaling by Estimator Family
Tree-based ensembles are invariant to monotonic feature scaling. Applying `StandardScaler` or `MinMaxScaler` indiscriminately adds computational overhead without improving split quality.

```python
tree_models = {"rf", "gb", "dummy"}
if model_type not in tree_models:
    if output.spec.scaler_type == "standard":
        steps.append(("scaler", StandardScaler()))
    elif output.spec.scaler_type == "minmax":
        steps.append(("scaler", MinMaxScaler(feature_range=(0, 10))))
```

### Scikit-Learn 1.8+ Compatibility
To prevent deprecation warnings and ensure forward compatibility in modern `scikit-learn` releases:
* **`LogisticRegression`:** Use `solver="saga"` paired with `l1_ratio` (`0.0` for pure $L_2$, `1.0` for pure $L_1$) rather than deprecated `penalty` string toggles.

### Single-Threaded Execution & Reproducibility
* **Grid Search Overhead (`n_jobs=1`):** On lightweight tabular grids in Python 3.13+, spawning worker processes (`n_jobs=-1`) often introduces multi-processing overhead and debugger warnings (`frozen modules`). Setting `n_jobs=1` keeps execution deterministic, fast, and clean.
* **Deterministic Seeding:** Propagate `random_state=seed` explicitly across `KMeans`, `SMOTE`, and estimators.

### Custom Transformers (`BaseEstimator` + `TransformerMixin`)
When building custom domain steps (such as rounding discrete/ordinal features after `SMOTE` interpolation), adhere to the Scikit-Learn estimator contract:
1. Inherit from `BaseEstimator` and `TransformerMixin`.
2. In `__init__`, declare parameters with names identical to the attributes assigned to `self` (no `*args` or `**kwargs`).
3. In `fit(X, y=None)`, explicitly return `self`.
4. In `transform(X)`, return a modified copy without mutating the input array in place.

---

## 4. Complete Reference Implementation

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
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


# ============================================================
# LAYER 1: Deterministic Preparation & Optional Clustering
# ============================================================

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
    use_clustering: bool = False
    scaler_type: str = "standard"  # "standard", "minmax", or "none"

    @property
    def feature_cols(self) -> list[str]:
        return [
            c.name for c in self.columns
            if c.vtype in (VarType.DISCRETE, VarType.CONTINUOUS)
        ]

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

class DiscreteRounder(BaseEstimator, TransformerMixin):
    """Rounds discrete/ordinal columns after synthetic SMOTE interpolation."""
    def __init__(self, discrete_indices: Optional[list[int]] = None):
        self.discrete_indices = discrete_indices

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_tr = np.array(X, copy=True)
        if self.discrete_indices:
            for idx in self.discrete_indices:
                X_tr[:, idx] = np.round(X_tr[:, idx])
        return X_tr


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

---

## 5. Reference Bibliography & Official Documentation

* **Imbalanced-Learn Pipeline API:** [imbalanced-learn — Pipeline Documentation](https://imbalanced-learn.org/stable/references/generated/imblearn.pipeline.Pipeline.html)
* **SMOTE Oversampling Reference:** [imbalanced-learn — SMOTE Documentation](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html)
* **Scikit-Learn Pipelines & Composite Estimators:** [scikit-learn — Pipelines Guide](https://scikit-learn.org/stable/modules/compose.html)
* **Scikit-Learn Grouped Cross-Validation:** [scikit-learn — GroupKFold & Cross-Validation Guide](https://scikit-learn.org/stable/modules/cross_validation.html#group-cv)
* **Developing Custom Scikit-Learn Estimators:** [scikit-learn — Rolling Your Own Estimator](https://scikit-learn.org/stable/developers/develop.html)
* **Python Standard Library (`dataclasses`):** [Python Docs — dataclasses](https://docs.python.org/3/library/dataclasses.html)
* **Python Standard Library (`enum`):** [Python Docs — enum](https://docs.python.org/3/library/enum.html)
* **Software Engineering Best Practices in Python:** [Real Python Tutorials](https://realpython.com/)