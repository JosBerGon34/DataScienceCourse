
**A Domain-Agnostic Practical & Conceptual Guide**

This document is a multi-purpose reference independent of any specific domain (surveys, clinical data, user logs, sensor data, etc.). Use it whenever observations are nested inside natural groups or clusters and you need a rigorous, leakage-free evaluation of predictive generalization.

---

## 1. The Core Problem: Violation of the i.i.d. Assumption

Standard cross-validation (`KFold`, `StratifiedKFold`) assumes that all rows in a dataset are **independent and identically distributed (i.i.d.)**.

When observations are nested inside higher-level groups (citizens within countries, patients within hospitals, measurements from the same device), this assumption breaks:
* **Shared Unobserved Variance:** Observations within the same group share contextual information (group effect / random effect).
* **Group Leakage:** If records from the same group appear in both training and validation splits, the model memorizes the group's signature rather than learning generalizable patterns.
* **Result:** Artificially inflated validation scores that collapse when deployed on new, unseen groups.

> **Golden Rule:** All records belonging to the same group must go **entirely** into the training fold or **entirely** into the validation/test fold.

---

## 2. `GroupKFold` — Mechanics and Basic Usage

`GroupKFold` is a deterministic cross-validation splitter that partitions the dataset into $k$ folds while keeping group boundaries intact.

```python
from sklearn.model_selection import GroupKFold

gkf = GroupKFold(n_splits=5)

for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups=groups)):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
    # All preprocessing and model training happen strictly inside this loop

```

### Core Components Explained

- **`groups` vector:** A 1D array or Series of the exact same length as `X` containing the group identifier for each row (e.g., country code, hospital ID). It is used **only** by the splitter to assign rows to folds and must **never** be included as a feature inside `X`.
    
- **`n_splits` constraint:** The number of splits ($k$) cannot exceed the total number of unique groups in `groups`.
    
- **`gkf.split(...)` generator:** Yields pairs of positional integer indices `(train_idx, val_idx)` rather than sliced DataFrames, allowing clean indexing via `.iloc[]`.
    

### Related Grouped Splitters

- **`GroupShuffleSplit`:** Performs randomized group-aware train/test splits (ideal for creating a final hold-out test set of unseen groups).
    
- **`LeaveOneGroupOut` (LOGO):** Sets $k$ equal to the number of unique groups, holding out one complete group per iteration (best when the total number of groups is small).
    
- **`StratifiedGroupKFold`:** Attempts to preserve target class proportions across folds while still respecting indivisible group boundaries.
    

## 3. Core API Mechanics: `fit`, `transform`, `fit_resample` & `predict`

To prevent **data leakage**, you must understand the strict separation between **learning parameters from data** and **applying learned rules to data**. Every Scikit-Learn and Imbalanced-Learn object relies on four foundational methods:

### 3.1 `fit(X_train, y_train=None)` — _The Learning Phase_

- **What it does:** Inspects **only** the training data to compute and store internal mathematical parameters (attributes ending with an underscore, such as `mean_`, `scale_`, `components_`, or `coef_`).
    
- **Crucial detail:** Calling `.fit()` **does not modify** `X_train`; it only learns the rules.
    
- **Leakage rule:** `.fit()` must **never** be called on validation or test data.
    

### 3.2 `transform(X)` — _The Application Phase_

- **What it does:** Takes any dataset (`X_train`, `X_val`, or `X_test`) and applies the exact mathematical transformation using the parameters **already stored** during `.fit()`.
    
- **Example:** If a scaler learned $\mu = 50$ and $\sigma = 10$ on `X_train`, calling `scaler.transform(X_val)` subtracts $50$ and divides by $10$ on `X_val`—it **never** recalculates the mean or standard deviation of `X_val`.
    

### 3.3 `fit_transform(X_train, y_train=None)` — _Shortcut for Train Only_

- **What it does:** Combines `.fit(X_train)` followed immediately by `.transform(X_train)` in a single optimized step.
    
- **Leakage rule:** Valid **exclusively** on the training fold. Calling `fit_transform()` on validation or test sets is a textbook data leakage bug.
    

### 3.4 `fit_resample(X_train, y_train)` — _Training-Only Row Synthesis_

- **What it does:** Exclusive to `imbalanced-learn` samplers (like `SMOTE`, `SMOTENC`, or `RandomUnderSampler`). It inspects class distributions in `y_train` and generates or removes rows to balance the training set.
    
- **Leakage rule:** Resampling changes the number of rows and creates synthetic observations. It must **never** be applied to validation or test sets, which must remain 100% real and unresampled.
    

### 3.5 `predict(X)` vs. `predict_proba(X)` — _Inference Phase_

- **`predict(X)`:** Applies the trained decision boundary (default threshold $0.50$ in binary classification) and outputs hard class labels (`0` or `1`). Required for discrete metrics like `F1-Score` and `Balanced Accuracy`.
    
- **`predict_proba(X)`:** Outputs continuous probability estimates $[0, 1]$ for each class (shape `(n_samples, n_classes)`). Required for threshold-independent and calibration metrics like `ROC-AUC` and `Log-Loss`.
    

## 4. Asymmetric Preprocessing (Inside-the-Fold Matrix)

Because validation data must never influence learned parameters, preprocessing is strictly asymmetric between training and validation folds:


|**Step / Operation**|**Training Fold (X_train, y_train)**|**Validation / Test Fold (X_val, y_val)**|**Why?**|
|---|---|---|---|
|**Feature Scaling** (Z-score, Min-Max, Robust)|`fit_transform()`|`transform()` only|Prevents test distribution extremes/means from shifting train scales.|
|**Missing Data Imputation** (Mean, Median, Hot-Deck)|`fit_transform()`|`transform()` only|Imputed test values must come strictly from train statistics.|
|**Dimensionality Reduction / Selection** (PCA, SelectKBest)|`fit_transform()`|`transform()` only|Projection axes/selected features must be discovered without seeing test targets.|
|**Categorical Encoding** (One-Hot, Target Encoding)|`fit_transform()`|`transform()` only|Target means or category mappings from test would leak target labels.|
|**Resampling** (SMOTE, SMOTENC, Undersampling)|`fit_resample()`|**Never applied**|Evaluation must measure performance on real, natural class distributions.|
|**Row-Level Deterministic Math** (`log1p`, ratios, flags)|Direct execution|Direct execution|Depends only on a single row's own values; zero cross-row leakage.|

## 5. Automation with `imblearn.Pipeline` & Custom Transformers

### 5.1 Why `imblearn.pipeline.Pipeline` is Mandatory

Standard `sklearn.pipeline.Pipeline` assumes every intermediate step preserves the exact number of rows (`n_samples`), so it crashes if you insert a resampling step like `SMOTE`.

`imblearn.pipeline.Pipeline` solves this natively:

- During `.fit(X_train, y_train)`: Executes `fit_transform()` on transformers, `fit_resample()` on samplers, and `.fit()` on the final estimator.
    
- During `.predict(X_val)` or `.predict_proba(X_val)`: Automatically **skips** the resampling step and passes `X_val` straight through `.transform()` into `.predict()`.

```python
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, cross_validate

pipe = ImbPipeline(steps=[
    ("scaler", StandardScaler()),
    ("smote", SMOTE(random_state=42)),
    ("model", LogisticRegression(max_iter=1000))
])

gkf = GroupKFold(n_splits=5)
cv_splits = list(gkf.split(X, y, groups=groups))

cv_results = cross_validate(
    estimator=pipe,
    X=X,
    y=y,
    cv=cv_splits,
    scoring=["roc_auc", "f1_macro", "balanced_accuracy"],
    n_jobs=-1
)

```

### 5.2 Anatomy of a Custom Transformer (`BaseEstimator` + `TransformerMixin`)

When your workflow requires custom domain logic inside a pipeline (e.g., rounding discrete columns after SMOTE interpolation), you build a custom transformer class:

```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class DiscreteRounder(BaseEstimator, TransformerMixin):
    def __init__(self, col_indices=None):
        # Parameter names in __init__ must match attribute names identically
        self.col_indices = col_indices

    def fit(self, X, y=None):
        # Stateless transformer: learns nothing, must return self
        return self

    def transform(self, X):
        X_out = X.copy()
        if self.col_indices is not None:
            for idx in self.col_indices:
                X_out[:, idx] = np.round(X_out[:, idx])
        return X_out
```

- **`BaseEstimator`:** Provides `.get_params()` and `.set_params()`, enabling compatibility with `GridSearchCV` and pipeline cloning.
    
- **`TransformerMixin`:** Automatically synthesizes `.fit_transform()` by chaining your `.fit()` and `.transform()` methods.
    

## 6. Ablation Study & Hypothesis Testing Framework

### 6.1 Experimental Design

An **Ablation Study** isolates the true predictive contribution of different feature blocks by holding three elements strictly constant across all runs:

1. The **classification algorithm** (e.g., `LogisticRegression`).
    
2. The **hyperparameter configuration**.
    
3. The **exact cross-validation splits** (`cv_splits` from `GroupKFold`).

|**Tier**|**Configuration Name**|**Input Features**|**Experimental Role**|
|---|---|---|---|
|**0**|Null / Dummy Baseline|None (majority class / stratified prior)|Establishes the random-guess floor.|
|**1**|Domain A Only (`Micro`)|Individual-level features only|Measures baseline predictive power without group context.|
|**2**|Domain B Only (`Macro`)|Group-level / contextual features only|Measures pure contextual predictive power on unseen groups.|
|**3**|Full / Hybrid (`Micro + Macro`)|Combined individual + group features|Tests whether adding context improves out-of-group generalization.|
|**4**|Model Family Contrast|Hybrid + alternative family (e.g., `GaussianNB`)|Verifies that findings are not an artifact of one specific algorithm.|
### 6.2 Formal Hypotheses & Decision Rule

- **Null Hypothesis ($H_0$):** Contextual/group features add no meaningful predictive power when generalizing to unseen groups ($\text{Score}_{\text{Hybrid}} \le \text{Score}_{\text{Micro}}$).
    
- **Alternative Hypothesis ($H_1$):** Contextual/group features consistently improve out-of-group generalization ($\text{Score}_{\text{Hybrid}} > \text{Score}_{\text{Micro}}$).
    
- **Practical Decision Rule:** To reject $H_0$, the performance gain ($\Delta = \text{Score}_{\text{Hybrid}} - \text{Score}_{\text{Micro}}$) must be **larger than the cross-fold standard deviation** ($\Delta > \text{Std}$) and consistent across primary metrics. Otherwise, the gain falls within inter-group noise.
    

## 7. Evaluation Metrics — Definitions & Reference Baselines

### 7.1 ROC-AUC (Area Under the ROC Curve)

- **What it is:** The area under the curve plotting True Positive Rate (Recall) against False Positive Rate ($1 - \text{Specificity}$) across all classification thresholds $\tau \in [0, 1]$.
    
- **What it measures:** The probability that the model assigns a higher predicted score to a randomly chosen positive instance than to a randomly chosen negative instance (**ranking discrimination**).
    
- **Key property:** **Threshold-independent**; unaffected by the arbitrary $0.50$ cut-off.
    
- **Benchmarks:** $0.50$ = pure random chance; $0.70\text{–}0.80$ = acceptable discrimination; $> 0.80$ = strong discrimination.
    

### 7.2 Balanced Accuracy

- **What it is:** The arithmetic mean of recall across both classes:
    

$$\text{Balanced Accuracy} = \frac{\text{Sensitivity (TPR)} + \text{Specificity (TNR)}}{2}$$

- **What it measures:** Classification accuracy corrected for class imbalance, giving equal weight to the positive and negative classes.
    
- **Benchmarks:** $0.50$ = random or majority-class `DummyClassifier` floor.
    

### 7.3 Macro F1-Score

- **What it is:** The unweighted average of the F1-score computed independently for each class $c \in \{1, \dots, C\}$:
    

$$\text{Macro F1} = \frac{1}{C} \sum_{c=1}^{C} F1_c, \quad \text{where} \quad F1_c = 2 \cdot \frac{\text{Precision}_c \cdot \text{Recall}_c}{\text{Precision}_c + \text{Recall}_c}$$

- **What it measures:** The harmonic balance between Precision (avoiding false alarms) and Recall (capturing true cases), treating minority and majority classes with equal importance.
    
- **Benchmarks:** $\sim 0.50$ in balanced binary tasks; a majority-class `DummyClassifier` typically scores $\sim 0.35\text{–}0.40$ because it gets $0.00$ F1 on the minority class.
    

### 7.4 Log-Loss (Binary Cross-Entropy)

- **What it is:** The negative log-likelihood of the true labels given the predicted probabilities:
    

$$\text{Log-Loss} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log(\hat{p}_i) + (1 - y_i) \log(1 - \hat{p}_i) \right]$$

- **What it measures:** **Probability calibration**. It heavily penalizes predictions that are both highly confident and wrong (e.g., predicting $\hat{p} = 0.99$ when $y = 0$).
    
- **Benchmarks:** **Lower is better.** A dummy baseline predicting $\hat{p} = 0.50$ for every row yields $\text{Log-Loss} = -\ln(0.5) \approx 0.693$.
    

### 7.5 Cross-Fold Standard Deviation ($\text{Std}$)

- **What it measures:** Generalization stability across different held-out groups.
    
- **Benchmarks:** $\text{Std} < 0.05$ indicates consistent generalization across groups; $\text{Std} > 0.10$ signals high heterogeneity (the model succeeds on some groups and fails on others).
    

## 8. Quick Reference & Operational Checklist

| **Metric**            | **Core Question Answered**                                       | **Chance / Dummy Floor**           | **Prioritize When…**                                   |
| --------------------- | ---------------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------ |
| **ROC-AUC**           | Can the model rank positives above negatives?                    | $0.50$                             | Probability ordering / risk ranking is the goal.       |
| **Balanced Accuracy** | Does the model perform well on both classes equally?             | $0.50$                             | Classes are imbalanced and hard labels are needed.     |
| **Macro F1**          | Is the precision-recall trade-off balanced per class?            | $\sim 0.35\text{–}0.50$            | Minority class detection is critical[cite: 5].         |
| **Log-Loss**          | Are predicted probabilities trustworthy and calibrated?[cite: 5] | $\sim 0.693$ (at $p=0.5$)[cite: 5] | Probabilities feed downstream decisions[cite: 5].      |
| **Fold Std**          | Is performance consistent across unseen groups?[cite: 5]         | $< 0.05$ (target)[cite: 5]         | Auditing robustness and inter-group variance[cite: 5]. |
### End-to-End Execution Checklist

1. **Isolate real training rows** using audit flags (`is_test == 0` & `is_synthetic == 0`) before splitting.
    
2. **Define the grouping vector (`groups`)** and drop group identifiers from `X`.
    
3. **Generate `GroupKFold` splits once** (`cv_splits = list(gkf.split(...))`) so all ablation tiers are evaluated on identical group partitions
    
4. **Encapsulate all stateful steps** (scaling, imputation, dimensionality reduction, `SMOTE`, custom rounders) inside `imblearn.pipeline.Pipeline`.
    
5. **Run the ablation tiers** (`Dummy` $\rightarrow$ `Micro` $\rightarrow$ `Macro` $\rightarrow$ `Hybrid`) and report all metrics as $\text{mean} \pm \text{std}$
    
6. **Evaluate $H_0$ vs. $H_1$** by checking whether $\Delta_{\text{Hybrid} - \text{Micro}} > \text{Std}$.
