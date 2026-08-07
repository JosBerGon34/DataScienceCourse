                    JupyterLab
                         │
                         │
              (Kernel Manager)
                         │
         ┌───────────────┴───────────────┐
         │                               │
      ds-core                      ds-scraping
         │                               │
         │                               │
 kernel.json                      kernel.json
         │                               │
         ▼                               ▼
/home/josu/.../.venv-core/bin/python
/home/josu/.../.venv-scraping/bin/python
         │
         ▼
 Python Interpreter
         │
         ▼
 site-packages
         │
         ▼
 pandas
 numpy
 duckdb
 playwright



 # Python Virtual Environment & Jupyter Kernel Setup

## Objective

This guide explains how to create a clean Python virtual environment (`venv`), install all required dependencies and register a Jupyter kernel for this project.

The goal is to guarantee that every notebook runs under the exact same Python environment.

---

# 1. Verify your Python version

This course has been developed using Python 3.13.

Check your installed version:

```bash
python3.13 --version
```

Expected output:

```text
Python 3.13.x
```

---

# 2. Create the virtual environment

From the project root:

```bash
python3.13 -m venv .venv-core
```

Project structure:

```
DataScienceCourse/
│
├── .venv-core/
├── data/
├── notebooks/
├── src/
└── requirements/
```

---

# 3. Activate the virtual environment

Linux / macOS

```bash
source .venv-core/bin/activate
```

Windows PowerShell

```powershell
.venv-core\Scripts\Activate.ps1
```

---

# 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# 5. Install project dependencies

Example:

```bash
pip install -r requirements/req-core.txt
```

Verify installed packages:

```bash
pip list
```

---

# 6. Install Jupyter Kernel

Every virtual environment must register its own Jupyter Kernel.

Install ipykernel:

```bash
pip install ipykernel
```

Register the environment:

```bash
python -m ipykernel install \
    --user \
    --name ds-core \
    --display-name "Python (DS Core)"
```

---

# 7. Verify kernel registration

Execute:

```bash
jupyter kernelspec list
```

Expected output:

```text
Available kernels:

ds-core
```

---

# 8. Launch JupyterLab

```bash
jupyter lab
```

The browser should automatically open.

---

# 9. Select the correct kernel

Inside any notebook:

```
Kernel
    ↓
Change Kernel
    ↓
Python (DS Core)
```

Always verify that the notebook is using the correct kernel.

---

# 10. Verify the active Python interpreter

Execute the following cell:

```python
import sys
import platform

print("Python:", sys.version)
print("Executable:", sys.executable)
print("Platform:", platform.platform())
```

Expected executable:

```
.../DataScienceCourse/.venv-core/bin/python
```

---

# 11. Updating project dependencies

Whenever the requirements file changes:

```bash
source .venv-core/bin/activate

pip install -r requirements/req-core.txt
```

No additional kernel registration is required.

---

# 12. Removing the environment

Delete the virtual environment:

```bash
rm -rf .venv-core
```

Delete the registered kernel:

```bash
jupyter kernelspec uninstall ds-core
```

---

# Recommended workflow

```
Git Repository
        │
        ▼
Virtual Environment (.venv-core)
        │
        ▼
Python Interpreter
        │
        ▼
Jupyter Kernel (ds-core)
        │
        ▼
JupyterLab
        │
        ▼
Notebook
```

The virtual environment contains the Python interpreter and installed packages.

The Jupyter kernel acts as a bridge between JupyterLab and the virtual environment.

JupyterLab executes notebooks through the selected kernel.