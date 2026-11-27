# 🚀 DataScienceCourse: Course Remodel & Applied Refactoring

> **Original Repository:** [https://github.com/JosBerGon34/4GA.DataScience](https://github.com/JosBerGon34/4GA.DataScience)

This repository contains a **comprehensive curriculum redesign (Remodel) and synthesis (Summary)** of the **4Geeks Academy** Data Science program. The primary objective is to reshape the learning journey by replacing traditional toy exercises with an **applied, rigorous, and progressive** approach using real-world datasets that directly feed into the **Final Capstone Project**.

---

## 🎯 Remodeling Objectives

1. **Applied Learning with Real-World Datasets:**
   * **Eurostat:** Macroeconomic and quantitative data (GDP, Unemployment Rate, Public Debt, Inflation Rate).
   * **European Social Survey (ESS):** Sociological survey microdata (ordinal variables covering public attitudes, institutional trust, and political ideology).
   * **Web Scraping & Relational Storage:** Cultural, sports, and socio-relational preference datasets scraped by country and persisted in SQL databases.

2. **Direct Alignment with the Capstone Pipeline:**
   * Every module—ranging from native Python data manipulation and calculus optimization to SQL persistence, EDA, cleaning, and feature engineering—actively builds the exact tools and data structures needed for the multi-level sociopolitical prediction pipeline.

3. **Methodological Rigor & Technical Best Practices:**
   * Eliminating common anti-patterns and experimental flaws (e.g., proper missing data handling without truncating valid extreme survey responses `0` and `10`, country-grouped splits `GroupKFold` to prevent data leakage, and feature contract validation by name).

---

## 🗺️ Course Structure & Syllabus (`git checkout main`)

The curriculum is structured into progressive modules moving from foundational core concepts to production deployment and interactive dashboards:

| Module | Applied Focus & Statement | Branch Checkout |
| :--- | :--- | :--- |
| **🟢 MODULE 1** | **Native Python & Code Optimization:**<br>• **1.1:** Native Data Structures, Strict Typing & Eurostat Averages.<br>• **1.2:** Code Refactoring, Pipeline Optimization & Primality Testing. | `git checkout Module1.1`<br>`git checkout Module1.2` |
| **🟢 MODULE 2** | **Linear Algebra & Calculus for ML:**<br>• **2.1:** Calculus & Linear Algebra for Machine Learning.<br>• **2.2:** Partial Derivatives, Loss Functions & Gradient Optimization. | `git checkout Module2.1`<br>`git checkout Module2.2` |
| **🟢 MODULE 3** | **Git, Web Scraping & Relational Persistence:**<br>• **3.1:** Standard Version Control & Git Flow for Data Science.<br>• **3.2:** Modern Web Scraping for Data Science.<br>• **3.3:** Relational Persistence with SQLAlchemy Core & DuckDB-SQLite. | `git checkout Module3.1`<br>`git checkout Module3.2b`<br>`git checkout Module3.3` |
| **🟢 MODULE 4** | **Probability & Bayesian Statistics:**<br>• **4.1:** Probability Fundamentals, Random Variables & Analytical CDF-PDF.<br>• **4.2:** Expectation, Variance & Bayesian Updating. | `git checkout Module4.1`<br>`git checkout Module4.2` |
| **🟢 MODULE 5** | **NumPy & Pandas:**<br>• **5.1:** High-Performance Data Ingestion, Merging & Reshaping. | `git checkout MOdule5.1` |
| **🟢 MODULE 6** | **Data Cleaning & Statistical Profiling:**<br>• **6.1:** Data Cleaning & Imputation — Advanced Survey Non-Response Codes (`77, 88, 99`) & Imputation Strategies.<br>• **6.2:** Statistical Profiling, Variable Typologies & Transformation Techniques. | `git checkout Module6.1`<br>`git checkout Module6.2` |
| **🟢 MODULE 7** | **Exploratory Data Analysis (EDA):**<br>• **7.1:** Exploratory Data Analysis (EDA), Stratified Distributions & Correlation Diagnostics. | `git checkout Module7.1` |
| **🟢 MODULE 8** | **Feature Engineering & Resampling:**<br>• **8.1:** Feature Engineering, PCA & Calibrated Resampling (SMOTE). | `git checkout Module8.1` |
| **🟢 MODULE 9** | **Predictive Modeling & Validation:**<br>• **9.1:** Predictive Modeling, Ablation Study & Country-Grouped Cross-Validation (`GroupKFold`). | `git checkout Module9.1` |
| **🟢 MODULE 10** | **Deployment, APIs & Interactive Dashboards:**<br>• **10.1:** Model Serialization, REST API Backend (Flask) and Standalone HTML/JS Client.<br>• **10.2:** Interactive Time Series EDA & Forecasting Dashboard (Plotly Dash). | `git checkout Module10.1`<br>`git checkout Module10.2` |
| **🎓 CAPSTONE** | **Final Capstone Project:** Multi-Level Modeling of European Sociopolitical & Attitudinal Outcomes (End-to-End Pipeline). | `git checkout Project`  |

---

## 🛠️ Tech Stack & Tools

* **Language:** Python 3.10+
* **Data Processing & Databases:** NumPy, Pandas, SciPy, SQLAlchemy, DuckDB, SQLite
* **Data Visualization & Dashboards:** Matplotlib, Seaborn, Plotly Dash
* **Machine Learning & Statistics:** Scikit-Learn, Statsmodels, XGBoost, Imbalanced-Learn
* **Deployment & APIs:** Flask, FastAPI, Native HTML/JS Client
* **Learning Environment:** Jupyter Notebooks, VS Code, NotebookLM
* **Instant Access:** All exercises from every branch (each branch corresponds to a module/submodule notebook) are converted to Markdown with cell output prints in the `docs/` folder, alongside theory notes and corrections. Cheatsheets, setup scripts, and the restructuring prompts used to refactor the original course are located in the `Background/` folder.

---

## 📍 Related Repositories

* 📂 **Original Repository (4GA.DataScience):** [JosBerGon34/4GA.DataScience](https://github.com/JosBerGon34/4GA.DataScience)
* 📂 **Remodeled Repository (DataScienceCourse):** [JosBerGon34/DataScienceCourse](https://github.com/JosBerGon34/DataScienceCourse) Current repository.

---

## 📖 DataScience Course Web Viewer

* [🗺️ Course Navigator Index](https://josbergon34.github.io/DataScienceCourse/)

*Maintained and refactored by [JosBerGon34](https://github.com/JosBerGon34).*