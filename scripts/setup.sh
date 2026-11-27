#!/usr/bin/env bash

# ==========================================================
# KnowledgeDome - Setup Jupyter Workspace
# ==========================================================

set -e

# ----------------------------------------------------------
# Resolve PROJECT_ROOT
# ----------------------------------------------------------
# Priority order:
#   1. First positional argument   -> ./setup.sh /custom/path
#   2. PROJECT_ROOT env variable   -> PROJECT_ROOT=/custom/path ./setup.sh
#   3. Auto-detect (default)       -> parent folder of this script
# ----------------------------------------------------------

if [[ -n "$1" ]]; then
    PROJECT_ROOT="$(cd "$1" && pwd)"
elif [[ -n "$PROJECT_ROOT" ]]; then
    PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"
else
    PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi

cd "$PROJECT_ROOT"

echo
echo "=========================================="
echo "Creating Jupyter Workspace"
echo "=========================================="
echo "Project root: $PROJECT_ROOT"
echo

# ----------------------------------------------------------
# Resolve Python interpreter (3.13 preferred, fallback to python3)
# ----------------------------------------------------------

if command -v python3.13 >/dev/null 2>&1; then
    PYTHON_BIN="python3.13"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
    echo "⚠️  python3.13 not found, falling back to: $(python3 --version)"
else
    echo "❌ No suitable Python interpreter found on this machine."
    exit 1
fi

"$PYTHON_BIN" -m venv .venv-core

source .venv-core/bin/activate

python -m pip install --upgrade pip

pip install -r requirements/ReqJupCore.txt

python -m ipykernel install \
    --user \
    --name ds-core \
    --display-name "Python (DS Core)"

echo
echo "=========================================="
echo "Workspace successfully created!"
echo "=========================================="

echo
echo "Activate it using:"
echo
echo "source .venv-core/bin/activate"
