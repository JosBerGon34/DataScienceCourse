
***Data Science Course**

---

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
│
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
```
***Important: The script will be executed in the root we are in the terminal, even if the script is located in diferent folder.

Make it executable:

```bash
chmod +x scripts/setup.sh
```

---

# Updating the Workspace

```
scripts/update.sh
```

```bash
#!/usr/bin/env bash

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
# Jupyter Workspace Launcher
# ==========================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_ROOT"

echo "=========================================="
echo "Starting KnowledgeDome Workspace..."
echo "=========================================="

# ----------------------------------------------------------
# Activate virtual environment
# ----------------------------------------------------------

source .venv-core/bin/activate

# ----------------------------------------------------------
# Start JupyterLab
# ----------------------------------------------------------

LOGFILE="/tmp/jupyterlab.log"

rm -f "$LOGFILE"

jupyter lab \
    --no-browser \
    --ServerApp.open_browser=False \
    > "$LOGFILE" 2>&1 &

# ----------------------------------------------------------
# Wait until JupyterLab is ready
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
# Check if server started correctly
# ----------------------------------------------------------

if [[ -z "$URL" ]]; then

    echo
    echo "ERROR: Unable to detect JupyterLab URL."
    echo

    cat "$LOGFILE"

    exit 1

fi

echo
echo "JupyterLab running:"
echo "$URL"
echo

# ----------------------------------------------------------
# Launch Chromium as Desktop Application
# ----------------------------------------------------------

chromium \
    --app="$URL" \
    --disable-session-crashed-bubble \
    --disable-infobars \
    --new-window \
    >/dev/null 2>&1 &

echo "Workspace ready!"
```
# Removing the Workspace

```
scripts/clean.sh
```

```bash
#!/usr/bin/env bash

jupyter kernelspec uninstall ds-core -f

rm -rf .venv-core

echo
echo "Workspace removed."
```

---

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