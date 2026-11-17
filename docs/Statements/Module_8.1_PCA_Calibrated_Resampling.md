🟢 < Module 8.1 > Feature Engineering, PCA & Calibrated Resampling (SMOTE)

##### 🎯 Context & Objectives

Data cannot be fed into a Machine Learning model exactly as it comes out of an Exploratory Data Analysis. In this module, you will finalize the feature matrix by applying deterministic transformations (replacing any stochastic binning to ensure reproducibility), reducing dimensionality for highly correlated blocks, and preparing the mathematical groundwork for handling imbalanced classes using **SMOTE** (Synthetic Minority Over-sampling Technique). A critical objective is to understand **when** and **how** to apply SMOTE without causing _data leakage_ or generating mathematically impossible synthetic records (like continuous decimals for categorical countries).

##### 📑 Exercise Instructions

###### 1. Syntactic / Algorithmic Level (Feature Engineering & Transformation)

Create a Python notebook (`notebooks/08_1_feature_engineering_resampling.ipynb`) that implements the following steps on your cleaned dataset:

- **Deterministic Thresholding (Fixing Stochastic Binning):**
    
    - Review any custom binning functions you planned to use (e.g., separating `happy` or `lrscale` into binary classes). If you previously used stochastic or weighted random approaches (like a custom `BinarizePond` function), replace them with **strict, deterministic threshold rules** (e.g., `value >= median` or `value >= 7`). Document why introducing randomness when constructing a target variable reduces the theoretical maximum achievable accuracy (Label Noise).
        
- **Dimensionality Reduction (The Institutional Trust Block):**
    
    - In Module 7, you discovered that `trstprl` (trust in parliament) and `trstlgl` (trust in the legal system) are highly correlated (ρ = 0.628).
        
    - Implement **PCA (Principal Component Analysis)** with `n_components=1` (using `sklearn.decomposition.PCA`) on these two variables to create a single `institutional_trust_index`. Briefly compare the explained variance of this component versus calculating a simple arithmetic mean.
        
- **Categorical Encoding:**
    
    - Apply `pd.get_dummies(drop_first=True)` to your nominal variables (e.g., macro-regions) to prevent perfect multicollinearity in linear models, as agreed upon during the EDA phase.
        

###### 2. Applied / Data Level (Calibrated Resampling with SMOTE)

Imbalanced classes require resampling, but executing it at the wrong time ruins the validity of the experiment.

- **The Golden Rule of Resampling:**
    
    - Define a function that accepts `X_train` and `y_train` and applies `imblearn.over_sampling.SMOTE` to balance the target classes.
        
    - **Crucial Conceptual Task:** Explain in your notebook why SMOTE must **never** be applied to the entire dataset before making the validation split. What happens to the test set and the _data leakage_ if you oversample before splitting?
        
- **Auditing Synthetic Generation (The Substrate Bias):**
    
    - Generate a test `X_train_resampled` by applying your SMOTE function.
        
    - Analyze the generated synthetic rows. Since SMOTE interpolates mathematically (calculating Euclidean distances) between neighboring points, what happens to discrete or ordinal variables (like the ISCED educational level or an economic cluster `0, 1, 2`)? Do they become continuous decimals (e.g., `cluster = 1.45`)?
        
    - Apply a post-processing function (iterative rounding) to the synthetic data to force these features back into valid discrete values.
        

##### 🌐 Official References & Documentation

- **Imbalanced-Learn (SMOTE):** [SMOTE Documentation](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html)
    
- **Scikit-Learn PCA:** [PCA Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
    

##### 📚 Recommended Manuals & CheatSheets

- **Handling Imbalanced Datasets:** [SMOTE for Imbalanced Classification with Python](https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/)
    
- **Feature Engineering:** _Feature Engineering for Machine Learning (Alice Zheng & Amanda Casari)_ — Dimensionality Reduction.
    

💻 **Your Challenge:** Create the notebook `notebooks/08_1_feature_engineering_resampling.ipynb`. Implement deterministic binning, extract the institutional trust PCA index, configure the SMOTE function (with rounding logic for ordinal values), and draft the explanation of why SMOTE is strictly a _post-split_ operation. Share your code when ready! 🚀📊