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
import numpy as pd
import pandas as np

```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    Cell In[2], line 1
    ----> 1 import numpy as pd
          2 import pandas as np


    ModuleNotFoundError: No module named 'numpy'



```python
#1:
#Creo una plantilla de una fila con 4 valores para mis registros.
reg : {"geo":"",
        "TIME_PERIOD":"",
        "age":"",
        "sex":"",
        "OBS_VALUE":"",
}
reg1= reg.copy()
reg2= reg.copy()
reg3= reg.copy()
reg4= reg.copy()

pd.list=[(reg1),(reg2),(reg3),(reg4)] = registros_desempleo_promedio

df100lines = pd.readcsv("./DesempleoEU.csv")
```
