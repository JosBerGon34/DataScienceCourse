```python
#DataScienceCourse/
#├── Background/               # Cheatsheets and reference manuals
#├── docs/                     # Exported Markdown notebooks for GitHub Pages
#├── notebooks/
#│   ├── 00_ProjectTemplate.ipynb
#│   └── SX.Y_DESC.ipynb       # Sequential step notebooks
#├── persisted/                # Final serialized joblib artifacts
#│   ├── descriptive/
#│   ├── models/
#│   └── framework/
#├── src/                      # Flat Python package (auto-discovered by setuptools)
#│   ├── __init__.py
#│   ├── paths.py              # OS-agnostic relative path resolution
#│   ├── descriptive_tools.py  # Statistical profiling & ESS metadata helpers
#│   ├── s0_screening.py       # Step 0: Exploratory screening & ESS cataloging
#│   ├── s1_ingestion.py       # Step 1: APIs, scraping & SQL persistence
#│   ├── s2_cleaning.py        # Step 2: Survey sanitization, macro merge & audit flags
#│   ├── s3_eda.py             # Step 3: Exploratory stats persistence
#│   ├── s4_features.py        # Step 4: Deterministic feature engineering
#│   ├── s5_modeling.py        # Step 5: GroupKFold modeling & benchmarking
#│   ├── wrapper.py            # Step 6.1: Global orchestrator & ablation runner
#│   ├── apps_dash/            # Standalone Plotly Dash sandbox
#│   ├── apps_fapi/            # Standalone FastAPI sandbox
#│   └── apps_flask/           # Standalone Flask sandbox
#├── temp/                     # Transitional checkpoints, raw HTML/XML (gitignored)
#├── tests/                    # Pytest data-contract & pipeline tests
#├── pyproject.toml            # Single source of truth for dependencies & CLI
#├── ProjectStatement.md       # Technical specification
#└── Index_Readme.md           # Sequential workflow guide
```


```python
import sys
from pathlib import Path

root = Path.cwd().resolve().parent if Path.cwd().name == "notebooks" else Path.cwd().resolve()
if str(root / "src") not in sys.path:
    sys.path.insert(0, str(root / "src"))

from paths import setup_workspace

PATHS = setup_workspace()
```
