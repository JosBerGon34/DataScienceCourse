'''Markdown

🟢 < Module 7.1 > Exploratory Data Analysis (EDA), Stratified Distributions & Correlation Diagnostics

##### 🎯 Context & Objectives

In Exploratory Data Analysis (EDA), the goal is not merely to compute global summary statistics, but to uncover structural patterns, cluster behaviors, and dependencies between predictors and target variables across different economic contexts. In this exercise, you will perform an advanced EDA on your cleaned master survey dataset (`surveys_clean` combined with macro features). You will analyze ordinal vs. continuous variable distributions, evaluate non-linear relationships, and construct stratified correlation heatmaps comparing different European country clusters (e.g., high-income vs. medium/low-income economic groups).

##### 📑 Exercise Instructions

###### 1. Syntactic / Algorithmic Level (Pandas & Seaborn EDA Fundamentals)

Create a Python notebook (`notebooks/07_1_exploratory_data_analysis.ipynb`) that implements the following technical steps:

- **Statistical Profiling & Distribution Metrics** :
    
    - Compute robust central tendency and dispersion metrics (median, IQR, mean, standard deviation) for key survey ordinals (e.g., `happy`, `lrscale`, `stfdem`) and engineered features (`EmployType`, `emplno`).
        
    - Identify skewness and modal concentrations (such as the point mass at `0` in `emplno` for wage earners).
        
- **Stratified Correlation Analysis (Spearman vs. Pearson)** :
    
    - Explain why **Spearman’s rank correlation** is theoretically superior to Pearson's correlation when analyzing ordinal Likert scales (0–10) in survey data.
        
    - Generate a correlation matrix and visualize it using a Seaborn heatmap (`sns.heatmap`), ensuring proper diverging colormaps and annotation of correlation coefficients.
        

###### 2. Applied / Data Level (Socio-Economic Stratification & Insights)

Evaluate how macroeconomic country clusters modulate individual behaviors:

- **Multi-Group Comparison** :
    
    - Group your dataset by country economic tiers or regional clusters (`cntgrp_fc` / `std_region`).
        
    - Compare the distribution of political ideology (`lrscale`) or institutional trust (`trstlgl`) across different economic clusters using boxplots or violin plots (`sns.boxplot` / `sns.violinplot`).
        
- **Insight Synthesis** :
    
    - Document 3 key empirical findings from your visualizations that support your core research hypothesis (e.g., how educational level `edulvlb` or employment relation `EmployType` shifts political or social trust distributions).
        

##### 🌐 Official References & Documentation

- **Seaborn Statistical Plots** : [Seaborn Heatmap & Distribution Tutorial](https://seaborn.pydata.org/generated/seaborn.heatmap.html)
    
- **Pandas Statistical and Descriptive Functions** : [Pandas Descriptive Statistics Guide](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
    

##### 📚 Recommended Manuals & CheatSheets

- **DataCamp Seaborn Cheat Sheet** : [Python Seaborn Data Visualization Cheat Sheet](https://www.datacamp.com/cheat-sheet/python-seaborn-cheat-sheet)
    
- **Exploratory Data Analysis Best Practices** : [Python for Data Analysis — Exploratory Data Analysis Chapter](https://wesmckinney.com/book/)
    

💻 **Your Challenge:** Create the notebook `notebooks/07_1_exploratory_data_analysis.ipynb` in your local environment, run the stratified descriptive statistics and correlation heatmaps, and share your code or key findings here when ready for review! 🚀📊

'''