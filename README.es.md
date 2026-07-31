# 🚀 DataScienceCourse: Course Remodel & Applied Refactoring

> **Repositorio de Origen:** [https://github.com/JosBerGon34/4GA.DataScience](https://github.com/JosBerGon34/4GA.DataScience)

Este repositorio contiene una **reestructuración profunda (Remodel) y síntesis (Summary)** del programa de Ciencia de Datos de **4Geeks Academy**. El objetivo principal es redefinir el recorrido de aprendizaje, reemplazando los ejercicios abstractos tradicionales por un enfoque **aplicado, riguroso y progresivo** sobre *datasets* reales que alimentan de forma directa el **Proyecto Final**.

---

## 🎯 Objetivos del Remodelado

1. **Aprendizaje Basado en Datasets Reales:**
   * **Eurostat:** Datos macroeconómicos y numéricos (PIB, desempleo, deuda pública, inflación).
   * **European Social Survey (ESS):** Microdatos de encuestas sociológicas (variables ordinales de actitudes, confianza política y bienestar).
   * **Web Scraping & Categóricos:** Datos de preferencias culturales, deportivas y socio-relacionales por país.

2. **Alineación con el Proyecto Final:**
   * Cada módulo de código nativo, análisis exploratorio (EDA), limpieza e ingeniería de características (*feature engineering*) construye directamente las herramientas necesarias para la tubería del proyecto de predicción de la postura ideológica.

3. **Rigor Metodológico y Corrección Técnica:**
   * Corrección de vicios de programación y errores de diseño experimental (p. ej., tratamiento de *missing data* sin eliminar respuestas válidas en los extremos `0` y `10`, *splits* agrupados por país para evitar *data leakage*, y modelos ordinales bien especificados).

---

## 🗺️ Estructura del Curso y Plan Docente

El contenido está dividido modularmente respetando la evolución progresiva desde los fundamentos hasta el despliegue en producción:

| Módulo | Descripción / Enfoque Aplicado |
| :--- | :--- |
| **🟢 MÓDULO 1:** | **Prework Review & Python Nativo:** Manipulación de estructuras complejas (listas, diccionarios anidados) e iteraciones eficientes sin librerías externas. |
| **🟢 MÓDULO 2:** | **Álgebra Lineal & Cálculo para ML:** Operaciones matriciales, vectores y derivadas orientadas a algoritmos de optimización. |
| **🟢 MÓDULO 3:** | **Git, GitHub & Gestión de Proyectos:** Flujos de trabajo colaborativos, control de versiones y estructuración de repositorios. |
| **🟢 MÓDULO 4:** | **Probabilidad & Estadística Descriptiva:** Cálculo muestral, distribuciones y análisis de variables socioeconómicas. |
| **🟢 MÓDULO 5:** | **Numpy & Pandas:** Carga, combinación y tratamiento de datasets masivos de Eurostat y el ESS. |
| **🟢 MÓDULO 6:** | **Limpieza & Imputación:** Estrategias avanzadas de nulos (diferenciación de códigos de no-respuesta `77, 88, 99` vs respuestas extremas válidas). |
| **🟢 MÓDULO 7:** | **Análisis Exploratorio de Datos (EDA):** Detección de patrones, análisis de correlación y visualización avanzada (Matplotlib/Seaborn). |
| **🟢 MÓDULO 8:** | **Feature Engineering & Balanceo:** Transformaciones de variables, clustering estructural (KMeans) y SMOTE bien calibrado. |
| **🟢 MÓDULO 9:** | **Modelado Predictivo & Validación:** Modelos de regresión/clasificación, tuning de hiperparámetros y validación cruzada agrupada por país (`GroupKFold`). |
| **🟢 MÓDULO 10:** | **Despliegue & Aplicación Web:** Integración de modelos predictivos mediante backend Flask y Frontend standalone. |

---

## 🛠️ Tecnologías y Herramientas

* **Lenguaje:** Python 3.10+
* **Procesamiento de Datos:** NumPy, Pandas, Scipy
* **Visualización:** Matplotlib, Seaborn
* **Machine Learning & Estadística:** Scikit-Learn, Statsmodels, XGBoost, Imbalanced-Learn
* **Despliegue & API:** Flask, HTML/JS Native Client
* **Entorno Formativo:** Jupyter Notebooks, VS Code, NotebookLM

---

## 📍 Repositorios Relacionados

* 📂 **Repositorio Original (4GA.DataScience):** [JosBerGon34/4GA.DataScience](https://github.com/JosBerGon34/4GA.DataScience)
* 📂 **Repositorio Remodelado (DataScienceCourse):** Repositorio actual.

---
*Desarrollado y mantenido por [JosBerGon34](https://github.com/JosBerGon34).*
