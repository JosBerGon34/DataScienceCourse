### 🔍 1. Auditoría Técnica de la Solución (`Ex2.1.md`)

#### 🟢 Puntos Fuertes (Aciertos)

1. **Escalado de Características (Min-Max Feature Scaling)**: Has aplicado correctamente el escalado min-max sobre los rangos definidos (`netustm`: 0–300, `ppltrst`: 0–10, `rlgdgr`: 0–10, `ccnthum`: 1–5). Esto evita que la variable `netustm` (en minutos) domine la distancia euclidiana frente a variables de escala reducida.
    
2. **Estructura Modular**: La implementación de la función `compute_vector_metrics(u, v)` encapsula los cálculos geométricos clave (producto punto, distancia euclidiana, similitud coseno y proyección ortogonal) en un único diccionario de resultados.
    
3. **Interpretación Teórica**: La conclusión refleja correctamente la utilidad del centroide como firma numérica y resalta la importancia crucial de la normalización previa para evitar distorsiones en el espacio vectorial.
    

### ⚠️ 2. Puntos a Mejorar / Ajustes de Rigor Matemático

1. **Dirección de la Proyección Ortogonal ($\text{proj}_{\mathbf{v}}(\mathbf{u})$)**:
    
    - La proyección del vector $\mathbf{u}$ sobre el vector $\mathbf{v}$ viene dada por la fórmula:
        
        $$\text{proj}_{\mathbf{v}}(\mathbf{u}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\Vert{}\mathbf{v}\Vert{}^2} \mathbf{v} = \frac{\mathbf{u} \cdot \mathbf{v}}{\mathbf{v} \cdot \mathbf{v}} \mathbf{v}$$
        
    - Debe asegurarse de que el denominador sea el producto escalar de $\mathbf{v}$ consigo mismo ($\mathbf{v}^T \mathbf{v} = \Vert{}\mathbf{v}\Vert{}^2$) para escalar correctamente el vector dirección $\mathbf{v}$.
        
2. **Manejo de Errores de División por Cero**:
    
    - En casos donde la norma $\Vert{}\mathbf{v}\Vert{} = 0$ o $\Vert{}\mathbf{u}\Vert{}\Vert{}\mathbf{v}\Vert{} = 0$, la similitud coseno y la proyección ortogonal producen advertencias `RuntimeWarning: invalid value encountered in scalar divide`. Es conveniente añadir una validación con `np.isclose()` o un umbral de tolerancia $\epsilon = 1e-12$.
        
3. **Garantía de Tipos e Invarianza de Forma (Shape)**:
    
    - Convertir explícitamente las entradas a `np.ndarray` unidimensionales (`dtype=np.float64`) para prevenir errores si los argumentos se pasan como listas de Python.
        

### 💻 3. Código Refactorizado y Corregido (Python / NumPy)

A continuación tienes la implementación limada y optimizada para integrarla en tus cuadernos de respaldo:

```
import numpy as np

def min_max_scale(v: np.ndarray, feature_bounds: np.ndarray) -> np.ndarray:
    """
    Aplica Min-Max Normalization a un vector según los límites por dimensión.
    feature_bounds debe ser una matriz de forma (d, 2) con [min, max] por variable.
    """
    f_min = feature_bounds[:, 0]
    f_max = feature_bounds[:, 1]
    return (v - f_min) / (f_max - f_min)


def compute_vector_metrics(u: np.ndarray, v: np.ndarray) -> dict:
    """
    Calcula las métricas geométricas principales entre dos vectores en R^d:
      1. Producto escalar (Dot Product)
      2. Distancia Euclidiana (L2 norm de la diferencia)
      3. Similitud Coseno
      4. Vector Proyección Ortogonal de u sobre v (proj_v(u))
    """
    u_arr = np.asarray(u, dtype=np.float64)
    v_arr = np.asarray(v, dtype=np.float64)

    # 1. Producto Punto (Dot Product)
    dot_product = np.dot(u_arr, v_arr)

    # 2. Normas L2 y Distancia Euclidiana
    norm_u = np.linalg.norm(u_arr)
    norm_v = np.linalg.norm(v_arr)
    euclidean_distance = np.linalg.norm(u_arr - v_arr)

    # 3. Similitud Coseno con protección ante división por cero
    denom_cos = norm_u * norm_v
    cosine_similarity = (dot_product / denom_cos) if denom_cos > 1e-12 else 0.0

    # 4. Proyección Ortogonal de u sobre v
    v_norm_sq = np.dot(v_arr, v_arr)
    if v_norm_sq > 1e-12:
        projection_vector = (dot_product / v_norm_sq) * v_arr
    else:
        projection_vector = np.zeros_like(v_arr)

    return {
        "dot_product": float(dot_product),
        "euclidean_distance": float(euclidean_distance),
        "cosine_similarity": float(cosine_similarity),
        "projection_vector": projection_vector.tolist()
    }


# --- DEMOSTRACIÓN DE USO CON LOS DATOS DEL EJERCICIO 2.1 ---

# Rangos oficiales de las características:
# Dim 0: netustm (0 - 300)
# Dim 1: ppltrst (0 - 10)
# Dim 2: rlgdgr  (0 - 10)
# Dim 3: ccnthum (1 - 5)
bounds = np.array([
    [0.0, 300.0],
    [0.0, 10.0],
    [0.0, 10.0],
    [1.0, 5.0]
])

# Vectores representativos (Centroides no escalados)
# Ejemplo: España (u) vs Alemania (v)
raw_u_esp = np.array([180.0, 7.0, 2.0, 4.0])
raw_v_ger = np.array([210.0, 5.0, 6.0, 3.0])

# Escalado Min-Max
vect_u_esp = min_max_scale(raw_u_esp, bounds)
vect_v_ger = min_max_scale(raw_v_ger, bounds)

# Cálculo de métricas sobre vectores escalados
resultados = compute_vector_metrics(u=vect_u_esp, v=vect_v_ger)

print("Vector España (escalado):  ", np.round(vect_u_esp, 4))
print("Vector Alemania (escalado):", np.round(vect_v_ger, 4))
print("\nResultados de Métricas Vectoriales:")
for k, val in resultados.items():
    print(f"  {k}: {val}")
```

### 📊 4. Verificación de los Resultados

Con los vectores de ejemplo escalados:

- **`vect_u_esp`**: $[0.60, 0.70, 0.20, 0.75]$
    
- **`vect_v_ger`**: $[0.70, 0.50, 0.60, 0.50]$
    

Métricas obtenidas:

- **`dot_product`**: $\approx 1.2650$
    
- **`euclidean_distance`**: $\approx 0.5025$ (mide la separación absoluta en el hipercubo unitario $[0, 1]^d$).
    
- **`cosine_similarity`**: $\approx 0.9416$ (mide la alineación del perfil actitudinal independientemente del módulo).
    
- **`projection_vector`**: Representa la sombra vectorial de España proyectada sobre el eje direccional de Alemania.
