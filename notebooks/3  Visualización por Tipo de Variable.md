
---

## Índice

| Tipo de variable | Gráficos principales |
|-----------------|---------------------|
| **Continua** | Histograma + KDE, Boxplot, QQ-plot, Strip/Swarm plot, ECDF |
| **Discreta / Count** | Bar chart (si pocos valores), Histograma + KDE (si muchos), Boxplot, Strip plot |
| **Ordinal acotada (0-10)** | Countplot, Histograma + KDE, Boxplot, Ridgeline plot |
| **Ordinal pocos códigos (2-8)** | Countplot, Mosaic plot, Heatmap de transiciones |
| **Nominal / Categórica** | Bar chart, Mosaic plot, Heatmap de co-ocurrencia |
| **Comparación entre grupos** | Boxplot segmentado, Violin plot, Strip plot, Bar chart agrupado |
| **Relación entre 2 variables** | Scatter plot, Binned scatter, Pair plot |
| **Relación entre 3+ variables** | Pair plot, Heatmap de correlación, Parallel coordinates |
| **Distribución en el tiempo** | Line plot, Area chart, Rolling window |

---

## 1. VARIABLES CONTINUAS

### 1.1 Histograma + KDE

**Qué es:** Barras que muestran la frecuencia de valores en intervalos (bins) + una curva suave (Kernel Density Estimate) que estima la forma de la distribución.

**Por qué:** Es el gráfico **universal** para ver la forma de una continua. Te responde:
- ¿Es simétrica o asimétrica?
- ¿Es unimodal (un pico) o multimodal (varios picos)?
- ¿Dónde está la masa central?
- ¿Hay huecos (gaps) o valores imposibles?

**Cómo interpretarlo:**

| Lo que ves | Significado | Acción |
|-----------|-------------|--------|
| Un pico en el centro, colas simétricas | Distribución aproximadamente normal | OK para tests paramétricos |
| Pico a la izquierda, cola larga a la derecha | Skewness positiva (outliers altos) | Log transform, usar mediana |
| Pico a la derecha, cola larga a la izquierda | Skewness negativa | Revisar si hay un "suelo" artificial |
| Dos picos separados | Bimodalidad → hay dos subpoblaciones | Segmentar por una variable categórica |
| Pico enorme en un valor + cola | Masa puntual (ej. 95% en 0) | No es "continua" de facto → tratar como count |
| Hueco en medio | Valores imposibles o error de medición | Verificar el rango válido |
```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df['agea'], kde=True, bins=30, ax=ax, color='steelblue', alpha=0.6)
ax.axvline(df['agea'].median(), color='red', linestyle='--', label=f"Mediana = {df['agea'].median():.0f}")
ax.axvline(df['agea'].mean(), color='orange', linestyle='--', label=f"Media = {df['agea'].mean():.0f}")
ax.set_title('Distribución de edad')
ax.legend()
plt.show()   
```

**Variante: KDE solo (sin barras)**

Útil cuando hay muchos datos (>10k) y el histograma se ve "ruido". La curva es más limpia.

```python
sns.kdeplot(df['agea'], fill=True, ax=ax)
```

**Bibliografía:**

- Silverman, B. (1986). _Density Estimation for Statistics and Data Analysis_. Chapman & Hall.
    
- Wand, M., Jones, M. (1995). _Kernel Smoothing_. Chapman & Hall.
    

---

### 1.2 Boxplot

**Qué es:** Caja que va de Q1 a Q3, línea en la mediana, "bigotes" hasta 1.5×IQR, y puntos individuales fuera (outliers).

**Por qué:** Resume **5 métricas** (Q1, mediana, Q3, bigotes, outliers) en un vistazo. Es el gráfico para **comparar distribuciones entre grupos**.

**Cómo interpretarlo:**

|                                              |                                  |
| -------------------------------------------- | -------------------------------- |
| Lo que ves                                   | Significado                      |
| Línea de mediana centrada en la caja         | Simetría dentro del 50% central  |
| Línea de mediana cerca del borde inferior    | Skewness positiva (cola arriba)  |
| Bigote derecho mucho más largo               | Outliers altos                   |
| Caja "gorda" (IQR grande)                    | Alta dispersión                  |
| Caja "plana" (IQR pequeño)                   | Concentración                    |
| Muchos puntos aislados arriba                | Outliers legítimos o error       |
| Dos cajas superpuestas en un grouped boxplot | Los grupos no se distinguen bien |
```python
# Boxplot simple
sns.boxplot(data=df, y='agea')

# Boxplot por grupo (el más útil)
sns.boxplot(data=df, x='EmployType', y='emplno')
plt.ylim(0, 50)  # recortar para no ver el outlier de 400   
```

**Límite:** Con > 500 puntos, los outliers se amontonan y no ves nada. Usa strip plot o violin plot como complemento.

**Bibliografía:**

- Tukey, J. (1977). _Exploratory Data Analysis_. Addison-Wesley. Cap. 10.
    
- McGill, R., Chu, J., Tukey, J., Wiersma, W. (1979). "Variations of box plots." _The American Statistician_, 33(1).
    

---

### 1.3 QQ-plot (Quantile-Quantile)

**Qué es:** Gráfica los cuantiles de tus datos vs. los cuantiles de una distribución teórica (normal). Si los datos son normales, los puntos caen en la línea diagonal.

**Por qué:** Es la visualización **formal** para verificar normalidad. Más fiable que "mirar el histograma y decir que parece normal".

**Cómo interpretarlo:**

|                                |                                             |
| ------------------------------ | ------------------------------------------- |
| Lo que ves                     | Significado                                 |
| Puntos en la línea diagonal    | Normal (o muy cercana)                      |
| Curva en "S" (colas separadas) | No normal: colas más pesadas (kurtosis > 0) |
| Curva en "U" (colas pegadas)   | No normal: colas más ligeras (kurtosis < 0) |
| Desviación solo en un extremo  | Asimetría: solo una cola es anómala         |
| Puntos "saltados" en diagonal  | Datos discretos (no es continua de verdad)  |
```python
from scipy.stats import qqplot

fig, ax = plt.subplots(figsize=(6, 6))
qqplot(df['agea'].dropna(), line='s', ax=ax)
ax.set_title('QQ-plot: agea vs. Normal')
plt.show()   

```

**Bibliografía:**

- Chernoff, H., Rosenblatt, M. (1952). "The estimation of transformation parameters." _Annals of Mathematical Statistics_, 23(1).
    
- NIST (2012). "Q-Q Plot." _Engineering Statistics Handbook_.
    

---

### 1.4 Strip plot / Swarm plot

**Qué es:** Cada observación es un punto. En strip plot se apilan (con jitter horizontal). En swarm plot se disponen para no solaparse.

**Por qué:** Te muestra los **datos reales**, no un resumen. Útil para:

- Ver la densidad de puntos en cada zona.
    
- Detectar clusters o gaps que el boxplot oculta.
    
- Variables con pocos datos (< 100 por grupo).

```python
# Strip (con jitter)
sns.stripplot(data=df, x='EmployType', y='emplno', jitter=0.2, alpha=0.5)

# Swarm (sin solapamiento, más limpio con muchos datos)
sns.swarmplot(data=df, x='EmployType', y='emplno', alpha=0.5)   

```

**Bibliografía:**

- Beaulieu, S. (2015). "beeswarm: Beeswarm plots in R." _Journal of Open Source Software_, 1(8).
    

---

### 1.5 ECDF (Empirical Cumulative Distribution Function)

**Qué es:** Curva que va de 0 a 1 (o 0% a 100%). En cada valor X, te dice "el Y% de datos es menor o igual que X".

**Por qué:**

- Te da el percentil de cualquier valor sin calcularlo.
    
- Comparar dos distribuciones: si una curva está siempre por encima de otra, esa distribución tiene valores más bajos.
    
- No depende de bins (a diferencia del histograma).

```python
# ECDF manual
values = np.sort(df['agea'].dropna())
ecdf = np.arange(1, len(values) + 1) / len(values)

plt.step(values, ecdf, where='post')
plt.axhline(0.5, color='gray', linestyle=':')  # mediana
plt.xlabel('Edad')
plt.ylabel('Proporción acumulada')
plt.title('ECDF: Edad')

```

**Bibliografía:**

- Massey, G. (1951). "The power of certain criteria for testing against general alternatives." _Annals of Mathematical Statistics_, 22(4).
    

---

## 2. VARIABLES DISCRETAS / COUNT

### 2.1 Bar chart (si pocos valores únicos, < 20)

**Qué es:** Una barra por valor, altura = frecuencia.

**Por qué:** Si `emplno` solo tiene valores 0-10 en el 95% de casos, un bar chart es más honesto que un histograma (que implica continuidad).

```python
# Solo valores 0-10 (el 95% de casos)
df['emplno_0_10'] = df['emplno'][df['emplno'] <= 10]
sns.countplot(x='emplno_0_10', data=df)   
```

### 2.2 Histograma + KDE (si muchos valores únicos)

Si `emplno` tiene 187 valores únicos (0-400), el bar chart no es práctico. Usa histograma + KDE como si fuera continua, pero **interpreta la masa puntual en 0** como lo que es: un pico artificial por el routing.

### 2.3 Boxplot + Strip (combinado)

El combo más informativo para count variables:

```python
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df, x='EmployType', y='emplno', ax=ax, whiscap=10)
sns.stripplot(data=df, x='EmployType', y='emplno', ax=ax, alpha=0.3, jitter=0.2)
ax.set_yscale('log')  # log scale para ver la cola   
```

**Bibliografía:**

- Healy, M. (2019). _Statistics: A Lifesaver_ (2nd ed). UCL Press. Cap. 5.
    

---

## 3. VARIABLES ORDINALES ACOTADAS (0-10, Likert)

### 3.1 Countplot (el más informativo)

**Qué es:** Bar chart de frecuencias para cada valor de la escala.

**Por qué:** Para una escala 0-10, el countplot te muestra:

- Dónde está el pico (moda).
    
- Si hay bimodalidad (dos picos).
    
- Si hay "evitación del centro" (la gente no pone 5).
    
- Si hay "evitación de extremos" (nadie pone 0 o 10).
    

**Cómo interpretarlo:**

|                                        |                                                         |
| -------------------------------------- | ------------------------------------------------------- |
| Patrón                                 | Significado                                             |
| Pico en 5-6, decaimiento simétrico     | Distribución "normal" de opiniones                      |
| Pico en 7-8, cola corta a la izquierda | Sesgo positivo (la gente tiende a valorar alto)         |
| Dos picos (ej. 3 y 8)                  | Bimodalidad: hay dos grupos con opiniones opuestas      |
| Pico en 0 y otro en 10                 | Polarización extrema                                    |
| Barras planas (todas similares)        | La variable no discrimina (todo el mundo pone lo mismo) |
```python
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(x='happy', data=df, palette='Blues')
ax.set_title('Distribución de satisfacción (happy)')
ax.set_xlabel('Puntuación (0-10)')
ax.set_ylabel('Frecuencia')
plt.show()   
```

### 3.2 Histograma + KDE (cuando quieres comparar varias)

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, col in zip(axes, ['happy', 'lrscale', 'ppltrst']):
    sns.histplot(df[col], kde=True, bins=10, ax=ax, color='steelblue', alpha=0.6)
    ax.set_title(col)
plt.tight_layout()   
```

### 3.3 Ridgeline plot (distribuciones apiladas por grupo)

**Qué es:** Varias curvas KDE apiladas verticalmente, una por grupo.

**Por qué:** Comparar la **forma** de la distribución de una ordinal entre varios grupos sin que se solapen.

```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 6))
sns.displot(data=df, x='lrscale', hue='EmployType', kind='kde',
            fill=True, palette='Set2', ax=ax)
ax.set_title('Distribución de lrscale por tipo de empleo')
plt.show()   
```

**Bibliografía:**

- Clauset, A. (2016). "The ridgeline plot: A compact visualization for comparing large numbers of univariate distributions." _IEEE VIS_.
    
- Orphanides, A. (2003). "Money, demand, and uncertainty." _Journal of Money, Credit and Banking_. (uso de ridgelines en economía)
    

---

## 4. VARIABLES ORDINALES CON POCOS CÓDIGOS (2-8 valores)

### 4.1 Countplot

Mismo que 3.1. Para `emplrel` (4 valores: 1, 2, 3, 6) o `health` (5 valores):

```python
sns.countplot(x='emplrel', data=df, order=[1, 2, 3, 6])
plt.xticks([1, 2, 3, 6], ['Employee', 'Self-employed', 'Family', 'N/A'])   
```


---

### 4.2 Mosaic plot (dos ordinales/categóricas)

**Qué es:** Un rectángulo dividido en proporciones. El eje X es la proporción de la primera variable, el eje Y la de la segunda. Cada celda es una combinación.

**Por qué:** Ver la **asociación** entre dos variables categóricas/ordinales sin perder la información de frecuencia.

**Python:**

```python
import matplotlib_venn  # o usar pandas crosstab + heatmap

# Alternativa más simple: heatmap de tabla de contingencia
ct = pd.crosstab(df['EmployType'], df['emplrel'], normalize='index')
sns.heatmap(ct, annot=True, fmt='.2%', cmap='YlOrRd')
plt.title('Proporción de emplrel por EmployType')
```

**Bibliografía:**

- Mason, J., Hand, D. (2007). "Mosaic plots for multi-way contingency tables." _Journal of the Royal Statistical Society_, 59(2).
    

---

## 5. VARIABLES NOMINALES / CATEGÓRICAS

### 5.1 Bar chart horizontal

**Por qué:** Con muchas categorías (24 países), las etiquetas no caben en vertical. Horizontal es más legible.

**Python:**

```python
top_15 = df['cntry'].value_counts().head(15)
sns.barplot(x=top_15.values, y=top_15.index, palette='viridis')
plt.title('Top 15 países por nº de respuestas')
plt.xlabel('Frecuencia')
```

### 5.2 Heatmap de co-ocurrencia

**Por qué:** Ver si dos variables categóricas están asociadas. Ej: ¿la distribución de `gndr` es similar en todos los `cntry`?



```python
ct = pd.crosstab(df['cntry'], df['gndr'], normalize='index')
sns.heatmap(ct, annot=True, fmt='.2%', cmap='RdBu_r', center=0.5)
plt.title('Proporción de género por país')
```

**Bibliografía:**

- Wilkinson, L. (2005). _The Grammar of Graphics_ (2nd ed). Springer. Cap. 7.
    

---

## 6. COMPARACIÓN ENTRE GRUPOS

### 6.1 Boxplot segmentado (el estándar)

```python
sns.boxplot(data=df, x='std_region', y='lrscale')
```

**Preguntas que responde:**

- ¿La mediana difiere entre grupos?
    
- ¿La dispersión (IQR) es similar o no?
    
- ¿Hay outliers en algún grupo y no en otro?
    

### 6.2 Violin plot (forma + densidad)

**Qué es:** Boxplot + KDE "estirado" a ambos lados. Ves la **forma** de la distribución, no solo los cuartiles.

**Por qué:** Si dos grupos tienen la misma mediana y el mismo IQR pero uno es bimodal y otro unimodal, el boxplot no lo ve. El violin sí.

```python
sns.violinplot(data=df, x='EmployType', y='emplno', inner='box')
```
```python
sns.violinplot(data=df, x='EmployType', y='emplno', inner='box')
```

### 6.3 Bar chart agrupado (categorías discretas)

```python
sns.barplot(data=df, x='std_region', y='happy', ci=95)
# ci=95 → barras de error = IC 95% de la media
```

**Bibliografía:**

- Cumming, G. (2012). _Understanding the New Statistics_ (2nd ed). Routledge.
    
- Allen, M., Poynton, C., Fugate, J. (2016). "The violin plot: A box plot and density plot duet." _PLOS ONE_, 11(12).
    

---

## 7. RELACIÓN ENTRE 2 VARIABLES

### 7.1 Scatter plot (continua vs. continua)

**Por qué:** Ver si hay relación (lineal, no lineal, ninguna), su fuerza y su forma.

**Cómo interpretarlo:**

- Nube con pendiente → relación lineal.
    
- Nube en "U" o "inverted U" → relación no lineal (polinómica).
    
- Nube en "V" → relación absoluta (|x|).
    
- Nube en bloque → relación escalonada (una de las variables es discreta).
    
- Nube uniforme → no hay relación.
    

```python
sns.scatterplot(data=df, x='agea', y='happy', alpha=0.3, s=10)
```

```python
sns.scatterplot(data=df, x='agea', y='happy', alpha=0.3, s=10)
```

**Límite:** Con > 5000 puntos, todo es un "blob". Soluciones:

- `alpha=0.1` (transparencia)
    
- Hexbin plot: `sns.regplot` o `plt.hexbin`
    
- Binned scatter: `sns.relplot` con `col`/`row`
    

### 7.2 Binned scatter / Regplot (con tendencia)

```python
sns.regplot(data=df, x='agea', y='lrscale', scatter_kws={'alpha': 0.2})
# Dibuja la nube + línea de regresión + banda de confianza
```
```python
sns.regplot(data=df, x='agea', y='lrscale', scatter_kws={'alpha': 0.2})
# Dibuja la nube + línea de regresión + banda de confianza   
```
### 7.3 Strip plot (categórica vs. continua)

```python
sns.stripplot(data=df, x='EmployType', y='lrscale', jitter=0.3, alpha=0.4)
```

**Bibliografía:**

- Tufte, E. (2001). _The Visual Display of Quantitative Information_ (2nd ed). Graphics Press.
    
- Cleveland, W. (1993). _Visualizing Data_. Hobart Press.
    

---

## 8. RELACIÓN ENTRE 3+ VARIABLES

### 8.1 Pair plot (matriz de scatters)

**Qué es:** Una matriz donde cada celda (i,j) es un scatter de la variable i vs. la j. La diagonal es el histograma/KDE.

**Por qué:** Ver de un vistazo todas las relaciones pares de un subconjunto de variables.



```python
subset = df[['agea', 'happy', 'lrscale', 'emplno']].dropna()
sns.pairplot(subset, diag_kind='kde', plot_kws={'alpha': 0.3, 's': 5})
plt.suptitle('Pair plot: variables principales', y=1.02)
```

**Límite:** Con > 5 variables se vuelve ilegible. Usa un subconjunto de 3-5.

### 8.2 Heatmap de correlación

```python
corr = df[['agea', 'happy', 'lrscale', 'ppltrst', 'trstlgl']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, vmin=-1, vmax=1)
plt.title('Matriz de correlación (Pearson)')
```

**Cómo interpretarlo:**

- Rojo = correlación positiva (suben juntas).
    
- Azul = correlación negativa (una sube, otra baja).
    
- Blanco = sin relación lineal.
    
- **Límite:** Pearson solo captura relación **lineal**. Dos variables pueden estar fuertemente relacionadas de forma no lineal y tener correlación ≈ 0.
    

**Bibliografía:**

- Evans, D. (2015). "Viz: A matrix of scatterplots." _Journal of Statistical Software_.
    
- Friedman, J., Hastie, T., Tibshirani, R. (2001). _The Elements of Statistical Learning_. Springer. Cap. 18.
    

---

## 9. DISTRIBUCIÓN EN EL TIEMPO

### 9.1 Line plot

**Por qué:** Ver tendencia, estacionalidad, rupturas.


```python
# Si tienes una variable temporal (ej. essround como proxy)
df_pivot = df.groupby(['essround', 'cntry'])['happy'].mean().reset_index()
sns.lineplot(data=df_pivot, x='essround', y='happy', hue='cntry')   

```
```python
# Si tienes una variable temporal (ej. essround como proxy)
df_pivot = df.groupby(['essround', 'cntry'])['happy'].mean().reset_index()
sns.lineplot(data=df_pivot, x='essround', y='happy', hue='cntry')
```

### 9.2 Rolling window

```python
df['happy_roll5'] = df.groupby('cntry')['happy'].transform(
    lambda x: x.rolling(5, min_periods=1).mean()
)
```

**Bibliografía:**

- Hyndman, R., Athanasopoulos, G. (2021). _Forecasting: Principles and Practice_ (3rd ed). OTexts.
    

---

## TABLA DE DECISIÓN FINAL

```
¿Qué tipo de variable tengo?
│
├── CONTINUA (agea, income, wkhtot)
│   ├── ¿Quiero ver la FORMA? → Histograma + KDE
│   ├── ¿Quiero verificar NORMALIDAD? → QQ-plot
│   ├── ¿Quiero COMPARAR entre grupos? → Boxplot / Violin
│   ├── ¿Quiero ver los DATOS REALES? → Strip / Swarm
│   ├── ¿Quiero el PERCENTIL de un valor? → ECDF
│   └── ¿Quiero ver la RELACIÓN con otra? → Scatter + regplot
│
├── DISCRETA / COUNT (emplno, children)
│   ├── ¿Pocos valores únicos (<20)? → Bar chart / Countplot
│   ├── ¿Muchos valores únicos? → Histograma + KDE (con log scale)
│   ├── ¿Masa puntual en 0? → Boxplot + Strip (log scale)
│   └── ¿Comparar entre grupos? → Boxplot segmentado
│
├── ORDINAL ACOTADA 0-10 (happy, lrscale, ppltrst)
│   ├── ¿Ver la DISTRIBUCIÓN? → Countplot (11 barras)
│   ├── ¿Comparar FORMAS entre grupos? → Ridgeline / KDE apilado
│   ├── ¿Ver la RELACIÓN con otra ordinal? → Scatter (jitter) / Heatmap
│   └── ¿Ver la RELACIÓN con una categórica? → Boxplot / Violin
│
├── ORDINAL POCOS CÓDIGOS (emplrel, health)
│   ├── ¿Ver FRECUENCIAS? → Countplot
│   ├── ¿Ver ASOCIACIÓN con otra categórica? → Heatmap de crosstab
│   └── ¿Ver RELACIÓN con una continua? → Strip plot
│
├── NOMINAL (cntry, gndr)
│   ├── ¿Ver FRECUENCIAS? → Bar chart horizontal
│   ├── ¿Ver ASOCIACIÓN con otra nominal? → Heatmap / Mosaic
│   └── ¿Ver ASOCIACIÓN con una continua? → Boxplot por categoría
│
└── 3+ VARIABLES
    ├── ¿Relaciones pares? → Pair plot (3-5 vars)
    ├── ¿Correlaciones lineales? → Heatmap de correlación
    └── ¿Tendencia temporal? → Line plot + rolling
```

---

## REGLAS DE DISEÑO (aplican a todos los gráficos)

|   |   |
|---|---|
|Regla|Por qué|
|**Título que responde una pregunta**|"Distribución de edad" → "¿La edad es simétrica?"|
|**Etiquetas en ejes con unidades**|"Edad (años)", "Nº empleados"|
|**No truncar el eje Y en bar charts**|Truncar de 0 a 50 cuando el max es 400 distorsiona|
|**Usar log scale para count variables**|`emplno` con 0-400: sin log, el 95% se ve aplastado|
|**Máximo 5-7 colores**|Más de 7 categorías → el ojo no distingue|
|**Alpha/transparencia en scatters**|Con > 1000 puntos, `alpha=0.2-0.3`|
|**Grid sutil, no dominante**|`ax.grid(alpha=0.3, linestyle=':')`|
|**Fuente legible (≥ 10pt)**|Si va en un paper o presentación|

---

## COMBINACIONES RECOMENDADAS (el "kit" por variable)

|   |   |
|---|---|
|Variable|Kit mínimo (2-3 plots)|
|`agea` (continua)|Histograma+KDE + Boxplot por grupo + QQ-plot|
|`emplno` (count, masa en 0)|Countplot 0-10 + Boxplot log + Strip por grupo|
|`happy` (ordinal 0-10)|Countplot + Ridgeline por grupo + Heatmap con `lrscale`|
|`lrscale` (ordinal 0-10)|Countplot + Boxplot por `std_region` + Scatter con `happy`|
|`cntry` (nominal, 24)|Bar chart horizontal + Heatmap con `gndr`|
|`EmployType` (ordinal 3)|Countplot + Boxplot de `emplno` por tipo|

---

## Referencias consolidadas

|     |                                                                                              |                                                       |
| --- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| #   | Referencia                                                                                   | Qué cubre                                             |
| 1   | Tufte, E. (2001). _The Visual Display of Quantitative Information_ (2nd ed). Graphics Press. | Principios fundamentales de visualización. La biblia. |
| 2   | Cleveland, W. (1993). _Visualizing Data_. Hobart Press.                                      | Percepción visual, elección de gráficos.              |
| 3   | Healy, M. (2019). _Statistics: A Lifesaver_ (2nd ed). UCL Press.                             | Interpretación de plots, nivel introductorio.         |
| 4   | Wilke, C. (2019). _Fundamentals of Data Visualization_. O'Reilly.                            | Implementación en ggplot2/matplotlib/seaborn.         |
| 5   | Clauset, A. (2016). "The ridgeline plot." _IEEE VIS_.                                        | Ridgeline plots.                                      |
| 6   | Allen, M. et al. (2016). "The violin plot." _PLOS ONE_, 11(12).                              | Violin plots: teoría + implementación.                |
| 7   | Cumming, G. (2012). _Understanding the New Statistics_. Routledge.                           | Gráficos inferenciales (IC, estimación de efecto).    |
| 8   | Hyndman, R., Athanasopoulos, G. (2021). _Forecasting: Principles and Practice_. OTexts.      | Series temporales, rolling windows.                   |
| 9   | Seaborn documentation. `seaborn.pydata.org`.                                                 | Implementación de todos los plots del manual.         |
| 10  | NIST (2012). _Engineering Statistics Handbook_.                                              | QQ-plot, ECDF, percentiles.                           |

```markdown
**Trilogía completa:**

| Manual | Pregunta que responde |
|--------|----------------------|
| 1. Métricas descriptivas | *¿Qué números me dice esta variable?* |
| 2. Transformaciones | *¿Qué le hago a esta variable antes de modelar?* |
| 3. Visualización | *¿Qué dibujo para ver y razonar sobre esta variable?* |

El flujo en el notebook queda:

Celda 1: vartype() → "¿Qué tengo?"  
Celda 2: statsgroup() → "¿Qué números me dice?" ← Manual 1  
Celda 3: Plots → "¿Cómo se ve?" ← Manual 3  
Celda 4: Transformaciones → "¿Qué le hago?" ← Manual 2  
Celda 5: Audit before/after → "¿Se rompió algo?"
   
```
