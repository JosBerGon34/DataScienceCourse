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


```python
import numpy as np
import pandas as pd
from pathlib import Path
```


```python
BASE_DIR = Path.cwd().parent
print(f"Directorio de trabajo actual: {BASE_DIR}")
```

    Directorio de trabajo actual: /home/josu/Documentos/DataSciencePractice



```python
TABLES_DIR = BASE_DIR / "data" / "raw" / "Tables"
csv_path = TABLES_DIR / "DesempleoEU.csv"
```


```python
#1:
#Creo una plantilla de una fila con 4 valores para mis registros.
reg: dict[str, str] = {"geo":"",
        "TIME_PERIOD":"",
        "age":"",
        "sex":"",
        "OBS_VALUE":"",
}
reg1= reg.copy()
reg2= reg.copy()
reg3= reg.copy()
reg4= reg.copy()
#Creo una lista pandas con 4 diccionarios por posicion.
registros_desempleo_promedio = [reg1,reg2,reg3,reg4]
#Genero un dataframe sample de 100 filas para el ejercicio respecto al csv original de desempleueu eurostat
df100lines = pd.read_csv(csv_path).sample(100)
```


```python
#Comprobamos el formato
print(type(registros_desempleo_promedio))
```

    <class 'list'>



```python
#Compruebo que haya cargado el csv correctamente
print(df100lines.info())
```

    <class 'pandas.DataFrame'>
    Index: 100 entries, 7636 to 10409
    Data columns (total 11 columns):
     #   Column       Non-Null Count  Dtype  
    ---  ------       --------------  -----  
     0   DATAFLOW     100 non-null    str    
     1   LAST UPDATE  100 non-null    str    
     2   freq         100 non-null    str    
     3   age          100 non-null    str    
     4   unit         100 non-null    str    
     5   sex          100 non-null    str    
     6   geo          100 non-null    str    
     7   TIME_PERIOD  100 non-null    int64  
     8   OBS_VALUE    99 non-null     float64
     9   OBS_FLAG     12 non-null     str    
     10  CONF_STATUS  0 non-null      float64
    dtypes: float64(2), int64(1), str(8)
    memory usage: 9.4 KB
    None



```python
print(type(registros_desempleo_promedio))
print(type(registros_desempleo_promedio[0]))
print(registros_desempleo_promedio[0])
```

    <class 'list'>
    <class 'dict'>
    {'geo': '', 'TIME_PERIOD': '', 'age': '', 'sex': '', 'OBS_VALUE': ''}



```python
#Cargamos datos del dataframe  a cada posicion de los diccionarios en la lista
#Ubicamos y ejecutamos mediante el Indice, solamente de las columnas requeridas(5):

indices = np.random.choice(df100lines.index, 4, replace=False)

for i, idx in enumerate(indices):
    fila = df100lines.loc[idx]

    registros_desempleo_promedio[i]["geo"] = fila["geo"]
    registros_desempleo_promedio[i]["TIME_PERIOD"] = fila["TIME_PERIOD"]
    registros_desempleo_promedio[i]["age"] = fila["age"]
    registros_desempleo_promedio[i]["sex"] = fila["sex"]
    registros_desempleo_promedio[i]["OBS_VALUE"] = fila["OBS_VALUE"]
```


```python
print(registros_desempleo_promedio)
```

    [{'geo': 'ES', 'TIME_PERIOD': np.int64(2015), 'age': 'Y25-54', 'sex': 'F', 'OBS_VALUE': np.float64(22.4)}, {'geo': 'EA20', 'TIME_PERIOD': np.int64(2010), 'age': 'Y15-29', 'sex': 'T', 'OBS_VALUE': np.float64(10.0)}, {'geo': 'PL', 'TIME_PERIOD': np.int64(2013), 'age': 'Y15-24', 'sex': 'M', 'OBS_VALUE': np.float64(25.8)}, {'geo': 'ES', 'TIME_PERIOD': np.int64(2025), 'age': 'Y55-74', 'sex': 'T', 'OBS_VALUE': np.float64(4.2)}]



```python
#Observamos la naturaleza de los datos dentro del diccionario 1(Posicion 0 de la lista) para OBS_Value.
registros_desempleo_promedio[0]["OBS_VALUE"]
```




    np.float64(22.4)




```python
#Recorremos la lista de diccionarios, printeando en orden las variables y los valores de cada diccionario
# y luego saltamos al siguiente diccionario, hasta recorrer los 4:

for i, diccionario in enumerate(registros_desempleo_promedio):
    print(f"\nDiccionario {i+1}")

    for clave, valor in diccionario.items():
        print(f"{clave}: {valor}")
```

    
    Diccionario 1
    geo: ES
    TIME_PERIOD: 2015
    age: Y25-54
    sex: F
    OBS_VALUE: 22.4
    
    Diccionario 2
    geo: EA20
    TIME_PERIOD: 2010
    age: Y15-29
    sex: T
    OBS_VALUE: 10.0
    
    Diccionario 3
    geo: PL
    TIME_PERIOD: 2013
    age: Y15-24
    sex: M
    OBS_VALUE: 25.8
    
    Diccionario 4
    geo: ES
    TIME_PERIOD: 2025
    age: Y55-74
    sex: T
    OBS_VALUE: 4.2



```python
#Creamos una iteracion que recorra la cantidad de diccionarios que contiene la lista
#Esta lista tiene tiene tantos valores como lo largo que es la suma de sus items.
#Luego printeamos la media de todos los valores de OBS_Value iterados por i.

from typing import Any


sumatorio = 0

for i in range(len(registros_desempleo_promedio)):
    sumatorio += registros_desempleo_promedio[i]["OBS_VALUE"]

media = round(sumatorio / len(registros_desempleo_promedio), 2)

print(media)
```

    15.6

