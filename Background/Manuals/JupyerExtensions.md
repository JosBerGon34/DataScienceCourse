# JupyterLab Extensions & Productivity Guide

## Objective

This document describes the recommended extensions and features used throughout the Data Science Course.

The goal is to improve productivity while keeping the environment lightweight and reproducible.

---

# File Browser

JupyterLab includes a built-in file explorer capable of previewing multiple file formats.

Supported formats include:

- Python (.py)
- Markdown (.md)
- CSV
- JSON
- HTML
- SQL
- YAML
- Images
- Notebooks (.ipynb)

Double-click any file to open it in a new tab.

---

# CSV Viewer

CSV files can be opened directly from the File Browser.

The built-in viewer allows:

- Column sorting
- Table scrolling
- Quick inspection
- No notebook execution required

Useful for validating datasets before loading them into pandas.

---

# DataFrame Viewer

Instead of relying on notebook outputs:

```python
df.head()
```

use the Variable Inspector extension to inspect DataFrames interactively.

Recommended information:

- Shape
- Column types
- Memory usage
- Values
- Index

---

# Variable Inspector

Recommended package:

```bash
pip install lckr-jupyterlab-variableinspector
```

Provides:

- Live variables
- DataFrames
- NumPy arrays
- Dictionaries
- Lists

Similar to Spyder's Variable Explorer.

---

# Table of Contents

The Table of Contents panel automatically detects:

- Markdown headings
- Notebook sections

Useful for navigating long notebooks.

---

# Terminal

JupyterLab includes an integrated Bash terminal.

Typical usage:

- Git
- pip
- venv activation
- DuckDB CLI
- Python scripts

No external terminal required.

---

# Markdown Preview

Markdown files open directly inside JupyterLab.

Useful for:

- README
- Documentation
- Course notes

---

# Search

Global search:

```
Ctrl + Shift + F
```

Allows searching across the entire repository.

---

# Recommended workflow

Repository

↓

File Browser

↓

CSV Preview

↓

Notebook

↓

Variable Inspector

↓

Terminal

↓

Git

Everything remains inside a single JupyterLab session.