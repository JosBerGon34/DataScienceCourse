## 📋 Capstone Project Execution Index: Sequential Pipeline & Architecture

**Notebook Naming & Compartmentalization Convention:** Each project phase is structured into sequential Jupyter Notebooks starting at `Step_X.0.ipynb`. Whenever a phase is modularized into sub-tasks (e.g., separate data sources, clustering routines, or model families), I will increment the numbering by `+0.1` (`X.1`, `X.2`, etc.) while keeping the repository clean and traceable.

### **STEP 0 (Notebooks `0.0` – `0.x`): Problem Formulation, Exploratory Screening & Hypothesis Design**

- **0.0 — Scope, Target Selection & Exploratory Screening:** I will collect the primary European Social Survey (ESS) microdata and macro control data. I will perform an exploratory scan (shape analysis, kurtosis/skewness profiling, missingness auditing, and `SelectKBest` univariate screening) to identify variables with empirical signal. From this evidence, I will formulate a multi-layered research hypothesis ($H_1$) against the null ($H_0$), stipulating the expected correlation structures and the target variable. `Country` is designated as a random effect (grouping factor), not a fixed predictor, to separate between-country variance from within-country signal.

- **0.1 — Reference Control Datasets & Variable Dictionary:** I will integrate auxiliary reference datasets (World Bank, Eurostat) to control for macro-level contexts (regional, cultural, and economic country groupings). I will define and execute an initial cataloging of every variable—documenting scale ranges, missingness codes, transformation requirements, and theoretical roles—and persist these metadata dictionaries into the pre-pipeline Wrapper.

> **Methodological note:** Hypothesis formulation follows a two-phase exploratory-confirmatory design (Tukey, 1977; Kerr, 1998). Phase 1 (Steps 0.0–3) is inductive: data structure informs variable selection and hypothesis generation. Phase 2 (Steps 4–5) is deductive: the formulated $H_0$ is tested confirmatorily with country-grouped cross-validation. This is not HARKing; the exploratory origin of the hypothesis is explicitly documented.   
    

### **STEP 1 (Notebooks `1.0` – `1.x`): Multi-Source Data Ingestion & SQL Persistence** 

- **1.0 — Automated Data Extraction (APIs & Web Scraping):** I will demonstrate end-to-end data collection capabilities by fetching macroeconomic indicators via public REST APIs (e.g., World Bank / Eurostat) and scraping structured reference tables from the web using resilient parsers.
    
- **1.1 — Relational Database Persistence & Filtering:** I will persist all raw and ingested datasets into a SQL database engine (SQLite / PostgreSQL via SQLAlchemy), applying structured SQL queries to perform initial schema validation and domain filtering.
    

### **STEP 2 (Notebooks `2.0` – `2.x`): Data Cleaning, Multi-Level Merging & Integrity Auditing** 

- **2.0 — Survey Integrity & Missing Data Sanitization:** I will clean the ESS microdata of null values and reserved non-response codes (`66`, `77`, `88`, `99`) while strictly preserving valid boundary responses (`0` and `10`) and maintaining the statistical integrity of each variable.
    
- **2.1 — Cross-Level Integration, Macro-Balancing & Audit Flags:** I will merge the cleaned individual micro-dataset with the country-level macro control datasets, creating structural country groupings where necessary while preserving genuine micro-level variance and biases. I will apply sample balancing exclusively across macro-control dimensions to keep the dataset realistic for training, catalog all transformations with explicit audit flag variables, and persist these rules into the pre-pipeline Wrapper.
    

### **STEP 3 (Notebooks `3.0` – `3.x`): Exploratory Data Analysis (EDA) & Statistical Profiling** 

- **3.0 — Core Variable Selection & Exploratory Balancing:** I will define and justify the core subset of variables essential for exploratory analysis, applying temporary balancing strictly on macro-control variables exclusively for unbiased visual exploration.
    
- **3.1 — Univariate, Bivariate & Interaction Analysis:** I will analyze each variable independently and examine cross-variable interactions (using rank-based metrics such as Spearman's $\rho$ for ordinal constructs). I will serialize all statistical summaries, distribution profiles, and analytical takeaways into dictionaries via `joblib`, embedding the pre-pipeline instructions into the Wrapper.
    

### **STEP 4 (Notebooks `4.0` – `4.x`): Feature Selection & Non-Linear Feature Engineering** 

- **4.0 — Statistical Feature Selection & Range-Impact Estimation:** I will apply multiple feature selection techniques and leverage the persisted statistical profiles to identify which predictors require mathematical transformations to capture their correlative impact across different value ranges.
    
- **4.1 — Derived Features & Non-Linear Interactions:** I will evaluate and construct derived features—grouping, encoding, and combining predictors through domain-driven and non-linear techniques—to capture stronger correlations and interaction effects. I will persist the complete transformation logic inside the `Wrap + Pipeline` architecture.
    

### **STEP 5 (Notebooks `5.0` – `5.x`): Predictive Modeling, Benchmarking & Leak-Free Validation** 

- **5.0 — Primary Optimal Model & Multi-Paradigm Benchmarking:** I will select and train the primary predictive model best suited to the ordinal/correlational nature of the data. In parallel, I will build two benchmark pipelines:
    
    1. A **Bayesian model** to evaluate posterior distributions, compare predictive scores, and test the robustness of my hypothesis.
        
    2. An **automated model-selection benchmark** (using dataset-profiling libraries) to identify which algorithm family best fits the empirical data structure, comparing all three approaches side by side.
        
- **5.1 — Golden Rules Compliance & Full Pipeline Serialization:** I will finalize the `Wrap + Pipeline` assembly, auditing and eliminating any data leakage or "golden rule" violations (ensuring country-grouped cross-validation and fold-isolated transformations). I will serialize the entire workflow via `joblib`, storing variable mapping dictionaries, pre-computed statistical metrics ready for front-end plotting, trained model artifacts, and the unified execution sequence of the general Wrapper and Pipeline.
    

### **STEP 6 (Notebooks `6.0` – `6.1` & Orchestration Script): Final Synthesis & End-to-End Automated Pipeline Execution**

- **6.0 — Executive & Technical Conclusions:** I will synthesize the end-to-end findings, evaluating the empirical evidence against my multi-layered hypothesis and null hypothesis, documenting model trade-offs, predictive ceilings, and methodological limitations.
    
- **6.1 — Full-Cycle Wrapper + Pipeline Automation & Ablation Execution:** I will globally implement and execute my automated `Wrapper + Pipeline` architecture from the initial data ingestion stage through to feature/layer ablation studies. I will verify that the entire workflow runs autonomously without manual intervention, systematically persisting every intermediate dataset, audit flag, statistical dictionary, ablation metric, and serialized `joblib` artifact along the way.
    

### **STEP 7 (Application Module `app/` & Notebook `7.0`): Decoupled Web Application & API Deployment** 

- **7.0 — Full-Stack Serving Framework (Flask / FastAPI / Dash):** I will build a decoupled web application that renders both the interactive Exploratory Data Analysis (EDA) dashboards and a real-time prediction interface driven by user-inputted predictors.
    
- **7.1 — Service Extensibility & Memory Optimization:** I will expose structured endpoints capable of serving predictions to external downstream services, leveraging the serialized `joblib` artifacts (dictionaries, pre-aggregated chart stats, and lightweight pipelines) to minimize memory footprint and optimize cold-start loading times.