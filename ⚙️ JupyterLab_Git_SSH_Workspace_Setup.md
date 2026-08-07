
***Comands to reactivate agent with your id to use git in new JupyterLab instances:
Find your ssh id, has to be the same as the registered on Github:

~/.ssh/

***Register that id with keychain program. (Downloadable in linux `sudo pacman -S keychain`)

eval $(keychain --eval --quiet id_ed25519)

***Make an instruction for reactivate it in every systemstart:

systemctl --user enable --now ssh-agent.service
ssh-add ~/.ssh/id_ed25519   # o el nombre de tu clave

## Purpose

This guide prepares a reproducible JupyterLab workspace with Git integration and GitHub SSH authentication.

The goal is to keep the workspace architecture clean:

```text
Project repository
│
├── .venv-core/
│   ├── JupyterLab
│   ├── IPykernel
│   ├── JupyterLab Git
│   └── NBDime
│
├── notebooks/
├── data/
├── src/
├── requirements/
└── scripts/
```

The following principles are intentionally maintained:

- JupyterLab and its extensions belong to the project's virtual environment.
- The Jupyter kernel points to that same virtual environment.
- Git belongs to the project repository.
- SSH credentials belong to the operating-system user.
- Chromium is only the graphical client for JupyterLab.
- No personal paths, emails, tokens, private keys, or machine-specific identifiers belong in the repository.

---

# 1. Prerequisites

The procedure assumes:

- Git is installed.
- Python is installed.
- Bash is available.
- Chromium is installed.
- The project repository already exists locally.
- A GitHub account is available.
- The project virtual environment has been created or can be created.

## Windows

When using Windows 11, run the project setup from a Bash environment such as Git Bash or another Bash-compatible terminal.

Avoid depending on PowerShell-specific commands in project scripts.

Project scripts should use dynamically resolved paths rather than hard-coded user paths.

For example:

```bash
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
```

Do not use machine-specific paths such as:

```text
/home/<username>/...
```

or:

```text
C:\Users\<username>\...
```

inside portable project scripts.

---

# 2. Activate the Project Virtual Environment

From the project root:

```bash
source .venv-core/bin/activate
```

Verify that Python belongs to the virtual environment:

```bash
python -c "import sys; print(sys.executable)"
```

Expected pattern:

```text
.../project/.venv-core/bin/python
```

All Jupyter-related packages in this guide should be installed while this environment is active.

---

# 3. Install JupyterLab Git Extensions

## Core Git integration

Install the JupyterLab Git extension inside the project's virtual environment:

```bash
python -m pip install --upgrade jupyterlab-git
```

Install NBDime for notebook-aware Git diffs:

```bash
python -m pip install --upgrade nbdime
```

If the project uses a dedicated requirements file, keep these dependencies there rather than installing them globally.

Example:

```text
requirements/
├── ReqJupCore.txt
├── ReqJupDev.txt
├── ReqJupML.txt
├── ReqJupDL.txt
└── ReqJupScrapping.txt
```

The exact grouping can be adapted to the project.

---

# 4. Verify the Jupyter Server Extensions

With the virtual environment active:

```bash
jupyter server extension list
```

The Git-related extension should appear as enabled and valid.

Typical relevant entries include:

```text
jupyterlab_git enabled
nbdime enabled
```

JupyterLab itself should also be enabled.

If validation reports an error, resolve the server-side installation before continuing.

---

# 5. Verify the JupyterLab Frontend Extension

Run:

```bash
jupyter labextension list
```

The Git frontend should appear in the installed extensions.

A typical installation contains:

```text
@jupyterlab/git
nbdime-jupyterlab
```

This distinction is important:

```text
JupyterLab frontend
        │
        └── @jupyterlab/git
                 │
                 ▼
Jupyter Server backend
        │
        └── jupyterlab_git
                 │
                 ▼
              system Git
```

The frontend provides the interface while the server extension connects that interface to Git operations.

---

# 6. Verify Git Itself

From the project root:

```bash
git --version
```

Then:

```bash
git status
```

Check the configured remote:

```bash
git remote -v
```

The project should use an SSH remote, for example:

```text
origin  git@github.com:OWNER/REPOSITORY.git (fetch)
origin  git@github.com:OWNER/REPOSITORY.git (push)
```

Replace `OWNER/REPOSITORY` with the actual project repository.

Do not place a personal repository URL in reusable documentation unless the documentation is intentionally project-specific.

---

# 7. Configure SSH for GitHub

SSH authentication is independent from the Python virtual environment.

The SSH identity belongs to the operating-system user:

```text
~/.ssh/
```

A typical setup contains:

```text
~/.ssh/
├── id_ed25519
├── id_ed25519.pub
└── known_hosts
```

## Important

Never commit or share:

```text
id_ed25519
```

This is the private key.

The public key:

```text
id_ed25519.pub
```

can be registered with GitHub.

---

# 8. Generate an ED25519 SSH Key

If the machine does not already have an appropriate GitHub SSH key, generate one:

```bash
ssh-keygen -t ed25519 -C "YOUR_GITHUB_EMAIL"
```

When asked where to save the key, the default location is normally appropriate:

```text
~/.ssh/id_ed25519
```

A passphrase is recommended.

After generation:

```bash
ls -la ~/.ssh
```

Expected files:

```text
id_ed25519
id_ed25519.pub
```

Recommended permissions:

```text
id_ed25519      600
id_ed25519.pub  644
```

The private key must remain readable only by the user.

---

# 9. Start the SSH Agent

Start an SSH agent in the current Bash session:

```bash
eval "$(ssh-agent -s)"
```

Expected output:

```text
Agent pid XXXXX
```

Add the private key:

```bash
ssh-add ~/.ssh/id_ed25519
```

If the key has a passphrase, enter it when requested.

Verify the loaded identity:

```bash
ssh-add -l -E sha256
```

A SHA256 fingerprint should be displayed.

---

# 10. Optional SSH Configuration

For a simple single-key GitHub setup, an SSH configuration file can explicitly select the key.

Create:

```bash
nano ~/.ssh/config
```

Example:

```text
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

Protect the configuration:

```bash
chmod 600 ~/.ssh/config
```

`IdentitiesOnly yes` tells SSH to use the explicitly configured identity instead of trying unrelated identities.

---

# 11. Register the Public Key in GitHub

Display the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the complete single line.

In GitHub:

```text
Settings
    → SSH and GPG keys
        → New SSH key
```

Use:

```text
Key type: Authentication Key
```

Give the key a descriptive machine-specific title, for example:

```text
Data Science Workstation
```

Paste the public key and save it.

A GitHub account can have multiple SSH keys, allowing different computers to use independent identities.

---

# 12. Test the GitHub SSH Connection

Run:

```bash
ssh -T git@github.com
```

A successful authentication produces a message similar to:

```text
Hi USER! You've successfully authenticated, but GitHub does not provide shell access.
```

This is the expected result.

The message confirms authentication; it does not provide shell access to GitHub.

---

# 13. Troubleshooting SSH

If authentication fails with:

```text
Permission denied (publickey).
```

run:

```bash
ssh -vT git@github.com
```

Look for:

```text
Offering public key: ...
```

and verify that the fingerprint corresponds to the public key registered in GitHub.

You can also inspect the loaded agent identities:

```bash
ssh-add -l -E sha256
```

The important distinction is:

```text
Connection failed
        ≠
Authentication failed
```

If the log reaches:

```text
Connection established.
```

and later reports:

```text
Permission denied (publickey).
```

the network connection to GitHub is working; the problem is authentication or key association.

Do not modify the router or Jupyter configuration until SSH authentication itself has been verified.

---

# 14. Verify the Repository Remote

After SSH authentication works:

```bash
cd /path/to/project
```

Then:

```bash
git remote -v
```

If necessary, configure the SSH remote:

```bash
git remote set-url origin git@github.com:OWNER/REPOSITORY.git
```

Test it without changing the working tree:

```bash
git fetch origin
```

`git fetch` updates the remote references but does not merge changes into the current working tree.

Inspect all branches:

```bash
git branch -a
```

Typical output:

```text
* current-branch
  remotes/origin/main
  remotes/origin/Module1.1
  remotes/origin/Module2.1
  remotes/origin/Module3.1
  remotes/origin/Module3.2b
```

---

# 15. JupyterLab Git Architecture

Once the previous layers work independently, JupyterLab Git can use the same Git installation and SSH identity.

The complete path is:

```text
Chromium
    │
    ▼
JupyterLab frontend
    │
    ▼
JupyterLab Git extension
    │
    ▼
Jupyter Server
    │
    ▼
system Git
    │
    ▼
SSH
    │
    ▼
GitHub
```

The Python environment does not contain the SSH identity.

Instead:

```text
.venv-core
    ├── JupyterLab
    ├── jupyterlab-git
    ├── nbdime
    └── project Python packages

OS user
    └── ~/.ssh/
          └── id_ed25519
```

This separation is intentional.

---

# 16. Chromium

Chromium can be used as the dedicated browser client for the local JupyterLab server.

The browser does not need GitHub credentials.

Authentication is performed by the server-side Git process through SSH.

Therefore:

```text
Chromium
    └── displays JupyterLab

JupyterLab
    └── runs inside .venv-core

Git
    └── runs on the local system

SSH
    └── authenticates the operating-system user
```

A clean Chromium profile can be used for the JupyterLab workspace.

Do not store browser-specific credentials or profile data inside the repository.

---

# 17. Project Scripts

A recommended project structure is:

```text
scripts/
├── setup.sh
├── run.sh
├── stop.sh
├── update.sh
└── clean.sh
```

The scripts should resolve the project root dynamically.

Example:

```bash
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
```

They should not depend on personal usernames or absolute machine-specific paths.

If `run.sh` stores the JupyterLab process identifier:

```text
.jupyter.pid
```

add it to `.gitignore`:

```gitignore
.jupyter.pid
```

Runtime state must not become repository content.

---

# 18. Recommended `.gitignore` Entries

The exact project `.gitignore` depends on the project, but typical Jupyter/Python runtime files include:

```gitignore
# Virtual environments
.venv/
.venv-core/

# Python cache
__pycache__/
*.py[cod]

# Jupyter
.ipynb_checkpoints/
.jupyter.pid

# Local environment files
.env
.env.*

# OS/editor files
.DS_Store
```

Do not ignore source notebooks, datasets, documentation, or project files that are intentionally part of the repository.

---

# 19. Verification Checklist

Before considering the workspace ready, verify each layer independently.

## Python

```bash
python -c "import sys; print(sys.executable)"
```

Must point to the project `.venv`.

## JupyterLab

```bash
jupyter lab --version
```

## Kernel

```bash
jupyter kernelspec list
```

The project kernel should point to the intended virtual environment.

## Git

```bash
git --version
git status
git remote -v
```

## Jupyter Git

```bash
jupyter server extension list
jupyter labextension list
```

Both frontend and backend Git components should be enabled.

## SSH

```bash
ssh-add -l -E sha256
ssh -T git@github.com
```

## Remote branches

```bash
git fetch origin
git branch -a
```

Only after these checks succeed should Git operations be performed through the JupyterLab interface.

---

# 20. Final Architecture

The completed workspace should follow this model:

```text
                         GitHub
                           ▲
                           │
                         SSH
                           ▲
                           │
                     System Git
                           ▲
                           │
                  Jupyter Server
                           ▲
                           │
                JupyterLab Git
                           ▲
                           │
                     JupyterLab
                           ▲
                           │
                    .venv-core
                           ▲
                           │
                       Python
                           ▲
                           │
                    Project code

Chromium ────────────────► JupyterLab UI
```

The responsibilities remain separated:

| Layer | Responsibility |
|---|---|
| Chromium | Graphical browser client |
| JupyterLab | Notebook and workspace interface |
| JupyterLab Git | Git interface inside JupyterLab |
| Jupyter Server | Server-side Jupyter operations |
| `.venv-core` | Python and project dependencies |
| IPykernel | Connects Jupyter notebooks to Python |
| Git | Local version control |
| SSH | Authentication |
| GitHub | Remote repository |

---

# 21. Golden Rules

1. Install JupyterLab and its extensions inside the project virtual environment.
2. Register the project kernel against that same virtual environment.
3. Keep Git authentication outside the Python environment.
4. Keep SSH private keys outside the repository.
5. Register only the public SSH key with GitHub.
6. Test SSH independently before troubleshooting JupyterLab Git.
7. Use `git fetch` when you only need to refresh remote references.
8. Treat `git switch`, `merge`, `pull`, `reset`, and `push` as separate operations with different effects.
9. Keep runtime files such as `.jupyter.pid` out of Git.
10. Use portable, dynamically resolved paths in project scripts.
11. Keep personal credentials, usernames, emails, tokens, and machine-specific paths out of repository documentation.
12. Use Chromium only as the client; do not couple browser configuration to Git authentication.

---

## Result

After completing this guide, the project has a self-contained JupyterLab environment with:

- a dedicated Python virtual environment;
- a dedicated JupyterLab installation;
- a registered project kernel;
- JupyterLab Git integration;
- NBDime notebook diff support;
- GitHub SSH authentication;
- portable project scripts;
- Chromium as the local graphical client;
- and a clear separation between project dependencies, version control, authentication, and browser presentation.
