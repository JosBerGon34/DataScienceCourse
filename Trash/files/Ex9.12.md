```python
-------------------------------------------------------------------------------------------------
DataScienceCourse/
├── notebooks/
│   ├── 00_template.ipynb           # Template, for copying and having relative paths functional.
│   ├── 01_limpieza_grupo1.ipynb
│   └── 05_eda_analisis.ipynb
├── src/
│   ├── __init__.py
│   ├── paths.py                    # Pathing Setup script
│   └── descriptive_tools.py        # Script datascience ds3on1, vartype, statsgroup
└── main.py                         # Entry point for the scripts./
        "ROOT": ROOT_DIR,
        "DATA": DATA_DIR,
        "TABLES": TABLES_DIR,
        "PROCESSED": PROCESSED_DATA_DIR
-------------------------------------------------------------------------------------------------
```


```python
%load_ext autoreload
%autoreload 2

import sys
from pathlib import Path
import os

ROOT_DIR = Path.cwd().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src import setup_workspace, query_to_df, ds3on1

# 1. Inicializar workspace y rutas
paths = setup_workspace()


# 2. Consultar directamente a PostgreSQL (vía DuckDB ATTACH)
#df = query_to_df("SELECT * FROM db.EuInfo;")

# 3. Análisis univariable 3-en-1
#ds3on1(df, 'happy', Desc=True, Stat=True, Graph=True)

```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload
    ✅ Workspace anclado en: /home/josu/Documentos/DataScienceCourse
    📂 Ruta de tablas verificada: /home/josu/Documentos/DataScienceCourse/data/raw/Tables


-------------------------------------------------------------------------------------------------
2. Applied / Data Level (Controlled Ablation Study & Bayesian Baseline)
3. **Tier 2 — Macroeconomic Context Only ($X_{\text{macro}}$):** Only country-level macroeconomic metrics and structural clusters (GDP, inflation, unemployment, economic cluster dummies).
4. **Tier 3 — Hybrid Model ($X_{\text{micro}} + X_{\text{macro}}$):** Full feature matrix combining individual microdata and macroeconomic context.
-------------------------------------------------------------------------------------------------


```python

```
