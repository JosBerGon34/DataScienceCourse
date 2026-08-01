# 1. Creación del dataset sintético
registros_desempleo = [
    {"geo": "ES", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": 11.5},
    {"geo": "DE", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": 3.8},
    {"geo": "FR", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": 7.2},
    {"geo": "IT", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": None}
]

# 2. Desarrollo de la función con filtrado estricto
def calcular_desempleo_promedio(registros: list) -> str:
    valores_validos = []
    
    for registro in registros:
        obs_val = registro.get("OBS_VALUE")
        
        # Comprobación de que obs_val es un int o float válido (excluyendo bool si fuera el caso)
        if isinstance(obs_val, (int, float)) and not isinstance(obs_val, bool):
            valores_validos.append(obs_val)
        else:
            pais = registro.get("geo", "Desconocido")
            print(f"⚠️  Aviso: El registro del país '{pais}' fue ignorado por contener un OBS_VALUE no válido ({obs_val}).")
    
    # Manejo de caso borde por si no existen valores válidos
    if not valores_validos:
        return "No hay registros válidos para calcular el promedio."
    
    promedio = sum(valores_validos) / len(valores_validos)
    
    return f"El promedio de desempleo para los países válidos es: {promedio:.2f}%"

# --- Prueba de la función ---
resultado = calcular_desempleo_promedio(registros_desempleo)
print(resultado)


# 1. En Python Nativo (como en el Ejercicio 1):
val = None
# val.dtype -> AttributeError: 'NoneType' object has no attribute 'dtype'
# type(val) -> <class 'NoneType'>  <-- Esto sí funciona en Python nativo.

# 2. En Pandas (si convertimos la lista a DataFrame):
import pandas as pd

df = pd.DataFrame(registros_desempleo)
df.info()  # <-- Aquí SÍ funcionan .info() y .dtypes perfectamente