[← Volver al Índice General](../index.md){: .back-to-index }

##### 🎯 Context & Objectives

In survey data engineering (such as the European Social Survey), failing to distinguish between **systematic non-response codes** (`66`, `77`, `88`, `99`) and **legitimate extreme scale values** (`0` and `10`) introduces catastrophic bias into machine learning models. Treating a valid response of `0` ("No trust at all") as a missing value deletes extreme opinions and artificially compresses the variance towards the mean.

In this exercise, you will build an automated, auditable data cleaning and imputation pipeline in Python. You will systematically convert ESS missing codes to standard `NaN`s, preserve valid scale boundaries, and compare single-variable/grouped imputation with multivariate algorithms (`IterativeImputer` / MICE).

##### 📑 Exercise Instructions

###### 1. Syntactic / Algorithmic Level (Systematic Missing Code Handling)

Create a Python notebook (`notebooks/06_1_data_cleaning_imputation.ipynb`) that implements the following technical workflow:

- **Explicit Code Mapping (Avoiding Heuristic Pitfalls):**
    
    - Define a explicit dictionary structure mapping specific ESS missing value codes (`66` = Not applicable, `77` = Refusal, `88` = Don't know, `99` = No answer, `999` = Not available) to `np.nan`.
        
    - **Crucial Rule:** Ensure that legitimate scale endpoints (`0` and `10`) for 11-point Likert variables (such as `ppltrst`, `stfdem`, `lrscale`, `happy`, `rlgdgr`) are **strictly preserved** and NEVER converted to `NaN`.
        
- **Missingness Diagnosis (MCAR vs. MAR vs. MNAR):**
    
    - Calculate and display missing data percentages per column across the dataset.
        
    - Filter and inspect rows where non-response occurs to determine whether missingness is completely random or correlated with demographics (e.g., age or education level).
        

###### 2. Applied / Data Level (Grouped vs. Multivariate Imputation)

Apply these transformations to your merged master dataset (`master_country_features` or `surveys`):

- **Grouped Baseline Imputation:**
    
    - Impute missing values in ordinal survey variables (e.g., `trstlgl`, `stfdem`, `polintr`) using country-level or regional-cluster medians (`cntgrp_fc`) using Pandas `.groupby().transform()`.
        
- **Multivariate Imputation (`IterativeImputer` / MICE):**
    
    - Utilize `sklearn.impute.IterativeImputer` (enabling experimental features via `from sklearn.experimental import enable_iterative_imputer`) to model missing features as a function of other respondent answers.
        
- **Distributional Audit & Impact Assessment:**
    
    - Compare the summary statistics (mean, standard deviation, median, IQR) and probability density plots (KDE) of key variables before and after imputation.
        
    - Verify that the proportion of extreme responses (`0`s and `10`s) remains intact after cleaning.
        

##### 🌐 Official References & Documentation

- **European Social Survey Methodology:** [ESS Data Documentation Report — Missing Values Guide](https://www.google.com/search?q=https://www.europeansocialsurvey.org/methodology)
    
- **Scikit-Learn Imputation Guide:** [Imputing Missing Values (`IterativeImputer`)](https://www.google.com/search?q=https://scikit-learn.org/stable/modules/impute.html%23multivariate-feature-imputation)
    
- **Pandas Missing Data Guide:** [Working with Missing Data in Pandas](https://pandas.pydata.org/docs/user_guide/missing_data.html)
    

##### 📚 Recommended Manuals & CheatSheets

- **Scikit-Learn Imputation Cheat Sheet:** [DataCamp Scikit-Learn Missing Value Handling](https://www.google.com/search?q=https://www.datacamp.com/cheat-sheet/scikit-learn-cheat-sheet-python)
    
- **Rubin's Missing Data Theory:** [Little & Rubin — Statistical Analysis with Missing Data Overview](https://www.wiley.com/)
    

💻 **Tu Desafío:** Crea el cuaderno `notebooks/06_1_data_cleaning_imputation.ipynb` en tu entorno local. Implementa el mapeo explícito de códigos (`77`, `88`, `99` $\rightarrow$ `NaN`) respetando los extremos válidos `0` y `10`, aplica `IterativeImputer` y compara las distribuciones resultantes[cite: 4, 6, 7].