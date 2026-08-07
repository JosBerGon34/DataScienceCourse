#!/usr/bin/env bash

set -e

echo
echo "=========================================="
echo "Creating Jupyter Workspace"
echo "=========================================="

python3.13 -m venv .venv-core

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

