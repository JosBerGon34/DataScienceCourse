🟢 < Module 4.2 > Expectation, Variance & Bayesian Updating

#### 🎯 Context & Objectives

In advanced socio-economic modeling, understanding central tendencies and dispersion is not enough; Data Scientists must quantify the expected value and variance of discrete and continuous random variables. Furthermore, when new data arrives (e.g., updated Eurostat macroeconomic releases or sequential European Social Survey waves), we must update our prior beliefs using **Bayesian Updating**.

In this exercise, you will implement mathematical expectation and variance computations, explore properties of linear combinations of random variables, and program a conjugate Bayesian update (Beta-Binomial model) to estimate the true proportion of public trust in European institutions based on survey samples.

#### 📑 Exercise Instructions

##### 1. Syntactic / Algorithmic Level (Expectation & Variance)

Create a Python notebook or script (`notebooks/Ex4.2.ipynb`) that implements the following technical steps:

- **Discrete Expectation & Variance**:
    
    - Define a discrete probability mass function (PMF) representing an ordinal survey score (e.g., political interest levels or institutional trust categories from 1 to 4).
        
    - Calculate the mathematical expectation $E[X] = \sum x_i P(X = x_i)$ and variance $Var(X) = E[X^2] - (E[X])^2$ manually using NumPy arrays, and verify your results against `scipy.stats`.
        
- **Continuous Variance Scaling**:
    
    - Take a continuous distribution (e.g., Gaussian inflation model from Exercise 4.1) and calculate the theoretical variance and standard deviation under linear scaling transformations ($Y = aX + b$).
        

##### 2. Applied / Data Level (Bayesian Updating on Survey Metrics)

Apply Bayesian inference to real survey microdata proportions:

- **Conjugate Beta-Binomial Update**:
    
    - Define a prior Beta distribution $\text{Beta}(\alpha_0, \beta_0)$ representing prior beliefs about a proportion (e.g., proportion of citizens showing high trust in politician system 'ppltrst').
        
    - Extract empirical counts (successes/failures) from your cleaned ESS master dataset subset for a specific European country.
        
    - Compute the posterior Beta distribution parameters ($\alpha_{new} = \alpha_0 + \text{successes}$, $\beta_{new} = \beta_0 + \text{failures}$).
        
    - Plot and compare the Prior, Likelihood, and Posterior probability density functions using `scipy.stats.beta`.
        

#### 🌐 Official References for Documentation

- **SciPy Stats Beta Distribution**: [scipy.stats.beta API Reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html)
    
- **NumPy Mathematical Functions**: [NumPy Statistics Documentation](https://numpy.org/doc/stable/reference/routines.statistics.html)
    

#### 📚 Recommended Manuals & CheatSheets

- **Python Probability & Statistics Cheatsheet**: [DataCamp Probability Cheat Sheet](https://www.google.com/search?q=https://www.datacamp.com/cheat-sheet/probability-and-statistics-cheat-sheet&authuser=1)
    

💻 **Your Challenge:** Create the notebook `notebooks/04_2_expectation_bayes.ipynb` in your local environment, run the analytical expectations and Bayesian updating steps, and paste your code/results here when ready.


```python
from pathlib import Path
import os
import pandas as pd
import random

#PATHING SCRIPT FOR EVERY EXCERSISE - PROJECT - WORKSPACE
# Literal definition of route pathings(Every user of remote repository must config this pathing in order to find the local repository of his computer)
# My case:
ROOT = Path("/home/josu/Documentos/DataScienceCourse")

# We verify the existence before continue
if not ROOT.exists():
    raise FileNotFoundError(f"❌ The route {ROOT} doesn't exist. Check it.")

# 2. Fix the workspace
os.chdir(ROOT)
print(f"✅ Worskspace enabled!: {os.getcwd()}")

# 3. Define relative pathings to work properly
DATA_TABLES = ROOT / "data" / "raw" / "Tables"

# Let's verify our table folder:
if not DATA_TABLES.exists():
    # If it fails, monitorize the issue: 
    data_dir = ROOT / "data"
    if data_dir.exists():
        print(f"⚠️ the folder 'data' exists but it doesn't have any 'Tables'. 'data' content: {os.listdir(data_dir)}")
    else:
        print(f"⚠️ The folder 'data' doesn't exist on ROOT workspace: {os.listdir(ROOT)}")
    raise FileNotFoundError(f"❌ The tables route {DATA_TABLES} is missing.")

print(f"📂 Tables route detected: {DATA_TABLES}")
```

    ✅ Worskspace enabled!: /home/josu/Documentos/DataScienceCourse
    📂 Tables route detected: /home/josu/Documentos/DataScienceCourse/data/raw/Tables



```python
#1)Discrete Expectation & Variance: Lets chose a table to get an ordinal variable to define the discrete mass function PMF:
# for example lets make the exercise with 'trstplt'
#We make our first filter(easy filtering) to save memory in the dataframe csv calling:
import pandas as pd
import numpy as np
import random
dfsurvey = (
    pd.read_csv(DATA_TABLES / 'EssSurveys.csv', usecols=['cntry', 'trstplt'])
    .sample(n=2500, random_state=42)
    .reset_index(drop=True)
)
```

#LETS check how we make a PMF from our discrete data in scipy wiki.
-------------------------------------
scipy.stats.rv_discrete.
pmf
pmf(k, *args, **kwds)[source]
Probability mass function at k of the given RV.

Parameters
:
k
array_like
Quantiles.

arg1, arg2, arg3,…
array_like
The shape parameter(s) for the distribution (see docstring of the instance object for more information)

loc
array_like, optional
Location parameter (default=0).

Returns
:
pmf
array_like
Probability mass function evaluated at k
----------------------------------------
#k its the unique values our column has. "k = np.unique(dfsurvey['trstplt'])" or calculate it
# Manually with operations min and max 'np.min() y np.max()'
#We will see the percentage of probability our unique value has on this 500rows to appear.



```python
#So our PMF looks like this :
import scipy.stats
import numpy as np
from scipy.stats import binom

k = np.unique(dfsurvey['trstplt'])
PMF = dfsurvey['trstplt'].value_counts(normalize=True).reindex(k, fill_value=0)
print(f"valores unicos 'trstplt': {k}  \n| funcion empirica PMF: {PMF}")
```

    valores unicos 'trstplt': [ 0  1  2  3  4  5  6  7  8  9 10 77 88 99]  
    | funcion empirica PMF: trstplt
    0     0.1528
    1     0.0712
    2     0.1260
    3     0.1220
    4     0.1076
    5     0.1616
    6     0.1172
    7     0.0808
    8     0.0356
    9     0.0100
    10    0.0032
    77    0.0036
    88    0.0080
    99    0.0004
    Name: proportion, dtype: float64



```python
# Continuous Variance Scaling: Now lets choose a continuous gaussian variable from our csv's or databases:
#In this case we must make a connection with a local database, and do easy filtering to extract only
# a dataframe with just our target column = inflationpct_2015_2025

import duckdb as db
import os
from dotenv import load_dotenv
load_dotenv()  # search .env on the directory
con = db.connect()
con.execute("ATTACH '' AS db (TYPE postgres, SCHEMA 'public')")
```




    <_duckdb.DuckDBPyConnection at 0x7f2c4c82d1b0>




```python
#Lets pick macro_features_matrix_2015_2025 and select only one column.
dfinflation = con.sql("SELECT inflationpct_2015_2025 FROM db.macro_features_matrix_2015_2025").df()
```


```python
#lets calculate theoretical variance and standard deviation 
x = dfinflation['inflationpct_2015_2025']

# Parametros originales (de describe)
var_x = x.var()
sd_x  = x.std()
lo, hi = x.min(), x.max()

# Escalamiento min-max
y = (x - lo) / (hi - lo)

# theorical variability (formula)
var_y_theo = var_x / (hi - lo)**2
sd_y_theo  = sd_x  / (hi - lo)

# Empirical variability (verification)
var_y_emp = y.var()
sd_y_emp  = y.std()

print(f"Var teórica: {var_y_theo:.6f}")
print(f"Var empírica: {var_y_emp:.6f}")  # THey must be equal.
```

    Var teórica: 0.067090
    Var empírica: 0.067090



```python
#2 Conjugate Beta-Binomial Update:
import numpy as np
import pandas as pd
from scipy.stats import beta
import matplotlib.pyplot as plt
#Lets define a country with high participation, in my case Belgium.
dfsurveys = (
    pd.read_csv(DATA_TABLES / 'EssSurveys.csv', usecols=['cntry', 'ppltrst'])
    .sample(n=2500, random_state=42)
    .reset_index(drop=True)
)
#Country filter
df_pais = dfsurveys[dfsurveys['cntry'] == 'BE'].reset_index(drop=True)

# Filter the unique values variable, deleting non contested samples
df_pais = df_pais[df_pais['ppltrst'].between(0, 10)].reset_index(drop=True)   


# Define "success" = high trust (ppltrst >= 7 => 10)
umbral = 7
n = len(df_pais)
k = int((df_pais['ppltrst'] >= umbral).sum())   # success
n_k = n - k                                      # failures

print(f"Country: {pais}, n={n}, sucesses (>=7)={k}, failures={n_k}")
print(f"Empirical percentage: {k/n:.3f}")

# Prior, means from 5 cases you expect an1 success and bn2 failures.
a0, b0 = 2, 3

# After.
a1 = a0 + k
b1 = b0 + n_k

print(f"\nPrior:     Beta({a0}, {b0})  → media={a0/(a0+b0):.3f}")
print(f"After: Beta({a1}, {b1})  → media={a1/(a1+b1):.3f}")

# Plot
x = np.linspace(0, 1, 500)
prior = beta.pdf(x, a0, b0)
likelihood = beta.pdf(x, k + 1, n_k + 1)  # Likelihood shape (Beta(k+1, n-k+1))
posterior = beta.pdf(x, a1, b1)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, prior, label=f'Prior Beta({a0},{b0})', lw=2)
ax.plot(x, likelihood, label=f'Likelihood ~Beta({k+1},{n_k+1})', lw=2, ls='--')
ax.plot(x, posterior, label=f'After Beta({a1},{b1})', lw=2, ls='-.')
ax.set_xlabel('p (high trust proportion)')
ax.set_ylabel('Density')
ax.set_title(f'Beta-Binomial Update — {pais} (n={n}, k={k})')
ax.legend()
plt.tight_layout()
plt.show()
```

    Country: BE, n=153, sucesses (>=7)=65, failures=88
    Empirical percentage: 0.425
    
    Prior:     Beta(2, 3)  → media=0.400
    After: Beta(67, 91)  → media=0.424



    
![png](Ex4.2_files/Ex4.2_9_1.png)
    



```python

```
