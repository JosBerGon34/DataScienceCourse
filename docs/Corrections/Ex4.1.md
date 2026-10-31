🟢 < Module 4.1 > Probability Fundamentals, Random Variables & Analytical CDF-PDF


### 🎯 Context & Objectives

To build reliable statistical models on socio-economic datasets (such as Eurostat macro indicators or ESS survey metrics), a Data Scientist must master probability spaces, joint and conditional probabilities, and continuous vs. discrete distributions.

In this exercise, you will model probability density functions (PDF) and cumulative distribution functions (CDF) using **SciPy Stats** and **NumPy**. You will analyze the behavior of real socio-economic metrics (e.g., inflation rate distributions across European regions) by fitting continuous theoretical distributions (Gaussian / Normal, Log-Normal) and calculating theoretical vs. empirical probability intervals.

### 📑 Exercise Instructions

#### 1. Syntactic / Algorithmic Level (Probability & SciPy Integration)

Create a Python notebook or script (`notebooks/Ex4.1.ipynb`) that implements the following technical steps:

1. **Analytical Distribution Setup**:
    
    - Import `scipy.stats` as `stats`.
        
    - Define a theoretical Gaussian random variable $X \sim \mathcal{N}(\mu, \sigma^2)$ representing the European Inflation Rate, where $\mu = 3.5\%$ and $\sigma = 1.2\%$.
        
    - Evaluate and plot the Probability Density Function (PDF) $f(x)$ over the range $[\mu - 4\sigma, \mu + 4\sigma]$.

```Python
import scipy.stats as stats
# loc = media (μ), scale = desviación estándar (σ)
inflacion_dist = stats.norm(loc=3.5, scale=1.2)
```

1. **Probability Intervals & Inverse CDF**:
    
    - Calculate the cumulative probability $P(X \le 4.0\%)$ using `stats.norm.cdf()`.
        
    - Compute the symmetric $95\%$ probability interval $[x_{\text{low}}, x_{\text{high}}]$ using the Percent Point Function (Inverse CDF) `stats.norm.ppf()`.

```Python
import numpy as np
eje_x = np.linspace(3.5 - 4*1.2, 3.5 + 4*1.2, 1000) # De μ-4σ a μ+4σ
curva_y = inflacion_dist.pdf(eje_x) # Mapeo de la función f(x)
```


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


```python
import duckdb
import pandas as pd

# 1. Lets initiate duckdb on memory
con = duckdb.connect()

# 2. Let's install the PostgreSQL extension on DuckDB
con.execute("LOAD postgres;")

# 3. We connect DuckDb on our local database
con.execute("ATTACH 'postgresql://Practice:12345@localhost:5432/DataScienceCourse' AS pg_db (TYPE postgres);")

# 4. We do the precharge query to filter.
query = """
    SELECT inflationpct_2015_2025 
    FROM pg_db.macro_features_matrix_2015_2025 
    WHERE inflationpct_2015_2025 IS NOT NULL
"""

# 5. Lets make the dataframe for the excercise
df = con.execute(query).df()

# Also the array, just with the data values.
inflacion_array = df['inflationpct_2015_2025'].values
```


```python
import scipy.stats as stats
import numpy as np

# 1. Calculate the mean, and also the standard deviation.
# the mean is the medium value of y range for the whole limit(number of samples) of the variable
media_empirica = np.mean(inflacion_array)
# The standard deviation (std) "gives us an idea of how far the ranges of the samples are from the arithmetic mean. 
# Furthermore, the theory indicates that "with a larger number it means that more varies
std_empirica = np.std(inflacion_array)

print(f"Media empírica: {media_empirica:.2f}% | Desviación empírica: {std_empirica:.2f}%")
# We can also have a global overview of the main statistics with .describe(), it only works on dataframes
df.describe()

```

    Media empírica: 37.50% | Desviación empírica: 14.22%





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>inflationpct_2015_2025</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>28.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>37.501786</td>
    </tr>
    <tr>
      <th>std</th>
      <td>14.479060</td>
    </tr>
    <tr>
      <th>min</th>
      <td>18.060000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>25.635000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>33.920000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>49.162500</td>
    </tr>
    <tr>
      <th>max</th>
      <td>73.960000</td>
    </tr>
  </tbody>
</table>
</div>




```python
import scipy.stats as stats
import numpy as np

# 2. Test de Kolmogorov-Smirnov 
# Instance teoric distribution with our empiric data
distribucion_teorica = stats.norm(loc=media_empirica, scale=std_empirica)

# execute cdf function
ks_stat, p_value = stats.kstest(inflacion_array, distribucion_teorica.cdf)

print(f"Estadístico KS: {ks_stat:.4f}")
print(f"P-Valor: {p_value:.4e}")

# Revealing the data scenario
alpha = 0.05
if p_value < alpha:
    print("ALERT: We reject the null hipothesis, the data doesnt follow a normal gaussian function.")
else:
    print("ESTABLE: We can't reject a null hipothesis, the data follows a normal gaussian function.")
```

    Estadístico KS: 0.1415
    P-Valor: 5.8096e-01
    ESTABLE: We can't reject a null hipothesis, the data follows a normal gaussian function.



```python
#The null hipothesis means that we dont reject the idea the variables are just non correlated between them. When we do a DataScience study about a dataset it means that the variables may not be correlated.
#So there is variables out of registering affecting indirectly and correlating them or maybe are just totally unconnected.
#In this excercise is a bit more basic, we just are comparing a variable witha  normal gaussian shape, to determinate if the variable is affected by  a hidden factor, altering the normal gaussian shape that almost every variable has
```
