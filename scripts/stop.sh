#!/usr/bin/env bash

# ==========================================================
# KnowledgeDome - Stop Jupyter Workspace
# ==========================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_ROOT"

echo
echo "=========================================="
echo "Stopping KnowledgeDome Workspace..."
echo "=========================================="

# ----------------------------------------------------------
# Activate Workspace
# ----------------------------------------------------------

source .venv-core/bin/activate

PID_FILE=".jupyter.pid"

# ----------------------------------------------------------
# Check PID
# ----------------------------------------------------------

if [[ ! -f "$PID_FILE" ]]; then

    echo
    echo "No running Workspace found."
    echo

    exit 0

fi

PID=$(cat "$PID_FILE")

# ----------------------------------------------------------
# Stop Process
# ----------------------------------------------------------

if ps -p "$PID" >/dev/null 2>&1; then

    echo
    echo "Stopping JupyterLab..."
    echo "PID: $PID"

    kill "$PID"

    sleep 2

else

    echo
    echo "Stored PID is no longer running."

fi

rm -f "$PID_FILE"

echo
echo "Workspace stopped successfully."
echo
