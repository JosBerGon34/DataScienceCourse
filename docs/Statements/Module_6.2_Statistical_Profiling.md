

🟢 < Module 6.2 > Statistical Profiling, Variable Typologies & Transformation Techniques

##### 🎯 Context & Objectives

Data cleaning alone is not enough to prepare a dataset for modeling; a Data Scientist must understand the mathematical and structural nature of every feature. In this module, you will formally classify variables into **continuous, discrete, multinomial ordinal, and categorical**, master the transformation techniques required to bridge them (e.g., discretizing continuous metrics into ordinal bins, factorizing ordinal Likert scales into categorical classes, or mapping structural features), **apply standardization and rescaling transformations to continuous variables, and implement outlier detection and treatment strategies to ensure robust modeling inputs**. You will also build basic distribution visualizations to inspect skewness, modality, variance, **and tail behavior** before feature engineering.

##### 📑 Exercise Instructions

###### 1. Syntactic / Algorithmic Level (Variable Typology & Transformation Functions)

Create a Python notebook (`notebooks/06_2_variable_profiling_transformations.ipynb`) that implements the following technical steps:

- **Variable Typology Definition & Profiling**:
    
    - Classify the project variables (`emplrel`, `edulvlb`, `emplno`, `happy`, `lrscale`, `cntry`, `EmployType`) into their exact statistical types: _Continuous_, _Discrete/Count_, _Multinomial Ordinal_, and _Nominal/Categorical_.
        
    - Compute statistical profiling metrics (mean, median, standard deviation, IQR, skewness, **kurtosis**, and unique value counts) for each category.
        
- **Transformation & Discretization Techniques**:
    
    - _Ordinal to Categorical / Binning:_ Use `pd.cut()` or `pd.qcut()` to transform 11-point ordinal scales (e.g., `happy` or `lrscale`) into structured categorical tiers (e.g., Low, Medium, High).
        
    - _Factorization & Mapping:_ Implement `pd.factorize()` and explicit `.map()` dictionaries to convert categorical text columns or custom groupings (like `EmployType`) into clean integer codes without breaking ordinal hierarchies.
        
- **Continuous Variable Transformations**:
    
    - _Rescaling & Standardization:_ Apply **min-max normalization** (`(x - min) / (max - min)`), **z-score standardization** (`(x - mean) / std`), and **log transformation** (`np.log1p()`) to continuous/count variables (e.g., `emplno`, `agea`). Document which transformation is appropriate for each variable type and distribution shape.
        
    - _Monotonic & Non-monotonic:_ Implement **Box-Cox** (`scipy.stats.boxcox`) and **Yeo-Johnson** (`scipy.stats.yeojohnson`) transformations for positively-skewed continuous features. Compare their effect on skewness and kurtosis before and after.
        
    - _Continuous to Discrete (Binning):_ Apply `pd.qcut()` (quantile-based) and `pd.cut()` (fixed-width) to a continuous variable (e.g., `emplno` or `agea`) to create ordinal bins. **Justify the choice of bin edges** (equal-frequency vs. equal-width vs. domain-informed) and document how the binning decision affects downstream model interpretability.
        
- **Outlier Detection & Treatment**:
    
    - _Detection:_ Implement at least **two** outlier detection methods:
        
        1. **IQR method:** Flag observations outside `[Q1 - 1.5×IQR, Q3 + 1.5×IQR]`.
            
        2. **Z-score / Modified Z-score:** Flag observations with `|z| > 3` (or `|modified z| > 3.5` using the MAD-based robust z-score).
            
    - _Treatment:_ For each detected outlier, apply and compare:
        
        1. **Removal:** Drop the observation.
            
        2. **Winsorization (clipping):** Cap values at the 1st and 99th percentiles (`np.clip`).
            
        3. **Imputation:** Replace with the group median (e.g., by `EmployType` or `std_region`).
            
    - _Decision criteria:_ Document **when** each treatment is appropriate (e.g., removal for data entry errors, winsorization for heavy-tailed legitimate variation, imputation for structural missingness). **Never remove outliers without first verifying they are not legitimate observations** (e.g., a self-employed respondent with 400 employees is not an outlier — it is a valid data point).
        

###### 2. Applied / Data Level (Visualizing Distributions & Structural Shifts)

- **Distribution Visualization**:
    
    - Create basic distribution plots (using Matplotlib / Seaborn histograms, KDE curves, and countplots) for key variables like `edulvlb` and `emplno`.
        
    - Visually inspect how the point mass at `0` for wage earners in `emplno` alters the distribution shape compared to self-employed cohorts.
        
    - **Create boxplots (or violin plots) segmented by `EmployType` or `std_region` to visually identify outliers and distributional shifts across subgroups.**
        
- **Transformation Impact Assessment**:
    
    - Compare the descriptive statistics of a variable before and after applying a transformation (e.g., raw 0–10 scale vs. 3-class factorized ordinal; raw `emplno` vs. log-transformed `emplno`). Document when it is mathematically appropriate to treat an ordinal variable as continuous versus categorical.
        
    - **For continuous transformations (log, Box-Cox, z-score): plot the original and transformed distributions side-by-side. Report the change in skewness and kurtosis as a quantitative measure of transformation effectiveness.**
        
- **Outlier Impact Assessment**:
    
    - **Before/after comparison:** For each outlier treatment strategy (removal, winsorization, imputation), report:
        
        - Change in mean, std, IQR, and skewness of the affected variable.
            
        - Number of observations affected (removed, clipped, imputed).
            
        - Visual overlay: original distribution (gray) vs. treated distribution (colored) on the same axis.
            
    - **Decision table:** Summarize in a table which treatment was applied to which variable, how many outliers were affected, and the resulting change in key statistics. Justify the choice per variable.
        

##### 🌐 Official References & Documentation

- **Pandas Categorical Data Guide:** Pandas Working with Categoricals
    
- **Seaborn Distribution Plots:** Seaborn Histplot & KDE Guide
    
- **Scipy Statistical Transformations:** scipy.stats.boxcox & yeojohnson
    

##### 📚 Recommended Manuals & CheatSheets

- **DataCamp Pandas Cheat Sheet:** Pandas Data Manipulation & Transformation
    
- **Statistical Data Types in Machine Learning:** Feature Engineering for Machine Learning (Book Overview)
    
- **Outlier Detection Methods:** [IQR vs. Z-Score vs. Isolation Forest — Comparison](https://towardsdatascience.com/outlier-detection-methods-5749d52d2703)
    

💻 **Your Challenge:** Create the notebook `notebooks/06_2_variable_profiling_transformations.ipynb`, build the statistical profiling summary table, apply the transformation techniques (binning, factorization, **log/Box-Cox, z-score**), **detect and treat outliers with documented justification**, generate the distribution plots for your cleaned dataset, **and produce the before/after comparison tables for both transformations and outlier treatments**. ¡Cuando estés listo, comparte tus resultados o código aquí para revisarlo! 🚀📊

