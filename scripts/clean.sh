#!/usr/bin/env bash

# ==========================================================
# KnowledgeDome - Remove Jupyter Workspace
# ==========================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_ROOT"

echo
echo "=========================================="
echo "Removing KnowledgeDome Workspace..."
echo "=========================================="
echo "Project root: $PROJECT_ROOT"
echo

if [[ -d ".venv-core" ]]; then
    source .venv-core/bin/activate 2>/dev/null || true
fi

jupyter kernelspec uninstall ds-core -f 2>/dev/null || echo "⚠️  Kernel 'ds-core' was not installed, skipping."

rm -rf .venv-core

echo
echo "Workspace removed."
