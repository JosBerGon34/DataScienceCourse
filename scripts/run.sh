#!/usr/bin/env bash

# ==========================================================
# KnowledgeDome - Run Jupyter Workspace
# ==========================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_ROOT"

echo
echo "=========================================="
echo "Starting KnowledgeDome Workspace..."
echo "=========================================="

# ----------------------------------------------------------
# Activate Workspace
# ----------------------------------------------------------

source .venv-core/bin/activate

# ----------------------------------------------------------
# Check if Workspace is already running
# ----------------------------------------------------------

PID_FILE=".jupyter.pid"

if [[ -f "$PID_FILE" ]]; then

    OLD_PID=$(cat "$PID_FILE")

    if ps -p "$OLD_PID" >/dev/null 2>&1; then

        echo
        echo "Workspace already running."
        echo "PID: $OLD_PID"
        echo

        exit 0

    else

        rm -f "$PID_FILE"

    fi

fi

# ----------------------------------------------------------
# Start JupyterLab
# ----------------------------------------------------------

LOGFILE="/tmp/jupyterlab.log"

rm -f "$LOGFILE"

jupyter lab \
    --no-browser \
    --ServerApp.open_browser=False \
    >"$LOGFILE" 2>&1 &

JUPYTER_PID=$!

echo "$JUPYTER_PID" > "$PID_FILE"

# ----------------------------------------------------------
# Wait for Server
# ----------------------------------------------------------

echo "Waiting for JupyterLab..."

URL=""

for i in {1..20}; do

    sleep 1

    URL=$(grep -o 'http://127\.0\.0\.1:[0-9]\+/lab[^ ]*' "$LOGFILE" | head -n1)

    if [[ -n "$URL" ]]; then
        break
    fi

done

# ----------------------------------------------------------
# Verify URL
# ----------------------------------------------------------

if [[ -z "$URL" ]]; then

    echo
    echo "ERROR: JupyterLab did not start."
    echo

    cat "$LOGFILE"

    rm -f "$PID_FILE"

    exit 1

fi

echo
echo "JupyterLab running:"
echo "$URL"
echo

# ----------------------------------------------------------
# Launch Chromium (NORMAL WINDOW)
# ----------------------------------------------------------

chromium \
    "$URL" \
    >/dev/null 2>&1 &

echo
echo "Workspace ready!"
echo
