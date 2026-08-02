### 💻 2. Applied Theory: Reference Implementation in Python / NumPy

```
import numpy as np

def compute_vector_geometry_demo():
    # 1. Feature Representation (Unscaled)
    # Dimension 0: netustm (0-300 minutes)
    # Dimension 1: ppltrst (0-10 social trust)
    # Dimension 2: rlgdgr  (0-10 religiosity)
    # Dimension 3: ccnthum (1-5 climate perception)
    
    u = np.array([180.0, 7.0, 2.0, 4.0], dtype=np.float64)  # Country A
    v = np.array([210.0, 5.0, 6.0, 3.0], dtype=np.float64)  # Country B

    # 2. Dot Product
    dot_prod = np.dot(u, v)

    # 3. L2 Norms & Euclidean Distance
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    raw_euclidean_dist = np.linalg.norm(u - v)

    # 4. Cosine Similarity
    cosine_sim = dot_prod / (norm_u * norm_v)

    # 5. Orthogonal Projection of u onto v
    proj_u_onto_v = (dot_prod / np.dot(v, v)) * v

    # 6. Min-Max Feature Scaling
    feat_min = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float64)
    feat_max = np.array([300.0, 10.0, 10.0, 5.0], dtype=np.float64)

    u_scaled = (u - feat_min) / (feat_max - feat_min)
    v_scaled = (v - feat_min) / (feat_max - feat_min)

    scaled_euclidean_dist = np.linalg.norm(u_scaled - v_scaled)

    # Print Results
    print(f"Raw Euclidean Distance: {raw_euclidean_dist:.4f}")
    print(f"Scaled Euclidean Distance: {scaled_euclidean_dist:.4f}")
    print(f"Dot Product: {dot_prod:.4f}")
    print(f"Cosine Similarity: {cosine_sim:.4f}")
    print(f"Projection Vector proj_v(u): {proj_u_onto_v}")

if __name__ == "__main__":
    compute_vector_geometry_demo()
```

## 🎯 ASSIGNMENT STATEMENT: Exercise 2.1

### **Vector Operations, Distance Metrics & Feature Projections in Socio-Economic Microdata**

#### **Context & Goal**

In quantitative sociology and comparative political economy, country profiles are represented as continuous feature vectors derived from aggregated survey microdata (e.g., European Social Survey). Distance metrics determine cluster membership (e.g., $k$-means), while orthogonal projections isolate specific sub-dimensional influences.

You are tasked with building a modular, vectorized geometric analysis engine using `NumPy`.

#### **Tasks & Requirements**

1. **Vector Specification**:
    
    Construct two 1D NumPy arrays with `dtype=np.float64`:
    
    - $\mathbf{u} = [180.0, 7.0, 2.0, 4.0]^T$ (Country A)
        
    - $\mathbf{v} = [210.0, 5.0, 6.0, 3.0]^T$ (Country B)
        
2. **Function Implementation**:
    
    Write a Python function `compute_vector_metrics(u: np.ndarray, v: np.ndarray) -> dict` that computes and returns a dictionary containing:
    
    - `'dot_product'`: $\mathbf{u}^T \mathbf{v}$
        
    - `'l2_norm_u'`: $\Vert{}\mathbf{u}\Vert{}_2$
        
    - `'l2_norm_v'`: $\Vert{}\mathbf{v}\Vert{}_2$
        
    - `'euclidean_distance'`: $\Vert{}\mathbf{u} - \mathbf{v}\Vert{}_2$
        
    - `'cosine_similarity'`: $\frac{\mathbf{u}^T \mathbf{v}}{\Vert{}\mathbf{u}\Vert{}_2 \Vert{}\mathbf{v}\Vert{}_2}$
        
    - `'projection_u_on_v'`: $\text{proj}_{\mathbf{v}}(\mathbf{u}) = \left(\frac{\mathbf{u}^T \mathbf{v}}{\mathbf{v}^T \mathbf{v}}\right)\mathbf{v}$
        
3. **Normalization Analysis**:
    
    Given feature domain bounds:
    
    $$\mathbf{x}_{\min} = [0.0, 0.0, 0.0, 1.0]^T, \quad \mathbf{x}_{\max} = [300.0, 10.0, 10.0, 5.0]^T$$
    
    - Transform $\mathbf{u}$ and $\mathbf{v}$ into $\mathbf{u}_{\text{scaled}}$ and $\mathbf{v}_{\text{scaled}}$ using Min-Max scaling.
        
    - Compute `'scaled_euclidean_distance'`.
        
    - In a docstring/markdown comment, explain why the raw Euclidean distance ($\approx 30.33$) was heavily dominated by the `netustm` feature (dimension 0), and how Min-Max scaling balances feature weight distribution across dimensions.

Excercise 2.1
Explanation: 
This excercise try to make us understand, the variables could be converted in to dots inside a multiplanar space, if we have exactly the location and the variables group
totally defined. We can make vectors betwen 2 dot locations groups, in this method we use one variable as clasify parameter, this reason will be the path of our vector.
For starting we will make a mean with values of variables identified on the example of this excercise. For setup a coherent hiperplanar dot(wich will describe the standard status of variables) for Spain and Germany.

# 1. Feature Representation (Unscaled)
    # Dimension 0: netustm (0-300 minutes)
    # Dimension 1: ppltrst (0-10 social trust)
    # Dimension 2: rlgdgr  (0-10 religiosity)
    # Dimension 3: ccnthum (1-5 climate perception)
#We can check the meaning and structure of variables on "./DataScienceCourse/Background/Prompts/PromptRegeneracionAsignatura.md"


```python
from pathlib import Path
import os
import pandas as pd
import random
import numpy as np
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
print(ROOT,DATA_TABLES)
```

    /home/josu/Documentos/DataScienceCourse /home/josu/Documentos/DataScienceCourse/data/raw/Tables



```python
#Lets prepare the variables for our main vectors U(Spanish Vector), V(German Vector).
# 1. We load the dataframe, after this we will filter for cntry values, and then we will prepare the data with min max.
dfESPDEraw = pd.read_csv(DATA_TABLES / "EssSurveys.csv")
```


```python
dfESPDEraw.info()
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



```python

# 2. Filter dataframe grouping by countries with the instruction .isin())

targetcountries: list[str] = ['DE', 'ES']
dfESPDEf0 = dfESPDEraw[dfESPDEraw["cntry"].isin(targetcountries)]
```


```python
dfESPDEf0.info()
```

    <class 'pandas.DataFrame'>
    RangeIndex: 4264 entries, 1594 to 5857
    Data columns (total 31 columns):
     #   Column    Non-Null Count  Dtype  
    ---  ------    --------------  -----  
     0   name      4264 non-null   str    
     1   essround  4264 non-null   int64  
     2   edition   4264 non-null   float64
     3   proddate  4264 non-null   str    
     4   idno      4264 non-null   int64  
     5   cntry     4264 non-null   str    
     6   dweight   4264 non-null   float64
     7   pspwght   4264 non-null   float64
     8   pweight   4264 non-null   float64
     9   anweight  4264 non-null   float64
     10  netustm   4264 non-null   int64  
     11  ppltrst   4264 non-null   int64  
     12  trstplt   4264 non-null   int64  
     13  bctprd    4264 non-null   int64  
     14  prtdgcl   4264 non-null   float64
     15  lrscale   4264 non-null   int64  
     16  happy     4264 non-null   int64  
     17  aesfdrk   4264 non-null   int64  
     18  health    4264 non-null   int64  
     19  rlgdnm    4264 non-null   int64  
     20  rlgdgr    4264 non-null   int64  
     21  ccnthum   4264 non-null   int64  
     22  hhmmb     4264 non-null   int64  
     23  gndr      4264 non-null   int64  
     24  agegroup  4264 non-null   int64  
     25  marsts    4264 non-null   int64  
     26  chldhhe   4264 non-null   int64  
     27  edulvlb   4264 non-null   int64  
     28  prob      4264 non-null   float64
     29  stratum   4264 non-null   int64  
     30  psu       4264 non-null   int64  
    dtypes: float64(7), int64(21), str(3)
    memory usage: 1.0 MB



```python
#Lets prepare the minmaxed dataset, its a must for visualize the data with a good perspective on the hiperplanar
#all the variables will have their variability representated between 0 and 1.
#So the distribution will be clearly understandable in a coherent proportion.
#1. Feature Representation (Unscaled)
    # Dimension 0: netustm (0-300 minutes)
    # Dimension 1: ppltrst (0-10 social trust)
    # Dimension 2: rlgdgr  (0-10 religiosity)
    # Dimension 3: ccnthum (1-5 climate perception)
    
from sklearn.preprocessing import MinMaxScaler

#Dimensions to Normalize  with standard min max.
dimensions = ["netustm", "ppltrst", "rlgdgr", "ccnthum"]

# Lets create our scaler script.
scaler = MinMaxScaler()

# We create dfESPDEf1 with the normalized variables only
dfESPDEf1 = dfESPDEf0[dimensions].copy()

# Apply the minmax.
dfESPDEf1[dimensions] = scaler.fit_transform(dfESPDEf1[dimensions])

# Append again cntry column
dfESPDEf1["cntry"] = dfESPDEf0["cntry"].values
    
    

```


```python
#Lets check all de dataframe info, and its content:
dfESPDEf1.info()

print(
    f"\n| DF content:\n{dfESPDEf1.head()}"
    f"\n\n| Var Description:\n{dfESPDEf1.describe()}"
)
```

    <class 'pandas.DataFrame'>
    RangeIndex: 4264 entries, 1594 to 5857
    Data columns (total 5 columns):
     #   Column   Non-Null Count  Dtype  
    ---  ------   --------------  -----  
     0   netustm  4264 non-null   float64
     1   ppltrst  4264 non-null   float64
     2   rlgdgr   4264 non-null   float64
     3   ccnthum  4264 non-null   float64
     4   cntry    4264 non-null   str    
    dtypes: float64(4), str(1)
    memory usage: 166.7 KB
    
    | DF content:
           netustm   ppltrst    rlgdgr   ccnthum cntry
    1594  0.060756  0.000000  0.113636  0.022989    DE
    1595  0.020252  0.090909  0.022727  0.034483    DE
    1596  0.020252  0.056818  0.113636  0.022989    DE
    1597  0.033753  0.056818  0.034091  0.011494    DE
    1598  0.074257  0.090909  0.000000  0.034483    DE
    
    | Var Description:
               netustm      ppltrst       rlgdgr      ccnthum
    count  4264.000000  4264.000000  4264.000000  4264.000000
    mean      0.148111     0.060360     0.047696     0.041726
    std       0.270897     0.037590     0.056463     0.104970
    min       0.000000     0.000000     0.000000     0.000000
    25%       0.013501     0.045455     0.011364     0.022989
    50%       0.027003     0.056818     0.045455     0.034483
    75%       0.067507     0.079545     0.079545     0.034483
    max       1.000000     1.000000     1.000000     1.000000



```python
# 3 Lets create class vectors for Spain(U) and Germany(V), throught logic mask vectorization.
# As we can see under, we make a boolean mask to upload all the data of dataframe throught this rule in to the variable, also we declare the values in to the
#numpy array position.

#We can check the meaning and structure of variables on "./DataScienceCourse/Background/Prompts/PromptRegeneracionAsignatura.md"
VectUesp = np.array(dfESPDEf1[dfESPDEf1["cntry"] == "ES"][["netustm","ppltrst", "rlgdgr", "ccnthum"]].mean())
VectVger= np.array(dfESPDEf1[dfESPDEf1["cntry"] == "DE"][["netustm","ppltrst", "rlgdgr", "ccnthum"]].mean())

```


```python
print(f"EspDist: {VectUesp} | GerDist: {VectVger}")
```

    EspDist: [0.17224966 0.06217955 0.04985457 0.0521293 ] | GerDist: [0.12971822 0.05897352 0.0460509  0.0337988 ]



```python

#Although these variables are ordinal, their numerical encoding allows us to
#construct an exploratory vector space. The resulting decimal values represent
#distribution centroids rather than actual response categories. Preserving their
#precision allows subtle positional differences between groups to be captured
#by vector metrics, without interpreting the centroids as literal modal or
#median categories.
#Lets do the function to calculate euclidian metrics, with our main template:

import numpy as np

def compute_vector_metrics(u: np.ndarray, v: np.ndarray) -> dict:
    """
    Calculate vectorial metrics and its distances
    for their socioeconomy reasons (all data must be float)

    """
    # 1.Dot Product
    dot_product = np.dot(u, v)
    
    # 2. L2 norm (Euclidean norms)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    
    # 3. Euclidian distance
    euclidean_dist = np.linalg.norm(u - v)
    
    # 4. Cosen simil
    cosine_sim = dot_product / (norm_u * norm_v)
    
    # 5. Ortogonal projection.
    proj_v_u = (dot_product / (norm_v ** 2)) * v
    
    return {
        "dot_product": float(dot_product),
        "euclidean_distance": float(euclidean_dist),
        "cosine_similarity": float(cosine_sim),
        "projection_vector": proj_v_u.tolist()
    }




resultados = compute_vector_metrics(u=VectUesp, v=VectVger)

print(resultados)

```

    {'dot_product': 0.030068621887681668, 'euclidean_distance': 0.0465797949289281, 'cosine_similarity': 0.9951289218177113, 'projection_vector': [0.16549947667408185, 0.07524067227692201, 0.05875350529658206, 0.043121808425323774]}



```python
#In conclusion:
#The centroid vector acts as a compact numerical signature of the central position of a cluster within the normalized feature space. 
#It does not uniquely identify the cluster as a cryptographic hash would, nor does it retain all of its density or internal distribution, but it allows you to efficiently compare its position, direction,
#and separation from other clusters using vector metrics. Important to normalize the data for not disturb the relative distances.
#Data summary:

print(
    f"\n|Spain country data cluster: \n{VectUesp}"
    f"\n\n|Germany country data cluster:\n{VectVger}"
    f"\n\n|Vectorial metrics Spain-Germany:\n{resultados}"
)
```

    
    |Spain country data cluster: 
    [0.17224966 0.06217955 0.04985457 0.0521293 ]
    
    |Germany country data cluster:
    [0.12971822 0.05897352 0.0460509  0.0337988 ]
    
    |Vectorial metrics Spain-Germany:
    {'dot_product': 0.030068621887681668, 'euclidean_distance': 0.0465797949289281, 'cosine_similarity': 0.9951289218177113, 'projection_vector': [0.16549947667408185, 0.07524067227692201, 0.05875350529658206, 0.043121808425323774]}

