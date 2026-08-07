# 🚀 DataScienceCourse: Course Remodel & Applied Refactoring

> **Original Repository:** [https://github.com/JosBerGon34/4GA.DataScience](https://github.com/JosBerGon34/4GA.DataScience)

This repository contains a **comprehensive curriculum redesign (Remodel) and synthesis (Summary)** of the **4Geeks Academy** Data Science program. The primary objective is to reshape the learning journey by replacing traditional toy exercises with an **applied, rigorous, and progressive** approach using real-world datasets that directly feed into the **Final Capstone Project**.

---

## 🎯 Remodeling Objectives

1. **Applied Learning with Real-World Datasets:**
   * **Eurostat:** Macroeconomic and quantitative data (GDP, Unemployment Rate, Public Debt, Inflation Rate).
   * **European Social Survey (ESS):** Sociological survey microdata (ordinal variables covering public attitudes, institutional trust, and political ideology).
   * **Web Scraping & Categorical Data:** Cultural, sports, and socio-relational preference datasets scraped by country.

2. **Direct Alignment with the Capstone Pipeline:**
   * Every module—ranging from native Python data manipulation to Exploratory Data Analysis (EDA), cleaning, and feature engineering—actively builds the exact tools and data structures needed for the ideology prediction pipeline.

3. **Methodological Rigor & Technical Best Practices:**
   * Eliminating common anti-patterns and experimental flaws (e.g., proper missing data handling without truncating valid extreme survey responses `0` and `10`, country-grouped splits to prevent data leakage, and correctly specified ordinal regression models).

---

## 🗺️ Course Structure & Syllabus ("Git checkout main")

The curriculum is structured into progressive modules moving from foundational core concepts to production deployment:

| Module | Description / Applied Focus |
| :--- | :--- |
| **🟢 MODULE 1:** | **Prework Review & Native Python:** Complex nested data structures (lists, dicts) and high-performance iterations without external libraries. "Git checkout Module1.1" |
| **🟢 MODULE 2:** | **Linear Algebra & Calculus for ML:** Matrix operations, vectors, and derivatives tailored for Machine Learning optimization algorithms."Git checkout Module2.1" |
| **🟢 MODULE 3:** | **Git, GitHub & Project Management:** Collaborative workflows, version control best practices, and repository architecture. |
| **🟢 MODULE 4:** | **Probability & Descriptive Statistics:** Sample metrics, distributions, and socio-economic variable analysis. |
| **🟢 MODULE 5:** | **NumPy & Pandas:** High-performance data ingestion, merging, and reshaping on Eurostat and ESS microdata datasets. |
| **🟢 MODULE 6:** | **Data Cleaning & Imputation:** Advanced missing data strategies (distinguishing survey non-response codes `77, 88, 99` from valid boundary responses). |
| **🟢 MODULE 7:** | **Exploratory Data Analysis (EDA):** Pattern discovery, correlation analysis, and advanced visualizations (Matplotlib/Seaborn). |
| **🟢 MODULE 8:** | **Feature Engineering & Resampling:** Data transformations, structural clustering (K-Means), and properly calibrated SMOTE oversampling. |
| **🟢 MODULE 9:** | **Predictive Modeling & Validation:** Regression/Classification models, hyperparameter tuning, and country-grouped cross-validation (`GroupKFold`). |
| **🟢 MODULE 10:** | **Deployment & Web Application:** Integrating trained models into a Flask backend paired with a standalone HTML/JS client interface. |

---

## 🛠️ Tech Stack & Tools

* **Language:** Python 3.10+
* **Data Processing & Analytics:** NumPy, Pandas, SciPy
* **Data Visualization:** Matplotlib, Seaborn
* **Machine Learning & Statistics:** Scikit-Learn, Statsmodels, XGBoost, Imbalanced-Learn
* **Deployment & APIs:** Flask, Native HTML/JS Client
* **Learning Environment:** Jupyter Notebooks, VS Code, NotebookLM
* **Instant Access:** All my excercises from every branch (each branch its a different module, ergo different notebook excercise.) are converted to markdown with cell output prints, you can find them from main in "docs" folder, aswell the theory and corrections in the same folder. Also you can find my cheatsheets, scripts and prompts (the one i used to reestructure the original course) in the "Background" folder.
---

## 📍 Related Repositories

* 📂 **Original Repository (4GA.DataScience):** [JosBerGon34/4GA.DataScience](https://github.com/JosBerGon34/4GA.DataScience)
* 📂 **Remodeled Repository (DataScienceCourse):** Current repository.

---
*Maintained and refactored by [JosBerGon34](https://github.com/JosBerGon34).*
