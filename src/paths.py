"""OS-agnostic relative path resolution and workspace anchoring."""

import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

DOCS_DIR = ROOT_DIR / "docs"
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
TEMP_DIR = ROOT_DIR / "temp"              # Alias: TABLES
PRST_DIR = ROOT_DIR / "persisted"         # Alias: PROCESSED
SRC_DIR = ROOT_DIR / "src"                # Alias: SOURCE

PRST_DESC_DIR = PRST_DIR / "descriptive"
PRST_MOD_DIR = PRST_DIR / "models"
PRST_FW_DIR = PRST_DIR / "framework"

DSH_DIR = SRC_DIR / "apps_dash"           # Alias: DASH
FSK_DIR = SRC_DIR / "apps_flask"          # Alias: FLASK
API_DIR = SRC_DIR / "apps_fapi"           # Alias: FAPI


def setup_workspace(create_missing: bool = True) -> dict[str, Path]:
    """
    Anchor CWD to ROOT_DIR, expose src/ in sys.path, verify structural
    directories, and return standardized workspace path nodes.
    """
    if not ROOT_DIR.exists():
        raise FileNotFoundError(f"[ERROR] Project root not found at: {ROOT_DIR}")

    os.chdir(ROOT_DIR)
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))

    managed = [
        TEMP_DIR,
        PRST_DIR,
        PRST_DESC_DIR,
        PRST_MOD_DIR,
        PRST_FW_DIR,
        DSH_DIR,
        FSK_DIR,
        API_DIR,
    ]

    # 1. Audit which structural directories are missing prior to creation
    missing_dirs = [d for d in managed if not d.exists()]

    if missing_dirs:
        missing_rel = [str(d.relative_to(ROOT_DIR)) for d in missing_dirs]
        if create_missing:
            for d in missing_dirs:
                d.mkdir(parents=True, exist_ok=True)
            print(f"[INIT] Missing structural folders created: {missing_rel}")
        else:
            raise FileNotFoundError(f"[ERROR] Missing required structural folders: {missing_rel}")
    else:
        print("[OK] Structural folder check passed: all required directories exist.")

    # 2. Confirm active working directory anchored at ROOT_DIR
    print(f"[OK] Workspace anchored at ROOT: {Path.cwd()} (relative base: '.')")

    return {
        "ROOT": ROOT_DIR,
        "TABLES": TEMP_DIR,
        "PROCESSED": PRST_DIR,
        "PROCESSED_DESC": PRST_DESC_DIR,
        "PROCESSED_MODELS": PRST_MOD_DIR,
        "PROCESSED_FW": PRST_FW_DIR,
        "SOURCE": SRC_DIR,
        "DASH": DSH_DIR,
        "FLASK": FSK_DIR,
        "FAPI": API_DIR,
    }