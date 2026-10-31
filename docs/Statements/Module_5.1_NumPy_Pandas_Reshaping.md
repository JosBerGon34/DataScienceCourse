'''Markdown

🟢 < Module 5.1 > NumPy & Pandas — High-Performance Data Ingestion, Merging & Reshaping

#### 🎯 Context & Objectives

In real-world data science pipelines, analytical data arrives fragmented across multiple sources (macroeconomic files from Eurostat, individual survey microdata waves from the European Social Survey, and scraped categorical attributes). To feed downstream machine learning models without introducing memory leaks or data corruption, a Data Scientist must master vectorized data manipulation, memory-efficient type casting, and relational merging using NumPy and Pandas.

In this exercise, you will build an optimized ingestion pipeline that merges multi-source datasets, restructures data shapes using pivot/melt operations, and handles complex multi-index groupings.

#### 📑 Exercise Instructions

##### 1. Syntactic / Algorithmic Level (Vectorized Operations & Reshaping)

Create a Python notebook or script (`notebooks/05_1_numpy_pandas_operations.ipynb`) that implements the following technical steps:

- **Vectorized Array Operations**:
    
    - Perform high-performance vectorized calculations on NumPy arrays (e.g., calculating standardized z-scores across multi-dimensional macro matrices without explicit Python `for` loops).
        
- **Data Reshaping (Wide vs. Long Formats)**:
    
    - Take a wide Eurostat macroeconomic table (where years are represented as individual columns) and transform it into a clean long-format tidy dataset using `pd.melt()`.
        
    - Reconstruct the wide matrix back using `pd.pivot_table()`, ensuring multi-level column indexing is properly flattened and cleaned.
        

##### 2. Applied / Data Level (Multi-Source Relational Merging)

Apply advanced Pandas joining techniques to your project datasets:

- **Relational Merging & Key Alignment**:
    
    - Load your cleaned CSV/DuckDB exports for country metadata (`GlobalCountriesLang.csv`), macroeconomic features, and ESS survey summaries.
        
    - Perform inner and outer joins (`pd.merge()`) using compound keys (e.g., country code `cntry` / `geo` and survey year/round) to prevent row explosion or silent data loss.
        
- **Hierarchical Groupings & Aggregations**:
    
    - Group the merged master dataset by macro-economic region clusters (`cntgrp_fc`) and compute multi-metric aggregated summaries (mean, median, IQR) for institutional trust variables.
        

#### 🌐 Official References for Documentation

- **Pandas Merging / Joining Guide**: [Pandas Merge, Join, and Concatenate Documentation](https://pandas.pydata.org/docs/user_guide/merging.html)
    
- **Pandas Reshaping Guide**: [Reshaping and Pivot Tables Documentation](https://pandas.pydata.org/docs/user_guide/reshaping.html)
    

#### 📚 Recommended Manuals & CheatSheets

- **Pandas Cheat Sheet**: [DataCamp Pandas Cheat Sheet (PDF)](https://www.google.com/search?q=https://www.datacamp.com/cheat-sheet/pandas-cheat-sheet)
    

💻 **Your Challenge:** Crea el cuaderno `notebooks/05_1_numpy_pandas_operations.ipynb` en tu entorno local, ejecuta las transformaciones y fusiones de alto rendimiento con tus datasets, y pásame tu código o resultados cuando estés listo para avanzar al Módulo 6 (Data Cleaning & Imputation).

'''