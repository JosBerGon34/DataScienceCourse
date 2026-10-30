[← Volver al Índice General](../index.md){: .back-to-index }

### 🎯 Context & Objectives

To build reliable statistical models on socio-economic datasets (such as Eurostat macro indicators or ESS survey metrics), a Data Scientist must master probability spaces, joint and conditional probabilities, and continuous vs. discrete distributions.

In this exercise, you will model probability density functions (PDF) and cumulative distribution functions (CDF) using **SciPy Stats** and **NumPy**. You will analyze the behavior of real socio-economic metrics (e.g., inflation rate distributions across European regions) by fitting continuous theoretical distributions (Gaussian / Normal, Log-Normal) and calculating theoretical vs. empirical probability intervals.

### 📑 Exercise Instructions

#### 1. Syntactic / Algorithmic Level (Probability & SciPy Integration)

Create a Python notebook or script (`notebooks/04_1_probability_distributions.ipynb`) that implements the following technical steps:

1. **Analytical Distribution Setup**:
    
    - Import `scipy.stats` as `stats`.
        
    - Define a theoretical Gaussian random variable $X \sim \mathcal{N}(\mu, \sigma^2)$ representing the European Inflation Rate, where $\mu = 3.5\%$ and $\sigma = 1.2\%$.
        
    - Evaluate and plot the Probability Density Function (PDF) $f(x)$ over the range $[\mu - 4\sigma, \mu + 4\sigma]$.
        
2. **Probability Intervals & Inverse CDF**:
    
    - Calculate the cumulative probability $P(X \le 4.0\%)$ using `stats.norm.cdf()`.
        
    - Compute the symmetric $95\%$ probability interval $[x_{\text{low}}, x_{\text{high}}]$ using the Percent Point Function (Inverse CDF) `stats.norm.ppf()`.
        

#### 2. Applied Data Science Level (Empirical Fitting on Master Dataset)

Evaluate whether your merged master dataset's economic metrics follow standard continuous distributions:

1. **Empirical Evaluation**:
    
    - Load the master country feature table generated in Exercise 3.3 (`macro_features_matrix_2015_2025` from PostgreSQL/DuckDB or CSV).
        
    - Select a target numerical feature (e.g., `inflationpct_2015_2025` or `demographicpct`).
        
    - Estimate empirical mean ($\hat{\mu}$) and empirical standard deviation ($\hat{\sigma}$).
        
2. **Theoretical vs. Empirical Comparison**:
    
    - Overlay the empirical histogram (`density=True`) with the fitted continuous Normal curve using `matplotlib.pyplot` or `seaborn`.
        
    - Calculate the Kolmogorov-Smirnov test (`stats.kstest`) to statistically test if the empirical metric significantly deviates from a theoretical Normal distribution.
        

### 🌐 Official References for Documentation

- **SciPy Stats Official Documentation**: [scipy.stats API Reference](https://docs.scipy.org/doc/scipy/reference/stats.html)
    
- **SciPy Normal Distribution (`norm`)**: [scipy.stats.norm](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html)
    

### 📚 Recommended Manuals & CheatSheets

- **Python SciPy Cheatsheet**: [DataCamp SciPy Cheat Sheet (PDF)](https://www.datacamp.com/cheat-sheet/scipy-cheat-sheet-linear-algebra-in-python)
    
- **Seaborn Statistical Visualization**: [Seaborn Distribution Plots Guide](https://seaborn.pydata.org/tutorial/distributions.html)
    

💻 **Your Challenge**: Create the notebook `notebooks/04_1_probability_distributions.ipynb` in your local environment, run the SciPy analytical computations and empirical KS-test, and paste your code/results when ready.

When you finish, we will proceed to **Exercise 4.2: Expectation, Variance & Bayesian Upda**