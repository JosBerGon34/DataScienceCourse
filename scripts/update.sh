#!/usr/bin/env bash

source .venv-core/bin/activate

python -m pip install --upgrade pip

pip install -r requirements/ReqJupCore.txt

echo
echo "Workspace updated."
