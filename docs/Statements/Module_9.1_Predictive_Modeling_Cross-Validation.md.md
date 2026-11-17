🟢 < Module 9.1 > Predictive Modeling, Ablation Study & Country-Grouped Cross-Validation (GroupKFold):

##### 🎯 Context & Objectives

In hierarchical socio-economic datasets—where individual survey respondents (ESS) are nested within countries and macroeconomic clusters (Eurostat)—standard random cross-validation (`KFold` or `StratifiedKFold`) violates the independent and identically distributed (**i.i.d.**) assumption[cite: 3, 4, 5]. Mixing citizens from the same country across training and validation folds allows models to memorize national baselines ("country leakage"), yielding artificially inflated evaluation scores.

In this module, you will build a leakage-free predictive modeling pipeline using **country-grouped cross-validation (`GroupKFold`)**[cite: 3, 4, 5] and execute a controlled **Feature Ablation Study**[cite: 3]. By keeping the algorithm and cross-validation splits fixed while varying the input feature blocks (Individual Microdata vs. Macroeconomic Clusters vs. Combined Hybrid), you will scientifically test whether macro-regional economic indicators provide statistically meaningful predictive power on unseen countries.

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

- **Multilevel & Hierarchical Modeling:** *Data Analysis Using Regression and Multilevel/Hierarchical Models (Andrew Gelman & Jennifer Hill)* — Chapter 11–12 (Nested/Clustered Survey Data)
- **Model Evaluation & Ablation:** *Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow (Aurélien Géron)* — Chapter 3 (Classification Metrics: ROC-AUC vs. F1).

💻 **Your Challenge:** Create `notebooks/09_1_predictive_modeling_groupkfold.ipynb` (or `notebooks/Ex9.1.ipynb`), implement the 5-fold `GroupKFold` pipeline with inside-the-fold `SMOTE`, run the 4-tier ablation comparison (`Dummy` vs. `Micro` vs. `Macro` vs. `Hybrid` + `GaussianNB`), and share your cross-validation metrics table to audit the scientific conclusion! 🚀📊