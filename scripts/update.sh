#!/usr/bin/env bash

# ==========================================================
# KnowledgeDome - Update Jupyter Workspace
# ==========================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_ROOT"

if [[ ! -d ".venv-core" ]]; then

    echo
    echo "ERROR: .venv-core not found."
    echo "Run setup.sh first to create the base workspace."
    echo

    exit 1

fi

source .venv-core/bin/activate

python -m pip install --upgrade pip

pip install -r requirements/ReqJupCore.txt

echo
echo "Workspace updated."
