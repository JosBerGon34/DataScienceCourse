
---

## Índice

| Tipo de variable | Transformaciones |
|-----------------|-----------------|
| **Continua** (agea, income, wkhtot) | Log, Box-Cox, Yeo-Johnson, Z-score, Min-max, √, 1/x, Winsorización, Binning |
| **Discreta / Count** (emplno, children) | Log1p, √, Binning, Winsorización, Zero-inflation split |
| **Ordinal acotada** (lrscale, happy, 0-10) | Binning, Centering, Reversal, Factorización, Tratar como continua |
| **Ordinal pocos códigos** (emplrel, health) | One-hot, Ordinal encoding, Target encoding |
| **Nominal / Categórica** (cntry, gndr) | One-hot, Ordinal, Target, Binary, Frequency, Grouping |
| **Texto** (si aparece) | Tokenización, TF-IDF, Embeddings |

---

## 1. VARIABLES CONTINUAS

### 1.1 Logarítmica — `log1p(x)`

**Definición:** Aplica `ln(1 + x)` a cada valor. El `+1` permite manejar ceros (ln(0) no existe).

**Cuándo usarla:**
- La variable es **positiva** (no tiene valores negativos).
- Tiene **cola larga a la derecha** (skewness > 1).
- Tiene **masa puntual en 0** con una cola de valores grandes (ej. `emplno`: 95% ceros + algunos 400).
- Quieres que el modelo no le dé peso desproporcionado a los valores extremos.

**Efecto:** Comprime la cola. Un salto de 1→2 se ve igual que un salto de 100→200.


```python
import numpy as np
df['emplno_log'] = np.log1p(df['emplno'])   
```

**En un plot:**

- Antes: histograma con una barra enorme en 0 y una cola que se extiende hasta 400.
    
- Después: la cola se "aplasta" hacia la izquierda. El 0 sigue en 0 (log1p(0)=0), pero el 400 pasa a ~6. El histograma se ve más compacto.
    

**Cuándo NO usarla:**

- Si la variable tiene valores negativos (edad no, pero un "cambio de temperatura" sí).
    
- Si la variable ya es simétrica (skewness ≈ 0) → no gana nada.
    

**Bibliografía:**

- Weisberg, S. (2021). _Applied Linear Regression_ (5th ed). Wiley. Cap. 3.
    
- Kleinberg, B., Tuzhilin, A. (2019). _Feature Engineering and Selection_ (2nd ed). CRC Press. Cap. 2.
    

---

### 1.2 Box-Cox

**Definición:** Familia de transformaciones paramétricas:


$$
y(λ)={λyλ−1​ln(y)​λ=0λ=0​
$$


El parámetro `λ` se **estima de los datos** (maximiza la verosimilitud gaussiana).

**Cuándo usarla:**

- Variable continua **estRICTAMENTE positiva** (no admite 0 ni negativos).
    
- Quieres una transformación "óptima" sin adivinar si es log, √, o 1/x.
    
- El objetivo es **maximizar la normalidad** de la variable.
    

**Efecto:** Similar a log, pero el exponente se ajusta. Si λ≈0 → es log. Si λ≈0.5 → es √. Si λ≈1 → no transforma.

```python
from scipy.stats import boxcox
transformed, lambda_opt = boxcox(df['agea'].values)
print(f"λ óptimo: {lambda_opt:.3f}")  
```

**Límite:** No funciona con ceros ni negativos. Si tu variable tiene 0, usa Yeo-Johnson (1.3).

**En un plot:**

- Igual que log: la cola se comprime. La diferencia es que el "grado" de compresión es el óptimo para TU variable, no uno fijo.
    

**Bibliografía:**

- Box, G., Cox, D. (1964). "An analysis of transformations." _Journal of the Royal Statistical Society_, 26(2).
    
- NIST (2012). "Box-Cox Transformation." _Engineering Statistics Handbook_.
    

---

### 1.3 Yeo-Johnson

**Definición:** Extensión de Box-Cox que **sí admite ceros y negativos**. Mismo objetivo (maximizar normalidad), mismo parámetro λ estimado.

**Cuándo usarla:**

- Variable continua con valores negativos o ceros.
    
- Quieres lo mismo que Box-Cox pero sin restricciones de signo.
```python
from scipy.stats import yeojohnson
transformed, lambda_opt = yeojohnson(df['col'].values.reshape(-1, 1))   
```

**Bibliografía:**

- Yeo, I., Johnson, R. (2000). "A new family of power transformations to improve normality or symmetry." _Biometrika_, 87(2).
    

---

### 1.4 Z-score (Estandarización)

**Definición:**

$$
z=sx−xˉ​
$$

Después de la transformación: media = 0, std = 1.

**Cuándo usarla:**

- Antes de **KMeans, SVM, Regresión con regularización (Ridge/Lasso), PCA**.
    
- Cuando quieres comparar variables con escalas distintas (edad en años vs. ingresos en miles de €).
    
- **No** es necesaria para árboles (Random Forest, XGBoost) — son invariantes a escalado.
    

**Efecto:** No cambia la forma de la distribución, solo la re-centra y re-escala. Si antes era asimétrica, sigue siéndolo.

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df['agea_z'] = scaler.fit_transform(df[['agea']])   
```

**En un plot:**

- Histograma con forma idéntica, pero el eje X ahora va de -2 a +2 (aprox.) en vez de 18 a 93.
    
- La línea de media está en 0.
    

**Bibliografía:**

- Bishop, C. (2006). _Pattern Recognition and Machine Learning_. Springer. Cap. 2.
    
- scikit-learn docs: `StandardScaler`.
    

---

### 1.5 Min-Max Normalización

**Definición:**

Xnorm= (X-Xmin)/(Xmax-Xmin)

Después: mínimo = 0, máximo = 1. Todo queda en [0, 1].

**Cuándo usarla:**

- Redes neuronales (las activaciones sigmoid/tanh prefieren input en [0,1] o [-1,1]).
    
- Cuando necesitas que todos los features estén en el mismo rango.
    
- **Menos robusta que Z-score** a outliers: un solo valor extremo estira la escala y comprime el resto.
    

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['agea_norm'] = scaler.fit_transform(df[['agea']])
```

**En un plot:**

- Misma forma, eje X de 0 a 1.
    
- Si hay un outlier en 93, todos los demás se aplastan entre 0 y 0.8.
    

**Bibliografía:**

- Bishop, C. (2006). _PRML_. Cap. 2.
    
- scikit-learn docs: `MinMaxScaler`.
    

---

### 1.6 Raíz cuadrada — `sqrt(x)`

**Definición:** `√x`. Compresión más suave que log.

**Cuándo usarla:**

- Variable de conteo con varianza ≈ media (distribución de Poisson).
    
- Skewness moderada (0.5 < skew < 1) → log es demasiado agresivo, √ es justo.

```python
df['col_sqrt'] = np.sqrt(df['col'].clip(lower=0))
```

**Bibliografía:**

- Weisberg, S. (2021). _Applied Linear Regression_. Cap. 3.
    

---

### 1.7 Recíproca — `1/x`

**Definición:** Invierte la variable. Valores grandes → pequeños, y viceversa.

**Cuándo usarla:**

- Variable que mide "tiempo por unidad" (ej. segundos por tarea) y quieres "velocidad".
    
- Skewness positiva fuerte y log no es suficiente.
    
- **Límite:** no funciona con 0 (1/0 = ∞).

```python
df['col_inv'] = 1 / df['col'].replace(0, np.nan) 
```

**Bibliografía:**

- Weisberg, S. (2021). _Applied Linear Regression_. Cap. 3.
    

---

### 1.8 Winsorización / Clipping

**Definición:** Capa los valores extremos en un percentil.

```python
x_winsorizado = clip(x, P1, P99)   
```

Todo lo que está por debajo del 1% → P1. Todo lo que está por encima del 99% → P99.

**Cuándo usarla:**

- Los outliers son **legítimos** (no son errores de entrada) pero distorsionan el modelo.
    
- Quieres mantener la observación (no borrarla) pero limitar su influencia.
    
- Variable con cola muy larga donde el 1% superior mueve la media.
    

**Diferencia con "remover outliers":**

|             |                   |                            |
| ----------- | ----------------- | -------------------------- |
|             | Remover           | Winsorizar                 |
| Filas       | Se pierden        | Se mantienen               |
| Información | Se pierde el dato | Se conserva (capado)       |
| Cuándo      | Error de entrada  | Variación legítima extrema |
```python
lower = df['emplno'].quantile(0.01)
upper = df['emplno'].quantile(0.99)
df['emplno_winsor'] = df['emplno'].clip(lower=lower, upper=upper)  	
```

**En un plot:**

- Histograma: las barras más extremas desaparecen o se "apilan" en P1 y P99.
    
- Boxplot: los bigotes se acortan, los outliers desaparecen (o se mueven a la punta del bigote).
    

**Bibliografía:**

- Winsor, C. (1926). "Small samples from approximate normal populations." _Journal of the Royal Statistical Society_, 9(1).
    
- Iglewicz & Hoaglin (1993). _How to Detect and Handle Outliers_. Cap. 3.
    

---

### 1.9 Binning de continua → ordinal

**Definición:** Divide la variable continua en intervalos (bins) y la convierte en ordinal.

**Cuándo usarla:**

- La relación con el target es **no lineal** (ej. la felicidad no sube linealmente con la edad).
    
- Quieres que un árbol o un modelo lineal capture "tramos" en vez de una pendiente constante.
    
- Para interpretabilidad: "31-50 años" se entiende mejor que "43.7 años".
    

**Métodos de binning:**

|             |                                                      |                                                                      |
| ----------- | ---------------------------------------------------- | -------------------------------------------------------------------- |
| Método      | Función                                              | Cuándo                                                               |
| `pd.cut()`  | Ancho fijo o edges manuales                          | Cuando el dominio define los tramos (edad: 18-30, 31-50, 51-65, 65+) |
| `pd.qcut()` | Frecuencia igual (cada bin tiene el mismo nº de obs) | Cuando no hay tramos naturales y quieres balance                     |

```python
# Edges manuales (domain-informed)
df['agea_bin'] = pd.cut(df['agea'], bins=[18, 30, 50, 65, 100],
                        labels=['18-30', '31-50', '51-65', '65+'])

# Cuantiles (equal-frequency, 4 bins)
df['agea_qcut'] = pd.qcut(df['agea'], q=4, duplicates='drop') 
```

**En un plot:**

- Antes: histograma continuo.
    
- Después: bar chart con 4 barras (una por bin). Se pierde la resolución interna del bin.
    

**Bibliografía:**

- McKinney, W. (2018). _Python for Data Analysis_. O'Reilly. Cap. 14.
    
- Chen, C., Maloof, M. (2007). "Fast binning methods for data visualization." _KDD_.
    

---

## 2. VARIABLES DISCRETAS / COUNT

### 2.1 Log1p (mismo que 1.1)

Es la transformación **más usada** para count variables. `emplno` con 95% ceros:

```python
df['emplno_log'] = np.log1p(df['emplno'])
# 0 → 0,  1 → 0.69,  5 → 1.79,  400 → 5.99   
```

La cola se comprime de 400 unidades a 6 unidades.

### 2.2 Raíz cuadrada

Más suave que log. Útil si la varianza ≈ media (Poisson):

```python
df['emplno_sqrt'] = np.sqrt(df['emplno'])
```

### 2.3 Binning

```python
df['emplno_bin'] = pd.cut(df['emplno'], bins=[-1, 0, 1, 5, 20, 500],
                          labels=['0', '1', '2-5', '6-20', '21+'])   
```

Útil cuando el modelo trata mejor categorías que números grandes.

### 2.4 Winsorización

Mismo que 1.8. Capar en P99 para que un self-employed con 400 empleados no domine la varianza.

### 2.5 Zero-inflation split

**Definición:** Separar la variable en dos:

1. **Binaria:** ¿es 0 o no? (Bernoulli)
    
2. **Condicionada:** dado que es > 0, ¿cuánto? (count truncada)
    

**Cuándo usarla:**

- > 50% de ceros (zero-inflated model).
    
- El "por qué es 0" es distinto del "por qué es 5 vs. 20".

```python
df['emplno_is_zero'] = (df['emplno'] == 0).astype(int)
df['emplno_nonzero'] = df['emplno'].where(df['emplno'] > 0)  # NaN si es 0   
```

**Bibliografía:**

- Hilbe, J. (2011). _Negative Binomial Regression_. Oxford University Press. Cap. 1.
    
- Kennedy, P. (2008). _A Guide to Econometrics_ (6th ed). MIT Press. Cap. 17.
    

---

## 3. VARIABLES ORDINALES ACOTADAS (0-10, Likert 1-5)

### 3.1 Binning (discretización en tiers)

**Definición:** Agrupar la escala 0-10 en 3-5 categorías.

**Cuándo usarla:**

- La relación con el target es **no lineal** (ej. no hay diferencia entre 4 y 5, pero sí entre 3 y 7).
    
- Quieres interpretabilidad: "baja confianza / media / alta confianza".
    
- El modelo es un árbol o un modelo lineal con interacciones.

```python
# 3 tiers (terciles)
df['happy_bin'] = pd.qcut(df['happy'], q=3, labels=['Low', 'Medium', 'High'])

# O con edges manuales
df['happy_bin2'] = pd.cut(df['happy'], bins=[-1, 3, 6, 10],
                          labels=['Low (0-3)', 'Medium (4-6)', 'High (7-10)'])   

```

**En un plot:**

- Antes: histograma con 11 barras.
    
- Después: bar chart con 3 barras. Más limpio, menos resolución.
    

**Bibliografía:**

- Agresti, A. (2010). _Categorical Data Analysis_ (3rd ed). Wiley. Cap. 1.
    

---

### 3.2 Centering (centrado)

**Definición:** Restar el punto medio de la escala.

xcentered​=x−5(para escala 0-10)

**Cuándo usarla:**

- En modelos con **interacciones** (A × B). Centrar reduce la multicolinealidad entre el main effect y la interacción.
    
- Para que el coeficiente de la constante (intercept) tenga interpretación: "el valor del target cuando la variable está en el punto medio".

```python
df['lrscale_c'] = df['lrscale'] - 5  # ahora va de -5 a +5
```

**En un plot:**

- Misma forma, el eje X va de -5 a +5 en vez de 0 a 10. El centro (0) es el punto medio de la escala.
    

**Bibliografía:**

- CENTERS, J., GREEN, S. (1990). "Main effects, interactions, and centering." _Journal of Educational Statistics_, 15(3).
    
- Stone, J. (2006). "Yet anotherCautionary tale about mean centering." _Structural Equation Modeling_, 13(4).
    

---

### 3.3 Reversal (inversión de escala)

**Definición:** Invertir la dirección de la escala.

xreversed​=max−x

**Cuándo usarla:**

- Algunas preguntas están formuladas en sentido contrario ("No confío en nadie" vs. "Confío en la gente").
    
- Para hacer **composite scores** (media de varias preguntas): todas deben apuntar en la misma dirección.

```python
df['ppltrst_rev'] = 10 - df['ppltrst']  # ahora 0 = "confío", 10 = "no confío"
```

**Bibliografía:**

- Hair, J., Black, W., Babin, B., Anderson, R. (2019). _Multivariate Data Analysis_ (8th ed). Cengage. Cap. 4.
    

---

### 3.4 Factorización (ordinal → categórico)

**Definición:** Tratar la ordinal como **nominal** (perder el orden).

**Cuándo usarla:**

- Cuando el orden no importa para el modelo (ej. `emplrel`: Employee / Self-employed / Family — no hay "más" o "menos").
    
- Para one-hot encoding.

```python
df['emplrel_cat'] = pd.Categorical(df['emplrel'], ordered=False)
# o directamente:
df = pd.get_dummies(df, columns=['emplrel'], prefix='emplrel') 
```

**Bibliografía:**

- Pedregosa, F. et al. (2011). "Scikit-learn: Machine learning in Python." _JMLR_, 12.
    

---

### 3.5 Tratar como continua

**Cuándo SÍ es aceptable:**

- Escala con ≥ 5 puntos (0-10, 1-7).
    
- La distribución es razonablemente simétrica (skewness < 0.5).
    
- No hay masa puntual extrema (ningún valor > 30% del total).
    
- El modelo es lineal y la relación con el target es aproximadamente lineal.
    

**Cuándo NO:**

- Escala con 2-3 puntos (sí/no, alto/bajo) → es binaria, no continua.
    
- Masa puntual > 30% en un valor → el "orden" es artificial.
    
- Relación no lineal con el target → binning es mejor.
    

**Bibliografía:**

- Hayes, A., Catherine, M. (2007). "Using the residual method to assess linearity." _Psychological Methods_, 12(1).
    
- Ruxton, G. (2006). "The error of treating ordinal data as interval data." _Acta Oecologica_, 20(3).
    

---

## 4. VARIABLES ORDINALES CON POCOS CÓDIGOS (2-8 valores)

### 4.1 One-hot encoding

**Definición:** Crear una columna binaria por cada categoría.
```python
emplrel = 1 → [1, 0, 0]  (Employee)
emplrel = 2 → [0, 1, 0]  (Self-employed)
emplrel = 3 → [0, 0, 1]  (Family)   
```

**Cuándo usarla:**

- **Nominal** (no hay orden): `cntry`, `gndr`.
    
- Ordinal con ≤ 5 niveles y el modelo no sabe aprovechar el orden (redes neuronales, SVM).
    
- **Problema:** con muchas categorías (24 países) → 24 columnas. Maledición de la dimensionalidad.

```python
df = pd.get_dummies(df, columns=['gndr'], prefix='gndr')
# gndr_1 (Male), gndr_2 (Female) 
```

**Bibliografía:**

- Pedregosa et al. (2011). _JMLR_.
    
- Goodfellow, I., Bengio, Y., Courville, A. (2016). _Deep Learning_. MIT Press. Cap. 6.
    

---

### 4.2 Ordinal encoding (preservar orden)

**Definición:** Mapear cada categoría a un entero que respeta el orden.

```python
health: 1→1, 2→2, 3→3, 4→4, 5→5  (Very good → Very bad) 
```

**Cuándo usarla:**

- Ordinal con orden claro (health, edulvlb).
    
- Modelos basados en árboles (RF, XGBoost) — pueden hacer splits en cualquier punto.
    
- **Límite:** para modelos lineales, asume que la distancia 1→2 es igual que 4→5 (a veces no es cierto).

```python
# Ya es ordinal si los códigos son 1,2,3,4,5
# Si son textos:
mapping = {'Very good': 1, 'Good': 2, 'Fair': 3, 'Bad': 4, 'Very bad': 5}
df['health_ord'] = df['health'].map(mapping) 
```

**Bibliografía:**

- Ordóñez, M., Vajda, S. (2014). "On the use of ordinal encoding for categorical variables." _IEEE SSCI_.
    

---

### 4.3 Target encoding (mean encoding)

**Definición:** Reemplazar cada categoría por la **media del target** para esa categoría.

```python
cntry = 'ES' → media de lrscale en España = 4.8
cntry = 'DE' → media de lrscale en Alemania = 5.2   
```

**Cuándo usarla:**

- Nominal con **muchas categorías** (24 países, 500 ciudades).
    
- Modelos lineales donde one-hot explota la dimensionalidad.
    
- **Riesgo:** data leakage si se calcula con el target completo. Hay que hacer cross-validation (encode en train, aplicar en test).

```python
# Simple (con leakage — solo para entender el concepto)
target_mean = df.groupby('cntry')['lrscale'].transform('mean')
df['cntry_target'] = target_mean

# Correcto (sin leakage):
from category_encoders import TargetEncoder
enc = TargetEncoder(cols=['cntry'])
df['cntry_target'] = enc.fit_transform(df[['cntry']], df['lrscale'])   
```

**Bibliografía:**

- Micci-Barre, D. (2001). "A hierarchical Bayesian model for classification with Bayesian logistic regression." _AAAI_.
    
- Grinsztajn, L., Oyallon, E., Varoquaux, G. (2022). "Why do tree-based models still outperform deep learning on typical tabular data?" _NeurIPS_.
    

---

## 5. VARIABLES NOMINALES / CATEGÓRICAS

### 5.1 One-hot encoding (mismo que 4.1)

Para `gndr` (2 valores) → 1 columna (binaria). Para `cntry` (24 valores) → 23 columnas (una se cae por dummy variable trap).

```python
df = pd.get_dummies(df, columns=['cntry'], drop_first=True, prefix='cntry')
```

### 5.2 Binary encoding

**Definición:** Convertir el código entero a binario. 24 categorías → 5 bits (2⁵=32 ≥ 24).

**Cuándo usarla:**

- Muchas categorías (> 10) y one-hot es demasiado amplio.
    
- Menos interpretable que one-hot, pero más compacta.

```python
from category_encoders import BinaryEncoder
enc = BinaryEncoder(cols=['cntry'])
df[['cntry_b0','cntry_b1','cntry_b2','cntry_b3','cntry_b4']] = enc.fit_transform(df[['cntry']])
```

### 5.3 Frequency encoding

**Definición:** Reemplazar cada categoría por su **frecuencia** (o proporción) en el dataset.

```python
cntry = 'IT' → 0.12  (12% de la muestra)
cntry = 'NO' → 0.03  (3% de la muestra)   
```

**Cuándo usarla:**

- El tamaño del grupo importa (un país con 2000 respondents es distinto de uno con 200).
    
- No requiere target → no hay leakage.
    
- Útil como feature adicional junto a one-hot.
```python
freq = df['cntry'].value_counts(normalize=True)
df['cntry_freq'] = df['cntry'].map(freq) 
```

### 5.4 Grouping rare categories

**Definición:** Agrupar las categorías que aparecen muy pocas veces en un bucket "Other".

**Cuándo usarla:**

- Una categoría aparece 3 veces de 41.000 → el modelo no puede aprender nada de ella.
    
- Regla práctica: si una categoría tiene < 5% (o < 30 obs) → "Other".

```python
threshold = df['cntry'].value_counts(normalize=True) * 0.05
rare = df['cntry'].value_counts(normalize=True)[lambda x: x < 0.05].index
df['cntry_grp'] = df['cntry'].where(~df['cntry'].isin(rare), 'Other')

```

### 5.5 Hash encoding

**Definición:** Aplicar una función hash a la categoría y mapear a un rango fijo de K buckets.

**Cuándo usarla:**

- Categorias con cardinalidad **muy alta** (millones de valores: IDs, URLs).
    
- Streaming: no necesitas "ver" todas las categorías antes de codificar.
    
- **Problema:** colisiones (dos categorías distintas pueden caer en el mismo bucket).

```python
from category_encoders import HashingEncoder
enc = HashingEncoder(cols=['cntry'], n_components=8)
df[['h0','h1','h2','h3','h4','h5','h6','h7']] = enc.fit_transform(df[['cntry']]) 
```

**Bibliografía:**

- Weinsberg, S. (2018). "A comparison of encoding schemes for rare categories." _Journal of Data Science_, 16(1).
    
- Grinsztajn et al. (2022). _NeurIPS_.
    

---

## 6. VARIABLES DE TEXTO (si aparecen)

### 6.1 Tokenización + Bag of Words

**Definición:** Cortar el texto en palabras → vector de frecuencias.

**Cuándo:** Texto corto (títulos, etiquetas). No para párrafos largos.

### 6.2 TF-IDF

**Definición:** Frecuencia del término ponderada por su rareza global.

**Cuándo:** Texto medio (resúmenes, comentarios). Reduce el peso de palabras comunes ("the", "de", "en").

### 6.3 Embeddings

**Definición:** Vector denso de dimensión fija (300, 768…) que captura semántica.

**Cuándo:** Texto largo, necesitas capturar significado (no solo frecuencia).

```python
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=1000)
df['text_vec'] = tfidf.fit_transform(df['text_column'])
```

**Bibliografía:**

- Jurafsky, D., Martin, J. (2023). _Speech and Language Processing_ (3rd ed). draft.
    
- Mikolov, T. et al. (2013). "Distributed representations of words and phrases." _NeurIPS_.
    

---

## Tabla resumen: "¿Qué le hago a esta variable?"

```markdown
¿Qué tipo es?
│
├── CONTINUA
│   ├── ¿Skewness > 1?
│   │   ├── ¿Tiene ceros/negativos? → Yeo-Johnson
│   │   └── ¿Solo positivos? → Box-Cox o log1p
│   ├── ¿Outliers legítimos? → Winsorización (P1/P99)
│   ├── ¿Antes de KMeans/SVM/PCA? → Z-score
│   ├── ¿Red neuronal? → Min-Max
│   └── ¿Relación no lineal con target? → Binning
│
├── DISCRETA / COUNT
│   ├── ¿>50% ceros? → Zero-inflation split o log1p
│   ├── ¿Cola larga? → log1p o √
│   └── ¿Pocos valores distintos? → Binning
│
├── ORDINAL 0-10 (o 1-7, 1-5)
│   ├── ¿≥5 puntos + simétrica + sin masa puntual? → Tratar como continua
│   ├── ¿Relación no lineal? → Binning (3-5 tiers)
│   ├── ¿Modelo con interacciones? → Centering
│   ├── ¿Preguntas inversas? → Reversal
│   └── ¿Orden no importa? → Factorización → One-hot
│
├── ORDINAL POCOS CÓDIGOS (2-8)
│   ├── ¿Hay orden? → Ordinal encoding
│   ├── ¿No hay orden? → One-hot
│   └── ¿Modelo lineal + muchas categorías? → Target encoding
│
└── NOMINAL
    ├── ¿Pocas categorías (≤10)? → One-hot
    ├── ¿Muchas categorías (>10)? → Target / Binary / Hash
    ├── ¿Categorías raras (<5%)? → Grouping en "Other"
    └── ¿El tamaño del grupo importa? → Frequency encoding   

```

## Referencias consolidadas

|     |                                                                                                                                                  |                                                        |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------ |
| #   | Referencia                                                                                                                                       | Qué cubre                                              |
| 1   | Weisberg, S. (2021). _Applied Linear Regression_ (5th ed). Wiley.                                                                                | Log, Box-Cox, √, 1/x, diagnóstico de transformaciones. |
| 2   | Box, G., Cox, D. (1964). "An analysis of transformations." _JRSS-B_, 26(2).                                                                      | Paper original de Box-Cox.                             |
| 3   | Yeo, I., Johnson, R. (2000). "A new family of power transformations." _Biometrika_, 87(2).                                                       | Yeo-Johnson.                                           |
| 4   | Kleinberg, B., Tuzhilin, A. (2019). _Feature Engineering and Selection_ (2nd ed). CRC Press.                                                     | Binning, encoding, pipeline completo.                  |
| 5   | Grinsztajn, L., Oyallon, E., Varoquaux, G. (2022). "Why do tree-based models still outperform deep learning on typical tabular data?" _NeurIPS_. | Encoding para tabulares, target encoding.              |
| 6   | Pedregosa, F. et al. (2011). "Scikit-learn: Machine learning in Python." _JMLR_, 12.                                                             | StandardScaler, MinMaxScaler, pipeline.                |
| 7   | Iglewicz, B., Hoaglin, D. (1993). _How to Detect and Handle Outliers_. ASQC.                                                                     | Winsorización, clipping, MAD.                          |
| 8   | Agresti, A. (2010). _Categorical Data Analysis_ (3rd ed). Wiley.                                                                                 | Ordinal → categórico, binning de ordinales.            |
| 9   | CENTERS, J., GREEN, S. (1990). "Main effects, interactions, and centering." _J. Educ. Statistics_, 15(3).                                        | Centering para interacciones.                          |
| 10  | Weinsberg, S. (2018). "A comparison of encoding schemes for rare categories." _J. Data Science_, 16(1).                                          | One-hot vs. target vs. binary vs. hash.                |
| 11  | Goodfellow, I., Bengio, Y., Courville, A. (2016). _Deep Learning_. MIT Press.                                                                    | One-hot, embeddings, normalización para redes.         |
| 12  | scikit-learn documentation. `sklearn.preprocessing`.                                                                                             | Implementación de todas las transformaciones estándar. |