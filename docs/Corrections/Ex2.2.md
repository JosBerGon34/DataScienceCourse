📘 Lesson 2.2: Partial Derivatives, Loss Functions & Gradient Optimization.

Example Structure Data:
'''
Imagine we want to model how socio-economic satisfaction depends on GDP growth rate(x1) and Social trust(x2)
We will build a simple linear regression model (y^=W1X1 +W2X2)  using synthetic data based on European Social Survey (ESS) and Eurostat metrics:

import numpy as np

# Synthetic Dataset: 4 Countries [x1: GDP Growth %, x2: Social Trust (0-10)]
X = np.array([
    [1.5, 7.0],  # Country A gender male
    [3.0, 5.0],  # Country A gender female
    [0.5, 8.5],  # Country B gender male
    [2.0, 4.0]   # Country B gender female
], dtype=np.float64)

# Target: Overall Life Satisfaction (0-10 scale)
y = np.array([7.2, 6.1, 8.0, 5.0], dtype=np.float64)

Exercise:

Step 1: Prepare your data from your tables, for example get data about spain and germany and divide the samples by gender,
then chose data related with people trust and life satisfaction, the best variables that collects semanticly
this fact is Gini coeficient or Available family Brute Rent. 
Step 2: Implement MSE Loss: Create a function compute_mse(X, y, w)

Step 3: Implement Gradient Calculation: Create a function compute_gradient(X, y, w)
that computes and returns the analytical gradient vector ∇L(w)

Step 4: Write an optimization loop fit_gradient_descent(X, y, lr=0.01, epochs=100) that:
    -Initializes weights w^(0)=[0,0,0.0]
    -Iteratively updates weights using w^(t+1)= w^(t) -η∇L(w^(t))
    -Tracks and prints the loss every 20 epochs.
    -Returns the optimized weights  w* and the loss history.


```python
from pathlib import Path
import os
import pandas as pd
import numpy as np
import random
#PATHING SCRIPT FOR EVERY EXCERSISE - PROJECT - WORKSPACE
# 1.Literal definition of route pathings(Every user of remote repository must config this pathing in order to find the local repository of his computer)
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
#Step 1: Data Select and preparation.
#We decide to select GiniCoef as economic data for the exercice (https://es.wikipedia.org/wiki/Coeficiente_de_Gini)
#X1=GiniCoef(from Spain and Germany)
'''
# Gini Coefficient Summary:
# -------------------------
# Measures income/wealth inequality within a population.
# Range: 0 to 1 (unitless index).
# - 0: Perfect equality (everyone has the same income).
# - 1: Perfect inequality (one person has all the income).
# Note: Sometimes expressed as a percentage (0 to 100).
# Derived from the Lorenz curve; higher values indicate greater disparity.
'''


dfGini =pd.read_csv(DATA_TABLES/"GiniCoefEU.csv")
```


```python
dfGini.info()

print(
    f"\n|DfGini content:\n{dfGini.head()}"
    f"\n\n|Var Description: \n{dfGini.describe()}"
)
```

    <class 'pandas.DataFrame'>
    RangeIndex: 870 entries, 0 to 869
    Data columns (total 10 columns):
     #   Column       Non-Null Count  Dtype  
    ---  ------       --------------  -----  
     0   DATAFLOW     870 non-null    str    
     1   LAST UPDATE  870 non-null    str    
     2   freq         870 non-null    str    
     3   age          870 non-null    str    
     4   statinfo     870 non-null    str    
     5   geo          870 non-null    str    
     6   TIME_PERIOD  870 non-null    int64  
     7   OBS_VALUE    870 non-null    float64
     8   OBS_FLAG     54 non-null     str    
     9   CONF_STATUS  0 non-null      float64
    dtypes: float64(2), int64(1), str(7)
    memory usage: 68.1 KB
    
    |DfGini content:
                  DATAFLOW        LAST UPDATE freq    age  statinfo geo  \
    0  ESTAT:ILC_DI12(1.0)  08/06/26 23:00:00    A  TOTAL  GINI_HND  AL   
    1  ESTAT:ILC_DI12(1.0)  08/06/26 23:00:00    A  TOTAL  GINI_HND  AL   
    2  ESTAT:ILC_DI12(1.0)  08/06/26 23:00:00    A  TOTAL  GINI_HND  AL   
    3  ESTAT:ILC_DI12(1.0)  08/06/26 23:00:00    A  TOTAL  GINI_HND  AL   
    4  ESTAT:ILC_DI12(1.0)  08/06/26 23:00:00    A  TOTAL  GINI_HND  AL   
    
       TIME_PERIOD  OBS_VALUE OBS_FLAG  CONF_STATUS  
    0         2017       36.8      NaN          NaN  
    1         2018       35.4      NaN          NaN  
    2         2019       34.3      NaN          NaN  
    3         2020       33.2      NaN          NaN  
    4         2021       33.0      NaN          NaN  
    
    |Var Description: 
           TIME_PERIOD   OBS_VALUE  CONF_STATUS
    count   870.000000  870.000000          0.0
    mean   2019.393103   30.056552          NaN
    std       3.409787    4.964868          NaN
    min    2014.000000   20.600000          NaN
    25%    2016.000000   26.600000          NaN
    50%    2019.000000   29.700000          NaN
    75%    2022.000000   32.700000          NaN
    max    2025.000000   46.800000          NaN



```python
#Lets filter the dataframe with the columns we want, grouping by
#discriminative values from 'geo'(countries), 'TIME_PERIOD', 'age'(it is calculated for ppl with less age than 18,
#and a global calculation for every age)
#At the same time we exclude other columns we dont want.
countries_gini: list[str]=['DE','ES']
year_gini = [2025]
age_gini: list[str]=['TOTAL']
#This vectorized one-line code applies a compound Boolean mask.
#Only rows satisfying all three conditions simultaneously are stored in dfGinif0.
#The column selection at the end of the expression also ensures that
#the new DataFrame contains only the three columns required for the analysis.
dfGinif0 = dfGini[dfGini["geo"].isin(countries_gini) & dfGini["TIME_PERIOD"].isin(year_gini) & dfGini["age"].isin(age_gini)][["geo", "TIME_PERIOD", "OBS_VALUE"]]

print(dfGinif0.head())
```

        geo  TIME_PERIOD  OBS_VALUE
    89   DE         2025       30.1
    150  ES         2025       30.8



```python
#import gc
#Recomended to delete deprecated variables and dataframes from previous steps.
#We can use this one for delete all local variables '%reset -f'
#gc.collect()
del dfGini
del age_gini
del year_gini
del countries_gini
```


```python
#In this case, Gini coeficient is expressed at OBS_VALUE column, 
#and its transformed in to float from 0.0 to 100.0
#Step1:
#Lets prepare the other 2 variables: X2=ppltrst(trust in others ppl from society),
# Y1=happy (overall life satisfaction)
# it will be filtered by gender and country reasons.
dfSurvey =pd.read_csv(DATA_TABLES/ "EssSurveys.csv")
dfSurvey.info()

print(
    f"\n|DfSurvey content:\n{dfSurvey.head()}"
    f"\n\n|Var Description: \n{dfSurvey.describe()}"
)

```

    <class 'pandas.DataFrame'>
    RangeIndex: 24602 entries, 0 to 24601
    Data columns (total 31 columns):
     #   Column    Non-Null Count  Dtype  
    ---  ------    --------------  -----  
     0   name      24602 non-null  str    
     1   essround  24602 non-null  int64  
     2   edition   24602 non-null  float64
     3   proddate  24602 non-null  str    
     4   idno      24602 non-null  int64  
     5   cntry     24602 non-null  str    
     6   dweight   24602 non-null  float64
     7   pspwght   24602 non-null  float64
     8   pweight   24602 non-null  float64
     9   anweight  24602 non-null  float64
     10  netustm   24602 non-null  int64  
     11  ppltrst   24602 non-null  int64  
     12  trstplt   24602 non-null  int64  
     13  bctprd    24602 non-null  int64  
     14  prtdgcl   23008 non-null  float64
     15  lrscale   24602 non-null  int64  
     16  happy     24602 non-null  int64  
     17  aesfdrk   24602 non-null  int64  
     18  health    24602 non-null  int64  
     19  rlgdnm    24602 non-null  int64  
     20  rlgdgr    24602 non-null  int64  
     21  ccnthum   24602 non-null  int64  
     22  hhmmb     24602 non-null  int64  
     23  gndr      24602 non-null  int64  
     24  agegroup  24602 non-null  int64  
     25  marsts    24602 non-null  int64  
     26  chldhhe   24602 non-null  int64  
     27  edulvlb   24602 non-null  int64  
     28  prob      24602 non-null  float64
     29  stratum   24602 non-null  int64  
     30  psu       24602 non-null  int64  
    dtypes: float64(7), int64(21), str(3)
    memory usage: 5.8 MB
    
    |DfSurvey content:
             name  essround  edition    proddate   idno cntry   dweight   pspwght  \
    0  ESS11e04_2        11      4.2  02.07.2026  50002    BE  1.014926  1.395880   
    1  ESS11e04_2        11      4.2  02.07.2026  50029    BE  1.014926  0.818828   
    2  ESS11e04_2        11      4.2  02.07.2026  50106    BE  1.014926  0.671998   
    3  ESS11e04_2        11      4.2  02.07.2026  50183    BE  1.014926  1.546446   
    4  ESS11e04_2        11      4.2  02.07.2026  50225    BE  1.014926  0.999171   
    
        pweight  anweight  ...  ccnthum  hhmmb  gndr  agegroup  marsts  chldhhe  \
    0  0.615074  0.858569  ...        4      2     2         1       6        6   
    1  0.615074  0.503640  ...        4      2     1         5      66        2   
    2  0.615074  0.413328  ...        3      3     1         5       6        2   
    3  0.615074  0.951178  ...        4      4     1         2       6        2   
    4  0.615074  0.614564  ...        4      6     1         3      66        6   
    
       edulvlb      prob  stratum   psu  
    0      413  0.000529      160   895  
    1      323  0.000529      158  1001  
    2      610  0.000529      161   955  
    3      710  0.000529      163  1066  
    4      423  0.000529      158  1025  
    
    [5 rows x 31 columns]
    
    |Var Description: 
           essround       edition          idno       dweight       pspwght  \
    count   24602.0  2.460200e+04  24602.000000  24602.000000  24602.000000   
    mean       11.0  4.200000e+00  69024.974189      1.000232      1.000000   
    std         0.0  8.881965e-16  11241.644530      0.272284      0.566334   
    min        11.0  4.200000e+00  50002.000000      0.142119      0.118618   
    25%        11.0  4.200000e+00  59408.000000      0.936796      0.695008   
    50%        11.0  4.200000e+00  68803.000000      0.998706      0.909871   
    75%        11.0  4.200000e+00  78286.000000      1.012759      1.154037   
    max        11.0  4.200000e+00  99403.000000      4.042132      4.342649   
    
                pweight      anweight       netustm       ppltrst       trstplt  \
    count  24602.000000  24602.000000  24602.000000  24602.000000  24602.000000   
    mean       1.418892      1.418892   1464.778148      5.460450      4.633607   
    std        1.135543      1.708731   2556.344212      4.666113      9.250238   
    min        0.211267      0.038882      0.000000      0.000000      0.000000   
    25%        0.342028      0.368696    120.000000      4.000000      2.000000   
    50%        0.745066      0.798156    240.000000      5.000000      4.000000   
    75%        2.253153      1.976135    600.000000      7.000000      6.000000   
    max        3.324269     12.997417   9999.000000     88.000000     99.000000   
    
           ...       ccnthum         hhmmb          gndr      agegroup  \
    count  ...  24602.000000  24602.000000  24602.000000  24602.000000   
    mean   ...      5.582473      3.137550      1.519104      4.634786   
    std    ...     12.626807      6.703359      0.499645      7.101080   
    min    ...      1.000000      1.000000      1.000000      1.000000   
    25%    ...      3.000000      2.000000      1.000000      3.000000   
    50%    ...      4.000000      2.000000      2.000000      4.000000   
    75%    ...      4.000000      3.000000      2.000000      6.000000   
    max    ...     99.000000     99.000000      2.000000     99.000000   
    
                 marsts       chldhhe       edulvlb          prob       stratum  \
    count  24602.000000  24602.000000  24602.000000  24602.000000  24602.000000   
    mean      34.923014      2.984757    458.198195      0.000471    732.462442   
    std       30.523349      2.175310    655.867848      0.000418    350.685627   
    min        1.000000      1.000000      0.000000      0.000028    116.000000   
    25%        6.000000      1.000000    311.000000      0.000125    412.000000   
    50%        6.000000      2.000000    322.000000      0.000342    680.000000   
    75%       66.000000      6.000000    610.000000      0.000757    993.000000   
    max       99.000000      9.000000   9999.000000      0.004807   1405.000000   
    
                    psu  
    count  24602.000000  
    mean   12269.735184  
    std     6046.873004  
    min      846.000000  
    25%     7982.250000  
    50%    10838.500000  
    75%    16194.000000  
    max    24391.000000  
    
    [8 rows x 28 columns]



```python
#We will chose the values from 'ppltrst'(X2) and 'happy'(Y1)
#filtering for -gender column 'gndr'
#and country column 'cntry' via 'DE' and 'ES' values.
from pandas.core.common import random_state


random.seed(13)
country_surveys: list[str] = ['DE', 'ES']
gender_surveys:  list[int] = [1,2]
    # 1 = Male, 2 = Female, 9 = No answer (unclassified, bugged sample)
dfSurveyf0= dfSurvey[dfSurvey["cntry"].isin(country_surveys) 
                  & dfSurvey["gndr"].isin(gender_surveys)][["cntry", "gndr", "happy","ppltrst"]]

#After using a compound boolean mask, we apply a random sampling.
dfSurveyf1= dfSurveyf0.sample(n=150, random_state=13).reset_index(drop=True)

#Clear Cache and notebook variables.


#Lets get some information about DataSet

dfSurveyf1.info()
print(
    f"\n|DfSurveyf1 content:\n{dfSurveyf1.head()}"
    f"\n\n|Var Description: \n{dfSurveyf1.describe()}"
)              
del dfSurvey, dfSurveyf0, country_surveys, gender_surveys

```

    <class 'pandas.DataFrame'>
    RangeIndex: 150 entries, 0 to 149
    Data columns (total 4 columns):
     #   Column   Non-Null Count  Dtype
    ---  ------   --------------  -----
     0   cntry    150 non-null    str  
     1   gndr     150 non-null    int64
     2   happy    150 non-null    int64
     3   ppltrst  150 non-null    int64
    dtypes: int64(3), str(1)
    memory usage: 4.8 KB
    
    |DfSurveyf1 content:
      cntry  gndr  happy  ppltrst
    0    ES     2      8        7
    1    DE     1      8        7
    2    ES     1      8        8
    3    DE     2      8        2
    4    DE     1      9        6
    
    |Var Description: 
                 gndr       happy     ppltrst
    count  150.000000  150.000000  150.000000
    mean     1.506667    7.613333    5.020000
    std      0.501630    1.690029    2.406563
    min      1.000000    0.000000    0.000000
    25%      1.000000    7.000000    3.000000
    50%      2.000000    8.000000    5.000000
    75%      2.000000    9.000000    7.000000
    max      2.000000   10.000000   10.000000



```python
#Lets clear the samples with no utility in this exercise,
#specificly the ordinal values attending to No Answer from
#respondent user.

'''
-happy 
77	Refusal*
88	Don't know*
99	No answer*

-ppltrst
77	Refusal*
88	Don't know*
99	No answer*
'''


happydelvalue: list[int]=[77,88,99]
#We use a vectorized NAND boolean mask in to the lines of the datasets.
#We can use isin refering the Not with ~ sign before the boolean mask statement
#For each column we filter

dfSurveyf2 = dfSurveyf1[
    (~dfSurveyf1["happy"].isin(happydelvalue))
    & (~dfSurveyf1["ppltrst"].isin(happydelvalue))
]


#Lets get some information about DataSet

dfSurveyf2.info()
print(
    f"\n|DfSurveyf2 content:\n{dfSurveyf2.head()}"
    f"\n\n|Var Description: \n{dfSurveyf2.describe()}"
)              


```

    <class 'pandas.DataFrame'>
    RangeIndex: 150 entries, 0 to 149
    Data columns (total 4 columns):
     #   Column   Non-Null Count  Dtype
    ---  ------   --------------  -----
     0   cntry    150 non-null    str  
     1   gndr     150 non-null    int64
     2   happy    150 non-null    int64
     3   ppltrst  150 non-null    int64
    dtypes: int64(3), str(1)
    memory usage: 4.8 KB
    
    |DfSurveyf2 content:
      cntry  gndr  happy  ppltrst
    0    ES     2      8        7
    1    DE     1      8        7
    2    ES     1      8        8
    3    DE     2      8        2
    4    DE     1      9        6
    
    |Var Description: 
                 gndr       happy     ppltrst
    count  150.000000  150.000000  150.000000
    mean     1.506667    7.613333    5.020000
    std      0.501630    1.690029    2.406563
    min      1.000000    0.000000    0.000000
    25%      1.000000    7.000000    3.000000
    50%      2.000000    8.000000    5.000000
    75%      2.000000    9.000000    7.000000
    max      2.000000   10.000000   10.000000



```python
#Lets reset de index setting the parameter to delete old index(drop=true)
#with a new ordered index, starting from zero
#We must select also (inplace=True) to allowing this command
#Overwrite in the existent dataframe
#dfSurveyf2.reset_index(drop=True, inplace=True)
del dfSurveyf1, happydelvalue
dfSurveyf2.head()
```




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
      <th>cntry</th>
      <th>gndr</th>
      <th>happy</th>
      <th>ppltrst</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ES</td>
      <td>2</td>
      <td>8</td>
      <td>7</td>
    </tr>
    <tr>
      <th>1</th>
      <td>DE</td>
      <td>1</td>
      <td>8</td>
      <td>7</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ES</td>
      <td>1</td>
      <td>8</td>
      <td>8</td>
    </tr>
    <tr>
      <th>3</th>
      <td>DE</td>
      <td>2</td>
      <td>8</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>DE</td>
      <td>1</td>
      <td>9</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>




```python
#STEP2:
#Lets create the arrays for implement MSE Lose, Gradient calculation, and Gradient Descent Loop:
#First location of the X array corresponds to Gini Coef applying a boolean mask
#discriminating by 'geo' that is the country
#Second location of X array will be the mean value of social trust filtering
#via boolean mask, discriminatig by 'cntry' and 'gndr' values.
#The four arrays of X , corresponds to 4 different samples, 1st:Country A('ES') is Spain and gender male(1) , 
#2nd: Country A and gender female(2)
#3d: Country B('DE') that is Germany and gender male
#4th: Conttry B and gender female.

X = np.array([
    [
        dfGinif0[dfGinif0["geo"] == "ES"]["OBS_VALUE"].iloc[0],
        dfSurveyf2[
            (dfSurveyf2["cntry"] == "ES")
            & (dfSurveyf2["gndr"] == 1)
        ]["ppltrst"].mean()
    ],

    [
        dfGinif0[dfGinif0["geo"] == "ES"]["OBS_VALUE"].iloc[0],
        dfSurveyf2[
            (dfSurveyf2["cntry"] == "ES")
            & (dfSurveyf2["gndr"] == 2)
        ]["ppltrst"].mean()
    ],

    [
        dfGinif0[dfGinif0["geo"] == "DE"]["OBS_VALUE"].iloc[0],
        dfSurveyf2[
            (dfSurveyf2["cntry"] == "DE")
            & (dfSurveyf2["gndr"] == 1)
        ]["ppltrst"].mean()
    ],

    [
        dfGinif0[dfGinif0["geo"] == "DE"]["OBS_VALUE"].iloc[0],
        dfSurveyf2[
            (dfSurveyf2["cntry"] == "DE")
            & (dfSurveyf2["gndr"] == 2)
        ]["ppltrst"].mean()
    ]
], dtype=np.float64)

print(X)
```

    [[30.8         5.125     ]
     [30.8         4.94117647]
     [30.1         4.95238095]
     [30.1         5.07142857]]



```python
#2.1
#Lets define the corresponding 4 values of Y array  (one value for each subgroup already defined)
#np.array([a, b, c, d])          # vector 1D → (4,)

#np.array([[a], [b], [c], [d]])  # matriz 2D → (4, 1)

#np.array([[a, b], [c, d]])      # matriz 2D → (2, 2)
#Our y must be a vector 1D.

y = np.array([
    
       dfSurveyf2[
            (dfSurveyf2["cntry"] == "ES")
            & (dfSurveyf2["gndr"] == 1)
       ]["happy"].mean()
    ,
    
       dfSurveyf2[
            (dfSurveyf2["cntry"] == "ES")
            & (dfSurveyf2["gndr"] == 2)
       ]["happy"].mean()
    ,
    
       dfSurveyf2[
            (dfSurveyf2["cntry"] == "DE")
            & (dfSurveyf2["gndr"] == 1)
       ]["happy"].mean()
    ,
    
       dfSurveyf2[
            (dfSurveyf2["cntry"] == "DE")
            & (dfSurveyf2["gndr"] == 2)
       ]["happy"].mean()
    ,
    
    
    
])

print(
    f"\n|y array1 value:\n{y}"
    f"\n| Dimensions of X 2D array:\n{X.shape}"
    f"\n\n| Dimensions of y 1D vector array:\n{y.shape}"
)

```

    
    |y array1 value:
    [7.875      7.38235294 7.52380952 7.69047619]
    | Dimensions of X 2D array:
    (4, 2)
    
    | Dimensions of y 1D vector array:
    (4,)



```python
#STEP 3:
#3.1 implement MSE Loss, create a function compute_mse(x,y,w) 
#that returns the scalar MSE loss for given weights (w)
#Lets calculate first the weights, then we make the function for calculate MSE loss:

# Algebraic Normal Equation solution
w = np.linalg.inv(X.T @ X) @ X.T @ y

print("Calculated weights (w):")
print(w)
```

    Calculated weights (w):
    [-0.0994786   2.11992165]



```python
import numpy as np
#3.1 lets create MSE loss function
def compute_mse(X, y, w):
    # 1. Calculate predictions: X dot w
    y_pred = X.dot(w)
    
    # 2. Calculate MSE: Mean of Squared Errors
    # The square (**2) must be INSIDE the mean function
    mse = np.mean((y - y_pred) ** 2)
    
    return mse

# Example Usage

loss = compute_mse(X, y, w)
print(f"MSE loss: {loss}")   
```

    MSE loss: 0.002778247318383842



```python
#3.2 Making "Implement Gradient Calculation" function compute_gradient(X, y, w)


def compute_gradient(X, y, w):
    # 1. Calculate N sample rate
    N = X.shape[0]
    
    # 2. Calcular target feature prediction with (Xw)
    y_pred = X.dot(w)
    
    # 3. Calculate error vector (Xw - y)
    error = y_pred - y
    
    # 4.Apply the formula (2/N) * X^T * error
    # X.T is the transposed matrix of X
    gradient = (2 / N) * X.T.dot(error)
    
    return gradient

# we dont need to save variable inputs because they are
# Already loaded.

grad = compute_gradient(X, y, w)
print(f"Gradient: {grad}")   
```

    Gradient: [-6.39055475e-11 -1.05559034e-11]



```python
#3.3 Lets Make a function for optimize the loop, gradient_descent
#with these conditions:
#the weights starts at w^0=[0.0,0.0]
#Iteratively updates weights using w^(t+1)= w^t - η∇L(w^(t))

import numpy as np

def gradient_descent(X, y, theta, alpha, iterations):
    # Inicialize estrictly with w=[0.0,0.0]
    w = np.zeros(X.shape[1])
    m = len(y)
    
    for i in range(iterations):
        # 1. Prediction
        y_pred = X.dot(w)
        
        # 2. Error and Gradient
        error = y_pred - y
        gradient = (2 / m) * X.T.dot(error)
        
        # 3. Weight update
        w = w - alpha * gradient
        
        # 4. Print every 20 iterations or epochs, applying a boolean mask
        # Looking in the residue , when it worths 0.
        if i % 20 == 0:
            # Calculate the income loss for showing it.
            current_loss = np.mean((y - y_pred) ** 2)
            print(f"Iteración {i}: Loss = {current_loss:.4f} | Pesos = {w}")
            
    return w
```


```python
#3.3 Lets introduce inputs to make the function run:
# X,y and w already are loaded in the memory of the notebook.

# Parámetros
theta_inicial = np.array([99.0, 99.0]) # This value will be ignored, the function resets w value.
alpha = 0.01 #The maximum step of gradient loop.
iterations = 100 #As the excercise demands.

# Execution
w_descent_loop = gradient_descent(X, y, theta_inicial, alpha, iterations)

print(f"Required Initial weights: [0.0, 0.0]")
print(f"Optimized weights: {w_descent_loop}")
```

    Iteración 0: Loss = 58.0665 | Pesos = [4.63938235 0.76549678]
    Iteración 20: Loss = 10559954500021586730649963775235651449396251949268992.0000 | Pesos = [5.93007802e+25 9.78024315e+24]
    Iteración 40: Loss = 1921698926668810560511130010865850116990797419820475676335100811043543344144312858404259066126475984896.0000 | Pesos = [7.99966973e+50 1.31935389e+50]
    Iteración 60: Loss = 349710480736683708684956181107172993249289616666453934890851707731960747570381243021590761263989025863295853770010264745816609824713748988791845103337472.0000 | Pesos = [1.07915470e+76 1.77980717e+75]
    Iteración 80: Loss = 63640260521496061713643077082649387338685737792940078550210239519808695588490711435260904948162865027680379294981709961630619929544996316604766429583838590745826383731183020950800908285491570680583421952.0000 | Pesos = [1.45577869e+101 2.40095822e+100]
    Pesos iniciales requeridos: [0.0, 0.0]
    Pesos optimizados: [-1.08794371e+125 -1.79430253e+124]



```python
#As we can observe the numbers arent, coherent, due the gap of scales.
#We can try to minmax X features to have a relative calculation.
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

print(X_scaled)
```

    [[1.         1.        ]
     [1.         0.        ]
     [0.         0.06095238]
     [0.         0.70857143]]



```python
w_descent_loop = gradient_descent(X_scaled, y, theta_inicial, alpha, iterations)

print(f"Required Initial weights wih X scaled minmax: [0.0, 0.0]")
print(f"Optimized weights wih X scaled minmax: {w_descent_loop}")
```

    Iteración 0: Loss = 58.0665 | Pesos = [0.07628676 0.06891423]
    Iteración 20: Loss = 41.7545 | Pesos = [1.38893436 1.27354386]
    Iteración 40: Loss = 32.4130 | Pesos = [2.36577719 2.20289321]
    Iteración 60: Loss = 27.0549 | Pesos = [3.08993486 2.92290563]
    Iteración 80: Loss = 23.9743 | Pesos = [3.6241389  3.48350089]
    Required Initial weights wih X scaled minmax: [0.0, 0.0]
    Optimized weights wih X scaled minmax: [3.99893818 3.90295046]



```python
#Looks like now our weights increases coherently and mse loss decreases fairly, but not enough,
#In this example i think 100 iterations looks like are not enough to optimize the process.
#Lets try with 1000iterations to finish the excercice.
iterations=1000
w_descent_loop = gradient_descent(X_scaled, y, theta_inicial, alpha, iterations)

print(f"Required Initial weights wih X scaled minmax and 1000epochs: [0.0, 0.0]")
print(f"Optimized weights wih X scaled minmax and 1000epochs: {w_descent_loop}")
```

    Iteración 0: Loss = 58.0665 | Pesos = [0.07628676 0.06891423]
    Iteración 20: Loss = 41.7545 | Pesos = [1.38893436 1.27354386]
    Iteración 40: Loss = 32.4130 | Pesos = [2.36577719 2.20289321]
    Iteración 60: Loss = 27.0549 | Pesos = [3.08993486 2.92290563]
    Iteración 80: Loss = 23.9743 | Pesos = [3.6241389  3.48350089]
    Iteración 100: Loss = 22.1970 | Pesos = [4.01572082 3.92248491]
    Iteración 120: Loss = 21.1662 | Pesos = [4.30038075 4.26850439]
    Iteración 140: Loss = 20.5638 | Pesos = [4.50503465 4.54327975]
    Iteración 160: Loss = 20.2078 | Pesos = [4.6499653  4.76329271]
    Iteración 180: Loss = 19.9942 | Pesos = [4.75044734 4.94106176]
    Iteración 200: Loss = 19.8632 | Pesos = [4.81797483 5.08610627]
    Iteración 220: Loss = 19.7806 | Pesos = [4.86118856 5.20567526]
    Iteración 240: Loss = 19.7267 | Pesos = [4.8865765 5.3052984]
    Iteración 260: Loss = 19.6901 | Pesos = [4.8990028 5.3892025]
    Iteración 280: Loss = 19.6642 | Pesos = [4.90210734 5.4606266 ]
    Iteración 300: Loss = 19.6450 | Pesos = [4.89860743 5.52206022]
    Iteración 320: Loss = 19.6303 | Pesos = [4.89052557 5.57542355]
    Iteración 340: Loss = 19.6186 | Pesos = [4.87936143 5.62220395]
    Iteración 360: Loss = 19.6091 | Pesos = [4.86622163 5.66355911]
    Iteración 380: Loss = 19.6012 | Pesos = [4.85191764 5.7003953 ]
    Iteración 400: Loss = 19.5946 | Pesos = [4.83703964 5.73342662]
    Iteración 420: Loss = 19.5890 | Pesos = [4.82201223 5.76321991]
    Iteración 440: Loss = 19.5842 | Pesos = [4.80713636 5.7902288 ]
    Iteración 460: Loss = 19.5801 | Pesos = [4.79262097 5.81481969]
    Iteración 480: Loss = 19.5766 | Pesos = [4.77860674 5.83729133]
    Iteración 500: Loss = 19.5736 | Pesos = [4.76518399 5.85788991]
    Iteración 520: Loss = 19.5709 | Pesos = [4.7524061  5.87682039]
    Iteración 540: Loss = 19.5687 | Pesos = [4.74029958 5.89425532]
    Iteración 560: Loss = 19.5667 | Pesos = [4.7288716 5.9103415]
    Iteración 580: Loss = 19.5650 | Pesos = [4.7181156  5.92520514]
    Iteración 600: Loss = 19.5636 | Pesos = [4.70801551 5.93895579]
    Iteración 620: Loss = 19.5623 | Pesos = [4.69854884 5.95168947]
    Iteración 640: Loss = 19.5612 | Pesos = [4.68968896 5.963491  ]
    Iteración 660: Loss = 19.5602 | Pesos = [4.68140681 5.97443594]
    Iteración 680: Loss = 19.5594 | Pesos = [4.67367209 5.98459198]
    Iteración 700: Loss = 19.5587 | Pesos = [4.66645416 5.99402019]
    Iteración 720: Loss = 19.5581 | Pesos = [4.65972266 6.00277591]
    Iteración 740: Loss = 19.5576 | Pesos = [4.65344796 6.01090952]
    Iteración 760: Loss = 19.5571 | Pesos = [4.64760143 6.01846703]
    Iteración 780: Loss = 19.5567 | Pesos = [4.64215563 6.02549062]
    Iteración 800: Loss = 19.5564 | Pesos = [4.63708445 6.03201907]
    Iteración 820: Loss = 19.5561 | Pesos = [4.63236314 6.03808806]
    Iteración 840: Loss = 19.5558 | Pesos = [4.62796831 6.04373053]
    Iteración 860: Loss = 19.5556 | Pesos = [4.62387799 6.0489769 ]
    Iteración 880: Loss = 19.5554 | Pesos = [4.62007149 6.05385531]
    Iteración 900: Loss = 19.5552 | Pesos = [4.61652947 6.05839184]
    Iteración 920: Loss = 19.5551 | Pesos = [4.61323379 6.06261064]
    Iteración 940: Loss = 19.5550 | Pesos = [4.6101675  6.06653411]
    Iteración 960: Loss = 19.5549 | Pesos = [4.6073148  6.07018302]
    Iteración 980: Loss = 19.5548 | Pesos = [4.60466089 6.07357669]
    Required Initial weights wih X scaled minmax and 1000epochs: [0.0, 0.0]
    Optimized weights wih X scaled minmax and 1000epochs: [4.60231127 6.07658058]


# Our best score is around iteration 860:
# Loss = 19.5556 | Weights = [4.62387799, 6.0489769]
# 1 
# Increasing the number of training iterations does not necessarily produce
# a significantly better result once Gradient Descent approaches convergence.
# The final performance is also limited by the model architecture, the available
# features, the dataset, and the selected hyperparameters.
# 2
# Another important conclusion from this exercise is that understanding where
# models and libraries come from is essential.
# 2.1
# Learning the mathematical and algebraic foundations behind an algorithm makes
# it much easier to understand how a model works internally instead of treating
# it as a black box.
# 2.2
# It is also important to understand the computational representation of that
# mathematics: Python syntax, NumPy arrays, matrix dimensions, shapes, and the
# correct structure of X, y, and the weight vector w.
# 2.3
# A mathematically correct idea can still produce incorrect results if its
# computational representation is wrong. Understanding both layers — mathematics
# and implementation — makes debugging and model interpretation much easier.


```python
# For finish lets use a terminal trick to convert all our ipynb notebook including
# Cell outputs printing.
# In this case, ill not export assets (pictures, graphics, etc).
# 1st step: of all you have to commit and push your project, remember to execute all notebooks before,
# 2nd step: save your project in your Jupyter lab or VSCode program.
# 3d step : Second click on your ipynb file and open integrated terminal.
# If u have fish or powershell type bash in the terminal to swap to bash lenguage.
# 4th step: for generate a md without assets
# Type: jupyter nbconvert --to markdown your_notebook.ipynb 
```
