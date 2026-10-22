
---

## Índice (orden de aparición en un notebook)

| # | Métrica | Familia |
|---|---------|---------|
| 1 | Tipo de variable | Clasificación |
| 2 | Count (n) | Existencia |
| 3 | Valores únicos | Existencia |
| 4 | Range | Extremo |
| 5 | Mínimo / Máximo | Extremo |
| 6 | Media (mean) | Tendencia central |
| 7 | Mediana (50%) | Tendencia central |
| 8 | Moda | Tendencia central |
| 9 | Cuartiles (Q1, Q3) | Posición |
| 10 | Varianza | Dispersión |
| 11 | Desviación estándar (std) | Dispersión |
| 12 | IQR | Dispersión robusta |
| 13 | MAD | Dispersión robusta |
| 14 | Coeficiente de variación (CV) | Dispersión relativa |
| 15 | P5 / P95 | Cola |
| 16 | % extremos | Forma |
| 17 | Skewness | Forma |
| 18 | Kurtosis | Forma |
| 19 | Shapiro-Wilk | Normalidad |

---

## 1. Tipo de variable

**Definición:** Clasificación de una columna según la naturaleza de sus valores.

**Uso:** Es el primer paso. Antes de calcular cualquier métrica necesitas saber si la variable es numérica (puedes sumar, restar, calcular media) o categórica (solo puedes contar frecuencias).

**Tipos básicos:**

| Tipo                 | Ejemplo                           | Operaciones válidas   |
| -------------------- | --------------------------------- | --------------------- |
| Numérica continua    | `agea` (edad: 23.4, 45.1)         | Media, std, min, max… |
| Numérica discreta    | `emplno` (nº empleados: 0, 1, 2…) | Media, std, moda…     |
| Ordinal              | `lrscale` (0-10, hay orden)       | Mediana, IQR, moda…   |
| Nominal / Categórica | `cntry` (país: AT, BE, DE…)       | Frecuencias, moda…    |
```python
num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = df.select_dtypes(include=['object']).columns.tolist()
```

- Numérica → histograma, KDE, boxplot
    
- Categórica → bar chart, countplot
    

**Bibliografía:** Field, A. (2018). _Discovering Statistics Using IBM SPSS Statistics_ (5th ed.). SAGE. Cap. 1.

---

## 2. Count (n)

**Definición:** Número de observaciones no faltantes (no-NaN) en la variable.

**Uso:** Te dice cuántos datos tienes realmente. Si esperas 41.000 y te salen 36.000, hay un 12% de missing que necesitas tratar.

```python
df['col'].count()          # → 36677
len(df['col'].dropna())    # → mismo   
```

**En un plot:** Es el eje X total del histograma (la suma de todas las barras = n).

**Bibliografía:** Wasserman, L. (2013). _All of Statistics_. Springer. Cap. 1.

---

## 3. Valores únicos (nunique)

**Definición:** Cuántos valores distintos tiene la variable.

**Uso:**

- Si `lrscale` tiene 11 únicos → correcto (0,1,2…10).
    
- Si `cntry` tiene 24 únicos → 24 países.
    
- Si `emplno` tiene 500 únicos → es continua/discreta de rango amplio.
    
- Si una variable "continua" tiene 3 únicos → algo está mal (¿estás binando sin querer?).
    

```python
df['col'].nunique()

```

**En un plot:** En un bar chart de valores únicos, es el número de barras.

**Bibliografía:** McKinney, W. (2018). _Python for Data Analysis_ (2nd ed.). O'Reilly. Cap. 3.

---

## 4. Range

**Definición:** `máximo − mínimo`. El "tamaño" total del recorrido de la variable.

**Uso:** Te da una primera idea de la escala. Un range de 10 (para `lrscale`) es muy distinto de un range de 400 (para `emplno`).

```python
df['col'].max() - df['col'].min()   
```

**En un plot:** En un boxplot, es la distancia total desde el "bigote" inferior hasta el superior (sin outliers).

**Bibliografía:** Lane, D. (2020). _How to Calculate the Range_. Statistics How To.

---

## 5. Mínimo y Máximo

**Definición:** El valor más pequeño y el más grande observado.

**Uso:**

- Detectan valores imposibles (¿edad = 200? ¿empleados = -5?).
    
- Definen los límites del eje en un gráfico.
    
- En variables 0-10, confirmar que min=0 y max=10 valida el rango.

```python
df['col'].min()
df['col'].max()   
```

**En un plot:**

- Histograma: los bordes del eje X.
    
- Boxplot: las puntas de los bigotes (o los outliers más extremos).
    
- Strip plot / swarm plot: los puntos más alejados del centro.
    

**Bibliografía:** Wilkinson, L. (2005). _The Grammar of Graphics_ (2nd ed). Springer. Cap. 4.

---

## 6. Media (mean)

**Definición:** Suma de todos los valores dividida entre el número de observaciones.

xˉ=n1​i=1∑n​xi​

**Uso:** Es el "centro de gravedad" de los datos. Si todos los valores fueran iguales a la media, la suma total sería la misma. Es la métrica de tendencia central más usada, pero **sensible a outliers**: un solo valor extremo la arrastra.

**Ejemplo:** 5 personas ganan 2.000€ y 1 gana 200.000€. Media = 36.000€ (no representa a nadie). Mediana = 2.000€ (sí representa).

```python
df['col'].mean()   
```

**En un plot:**

- Histograma/KDE: una línea vertical en la posición de la media. Si la distribución es simétrica, cae en el pico. Si hay cola a la derecha, la media se desplaza hacia la cola.
    
- Boxplot: no se dibuja directamente, pero si añades un punto/diamante, es la media.
    

**Bibliografía:**

- Walpole, R., Myers, R., Myers, S., Ye, K. (2012). _Probability & Statistics for Engineers & Scientists_ (9th ed). Pearson. Cap. 3.
    
- Brown, C. (2020). "Mean, Median, Mode." _Statistics by Jim_.
    

---

## 7. Mediana (50%, percentil 50)

**Definición:** El valor que deja el 50% de las observaciones por debajo y el 50% por encima.

**Uso:** Es la tendencia central **robusta**. No se mueve si cambias un valor extremo. En distribuciones asimétricas (como `emplno`, donde el 95% es 0), la mediana (0) representa mejor al "típico" que la media (0.32).

```python
df['col'].median()
df['col'].quantile(0.50)   # → mismo   
```

**En un plot:**

- Boxplot: la **línea horizontal dentro de la caja**. Es lo primero que ves.
    
- Histograma: una línea vertical. En distribuciones asimétricas, está más cerca del pico que la media.
    

**Bibliografía:**

- Molinari, F. (2021). "The median: a robust measure of central tendency." _The American Statistician_, 75(4).
    
- Iglewicz, B., Hoaglin, D. (1993). _How to Detect and Handle Outliers_. ASQC. Cap. 2.
    

---

## 8. Moda

**Definición:** El valor que más se repite.

**Uso:** Útil en variables discretas con pocos valores (ej. `emplrel`: 1, 2, 3, 6). Te dice "la respuesta más frecuente". En variables continuas casi no tiene sentido (cada valor es único).

**Frecuencia de la moda:** Cuántas veces aparece. Si la moda es 5 y aparece 40.000 veces de 180.000, hay una concentración fuerte en ese valor.

```python
moda = df['col'].mode()                    # → Series con el/los valores más frecuentes
freq = df['col'].value_counts().iloc[0]    # → cuántas veces aparece   
```

**En un plot:**

- Bar chart / countplot: la **barra más alta**.
    
- Histograma: el pico (en variables discretas).
    
- KDE: el máximo de la curva.
    

**Bibliografía:**

- Sullivan, M. (2017). _Statistics: Informed Decisions Using Data_ (5th ed). Pearson. Cap. 2.
    
- DeGroot, M., Schervish, M. (2012). _Probability and Statistics_ (4th ed). Addison-Wesley. Cap. 2.
    

---

## 9. Cuartiles (Q1 = 25%, Q3 = 75%)

**Definición:**

- **Q1 (25%):** El valor que deja el 25% de datos por debajo.
    
- **Q3 (75%):** El valor que deja el 75% de datos por debajo.
    

**Uso:** Dividen los datos en 4 partes iguales. Te dicen dónde se concentra la "masa" central. La distancia Q3−Q1 es el IQR (métrica 12). En un boxplot, son los **bordes de la caja**.

```python
df['col'].quantile(0.25)   # Q1
df['col'].quantile(0.75)   # Q3   
```

**En un plot:**

- **Boxplot:** Q1 = borde inferior de la caja, Q3 = borde superior. La caja "encierra" el 50% central de los datos.
    
- Histograma: líneas verticales en el 25% y 75% del área acumulada.
    

**Bibliografía:**

- Tukey, J. (1977). _Exploratory Data Analysis_. Addison-Wesley. Cap. 10 (boxplots).
    
- McGill, R., Chu, J., Tukey, J., Wiersma, W. (1979). "Variations of box plots." _The American Statistician_, 33(1).
    

---

## 10. Varianza

**Definición:** Media de las desviaciones al cuadrado respecto a la media.

$$
s2=n−11​i=1∑n​(xi​−xˉ)2
$$

**Uso:** Mide cuánto se "esparcen" los datos alrededor de la media. A mayor varianza, más dispersión. El problema: está en **unidades al cuadrado** (si la variable es en años, la varianza es en años²), lo que la hace difícil de interpretar directamente.

```python
df['col'].var()   # → varianza muestral (n-1)  
```

**En un plot:**

- No se ve directamente, pero: cuanto más "plano y ancho" es el histograma, mayor varianza. Cuanto más "alto y estrecho", menor varianza.
    
- En un scatter plot, la "nube" más dispersa = mayor varianza.
    

**Bibliografía:**

- Walpole et al. (2012). _Probability & Statistics_. Cap. 3.
    
- Freedman, D., Pisani, R., Purves, R. (2007). _Statistics_ (4th ed). W.W. Norton. Cap. 15.
    

---

## 11. Desviación estándar (std)

**Definición:** Raíz cuadrada de la varianza.

$$
s=sqrt(s2)​
$$

**Uso:** Es la varianza "traducida" a las unidades originales de la variable. Si `agea` tiene std=15, significa que "típicamente" las edades se desvían ±15 años de la media. Es la métrica de dispersión más usada.

**Regla empírica (distribuciones simétricas):**

- ~68% de datos dentro de media ± 1 std
    
- ~95% dentro de media ± 2 std
    
- ~99.7% dentro de media ± 3 std

```python
df['col'].std()
```

**En un plot:**

- Histograma + KDE: si dibujas bandas en media±1σ y media±2σ, ves qué proporción cae dentro.
    
- Boxplot: no se dibuja directamente, pero una caja "gorda" sugiere std alta.
    

**Bibliografía:**

- Freedman et al. (2007). _Statistics_. Cap. 15.
    
- Lane, D. (2020). "Standard Deviation." _Statistics How To_.
    

---

## 12. IQR (Interquartile Range)

**Definición:** `Q3 − Q1`. El rango que cubre el 50% central de los datos.

**Uso:** Es la dispersión **robusta** por excelencia. No se ve afectada por outliers (a diferencia de std). Si tienes una variable con 95% de ceros y un 5% de valores enormes, la std es enorme pero el IQR sigue siendo 0. Para variables con masa puntual (`emplno`), el IQR es más honesto que la std.

```python
iqr = df['col'].quantile(0.75) - df['col'].quantile(0.25)  
```

**En un plot:**

- **Boxplot:** es la **altura de la caja**. Una caja alta = IQR grande = dispersión. Una caja plana = IQR pequeño = concentración.
    
- Es la referencia para detectar outliers: cualquier punto fuera de `[Q1 − 1.5×IQR, Q3 + 1.5×IQR]` se marca como outlier.
    

**Bibliografía:**

- Tukey, J. (1977). _Exploratory Data Analysis_. Cap. 10.
    
- Iglewicz & Hoaglin (1993). _How to Detect and Handle Outliers_. Cap. 2.
    

---

## 13. MAD (Median Absolute Deviation)

**Definición:** La mediana de las desviaciones absolutas respecto a la mediana.

MAD=median(∣xi​−median(x)∣)

**Uso:** Es aún **más robusta** que el IQR. Mientras el IQR usa 2 puntos (Q1, Q3), la MAD usa todos los datos pero con la mediana (robusta) en vez de la media (frágil). Es la base del "modified Z-score" para detectar outliers.

**Cuándo usarla:** Cuando la distribución es muy asimétrica o tiene muchos outliers y quieres una medida de dispersión que no se mueva.

```python
mad = (df['col'] - df['col'].median()).abs().median()   
```

**En un plot:**

- No se dibuja directamente.
    
- En un strip plot / swarm plot, imagina la mediana como centro: la MAD es "la distancia típica" de los puntos a ese centro.
    

**Bibliografía:**

- Iglewicz & Hoaglin (1993). _How to Detect and Handle Outliers_. Cap. 2.
    
- Rousseeuw, P., Croux, C. (1993). "Alternatives to the median absolute deviation." _Journal of Computational and Graphical Statistics_, 2(1).
    

---

## 14. Coeficiente de Variación (CV)

**Definición:** `std / mean`. La dispersión **relativa** a la magnitud de la variable.

CV=xˉs​

**Uso:** Permite comparar la dispersión entre variables con escalas distintas. `agea` (media=45, std=15) tiene CV=0.33. `emplno` (media=0.32, std=4.07) tiene CV=12.7. El CV te dice que `emplno` es **muchísimo más variable** respecto a su propio tamaño que `agea`.

**Límite:** No tiene sentido si la media es 0 o negativa (ej. temperatura en °C puede ser negativa).

```python
cv = df['col'].std() / df['col'].mean()
```

**En un plot:**

- No se dibuja directamente.
    
- Visualmente: dos histogramas con la misma "forma" pero uno en escala 0-100 y otro en 0-1000 → el de 0-1000 parece "más disperso" en unidades absolutas, pero el CV es el mismo.
    

**Bibliografía:**

- Evans, M., Fitzmaurice, G., Van Den Broucke, S. (2014). "Distributions in Cross-Section, Time Series, and Panel Data." _Econometric Reviews_, 33(6).
    
- Altman, D. (1996). "Confidence intervals for the standard deviation and coefficient of variation." _Statistics in Medicine_, 15(19).
    

---

## 15. P5 y P95 (Percentiles 5 y 95)

**Definición:**

- **P5:** El valor por debajo del cual está el 5% de los datos.
    
- **P95:** El valor por debajo del cual está el 95% de los datos.
    

**Uso:** Te dicen dónde están las **colas** de la distribución. Si P5=0 y P95=8 (en una escala 0-10), el 90% central está entre 0 y 8, y solo el 5% superior supera 8. Es más informativo que min/max porque no se ve afectado por un solo outlier extremo.

```python
df['col'].quantile(0.05)   # P5
df['col'].quantile(0.95)   # P95   
```

**En un plot:**

- Histograma: líneas verticales en el 5% y 95% del área acumulada.
    
- Boxplot extendido: si usas "1.5×IQR" como bigotes, los bigotes se acercan a P5/P95 en distribuciones simétricas.
    
- QQ-plot: los puntos de las colas se desvían de la línea diagonal.
    

**Bibliografía:**

- Hyndman, R., Fan, Y. (1996). "Sample quantiles in statistical packages." _The American Statistician_, 50(4).
    
- NIST/SEMATECH (2012). "Percentile." _Engineering Statistics Handbook_.
    

---

## 16. % Extremos

**Definición:** Proporción de observaciones en los valores más extremos de la variable.

**Uso:**

- En escalas 0-10: % que puso 0 + % que puso 10. Te dice si hay "polarización" (gente que va a los extremos) o "centración" (gente que se queda en 4-6).
    
- En count variables (`emplno`): % que tiene 0 empleados (masa puntual) + % que tiene >100 (cola extrema).

```python
# Escala 0-10
pct_0  = (df['col'] == 0).mean() * 100
pct_10 = (df['col'] == 10).mean() * 100
pct_mid = df['col'].between(4, 6).mean() * 100

# Count variable
pct_zero = (df['col'] == 0).mean() * 100
pct_high = (df['col'] > 100).mean() * 100   
```

**En un plot:**

- Histograma: la **primera y última barra** (o las primeras/últimas pocas). Si son muy altas → polarización. Si son muy bajas → concentración central.
    
- Bar chart: las barras de los extremos vs. las del centro.
    

**Bibliografía:**

- Healy, M. (2019). _Statistics: A Lifesaver_ (2nd ed). UCL Press. Cap. 4.
    
- Field, A. (2018). _Discovering Statistics_. Cap. 2.
    

---

## 17. Skewness (Asimetría)

**Definición:** Mide si la distribución es simétrica o tiene una "cola" más larga que la otra.

$$
Skewness=s3n1​∑(xi​−xˉ)3​
$$

**Interpretación:**

|   |   |
|---|---|
|Valor|Significado|
|≈ 0|Simétrica (cola izquierda ≈ cola derecha)|
|> 0|Cola a la **derecha** (hay pocos valores muy altos). Ej: ingresos, `emplno`|
|< 0|Cola a la **izquierda** (hay pocos valores muy bajos). Ej: notas en un examen fácil|

**Uso:** Te dice si la media es fiable como "centro". Si skewness es alta, la media está arrastrada por la cola y la mediana es mejor representante.

```python
from scipy.stats import skew
skew(df['col']) 
```

**En un plot:**

- **Histograma / KDE:** visualmente, ¿la cola es más larga a la izquierda o a la derecha? Si el pico está a la izquierda y la cola se extiende a la derecha → skewness positiva.
    
- **Boxplot:** si el bigote derecho es mucho más largo que el izquierdo → skewness positiva. Si la línea de la mediana está más cerca del borde inferior de la caja → skewness positiva.
    

**Bibliografía:**

- Johnson, R., Kotz, S., Balakrishnan, N. (1994). _Continuous Univariate Distributions_ (2nd ed). Wiley. Cap. 1.
    
- Pearson, K. (1895). "Notes on the theory and application of skew frequency curves." _Biometrika_, 13(3).
    

---

## 18. Kurtosis (exceso)

**Definición:** Mide si la distribución tiene **colas más pesadas o más ligeras** que una normal, y si el pico es más agudo o más plano.

$$
Kurtosis (exceso)=s4n1​∑(xi​−xˉ)4​−3
$$

**Interpretación:**

|   |   |
|---|---|
|Valor|Significado|
|≈ 0|Mesocúrtica (como una normal)|
|> 0|**Leptocúrtica**: pico más agudo + colas más pesadas. Hay más datos en el centro Y más en los extremos.|
|< 0|**Platicúrtica**: pico más plano + colas más ligeras. Típico de escalas 0-10 (los datos se "apilan" en el centro)|

**Uso:** En escalas 0-10, la kurtosis suele ser negativa (platicúrtica) porque hay un tope físico: no puedes poner 11. Los datos se concentran en 4-6 y las colas son cortas.

```python
from scipy.stats import kurtosis
kurtosis(df['col'])   # → excess kurtosis (normal = 0)   
```

**En un plot:**

- **KDE / Histograma:** compara con una curva normal (campana). Si tu distribución es más "aplanada" con los bordes más rellenos → kurtosis negativa. Si es más "puntiaguda" con colas más llenas → kurtosis positiva.
    
- **QQ-plot:** en los extremos, si los puntos se alejan de la línea hacia arriba → colas pesadas (kurtosis > 0). Si se alejan hacia abajo → colas ligeras (kurtosis < 0).
    

**Bibliografía:**

- Johnson et al. (1994). _Continuous Univariate Distributions_. Cap. 1.
    
- Pearson, K. (1905). "Moment and percentile measures of skewness." _Biometrika_, 4(3).
    

---

## 19. Shapiro-Wilk (Test de Normalidad)

**Definición:** Test estadístico que responde a la pregunta: _"¿Es razonable modelar estos datos como una distribución normal?"_

- **H₀ (hipótesis nula):** Los datos siguen una normal.
    
- **H₁:** No siguen una normal.
    

**Resultado:**

- **p < 0.05** → Rechazo H₀ → **No es normal**.
    
- **p > 0.05** → No rechazo H₀ → No hay evidencia contra la normalidad (no significa que "sea" normal).
    

**Uso:** Antes de aplicar tests paramétricos (t-test, ANOVA, regresión lineal) que asumen normalidad, verificas con Shapiro. En variables ordinales discretas (0-10) **siempre** va a dar p ≈ 0 (no es normal, porque es discreta). Eso no es un problema: significa que debes usar tests no paramétricos (Mann-Whitney, Kruskal-Wallis) o tratar la variable como ordinal.

**Límite:** Con n > 5000 el test es demasiado potente (cualquier desviación mínima da p < 0.05). Por eso se aplica sobre una muestra de 5000.

```python
from scipy.stats import shapiro
stat, p = shapiro(df['col'].sample(5000, random_state=42))
print(f"W={stat:.4f}, p={p:.2e}")   
```

**En un plot:**

- **QQ-plot (Quantile-Quantile):** es la visualización asociada. Si los puntos caen en la línea diagonal → normal. Si se curvan en "S" → no normal. Si las colas se separan → kurtosis extrema.
    
- **Histograma + curva normal superpuesta:** si la campana no "encaja" con las barras → no normal.
    

**Bibliografía:**

- Shapiro, S., Wilk, M. (1965). "An analysis of variance test for normality." _Biometrika_, 52(3/4).
    
- D'Agostino, R., Stephens, M. (1986). _Goodness-of-Fit Techniques_. Wiley. Cap. 3.
    

---

## Resumen Visual: Boxplot Anotado

Un boxplot contiene **7 de las 19 métricas** a la vez:

```markdown
        ┌─ P95 (aprox.)
        │
   ○ ← outlier ( > Q3 + 1.5×IQR )
        │
  ──────┼──────  ← Q3 (75%)
        │
  ──────┼──────  ← Mediana (50%)  ←── línea central
        │
  ──────┼──────  ← Q1 (25%)
        │
   ○ ← outlier ( < Q1 - 1.5×IQR )
        │
        └─ P5 (aprox.)

  Altura de la caja = IQR
  Longitud total de bigotes ≈ Range (sin outliers)
  Si la mediana está cerca de Q1 → skewness positiva
  Si la caja es "gorda" → alta dispersión (std/IQR)   

```

## Referencias consolidadas

|     |                                                                                                              |                                                                                        |
| --- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| #   | Referencia                                                                                                   | Qué cubre                                                                              |
| 1   | Field, A. (2018). _Discovering Statistics Using IBM SPSS Statistics_ (5th ed). SAGE.                         | Tipos de variable, medidas de tendencia y dispersión, normalidad. Nivel introductorio. |
| 2   | Walpole, R. et al. (2012). _Probability & Statistics for Engineers & Scientists_ (9th ed). Pearson.          | Media, varianza, std, percentiles. Formalismo matemático.                              |
| 3   | Tukey, J. (1977). _Exploratory Data Analysis_. Addison-Wesley.                                               | Boxplots, IQR, EDA. La referencia original.                                            |
| 4   | Iglewicz, B., Hoaglin, D. (1993). _How to Detect and Handle Outliers_. ASQC.                                 | MAD, modified Z-score, IQR method.                                                     |
| 5   | Freedman, D., Pisani, R., Purves, R. (2007). _Statistics_ (4th ed). W.W. Norton.                             | Intuición estadística, CV, dispersión. Muy claro.                                      |
| 6   | Hyndman, R., Fan, Y. (1996). "Sample quantiles in statistical packages." _The American Statistician_, 50(4). | Percentiles, cómo se calculan.                                                         |
| 7   | Shapiro, S., Wilk, M. (1965). "An analysis of variance test for normality." _Biometrika_, 52(3/4).           | Test de Shapiro-Wilk. Paper original.                                                  |
| 8   | Healy, M. (2019). _Statistics: A Lifesaver_ (2nd ed). UCL Press.                                             | Interpretación de métricas, plots. Nivel bachillerato-1º.                              |
| 9   | McKinney, W. (2018). _Python for Data Analysis_ (2nd ed). O'Reilly.                                          | Pandas: select_dtypes, quantile, describe, mode.                                       |
| 10  | NIST/SEMATECH (2012). _Engineering Statistics Handbook_.                                                     | Percentiles, skewness, kurtosis. Definiciones estándar.                                |
FUNCIONES UTILES:
Habrán dos funciones generales, la primera <font color="#ffc000">vartype</font>, sera la basica de clasificacion, nos indicara en una variable tipo diccionario. Cuales son numericas o categoricas , continuas o discretas.
La segunda función, <font color="#ffff00">statsgroup</font>, hara una evaluacion de metricas mas
utilizadas para cada tipo de clase de variable reflejada en <font color="#ffff00">vartype</font>.
Ademas nos escribira en print instrucciones para observar detalladamente
esa variable por si la funcion ha detectado que tiene asimetrias, outliers en sus datos. Nos basaremos en las funciones que ya tenemos hechas.

```python
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, shapiro

# ═══════════════════════════════════════════════════════════════════════
# 1. VARTYPE — Classification
# ═══════════════════════════════════════════════════════════════════════
def vartype(df):
    """
    Classify each column into a statistical type.
    Returns a dict: {column: (family, sub_type, description)}
    
    Families: 'numeric' | 'categorical'
    Sub_types: 'continuous' | 'discrete_count' | 'ordinal_bounded' | 'nominal'
    """
    result = {}
    
    for col in df.columns:
        s = df[col].dropna()
        
        if s.dtype in ['object', 'category'] or s.nunique() <= 5 and s.dtype == 'int64':
            # Categorical (text or very few integer codes)
            if s.nunique() <= 10:
                result[col] = ('categorical', 'nominal', f'{s.nunique()} categories')
            else:
                result[col] = ('categorical', 'nominal', f'{s.nunique()} categories')
        
        elif s.dtype in ['int64', 'Int64', 'float64']:
            # Numeric — determine sub-type
            n_unique = s.nunique()
            vmin, vmax = s.min(), s.max()
            is_int = s.dropna().apply(lambda x: float(x).is_integer()).all()
            
            if is_int and 0 <= vmin and vmax <= 10 and n_unique <= 11:
                # Ordinal bounded scale (0-10)
                result[col] = ('numeric', 'ordinal_bounded', f'range {vmin:.0f}-{vmax:.0f}, {n_unique} values')
            
            elif is_int and vmin >= 0 and n_unique > 11:
                # Discrete count (0, 1, 2, ... large range)
                result[col] = ('numeric', 'discrete_count', f'range {vmin:.0f}-{vmax:.0f}, {n_unique} values')
            
            elif is_int and n_unique <= 8:
                # Few integer codes → ordinal (e.g. emplrel: 1,2,3,6)
                result[col] = ('numeric', 'ordinal_bounded', f'{n_unique} codes: {sorted(s.unique())}')
            
            else:
                # Continuous
                result[col] = ('numeric', 'continuous', f'range {vmin:.1f}-{vmax:.1f}')
        
        else:
            result[col] = ('unknown', 'unknown', f'dtype={s.dtype}')
    
    return result


def print_vartype(df):
    """Pretty-print the vartype classification."""
    types = vartype(df)
    
    print(f"{'='*65}")
    print(f"  VARIABLE TYPOLOGY  (n={len(df)} rows, {len(df.columns)} cols)")
    print(f"{'='*65}")
    print(f"{'Column':<15} {'Family':<12} {'Sub-type':<18} {'Detail'}")
    print(f"{'-'*65}")
    for col, (fam, sub, desc) in types.items():
        print(f"{col:<15} {fam:<12} {sub:<18} {desc}")
    
    # Summary
    n_num = sum(1 for f, _, _ in types.values() if f == 'numeric')
    n_cat = sum(1 for f, _, _ in types.values() if f == 'categorical')
    print(f"{'-'*65}")
    print(f"  Numeric: {n_num}  |  Categorical: {n_cat}  |  Total: {len(types)}")
    print(f"{'='*65}\n")
    
    return types


# ═══════════════════════════════════════════════════════════════════════
# 2. STATSGROUP — Type-aware profiling
# ═══════════════════════════════════════════════════════════════════════
def statsgroup(df, col, var_types=None):
    """
    Print a statistical profile for one variable, adapting metrics
    to its type. Includes diagnostic warnings.
    
    Parameters:
        df : DataFrame
        col : column name
        var_types : dict from vartype() (optional, computed if None)
    """
    if var_types is None:
        var_types = vartype(df)
    
    family, sub_type, desc = var_types[col]
    s = df[col].dropna()
    n = len(s)
    n_null = df[col].isna().sum()
    
    print(f"{'='*55}")
    print(f"  {col}  [{family}/{sub_type}]  (n={n}, nulls={n_null})")
    print(f"{'='*55}")
    
    # ─── CATEGORICAL / NOMINAL ───────────────────────────────────────────
    if family == 'categorical':
        print(f"\n  Top 10 values:")
        vc = s.value_counts()
        for val, cnt in vc.head(10).items():
            bar = '█' * int(cnt / vc.max() * 30)
            print(f"    {str(val):<15} {cnt:>6}  ({cnt/n*100:5.1f}%)  {bar}")
        if len(vc) > 10:
            print(f"    ... +{len(vc)-10} more")
        print(f"\n  Unique: {s.nunique()}")
        print(f"  Dominant: {vc.index[0]} ({vc.iloc[0]/n*100:.1f}%)")
        
        if vc.iloc[0] / n > 0.5:
            print(f"\n  ⚠️  WARNING: Top category > 50% of data. "
                  f"Check if this is expected or a data issue.")
    
    # ─── NUMERIC / ORDINAL BOUNDED (0-10 scales, few codes) ─────────────
    elif sub_type == 'ordinal_bounded':
        print(f"\n  {'Metric':<15} {'Value'}")
        print(f"  {'-'*35}")
        print(f"  {'Mean':<15} {s.mean():.4f}")
        print(f"  {'Median':<15} {s.median():.4f}")
        
        moda = s.mode()
        if not moda.empty:
            print(f"  {'Mode':<15} {moda.iloc[0]:.4f}  (freq: {s.value_counts().iloc[0]})")
        
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        print(f"  {'Q1 / Q3':<15} {q1:.4f} / {q3:.4f}")
        print(f"  {'IQR':<15} {q3-q1:.4f}")
        print(f"  {'Std':<15} {s.std():.4f}")
        print(f"  {'Min / Max':<15} {s.min():.4f} / {s.max():.4f}")
        print(f"  {'Unique':<15} {s.nunique()}")
        
        # Shape
        sk = skew(s)
        ku = kurtosis(s)
        print(f"  {'Skewness':<15} {sk:.4f}")
        print(f"  {'Kurtosis':<15} {ku:.4f}  (excess)")
        
        # Extremes
        vmin, vmax = s.min(), s.max()
        pct_min = (s == vmin).mean() * 100
        pct_max = (s == vmax).mean() * 100
        mid_lo = int(vmin + (vmax - vmin) * 0.35)
        mid_hi = int(vmin + (vmax - vmin) * 0.65)
        pct_mid = s.between(mid_lo, mid_hi).mean() * 100
        print(f"\n  % min ({vmin:.0f}):  {pct_min:.2f}%")
        print(f"  % max ({vmax:.0f}):  {pct_max:.2f}%")
        print(f"  % center ({mid_lo}-{mid_hi}): {pct_mid:.2f}%")
        
        # Diagnostics
        _diagnostics_ordinal(s, sk, ku)
    
    # ─── NUMERIC / DISCRETE COUNT (emplno, etc.) ────────────────────────
    elif sub_type == 'discrete_count':
        print(f"\n  {'Metric':<15} {'Value'}")
        print(f"  {'-'*35}")
        print(f"  {'Mean':<15} {s.mean():.4f}")
        print(f"  {'Median':<15} {s.median():.4f}")
        
        moda = s.mode()
        if not moda.empty:
            print(f"  {'Mode':<15} {moda.iloc[0]:.4f}  (freq: {s.value_counts().iloc[0]})")
        
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        mad = (s - s.median()).abs().median()
        print(f"  {'Q1 / Q3':<15} {q1:.4f} / {q3:.4f}")
        print(f"  {'IQR':<15} {iqr:.4f}")
        print(f"  {'MAD':<15} {mad:.4f}")
        print(f"  {'Std':<15} {s.std():.4f}")
        print(f"  {'Min / Max':<15} {s.min():.4f} / {s.max():.4f}")
        print(f"  {'Unique':<15} {s.nunique()}")
        
        # Point mass
        pct_zero = (s == 0).mean() * 100
        print(f"\n  % zeros (point mass): {pct_zero:.2f}%")
        
        if pct_zero > 50:
            print(f"  ⚠️  WARNING: >50% of values are 0. "
                  f"Distribution is heavily concentrated at the mode.")
            print(f"     → Use median/IQR over mean/std for summary.")
            print(f"     → Log transform (log1p) before linear modeling.")
        
        # Outliers (IQR method, only on non-zero values)
        nonzero = s[s > 0]
        if len(nonzero) > 10:
            upper_fence = q3 + 1.5 * iqr if iqr > 0 else nonzero.quantile(0.99)
            outliers = nonzero[nonzero > upper_fence]
            if len(outliers) > 0:
                print(f"\n  ⚠️  {len(outliers)} potential outliers (> {upper_fence:.1f})")
                print(f"      Max: {outliers.max():.0f}, P99: {nonzero.quantile(0.99):.1f}")
                print(f"      → Verify: are these legitimate (e.g. large firms)?")
                print(f"      → Consider winsorization at P99 if modeling.")
    
    # ─── NUMERIC / CONTINUOUS (agea, wkhtot, etc.) ──────────────────────
    elif sub_type == 'continuous':
        print(f"\n  {'Metric':<15} {'Value'}")
        print(f"  {'-'*35}")
        print(f"  {'Mean':<15} {s.mean():.4f}")
        print(f"  {'Median':<15} {s.median():.4f}")
        print(f"  {'Std':<15} {s.std():.4f}")
        
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        mad = (s - s.median()).abs().median()
        cv = s.std() / s.mean() if s.mean() != 0 else np.nan
        print(f"  {'Q1 / Q3':<15} {q1:.4f} / {q3:.4f}")
        print(f"  {'IQR':<15} {iqr:.4f}")
        print(f"  {'MAD':<15} {mad:.4f}")
        print(f"  {'CV':<15} {cv:.4f}")
        print(f"  {'Min / Max':<15} {s.min():.4f} / {s.max():.4f}")
        print(f"  {'P5 / P95':<15} {s.quantile(0.05):.4f} / {s.quantile(0.95):.4f}")
        
        # Shape
        sk = skew(s)
        ku = kurtosis(s)
        print(f"  {'Skewness':<15} {sk:.4f}")
        print(f"  {'Kurtosis':<15} {ku:.4f}  (excess)")
        
        # Outliers
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        n_out = ((s < lower) | (s > upper)).sum()
        if n_out > 0:
            print(f"\n  ⚠️  {n_out} outliers by IQR method "
                  f"(fences: [{lower:.1f}, {upper:.1f}])")
            print(f"      → Inspect: data entry errors or legitimate tails?")
        
        # Normality
        sample = s.sample(min(5000, n), random_state=42)
        stat, p = shapiro(sample)
        verdict = "NOT normal" if p < 0.05 else "No evidence against normality"
        print(f"\n  Shapiro-Wilk: W={stat:.4f}, p={p:.2e} → {verdict}")
        
        _diagnostics_continuous(s, sk, ku)
    
    print(f"{'='*55}\n")


# ─── Diagnostic helpers ──────────────────────────────────────────────────
def _diagnostics_ordinal(s, sk, ku):
    """Print warnings for ordinal bounded variables."""
    print(f"\n  ── Diagnostics ──")
    
    if abs(sk) > 0.5:
        direction = "right" if sk > 0 else "left"
        print(f"  ⚠️  Skewness = {sk:.2f} (moderate/heavy {direction} skew)")
        print(f"      → Mean is pulled toward the {direction} tail.")
        print(f"      → Prefer median over mean for summary.")
        print(f"      → Check if binning (Low/Med/High) is more appropriate.")
    elif abs(sk) > 0.2:
        print(f"  ℹ️  Mild skewness ({sk:.2f}). Mean ≈ median, OK for most uses.")
    
    if ku < -0.5:
        print(f"  ℹ️  Platykurtic (kurtosis={ku:.2f}): flatter than normal.")
        print(f"      → Typical for bounded 0-10 scales (physical ceiling/floor).")
    
    if ku > 1:
        print(f"  ⚠️  Leptokurtic (kurtosis={ku:.2f}): heavy tails + sharp peak.")
        print(f"      → Check for bimodality (two subgroups?).")
        print(f"      → Plot a histogram before assuming unimodality.")
    
    # Bimodality hint
    vc = s.value_counts().sort_index()
    if len(vc) >= 5:
        peaks = [i for i in range(1, len(vc)-1) if vc.iloc[i] > vc.iloc[i-1] and vc.iloc[i] > vc.iloc[i+1]]
        if len(peaks) >= 2:
            print(f"  ⚠️  Possible BIMODALITY: peaks at {peaks[0]} and {peaks[1]}.")
            print(f"      → Consider splitting into subgroups or using a mixture model.")


def _diagnostics_continuous(s, sk, ku):
    """Print warnings for continuous variables."""
    print(f"\n  ── Diagnostics ──")
    
    if abs(sk) > 1:
        direction = "right" if sk > 0 else "left"
        print(f"  ⚠️  Heavy {direction} skew (skewness={sk:.2f}).")
        print(f"      → Log transform (log1p) or Box-Cox recommended.")
        print(f"      → Mean is NOT representative; use median.")
    elif abs(sk) > 0.5:
        print(f"  ⚠️  Moderate skew (skewness={sk:.2f}).")
        print(f"      → Consider log1p() if using linear models.")
    
    if ku > 2:
        print(f"  ⚠️  Heavy tails (kurtosis={ku:.2f}).")
        print(f"      → Outliers may dominate variance-based methods.")
        print(f"      → Consider winsorization or robust regression.")
    
    if abs(sk) <= 0.5 and abs(ku) <= 1:
        print(f"  ✅  Shape is reasonable (skew={sk:.2f}, kurt={ku:.2f}).")
        print(f"     No transformation needed for most linear methods.")


# ═══════════════════════════════════════════════════════════════════════
# 3. USAGE
# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Classify all columns
    types = print_vartype(df_62)
    
    # Profile each column (adapts metrics to type)
    for col in df_62.columns:
        statsgroup(df_62, col, var_types=types)   

```

-------------------------------------------------------------
## Output ejemplo

```markdown
=================================================================
  VARIABLE TYPOLOGY  (n=2400 rows, 8 cols)
=================================================================
Column          Family       Sub-type           Detail
-----------------------------------------------------------------
emplno          numeric      discrete_count     range 0-400, 187 values
agea            numeric      continuous         range 18.0-93.0
emplrel         numeric      ordinal_bounded    4 codes: [1, 2, 3, 6]
edulvlb         numeric      discrete_count     range 0-800, 28 values
happy           numeric      ordinal_bounded    range 0-10, 11 values
lrscale         numeric      ordinal_bounded    range 0-10, 11 values
cntry           categorical  nominal            24 categories
EmployType      numeric      ordinal_bounded    3 codes: [1, 2, 3]
-----------------------------------------------------------------
  Numeric: 7  |  Categorical: 1  |  Total: 8
=================================================================


=======================================================
  emplno  [numeric/discrete_count]  (n=2400, nulls=0)
=======================================================

  Metric          Value
  -----------------------------------
  Mean            0.3195
  Median          0.0000
  Mode            0.0000  (freq: 2287)
  Q1 / Q3         0.0000 / 0.0000
  IQR             0.0000
  MAD             0.0000
  Std             4.0736
  Min / Max       0.0000 / 400.0000
  Unique          187

  % zeros (point mass): 95.29%
  ⚠️  WARNING: >50% of values are 0. 
     → Use median/IQR over mean/std for summary.
     → Log transform (log1p) before linear modeling.

  ⚠️  12 potential outliers (> 3.5)
      Max: 400, P99: 18.0
      → Verify: are these legitimate (e.g. large firms)?
      → Consider winsorization at P99 if modeling.
=======================================================


=======================================================
  happy  [numeric/ordinal_bounded]  (n=2400, nulls=0)
=======================================================

  Metric          Value
  -----------------------------------
  Mean            6.8425
  Median          7.0000
  Mode            7.0000  (freq: 512)
  Q1 / Q3         6.0000 / 8.0000
  IQR             2.0000
  Std             2.1034
  Min / Max       0.0000 / 10.0000
  Unique          11
  Skewness        -0.5231
  Kurtosis        -0.7812  (excess)

  % min (0):  1.25%
  % max (10): 18.75%
  % center (3-7): 52.33%

  ── Diagnostics ──
  ⚠️  Skewness = -0.52 (moderate/heavy left skew)
      → Mean is pulled toward the left tail.
      → Prefer median over mean for summary.
      → Check if binning (Low/Med/High) is more appropriate.
  ℹ️  Platykurtic (kurtosis=-0.78): flatter than normal.
      → Typical for bounded 0-10 scales (physical ceiling/floor).
=======================================================   

```