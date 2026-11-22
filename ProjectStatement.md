## 🎓 Final Capstone Project: Multi-Level Modeling of European Sociopolitical & Attitudinal Outcomes (End-to-End Pipeline)

### 1. Problem Statement & Multi-Layered Hypothesis Framework

The objective of this capstone is to design, validate, and deploy an end-to-end Data Science pipeline that evaluates how national macroeconomic contexts, country-level structural profiles, and individual micro-level sociodemographic/attitudinal controls jointly covary with key European Social Survey (ESS) target outcomes:

- **Candidate Target Variables ($Y$):** Political self-placement (`lrscale`, 0–10), subjective well-being (`happy`, 0–10), political interest (`polintr`, 1–4), or institutional trust (`trstprl`, `trstplt`, `trstsci`, 0–10).
    

#### Research Hypotheses (Multi-Layered Architecture)

- **Null Hypothesis ($H_0$):** Neither macroeconomic structural regimes (GDP per capita, average net annual wage, inflation) nor individual micro-level sociodemographic and attitudinal controls exhibit statistically significant explanatory or predictive power over the distributions of the selected target outcomes ($Y$) across European Union countries.
    
- **Alternative Hypothesis ($H_1$ — Layered Structure):**
    
    - **Layer 1 (Macro-Structural Regime):** Grouping EU countries into economically homogeneous clusters (e.g., high-income core, EU-average, and lower-income/catching-up economies) captures significant baseline shifts in the distribution of $Y$.
        
    - **Layer 2 (Micro-Sociodemographic & Control Variables):** Individual-level controls—such as education (`edulvla`/`edlvd*`), household income/feeling about income (`hincfel`), age, gender, urban/rural domicile, minority status (`blgetmg`), and social trust (`ppltrst`, `pplfair`)—account for substantial within-country variance beyond macroeconomic grouping alone.
        
    - **Layer 3 (Cross-Level Interaction & Attitudinal Alignment):** Combining macro-economic clusters with micro-level attitudinal constructs (satisfaction with economy/government `stfeco`, `stfgov`, and institutional trust `trst*`) yields higher out-of-sample predictive generalization than macro-only or ungrouped country-dummy baselines.
        
- **Methodological Scope (Correlational vs. Causal):** The study is **strictly correlational and predictive, not causal**. Your technical report must explicitly document that covariation between a country's economic cluster and individual attitudes does not imply direct causality due to unobserved historical, institutional, and cultural confounders.
    

### 2. Pipeline Architecture & Engineering Requirements

#### Phase 1: Resilient Data Ingestion & Macroeconomic Clustering

- **Web Scraping & API Extraction:** Retrieve national macroeconomic indicators (GDP per capita, average annual net wage, inflation rate) from Eurostat / Datosmacro. Implement explicit defensive guards (raise a `RuntimeError` if scraped tables return empty and log row counts per country) to prevent silent schema breakage.
    
- **Macro-Regime Segmentation (K-Means):** Scale macroeconomic features using `RobustScaler` (passing DataFrames with preserved column names to avoid feature-name warnings) and fit `KMeans` initialized with 3 substantively anchored country centroids: **Germany** (above-EU average), **Spain** (EU average), and **Hungary** (below-EU average).
    

#### Phase 2: Survey Cleaning, Missing Data Integrity & Persistence

- **ESS Missing Code Handling:** Strictly separate reserved survey non-response/routing codes (`6`, `7`, `8`, `9` or `66`, `77`, `88`, `99` depending on scale width) from valid boundary values on 0–10 Likert scales (`0` and `10`). Removing `0` or `10` as statistical outliers is strictly prohibited.
    
- **Distribution-Aware Imputation:** For high-missingness variables (e.g., `trstsci`, `lawobey`), perform country-stratified imputation or `IterativeImputer` (MICE) rather than listwise row deletion, always fixing a reproducible random generator (`np.random.default_rng(seed)`).
    
- **Relational Persistence:** Store cleaned macro, micro, and merged datasets in SQLite and/or PostgreSQL, validating schema alignment (column names and dtypes) prior to every table insertion.
    

#### Phase 3: Exploratory Data Analysis (EDA) & Controlled Resampling

- **Multi-Level EDA:** Analyze target and predictor distributions globally, by country (`cntry`), and by economic cluster (`cntgrp_fc`). Use **Spearman’s rank correlation ($\rho$)** rather than Pearson’s $r$ for ordinal Likert scales, grouping latent constructs visually (`trst*`, `stf*`, `ppl*`).
    
- **Class & Sample Imbalance Control:** Address country sample size disparities (e.g., Germany vs. Croatia). If applying oversampling (such as `SMOTE`), execute it **strictly inside training folds** and verify that country/cluster labels remain aligned without corruption.
    

#### Phase 4: Deterministic Feature Engineering & Collinearity Control

- **Deterministic Target & Feature Construction:** Engineer derived features and discretize target bins (if framing as ordinal/multiclass classification) using **100% deterministic threshold rules**—never inject random noise or stochastic tie-breaking into target labels.
    
- **Geographic Redundancy Control:** Do not include both the exact country identifier (`cnt_fc`) and the macroeconomic cluster (`cntgrp_fc`) simultaneously in the primary hypothesis model, as the model will memorize country IDs instead of learning macro-structural patterns. Train and compare three nested specifications corresponding to your hypothesis layers:
    
    - _Model 1 (Macro-Only Baseline):_ Economic cluster (`cntgrp_fc`) only.
        
    - _Model 2 (Hypothesis Model — Macro + Micro Controls):_ `cntgrp_fc` + sociodemographic controls + attitudinal scales.
        
    - _Model 3 (Country Fixed-Effects Benchmark):_ Exact country identifier (`cnt_fc`) + micro controls.
        

#### Phase 5: Predictive Modeling & Leak-Free Validation

- **Country-Grouped Cross-Validation:** Standard row-level random `train_test_split` is prohibited. Use **`GroupKFold` or `GroupShuffleSplit`** grouped by `cntry` so respondents from the same country never appear in both training and validation splits, preventing geographic data leakage.
    
- **Algorithm Selection:**
    
    - For ordinal targets (`lrscale`, `happy`, `polintr`, `trst*`), benchmark order-aware models (`statsmodels.miscmodels.ordinal_model.OrderedModel` or `mord.LogisticAT`) alongside tree ensembles (`RandomForest`, `XGBoost` / `LightGBM`) and regularized linear/logistic baselines.
        
    - Report honest out-of-sample metrics (Ordinal MAE, Quadratic Weighted Kappa, Macro F1, or $R^2$ / RMSE) across grouped folds, analyzing why predictive ceiling effects occur in cross-national attitudinal survey data.
        

#### Phase 6: Decoupled Web Application Deployment (Flask + Vanilla HTML/JS)

Replace monolithic prototypes with a reproducible client-server architecture:

1. **Path & Environment Hygiene:** Eliminate all hardcoded OS paths using `pathlib.Path` and provide a pinned `requirements.txt`.
    
2. **REST Backend (`Flask`):** Expose a `/predict` endpoint that loads the serialized pipeline (`.pkl`), inspects `model.feature_names_in_`, and **validates incoming JSON payloads by feature name (not positional index)**, returning descriptive HTTP 400 errors on missing or malformed fields.
    
3. **Interactive Frontend (`HTML5 / CSS / JS`):** Build a clean web interface allowing users to select a target variable, country economic tier, and individual micro-controls, sending asynchronous `fetch()` requests to Flask and rendering real-time predicted probabilities/scores (with a graceful local fallback mode if the API is offline).
    

### 3. Expected Deliverables & Official References

- **Repository Structure:** Modular Python package (`src/`), end-to-end executed notebooks (`notebooks/`), web application (`app/`), database artifact (`data/`), and `requirements.txt`.
    
- **Official Technical Documentation:**
    
    - _ESS Methodology & Missing Value Protocols:_ `europeansocialsurvey.org/methodology`
        
    - _Scikit-Learn Group Cross-Validation:_ `scikit-learn.org/stable/modules/cross_validation.html#group-cv`
        
    - _Statsmodels Ordinal Regression (`OrderedModel`):_ `statsmodels.org/stable/examples/notebooks/generated/ordinal_regression.html`
        
    - _Flask & Python `pathlib` Documentation:_ Official Python & Pallets Flask docs.