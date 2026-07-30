📌 Contexto Aplicado (Proyecto ESS / Eurostat)
En datos procedentes de APIs como Eurostat o encuestas sociológicas, a menudo recibes los datos organizados en estructuras anidadas (listas de diccionarios por región/país). 
Antes de cargar los datos en un DataFrame de Pandas, necesitas filtrar y transformar listas de respuestas individuales para calcular métricas descriptivas básicas de un país determinado sin incurrir en sesgos por valores atípicos de codificación.
📐 1. Instrucciones a nivel Sintáctico-AlgebraicoDada una colección de observaciones $S = \{x_1, x_2, \dots, x_N\}$ proveniente de una encuesta, donde cada $x_i \in \mathbb{R} \cup \{None, 77, 88, 99\}$:
Filtrado Formal: Construye un subconjunto $S_{\text{válidos}} = \{x_i \in S \mid x_i \in [0, 10]\}$, excluyendo todo $x_i > 10$ o $x_i$ no numérico (respetando los códigos de no-respuesta del sistema ESS).
Métricas a calcular:Media muestral ($\bar{x}$):$$\bar{x} = \frac{1}{\vert{}S_{\text{válidos}}\vert{}} \sum_{x \in S_{\text{válidos}}} x$$Varianza muestral ($s^2$):$$s^2 = \frac{1}{\vert{}S_{\text{válidos}}\vert{} - 1} \sum_{x \in S_{\text{válidos}}} (x - \bar{x})^2$$Desviación típica ($s$): $s = \sqrt{s^2}$💻 2. Instrucciones Aplicadas en Python (Nativo)Crea una función llamada analizar_escala_politica(encuestas: list[dict], clave_variable: str) -> dict que:Reciba una lista de diccionarios que representan respuestas individuales a la escala ideológica lrscale (0 = Izquierda extrema, 10 = Derecha extrema) en un país determinado (ej. "ES").Filtre las respuestas dejando solo las numéricas en el rango [0, 10]. (Recuerda descartar valores como 77 "Refusal", 88 "Don't know" o 99 "No answer", así como None).Calcule mediante bucles e iteraciones nativas de Python (sin usar math, numpy ni pandas por ahora):
Total de respuestas procesadas vs. válidas.La media muestral.La desviación típica muestral.Retorne un diccionario con el resumen numérico.

Dataset de prueba para tu Notebook:
respuestas_ess_es = [
    {"id": 1, "cntry": "ES", "lrscale": 5},
    {"id": 2, "cntry": "ES", "lrscale": 2},
    {"id": 3, "cntry": "ES", "lrscale": 8},
    {"id": 4, "cntry": "ES", "lrscale": 88},  # No sabe
    {"id": 5, "cntry": "ES", "lrscale": 0},   # Extrema izquierda (¡VÁLIDO!)
    {"id": 6, "cntry": "ES", "lrscale": 10},  # Extrema derecha (¡VÁLIDO!)
    {"id": 7, "cntry": "ES", "lrscale": None},# Ausente
    {"id": 8, "cntry": "ES", "lrscale": 77},  # Rechaza responder
    {"id": 9, "cntry": "ES", "lrscale": 4},
    {"id": 10, "cntry": "ES", "lrscale": 6}
]

📚 Recurso Web y CheatSheet Sugerido
Documentación Oficial: Revisa el tratamiento de estructuras de control y funciones nativas en la Documentación oficial de Python - Control Flow.

Guía de referencia rápida: Revisa cualquier CheatSheet de Python Data Structures (listas, diccionarios y list comprehensions) para optimizar los bucles.

Pruébalo en tu cuaderno local y cuando tengas tu solución lista, compártela o dame luz verde para revisarla.