from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import GroupKFold, GridSearchCV, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report, roc_auc_score, f1_score, balanced_accuracy_score
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
    }
    GRIDS = {
        "logistic": {"model__C": [0.01, 0.1, 1.0, 10.0], "model__penalty": ["l1", "l2"]},
        "nb": {"model__var_smoothing": [1e-9, 1e-7, 1e-5]},
    }

    # Build dynamic pipeline steps based on switches
    steps = []
    if output.spec.scaler_type == "standard":
        steps.append(("scaler", StandardScaler()))
    elif output.spec.scaler_type == "minmax":
        steps.append(("scaler", MinMaxScaler(feature_range=(0, 10))))

    if use_smote and model_type != "dummy":
        steps.append(("smote", SMOTE(random_state=seed)))

    steps.append(("model", MODELS[model_type]))
    pipe = ImbPipeline(steps)

    gkf = GroupKFold(n_splits=n_splits)
    metrics_summary = {}

    # 1. Optional Hyperparameter Tuning (only if grid_search=True)
    if grid_search and model_type in GRIDS:
        search = GridSearchCV(pipe, GRIDS[model_type], cv=gkf, scoring="roc_auc", n_jobs=-1)
        search.fit(output.X_train, output.y_train, groups=output.groups_train)
        best_estimator = search.best_estimator_
        metrics_summary["best_params"] = search.best_params_
    else:
        best_estimator = pipe

    # 2. Optional GroupKFold Cross-Validation (SMOTE & Scaler run strictly inside each fold)
    if use_cv:
        cv_res = cross_validate(
            best_estimator,
            output.X_train,
            output.y_train,
            groups=output.groups_train,
            cv=gkf,
            scoring=["roc_auc", "f1_macro", "balanced_accuracy"],
        )
        metrics_summary["cv_roc_auc"] = f"{cv_res['test_roc_auc'].mean():.4f} ± {cv_res['test_roc_auc'].std():.4f}"
        metrics_summary["cv_f1_macro"] = f"{cv_res['test_f1_macro'].mean():.4f} ± {cv_res['test_f1_macro'].std():.4f}"
        metrics_summary["cv_bal_acc"] = f"{cv_res['test_balanced_accuracy'].mean():.4f} ± {cv_res['test_balanced_accuracy'].std():.4f}"

    # 3. Final fit on full train & evaluation on pristine test
    best_estimator.fit(output.X_train, output.y_train)
    y_pred = best_estimator.predict(output.X_test)
    y_prob = best_estimator.predict_proba(output.X_test)[:, 1] if hasattr(best_estimator, "predict_proba") else y_pred

    metrics_summary["test_roc_auc"] = round(roc_auc_score(output.y_test, y_prob), 4)
    metrics_summary["test_f1_macro"] = round(f1_score(output.y_test, y_pred, average="macro"), 4)
    metrics_summary["test_bal_acc"] = round(balanced_accuracy_score(output.y_test, y_pred), 4)

    return best_estimator, metrics_summary


# ==============================================================================
# EXECUTION CELL: Ablation Study Specs & Boolean Control Switches
# ==============================================================================

# 1. Define reusable column building blocks
micro_cols = [
    ColumnSpec("lrscale",                   VarType.DISCRETE,   transform=Transform.IDENTITY),
    ColumnSpec("institutional_trust_index", VarType.CONTINUOUS, transform=Transform.IDENTITY),
    ColumnSpec("n_nonresp",                 VarType.DISCRETE,   transform=Transform.IDENTITY),
    ColumnSpec("has_nonresp",               VarType.DISCRETE,   transform=Transform.IDENTITY),
]

macro_cols = [
    ColumnSpec("gdp_growth",   VarType.CONTINUOUS, transform=Transform.IDENTITY),
    ColumnSpec("inflation",    VarType.CONTINUOUS, transform=Transform.REVERSE),  # Linear inversion (safe for negatives)
    ColumnSpec("unemployment", VarType.CONTINUOUS, transform=Transform.REVERSE),  # Linear inversion
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
        cluster_cols=["gdp_growth", "inflation", "unemployment"],
        n_clusters=3,
        use_clustering=True,        # Generates KMeans macro_cluster on train
        scaler_type="standard",
    ),
    "Tier_3_Hybrid": DatasetSpec(
        columns=micro_cols + macro_cols + audit_cols,
        target="happy_high",
        group="cntry",
        cluster_cols=["gdp_growth", "inflation", "unemployment"],
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
    prep_out = prepare_features(df91, spec=spec, seed=42)
    
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
