📜 Código Original (Sin optimizar)
Imagina que recibes el siguiente script escrito por un compañero para procesar una lista de números enteros, filtrar ciertos datos, sumarlos y verificar si el resultado total es un número primo:

''
# Código ineficiente a refactorizar
numeros = [12, 15, 7, 22, 19, 30, 11, 4, 8, 17]

# 1. Filtrar pares
pares = []
for n in numeros:
    if n % 2 == 0:
        pares.append(n)

# 2. Sumar los números filtrados manualmente
suma_total = 0
for p in pares:
    suma_total = suma_total + p

# 3. Función de primalidad ineficiente
def es_primo(numero):
    if numero < 2:
        return False
    # Revisa TODOS los números hasta 'numero'
    for i in range(2, numero):
        if numero % i == 0:
            return False
    return True

print(f"Resultado: {suma_total}, ¿Primo? {'Sí' if es_primo(suma_total) else 'No'}")
''

🛠️ Puntos clave a optimizar:
Evitar la duplicación de recorridos: 
En lugar de hacer múltiples bucles for (uno para filtrar y otro para sumar), 
aprovecha las funciones integradas de Python.Uso de funciones nativas integradas: 
Sustituye el bucle de acumulación manual de suma por la función optimizada sum() y compresión de listas (o expresiones generadoras).Optimización matemática del test de primalidad (is_prime): * Comprobar divisores únicamente hasta la raíz cuadrada del número ($\sqrt{N}$), descartando múltiplos de 2 inmediatamente.Modularidad: Organizar la lógica en funciones específicas bien documentadas.

'import math

def es_primo_optimizado(n: int) -> bool:
    """
    Verifica si un número es primo con complejidad O(sqrt(N)).
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Solo comprobamos impares hasta sqrt(n)
    limite = int(math.isqrt(n))
    for i in range(3, limite + 1, 2):
        if n % i == 0:
            return False
    return True

def procesar_y_evaluar(numeros: list[int]) -> str:
    """
    Filtra números pares, los suma eficientemente y evalúa si el total es primo.
    """
    # Expresión generadora / filtrado directo en sum() en un solo paso O(N)
    suma_total = sum(n for n in numeros if n % 2 == 0)
    
    primo_flag = es_primo_optimizado(suma_total)
    
    return f"Resultado: {suma_total}, ¿Primo? {'Sí' if primo_flag else 'No'}"

# --- Prueba del script ---
numeros = [12, 15, 7, 22, 19, 30, 11, 4, 8, 17]
print(procesar_y_evaluar(numeros))'

📊 Comparativa de Complejidad y RendimientoAspectoVersión Ineficiente
Versión OptimizadaRecorrido de Datos2 pasadas a la lista ($O(2N)$)1 sola pasada con expresión generadora ($O(N)$)Suma
Bucle for explicito nativoFunción C-optimized nativa sum()PrimalidadEvalúa $N-2$ iteraciones ($O(N)$)Evalúa $\sqrt{N}/2$ iteraciones ($O(\sqrt{N})$)