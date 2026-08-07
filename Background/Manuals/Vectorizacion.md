🧠 Fundamentos Teóricos de la Vectorización
La vectorización es la técnica de reemplazar bucles explícitos en Python (que son lentos debido a la sobrecarga del intérprete y la verificación dinámica de tipos) por operaciones de arreglos optimizadas ejecutadas en código de bajo nivel (C/Fortran). 

Mecanismo: Bibliotecas como NumPy almacenan datos en bloques de memoria contiguos y homogéneos. Esto permite que la CPU aplique instrucciones SIMD (Single Instruction, Multiple Data), procesando múltiples elementos simultáneamente.
Rendimiento: Mientras un bucle for en Python puede tardar milisegundos en iterar millones de elementos, una operación vectorizada equivalente lo hace en microsegundos, ofreciendo aceleraciones de 10x a 100x.
Aplicación: Es ideal para filtrado, sumas, multiplicaciones y operaciones matemáticas complejas sobre grandes volúmenes de datos numéricos. 

⚡ Refactorización del Script (Enfoque Vectorizado)
Este script transforma tu lógica original utilizando NumPy para eliminar iteraciones manuales y optimizar la prueba de primalidad mediante operaciones de arreglos.

import numpy as np

def es_primo_vectorizado(n: int) -> bool:
    """
    Verifica primalidad optimizada O(sqrt(n)).
    Nota: Para verificar primalidad de MÚLTIPLES números a la vez, 
    se usaría una máscara booleana sobre un array (ver explicación abajo).
    Aquí aplicamos la lógica matemática optimizada para un escalar resultado de la suma.
    """
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    # Solo evaluamos impares hasta la raíz cuadrada
    limite = int(np.sqrt(n)) + 1
    return not np.any(n % np.arange(3, limite, 2) == 0)

def procesar_numeros(numeros: list[int]) -> tuple[int, bool]:
    """
    Pipeline vectorizado:
    1. Conversión a array NumPy.
    2. Filtrado booleano (masking).
    3. Suma vectorizada.
    4. Verificación de primalidad.
    """
    # 1. Vectorización de datos
    arr = np.array(numeros)
    
    # 2. Filtrado vectorizado (elimina el bucle 'for' y el 'if')
    # Crea una máscara booleana: [False, False, True, ...]
    mascara_pares = arr % 2 == 0
    
    # 3. Suma vectorizada sobre los elementos filtrados
    suma_total = np.sum(arr[mascara_pares])
    
    # 4. Chequeo de primalidad
    es_primo_resultado = es_primo_vectorizado(suma_total)
    
    return suma_total, es_primo_resultado

# --- Ejecución ---
numeros = [12, 15, 7, 22, 19, 30, 11, 4, 8, 17]
suma, primo = procesar_numeros(numeros)

print(f"Resultado: {suma}, ¿Primo? {'Sí' if primo else 'No'}")  


🛠️ Explicación Teórico-Práctica del Código
1. Eliminación de Iteraciones (Filtrado y Suma)
En el código original, usabas dos bucles for secuenciales. En la versión vectorizada:

Conversión: np.array(numeros) mueve los datos a memoria contigua.
Máscara Booleana: La expresión arr % 2 == 0 no itera elemento por elemento en Python. NumPy aplica la operación módulo a todo el bloque de memoria de una vez, devolviendo un array de booleanos ([True, False, ...]).
Indexado por Máscara: arr[mascara_pares] extrae solo los valores donde la máscara es True en una operación de memoria altamente optimizada.
Suma: np.sum() ejecuta la acumulación en C, evitando la sobrecarga de crear variables temporales en cada iteración de Python. 
2. Optimización Matemática (Primalidad)
Aunque la suma resultante es un solo número (escalar), aplicamos la optimización algorítmica solicitada:

Complejidad: Se reduce de $O(N)$ a $O(\sqrt{N})$.
Implementación: En lugar de range(2, numero), usamos np.arange(3, limite, 2). Esto genera un vector de divisores impares hasta la raíz cuadrada.
Operación Vectorial: n % vector == 0 calcula todos los restos simultáneamente. np.any() verifica si hubo algún cero (divisor exacto) de forma inmediata.
3. Diseño Modular
Type Hinting: Se definen tipos (list[int], tuple[int, bool]) para claridad y soporte de IDEs.
Docstrings: Cada función documenta su propósito y complejidad, facilitando el mantenimiento. 


📊 Comparativa de Rendimiento (Cheatsheet)
Operación	Enfoque Original (Python Puro)	Enfoque Vectorizado (NumPy)	Ganancia Estimada
Filtrado	Bucle for + if + append	Máscara booleana arr[cond]	20x - 50x más rápido
Suma	Acumulador manual en bucle	np.sum() (C-backend)	10x - 30x más rápido
Primalidad	Bucle hasta $N$	Bucle hasta $\sqrt{N}$ + Vectorización	Algorítmicamente superior
Legibilidad	15+ líneas de lógica explícita	4 líneas de expresión declarativa	Código más limpio

Nota: Para listas muy pequeñas (como tu ejemplo de 10 números), la diferencia de tiempo es imperceptible (microsegundos). La vectorización brilla y es necesaria cuando trabajas con miles o millones de elementos, donde el enfoque original podría congelar tu aplicación. 

Fuentes:

[text](https://medium.com/swlh/high-performance-boolean-indexing-in-numpy-and-pandas-7fb5d84e28ed)
[text](https://reintech.io/blog/optimizing-boolean-masked-array-operations-numpy)
[text](https://apxml.com/courses/advanced-python-programming-ml/chapter-2-python-performance-optimization-ml/optimizing-numpy-operations)