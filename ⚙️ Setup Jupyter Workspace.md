
***Data Science Course**

---
***Requirements:
Linux
Bash terminal
Github account and repositories
Clean and not used Chromium explorer.


# Overview

This project uses a **self-contained Jupyter Workspace** architecture.

The operating system only provides the Python interpreter.

Everything else—including JupyterLab, kernels and scientific libraries—is installed inside the project's virtual environment.

This guarantees:

- Complete reproducibility
- Zero dependency conflicts
- Easy maintenance
- Project portability
- One isolated environment per project

---

# Workspace Architecture

```
Git Repository
        │
        ▼
Virtual Environment (.venv-core)
        │
        ▼
JupyterLab
        │
        ▼
Kernel (ds-core)
        │
        ▼
Python Interpreter
        │
        ▼
Scientific Libraries
        │
        ▼
Notebook Execution
```

---

# Project Structure

```
DataScienceCourse/

├── docs/
│
├── notebooks/
│
├── src/
│
├── data/
│
├── requirements/
│   ├── ReqJupCore.txt
│   ├── ReqJupScraping.txt
│   ├── ReqJupML.txt
│   ├── ReqJupDeepLearning.txt
│   └── ReqJupDev.txt
│
├── scripts/
│   ├── setup.sh
│   ├── update.sh
│   └── clean.sh
│	└── stop.sh
│	└──setup scraping.sh
└── .venv-core/
```

---

# System Requirements

Only two applications are required on the operating system:

- Python 3.13
- Git

Everything else is installed inside the Workspace.

---

# Creating the Workspace

From the repository root:

```bash
python3.13 -m venv .venv-core
```

---

# Activating the Workspace

Linux

```bash
source .venv-core/bin/activate
```

Verify:

```bash
which python
```

Expected:

```
.../DataScienceCourse/.venv-core/bin/python
```

---

# Upgrading pip

```bash
python -m pip install --upgrade pip
```

---

# Installing the Workspace

Install the complete Core profile:

```bash
pip install -r requirements/ReqJupCore.txt
```

This installs:

- JupyterLab
- Notebook
- ipykernel
- pandas
- numpy
- duckdb
- matplotlib
- plotly

and every dependency required for the course.

---

# Registering the Kernel

Register the virtual environment as a Jupyter Kernel:

```bash
python -m ipykernel install \
    --user \
    --name ds-core \
    --display-name "Python (DS Core)"
```

Verify:

```bash
jupyter kernelspec list
```

Expected output:

```
Available kernels

ds-core
```

---

# Launching JupyterLab

Always launch JupyterLab from the activated Workspace.

```bash
jupyter lab
```

Never use the system Jupyter installation.

---

# Verifying the Installation

Execute:

```bash
which python

which jupyter

python --version

jupyter --version

jupyter kernelspec list
```

Both Python and Jupyter should belong to the virtual environment.

---

# Workspace Profiles

The project is organized into modular Workspace profiles.

## ReqJupCore.txt

Contains the base Data Science environment.

Example:

```text
jupyterlab
notebook
ipykernel

numpy
pandas
duckdb

matplotlib
plotly
```

---

## ReqJupScraping.txt

Extends the Core profile.

```text
-r ReqJupCore.txt

beautifulsoup4
lxml
playwright
aiohttp
```

---

## ReqJupML.txt

Machine Learning environment.

```text
-r ReqJupCore.txt

scikit-learn
xgboost
lightgbm
```

---

## ReqJupDeepLearning.txt

Deep Learning profile.

```text
-r ReqJupML.txt

torch
torchvision
tensorflow
```

---

## ReqJupDev.txt

Development tools.

```text
-r ReqJupCore.txt

black
ruff
pytest
mypy
```

---

# Automatic Installation

Instead of manually executing every command, use the setup script.

Create:

```
scripts/setup.sh
```

```bash
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
```

Make it executable, every script, changing the name :

```bash
chmod +x scripts/setup.sh
```

***Instructions:

```bash
cd ~/Desktop

PROJECT_ROOT=/home/user/Documents/DataScienceCourse/ \
  /home/user/Documentos/DataScienceCourse/scripts/setup.sh
```
With this command line we adjust the project root with the absolute path, and also we execute the script with the same kind of path. We can execute from every folder we open
the terminal.

---

# Updating the Workspace

```
scripts/update.sh
```

```bash
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

```

---
Run:

```bash
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
```
# Removing the Workspace

```
scripts/clean.sh
```

```bash
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

```

---
# Stopping the WorkSpace safely:

```bash
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

```

# Install Scrapping tools, Playwright dependancies:

***This API is very strong but is a bit special, the right way to use it, is let it download his
own chromium explorer so we can use global Chromium as JupyterLab IDE, and the invisible Chromium to download HTMLS and parse them via BeauyfoulSoup and pandas.

```bash
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

```

# Recommended Workflow

```
Clone Repository

↓

Create Workspace

↓

Activate Workspace

↓

A) Run the scripts: 1) setup.sh, 2)Update.sh, 3) Run.sh 
B) Run Run.sh only if you did the previous 2 steps already.
C) Use clean.sh if your .venv is corrupt or failing.
D) Stop the Jupyter IDE executing stop.sh
E) Use setup_scrapping.sh if you need to scrap tables or texts.
↓

Launch JupyterLab

↓

Open Notebook

↓

Select ds-core Kernel

↓

Start Coding
```

---
***HOW TO EXECUTE SCRIPTS:
Navigate to the root of your cloned repository, open bash terminal  and type
the location of your script folder. ex: 

```bash
/home/user/documents/DataScienceCourse/Scripts/run.sh
```

# Design Philosophy

The repository owns its Python environment.

The operating system only provides Python.

Every scientific dependency—including JupyterLab—is managed inside the Workspace.

This approach guarantees that every student, collaborator or future version of the project executes exactly the same environment.

One Project

↓

One Workspace

↓

One JupyterLab

↓

One Kernel

↓

One Reproducible Development Environment