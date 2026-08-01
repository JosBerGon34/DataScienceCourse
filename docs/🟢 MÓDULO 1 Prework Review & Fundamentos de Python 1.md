#### **Ejercicio 1: Estructuras de Datos Nativas, Tipado Estricto y Promedios sobre Registros de Eurostat**

#### 📐 1. Instrucciones a Nivel Sintáctico-Algebraico

Sea un conjunto de datos tabular representado como una secuencia finita $D = \{r_1, r_2, \dots, r_n\}$, donde cada elemento $r_i$ es una tupla clave-valor (mapeo o diccionario en ciencias del cómputo):

$$r_i = \{ k_1: v_{i,1}, k_2: v_{i,2}, \dots, k_m: v_{i,m} \}$$

Definimos la función de extracción $g(r_i, k)$ que obtiene el valor asociado a la clave $k$. Para calcular la media aritmética $\bar{x}$ sobre una clave numérica específica $k_{\text{target}}$:

$$\bar{x} = \frac{1}{\vert{}D'\vert{}} \sum_{r_i \in D'} g(r_i, k_{\text{target}})$$

donde $D' = \{ r_i \in D \mid g(r_i, k_{\text{target}}) \in \mathbb{R} \}$ es el subconjunto válido que excluye valores nulos ($None$) o no numéricos para evitar errores de tipo ($\text{TypeError}$).

#### 💼 2. Contextualización Aplicada

En los microdatos macroeconómicos de Eurostat (como los datos de desempleo `sample_DesempleoEU.csv`), la información se compone de múltiples dimensiones socioeconómicas: país (`geo`), periodo temporal (`TIME_PERIOD`), estrato de edad (`age`), sexo (`sex`) y la variable observada (`OBS_VALUE`).

Antes de cargar estos datos en DataFrames de Pandas, es fundamental saber procesarlos en **Python nativo** usando colecciones (`list` y `dict`), validando que las métricas numéricas sean homogéneas y filtrando irregularidades.

#### 📚 3. Fuentes Web Oficiales

- **Documentación Oficial de Python — Estructuras de Datos (`dict`, `list`):**
    
    [Python Docs: Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
    
- **Documentación Oficial de Python — Control de Flujo y Funciones:**
    
    [Python Docs: Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html)
    
- **Documentación Oficial de Python — Formateo con f-strings (PEP 498):**
    
    [Python Docs: Formatted String Literals](https://www.google.com/search?q=https://docs.python.org/3/reference/lexical_analysis.html%23f-strings)
    

#### 📄 4. CheatSheet y Manuales Recomendados

- **CheatSheet de Python Nativo:** [Python 3 Executive Summary & Syntax CheatSheet (Real Python)](https://realpython.com/python-cheat-sheet/)
    
- **Manual de Referencia:** Consulta la sección de _Mapping Types — `dict`_ y _Sequence Types — `list`_ en la referencia estándar de Python.
    

### 💻 Tu Reto (Escribe el código en tu cuaderno local):

1. **Creación del dataset sintético:** Crea una lista de diccionarios llamada `registros_desempleo` con 4 registros basados en Eurostat:
    
    - Registro 1: `{"geo": "ES", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": 11.5}`
        
    - Registro 2: `{"geo": "DE", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": 3.8}`
        
    - Registro 3: `{"geo": "FR", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": 7.2}`
        
    - Registro 4 (dato corrupto/inválido): `{"geo": "IT", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": None}`
        
2. **Desarrollo de la función con filtrado estricto:** Escribe una función llamada `calcular_desempleo_promedio(registros: list) -> str` que:
    
    - Recorra la lista `registros`.
        
    - Verifique mediante `isinstance()` o comprobación de tipo si `OBS_VALUE` es un número (`int` o `float`) válido.
        
    - Si encuentra un valor nulo (`None`) o no numérico, imprima un aviso por consola indicando qué país (`geo`) ha sido ignorado.
        
    - Calcule el promedio de los registros válidos.
        
    - Retorne una cadena formateada con `f-string` especificando el resultado final redondeado a **2 decimales**.
        

**Copia y pega tu código solucionado cuando lo tengas listo.** Revisaremos la lógica, el manejo de errores y pasaremos inmediatamente al Ejercicio 2.