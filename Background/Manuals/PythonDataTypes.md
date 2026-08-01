🔍 Comandos para Inspeccionar Tipos de Datos
Para identificar correctamente la estructura y el tipo de dato interno, utiliza estos comandos según el contenedor:

1. Estructuras Nativas de Python (Listas, Diccionarios, Tuplas)
Estas estructuras son dinámicas y heterogéneas (pueden mezclar tipos). Python no tiene un atributo .dtype nativo para ellas. 

Comando Principal: type(variable) → Devuelve la clase del contenedor (<class 'list'>, etc.).
Inspección de Elementos: Debes revisar el primer elemento o usar set para ver la variedad interna.

datos = [10, 20.5, "texto"]
dicc = {"a": 1, "b": 2}
tupla = (1, 2, 3)

# Identificar contenedor
print(type(datos))   # <class 'list'>
print(type(dicc))    # <class 'dict'>
print(type(tupla))   # <class 'tuple'>

# Identificar tipos internos (útil para depuración)
print({type(x) for x in datos}) # {<class 'int'>, <class 'float'>, <class 'str'>}   


2. Arrays de NumPy
Estas estructuras son estáticas y homogéneas (un solo tipo para todos). 

Comando Principal: array.dtype → Devuelve el tipo de dato exacto en memoria (ej. int32, float64). 
Comando Secundario: array.shape → Devuelve las dimensiones (ej. (10,) o (3, 4)).

import numpy as np
arr = np.array([1, 2, 3])

print(type(arr))   # <class 'numpy.ndarray'>
print(arr.dtype)   # int64 (o int32 según sistema)
print(arr.shape)   # (3,)   

🧠 Aclaración: ¿Qué necesitan las funciones vectorizadas?
Corrección importante: Para que una operación sea vectorizada en NumPy, NO es estrictamente necesario pasar una "tupla de enteros". 

Entrada Ideal: Lo óptimo es pasar un np.array (o un objeto que se pueda convertir rápidamente en uno, como una lista de números homogéneos). 
El rol de la Tupla:
Si pasas una tupla (1, 2, 3) a una función de NumPy (ej. np.sum((1, 2, 3))), NumPy la convierte internamente a un array temporal antes de operar. Esto tiene un pequeño costo extra.
Las tuplas se usan frecuentemente para definir índices multidimensionales o formas (shape), no necesariamente como los datos en sí mismos para el cálculo masivo.
Tipos de Datos Válidos:
Las operaciones vectorizadas funcionan principalmente con tipos numéricos: int (enteros), float (flotantes), bool (booleanos) y complex (complejos).
Si intentas vectorizar operaciones matemáticas sobre una lista que contiene strings o None, obtendrás errores o comportamientos lentos (object dtype). 

📋 Tabla Resumen de Tipos y Comandos
Estructura	Comando Tipo Contenedor	Comando Tipo Interno	¿Homogéneo?	¿Vectorizable Nativo?
Lista (list)	type(x)	type(x[0])	❌ No	❌ (Requiere conversión)
Diccionario (dict)	type(x)	type(list(x.values())[0])	❌ No	❌ (Usar .values())
Tupla (tuple)	type(x)	type(x[0])	❌ No	⚠️ (Conversión automática)
Array NumPy	type(x)	x.dtype	✅ Sí	✅ Sí (Nativo)

Ejemplo Práctico de Conversión para Vectorización
Si tienes datos en una lista o tupla y quieres asegurar la máxima velocidad:

datos_origen = [1, 2, 3, 4]  # Puede ser lista o tupla

# Forma correcta de preparar para vectorización
arr_optimizado = np.array(datos_origen, dtype=np.float64) 

# Verificación
print(f"Tipo interno: {arr_optimizado.dtype}") # float64
print(f"¿Listo para vectorizar? {isinstance(arr_optimizado, np.ndarray)}") # True 

Conclusión: Usa dtype solo en arrays de NumPy. Para listas/tuplas, usa type(). Para vectorizar, convierte siempre tus datos a np.array explícitamente antes de operar, asegurando que contengan solo números (int, float) o booleanos. 

Ejemplo Visualizacion de Datos y tipos :
Numberlist = [12, 15, 7, 22, 19, 30, 11, 4, 8, 17]

# Opción A: Imprimir lista completa, tipo de lista y tipo del primer elemento en una sola línea
print(f"Lista: {Numberlist} | Tipo Contenedor: {type(Numberlist)} | Tipo 1er Elemento: {type(Numberlist[0])}")

# Salto de línea explícito para separar bloques
print("\n--- Detalle por posición ---")

# Opción B: Iterar para ver el tipo de CADA posición (Recomendado)
for i, valor in enumerate(Numberlist):
    print(f"Posición {i}: Valor = {valor}, Tipo = {type(valor)}")

# Opción C: Obtener una lista rápida solo con los tipos (Para depuración rápida)
tipos = [type(x) for x in Numberlist]
print(f"\nResumen de tipos: {tipos}")   
