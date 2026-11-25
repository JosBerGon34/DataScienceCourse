## 📋 Capstone Project Execution Index: Sequential Pipeline & Layered Architecture

**Notebook & Module Naming Convention:**

- **Macro-Phases (`Step_X.Y.ipynb` / `src/steps/sX_Y.py`):** Represent sequential execution stages of the data science lifecycle. Sub-tasks increment by `+0.1` (`X.1`, `X.2`).
    
- **Architectural Data Layers (`L0` – `L5`):** Represent cumulative information tiers persisted in DuckDB/PostgreSQL and evaluated sequentially during confirmatory modeling and ablation studies.
    

### 🏗️ Architectural Layer Hierarchy (`L0` – `L5`)

The dataset is constructed and audited across six cumulative layers before and during feature engineering:

- **L0 — Metadata Dictionary & Semantic Schema Configuration:** Parsing of the ESS11 HTML/XML Codebook into structured JSON/SQL dictionaries (`valid_cols.json` and `blacklist.json`), cataloging scale ranges, valid boundary values (`0` and `10`), routing codes (`6/66/666`), non-response codes (`7/77`, `8/88`, `9/99`), and `COALESCE` rules for harmonized variables.
    
- **L1 — DuckDB Feature Projection & Micro-Sanitization Rules:** Pushdown column projection in DuckDB (`WHERE essround = 11`), exclusion of country-specific/legacy items, pre-cleaning calculation of row-level evasion signals (`audit_evasion_ratio`, `audit_midpoint_rate`), recoding of pure non-response codes to `NULL` (preserving structural `6/66` routing codes for exploratory profiling), `COALESCE` consolidation, and dynamic pruning of columns exceeding the `35%` real-null threshold.
    
- **L2 — European Macro-Regional Geopolitical Layer:** Integration of standardized European macro-regional mappings (`Northern`, `Western`, `Southern`, `Eastern`) with categorical labels and factorized keys (`region_fc`), ensuring balanced regional representation (minimum viable countries per macro-region) without leaking exact country identifiers (`cntry` kept strictly as a random grouping factor).
    
- **L3 — Macroeconomic API Ingestion & Tri-Tier Clustering (`Poor`, `Mid`, `Rich`):** Automated ingestion of external macroeconomic indicators (GDP per capita, inflation, unemployment, government debt) via World Bank / Eurostat REST APIs, directional polarity alignment (inverting inflation, unemployment, and debt so higher values reflect stronger macro performance), and unsupervised/anchored K-Means segmentation into three structural economic tiers (`ecocluster_fc`: `0 = Poor/Emerging`, `1 = Mid/EU-Average`, `2 = Rich/Core`).
    
- **L4 — Strategic Feature Grouping, Collinearity Pruning & Signal Classification (`_comp` vs. `_triv`):**
    
    - **L4.1 — Semantic Block Aggregation & Collinearity Filtering:** Grouping variables into theoretical domains (Institutional Trust, Political Efficacy, Schwartz Human Values, Biographical Experience) and pruning redundant intra-block collinearity ($\rho > 0.85$) and zero-signal noise via `SelectKBest` / Spearman $\rho$.
        
    - **L4.2 — Authenticity & Refuge/Ceiling Disambiguation (`_comp` vs. `_triv`):** Exploiting biographical experience variables and their baseline IQR refuge rates (`exp_refuge_rate`, inverse IQR rarity weights, and intra-block disparity `_gr`) to separate genuine attitudinal stances from defensive midpoint refuge (`lrscale == 5`) and artificial ceiling inflation (`happy` / `stflife` at `7–8`). Variables are tagged according to their empirical role and signal integrity:
        
        - **`_comp` (Complementary / Composite Signal):** High-signal predictors, semantic block indices, and dissonance/authenticity detectors that actively disambiguate fake neutrals and ceiling bias.
            
        - **`_triv` (Inocuous / Baseline Control):** Low-collinearity contextual, demographic, or structural routing controls (`has_partner`, `is_employed`) retained as neutral baseline covariates without distorting the primary attitudinal space.
            
- **L5 — Multi-Layered Hypothesis Declaration ($H_0$ vs. $H_1$) & Ablation Sub-Layers:** Formal specification of the nested confirmatory testing hierarchy evaluated under country-grouped cross-validation (`GroupKFold` by `cntry`):
    
    - **L5.0 ($H_0$ — Null Baseline):** Target variance is explained solely by baseline micro-covariates (`_triv`) and random country-level intercepts, assuming all midpoint (`5`) and high-wellbeing (`7–8`) responses represent genuine, homogeneous preferences.
        
    - **L5.1 ($H_1a$ — Macro-Regional Context Layer):** Evaluates the incremental predictive and structural effect of European macro-regions (`L2`) over $H_0$.
        
    - **L5.2 ($H_1b$ — Macroeconomic Tier Layer):** Evaluates the incremental effect of economic clusters (`Poor` / `Mid` / `Rich`, `L3`) and macro-polarity alignment on shifting baseline attitudinal distributions.
        
    - **L5.3 ($H_1c$ — Composite Semantic & Authenticity Layer):** Evaluates the full multi-layer hypothesis incorporating `_comp` feature groups, biographical friction indices, and fake-neutral / ceiling disambiguation features (`L4`), testing whether isolating defensive response styles significantly improves out-of-sample generalization (Wilcoxon signed-rank test, $p < 0.05$).
        

### 🚀 Sequential Execution Steps (`Step 0` – `Step 7`)

#### **STEP 0 (Notebooks `0.0` – `0.1` | `src/steps/s0_*.py`): Dictionary Architecture & DuckDB Ingestion (`L0` – `L1`)**

- **0.0 — Codebook Parsing & Metadata Configuration (`L0`):** Parse the ESS11 HTML/XML Codebook into `valid_cols.json` and `blacklist.json`, defining domain sectors, scale bounds, non-response masks, and `COALESCE` pairs, and persist metadata into DuckDB/SQLite.
    
- **0.1 — DuckDB Pushdown Filtering & Initial Sanitization (`L1`):** Execute dynamic SQL queries over raw ESS11 data to filter round 11, compute pre-imputation evasion/midpoint audit metrics, sanitize `7/8/9` non-response codes to `NULL` (leaving `6/66` intact for exploratory routing), apply `COALESCE`, prune columns with `> 35%` real nulls, and persist the clean snapshot (`./temp/ess11_clean.duckdb` / `.parquet`).
    

#### **STEP 1 (Notebooks `1.0` – `1.1` | `src/steps/s1_*.py`): Multi-Source Macro Enrichment & Clustering (`L2` – `L3`)**

- **1.0 — Macro-Regional Mapping & External API Extraction (`L2` & `L3`):** Map surviving countries to European macro-regions (`L2`) and query World Bank / Eurostat REST APIs with defensive schema guards to retrieve macroeconomic indicators (`L3`).
    
- **1.1 — Polarity Alignment, Tri-Tier Economic Clustering & Relational Persistence (`L3`):** Normalize macro indicators, align directional polarity, fit `RobustScaler` + anchored K-Means (`Poor`, `Mid`, `Rich`), and persist the integrated relational schema in DuckDB/PostgreSQL.
    

#### **STEP 2 (Notebooks `2.0` – `2.1` | `src/steps/s2_*.py`): Exploratory Screening, Signal Classification & Hypothesis Design (`L4` – `L5`)**

- **2.0 — Exploratory Profiling & Collinearity/Signal Screening (`L4.1`):** Perform distribution profiling (skewness, kurtosis, IQR refuge mass), handle structural `6/66` routing flags, filter intra-block collinearity, and execute univariate/rank screening (`Spearman` $\rho$, `SelectKBest`) excluding `cntry` to prevent geographic leakage.
    
- **2.1 — `_comp` / `_triv` Taxonomy & Multi-Layered $H_0$ / $H_1$ Formulation (`L4.2` & `L5`):** Classify surviving variables into `_comp` and `_triv` roles, define empirical rules for fake-neutral and ceiling detection via biographical experience variables, and formally lock in hypotheses `L5.0` ($H_0$) through `L5.3` ($H_1c$).
    

> **Methodological Note:** Steps `0` through `2` constitute the **inductive exploratory phase** (Tukey, 1977; Kerr, 1998). Once `L5` is locked at the end of `Step 2.1`, Steps `3` through `5` proceed strictly as a **deductive confirmatory pipeline** under leak-free country-grouped cross-validation.

#### **STEP 3 (Notebooks `3.0` – `3.1` | `src/steps/s3_*.py`): Multi-Level EDA & Imputation Integrity**

- **3.0 — Cross-Level Visual & Statistical EDA:** Analyze target and predictor distributions across macro-regions (`L2`), economic tiers (`L3`), and `_comp` / `_triv` groups (`L4`), applying temporary macro-balancing exclusively for unbiased visualization.
    
- **3.1 — Fold-Safe Imputation & Bitmask Audit Trail:** Implement country-stratified hot-deck / MICE imputation for residual missingness and structural encoding of `6/66` routing codes, tracking all row-level transformations via cumulative `audit_flag` bitmasking and serializing statistical profiles via `joblib`.
    

#### **STEP 4 (Notebooks `4.0` – `4.1` | `src/steps/s4_*.py`): Non-Linear Feature Engineering (`_comp` & `_triv` Pipeline)**

- **4.0 — Semantic Block & Intra-Subject Disparity Engineering:** Compute block-level continuous aggregates (`_mean`), ordinal thresholds (`_ord`), and intra-block disparity (`_gr`) strictly inside training folds.
    
- **4.1 — Fake-Neutral & Ceiling Disambiguation Features:** Materialize inverse IQR rarity weights (`exp_refuge_rate`), clean biographical friction indices, `neutral_shield_score`, and `happy_ceiling_dissonance`, encapsulating the entire deterministic transformation logic inside the `Wrapper + Pipeline`.
    

#### **STEP 5 (Notebooks `5.0` – `5.1` | `src/steps/s5_*.py`): Confirmatory Modeling, Layer Ablation & Serialization**

- **5.0 — Nested Hypothesis Testing (`L5.0`–`L5.3`) & Multi-Paradigm Benchmarking:** Train order-aware (`OrderedModel` / `LogisticAT`), gradient-boosted (`LightGBM` / `XGBoost`), and Bayesian benchmark models across the nested `L5` sub-layers using `GroupKFold` grouped by `cntry`.
    
- **5.1 — Golden Rules Audit & Full Pipeline Serialization:** Verify zero data leakage across folds, run Wilcoxon significance tests across `L5` sub-layers, and serialize the unified `Wrapper + Pipeline`, feature dictionaries, and pre-computed EDA metrics via `joblib`.
    

#### **STEP 6 (Notebooks `6.0` – `6.1` & CLI Orchestration): Synthesis & End-to-End Automated Execution**

- **6.0 — Executive & Technical Synthesis:** Evaluate empirical evidence against $H_0$ and $H_1a$–$H_1c$, documenting predictive ceilings, fake-neutral reclassification gains, and cross-regional trade-offs.
    
- **6.1 — Automated `Wrapper + Pipeline` & Ablation Execution:** Execute the full pipeline end-to-end via CLI (`run-pipeline` / `build-db`), verifying deterministic reproduction of all databases, `audit_flag` logs, ablation tables, and `.joblib` artifacts.
    

#### **STEP 7 (Application Module `src/apps_*` & Notebook `7.0`): Decoupled Web Application & API Serving**

- **7.0 — Full-Stack Serving Framework (`Flask` / `FastAPI` / `Dash`):** Build a decoupled web application rendering interactive multi-layer EDA dashboards and real-time prediction endpoints driven by user-inputted predictors.
    
- **7.1 — Isolated Sandbox Deployment & Memory Optimization:** Package lightweight deployment profiles (`web_dash`, `web_flask`, `web_fapi`) backed by serialized `joblib` artifacts to guarantee schema validation by feature name, minimal memory footprint, and fast cold-start latency.