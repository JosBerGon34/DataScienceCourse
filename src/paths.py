# src/paths.py
"""
Standardized relative path resolution and workspace anchoring module.

Ensures deterministic, OS-agnostic portability across local environments,
JupyterLab instances, and containerized deployments without hardcoded paths.
"""

import os
import sys
from pathlib import Path

# 1. Dynamic detection of the repository root (src/paths.py -> parent -> root)
ROOT_DIR = Path(__file__).resolve().parent.parent

# 2. Primary directory nodes aligned with the project architecture
DOCS_DIR = ROOT_DIR / "docs"
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
TEMP_DIR = ROOT_DIR / "temp"              # Alias: TABLES (transitional tables, XML/HTML cache)
PRST_DIR = ROOT_DIR / "persisted"         # Alias: PROCESSED (final serialized joblib artifacts)
SRC_DIR = ROOT_DIR / "src"                # Alias: SOURCE (reusable core modules)
APPS_DIR = SRC_DIR / "apps"

# Subdirectories for persisted artifacts
PRST_DESCRIPTIVE_DIR = PRST_DIR / "descriptive"
PRST_MODELS_DIR = PRST_DIR / "models"
PRST_FRAMEWORK_DIR = PRST_DIR / "framework"

# Decoupled web framework sandboxes (run-ready for deployment)
DSH_DIR = APPS_DIR / "app_dash"           # Alias: DASH (ready for Plotly Cloud)
FSK_DIR = APPS_DIR / "app_flask"          # Alias: FLASK (ready for standalone deployment)


def setup_workspace(create_missing: bool = True) -> dict[str, Path]:
    """
    Anchor the runtime working directory to ROOT_DIR, inject 'src/' into sys.path
    for seamless module imports from notebooks, and return standardized path nodes.

    Args:
        create_missing: If True, automatically creates missing transitional and
            persisted directories. If False, raises FileNotFoundError when absent.

    Returns:
        Dictionary mapping standardized node keys to resolved pathlib.Path objects.

    Raises:
        FileNotFoundError: If ROOT_DIR cannot be resolved or required directories
            are missing when create_missing is False.
    """
    if not ROOT_DIR.exists():
        raise FileNotFoundError(f"[ERROR] Unable to locate project root at: {ROOT_DIR}")

    # Anchor current working directory to the repository root
    os.chdir(ROOT_DIR)

    # Ensure 'src' is discoverable in sys.path regardless of notebook subfolder depth
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))

    # Managed directory hierarchy required for transitional and persisted states
    managed_dirs = [
        TEMP_DIR,
        PRST_DIR,
        PRST_DESCRIPTIVE_DIR,
        PRST_MODELS_DIR,
        PRST_FRAMEWORK_DIR,
        APPS_DIR,
        DSH_DIR,
        FSK_DIR,
    ]

    if create_missing:
        for directory in managed_dirs:
            directory.mkdir(parents=True, exist_ok=True)
    else:
        missing = [str(d) for d in managed_dirs if not d.exists()]
        if missing:
            raise FileNotFoundError(
                f"[ERROR] Missing required workspace directories: {missing}"
            )

    print(f"[OK] Workspace anchored at: {ROOT_DIR}")

    return {
        "ROOT": ROOT_DIR,
        "TABLES": TEMP_DIR,
        "PROCESSED": PRST_DIR,
        "PROCESSED_DESC": PRST_DESCRIPTIVE_DIR,
        "PROCESSED_MODELS": PRST_MODELS_DIR,
        "PROCESSED_FW": PRST_FRAMEWORK_DIR,
        "SOURCE": SRC_DIR,
        "APPS": APPS_DIR,
        "DASH": DSH_DIR,
        "FLASK": FSK_DIR,
    }    