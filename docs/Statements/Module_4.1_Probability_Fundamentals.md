

# 🟢 < Module 4.1 > Probability Fundamentals, Random Variables & Analytical CDF-PDF

## 🎯 Context & Objectives
To build reliable statistical models on socio-economic datasets (such as Eurostat macro indicators or ESS survey metrics), a Data Scientist must master probability spaces, joint and conditional probabilities, and continuous vs. discrete distributions[cite: 13].

In this exercise, you will model probability density functions (PDF) and cumulative distribution functions (CDF) using **SciPy Stats** and **NumPy**[cite: 13]. You will analyze the behavior of real socio-economic metrics (e.g., inflation rate distributions across European regions) by fitting continuous theoretical distributions (Gaussian / Normal, Log-Normal) and calculating theoretical vs. empirical probability intervals[cite: 13].

---

## 📑 Exercise Instructions

### 1. Syntactic / Algorithmic Level (Probability & SciPy Integration)
Create a Python notebook or script (`notebooks/04_1_probability_distributions.ipynb`) that implements the following technical steps[cite: 13]:

1. **Analytical Distribution Setup**:
   * Import `scipy.stats as stats`[cite: 13].
   * Define a theoretical Gaussian random variable $X \sim \mathcal{N}(\mu, \sigma^2)$ representing the European Inflation Rate, where $\mu = 3.5\%$ and $\sigma = 1.2\%$[cite: 13].
   * Evaluate and plot the Probability Density Function (PDF) $f(x)$ over the range $[\mu - 4\sigma, \mu + 4\sigma]$[cite: 13].

2. **Probability Intervals & Inverse CDF**:
   * Calculate the cumulative probability $P(X \le 4.0 \%)$ using `stats.norm.cdf()`[cite: 13].
   * Compute the symmetric $95\%$ probability interval $[x_{\text{low}}, x_{\text{high}}]$ using the Percent Point Function (Inverse CDF) `stats.norm.ppf()`[cite: 13].

---

### 2. Applied Data Science Level (Empirical Fitting on Master Dataset)
Evaluate whether your merged master dataset's economic metrics follow standard continuous distributions[cite: 13]:

1. **Empirical Evaluation**:
   * Load the master country feature table generated in Exercise 3.3 (`macro_features_matrix_2015_2025` from PostgreSQL/DuckDB or CSV)[cite: 13].
   * Select a target numerical feature (e.g., inflation rate or demographic percentage)[cite: 13].
   * Estimate empirical mean ($\hat{\mu}$) and empirical standard deviation ($\hat{\sigma}$)[cite: 13].

2. **Theoretical vs. Empirical Comparison**:
   * Overlay the empirical histogram (`density=True`) with the fitted continuous Normal curve using `matplotlib.pyplot` or `seaborn`[cite: 13].
   * Calculate the Kolmogorov-Smirnov test (`stats.kstest`) to statistically test if the empirical metric significantly deviates from a theoretical Normal distribution[cite: 13].

---

## 🌐 Official References & Documentation
* **SciPy Stats Official Documentation**: [scipy.stats API Reference](https://docs.scipy.org/doc/scipy/reference/stats.html)[cite: 13]
* **SciPy Normal Distribution (norm)**: [scipy.stats.norm](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html)[cite: 13]

---
> 💻 **Your Challenge:** Create the notebook `notebooks/04_1_probability_distributions.ipynb` locally, run the SciPy analytical computations and empirical KS-test, and verify your distributions before moving on to Module 4.2! 🚀📊[cite: 13]

