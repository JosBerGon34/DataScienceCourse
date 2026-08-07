#!/usr/bin/env bash

# ==========================================================
# KnowledgeDome - Setup Scraping (Playwright)
# ----------------------------------------------------------
# Purpose:
#     Install scraping-specific dependencies on top of the
#     base workspace, and download Playwright's own Chromium
#     (decoupled from the system's chromium).
#
# Requires:
#     .venv-core already created via setup.sh
# ==========================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_ROOT"

echo
echo "=========================================="
echo "Setting up Scraping capabilities..."
echo "=========================================="
echo "Project root: $PROJECT_ROOT"
echo

# ----------------------------------------------------------
# Verify base workspace exists
# ----------------------------------------------------------

if [[ ! -d ".venv-core" ]]; then

    echo
    echo "ERROR: .venv-core not found."
    echo "Run setup.sh first to create the base workspace."
    echo

    exit 1

fi

# ----------------------------------------------------------
# Activate Workspace
# ----------------------------------------------------------

source .venv-core/bin/activate

# ----------------------------------------------------------
# Install scraping dependencies
# ----------------------------------------------------------

pip install -r requirements/ReqJupScrapping.txt

# ----------------------------------------------------------
# Download Playwright's own Chromium (not the system's)
# ----------------------------------------------------------

playwright install chromium

echo
echo "=========================================="
echo "Scraping capabilities ready!"
echo "=========================================="
