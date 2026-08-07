
#### 1. Syntactic / Terminal Operations (`git` CLI)


Execute the following standard and advanced CLI sequence in your local environment (Bash/Zsh):

1. **Initialization & Global/Local Configuration**:

- Verify or set up your local user signature (`user.name` and `user.email`).

- Ensure default branch naming is set to `main`.

***Bash
```
#1 Lets type bash on fish terminal to swap language
~/Documentos/DataScienceCourse main
Welcome to fish, the friendly interactive shell
Type help for instructions on how to use fish

❯'bash'
[****@cachyos- **** DataScienceCourse]$ (user hided info)

#2 Let's type next command to ensure we are linked to github from
#local workspace, in my case VSCodium.
~/Documentos/DataScienceCourse main

❯ 'git config user.name'
  'git config user.email'  
******Gon34 -Github Account (hided info)
*******jbg@gmail.com -Email, (hided info)

#3 Let's check if we are in the main branch, just swaping to main branch
#with git checkout command.
~/Documentos/DataScienceCourse main*(this identification tells us in wich brand we are)*

❯ 'git checkout main'
Ya en 'main'
Tu rama está actualizada con 'origin/main'.

```

2. **Branching & Isolation (_Feature Branch_)**:

- Create and switch to a new branch named `Module3.1` branching off from `main`.

***Bash
```
#1 Let's make a new branch with the comand switch
[****@cachyos- **** DataScienceCourse]$
 
❯'git switch -c Module3.1'
Cambiado a nueva rama 'Module3.1'

```

3. **Ignored Files Management (`.gitignore`)**:

- Create or update a `.gitignore` file at the root of your repository.

- Configure rules to ignore:

- Heavy/local datasets (`*.csv`, `*.parquet`, `*.sqlite`), preserving only small sample files.

- Jupyter Notebook checkpoints (`.ipynb_checkpoints/`).

- Virtual environments, cache, and sensitive environment keys (`.env`, `.venv/`, `__pycache__/`).


	#Recomended structure:

DataScienceCourse/
│
├── notebooks/
├── src/
├── samples/               ← We can upload samples of csv, shorting the memory used.
│   ├── survey_sample.csv
│   └── gini_sample.csv
│
├── datasets/              ← we dont need to upload csv's, or other formats related to	 tables		
│   ├── survey.csv
│   ├── gini.parquet
│   └── eurostat.sqlite
│
├── .venv/                 ← Ignored
├── .env                   ← Ignored
├── requirements.txt
├── README.md
└── .gitignore

***.gitignore list
```
# ==========================================================
# Data Science Project - .gitignore
# ==========================================================

# ----------------------------------------------------------
# Virtual Environments
# ----------------------------------------------------------
.venv/
venv/
env/
ENV/
.pracc/
.pracc313/

# ----------------------------------------------------------
# Python Cache
# ----------------------------------------------------------
__pycache__/
*.py[cod]
*$py.class

# ----------------------------------------------------------
# Jupyter
# ----------------------------------------------------------
.ipynb_checkpoints/

# ----------------------------------------------------------
# Environment Variables / Secrets
# ----------------------------------------------------------
.env
.env.*
*.env

# ----------------------------------------------------------
# Local Datasets
# Ignore heavy datasets while preserving sample datasets
# ----------------------------------------------------------
*.csv
*.parquet
*.sqlite
*.db

# Keep small example datasets
!samples/
!samples/**
!datasets_sample/
!datasets_sample/**

# ----------------------------------------------------------
# Generated Outputs
# ----------------------------------------------------------
*.log
*.tmp
*.bak

# ----------------------------------------------------------
# IDE
# ----------------------------------------------------------
.vscodium/
.idea/

# (Optional) Keep workspace settings if collaborating
#!.vscodium/settings.json

# ----------------------------------------------------------
# OS Files
# ----------------------------------------------------------
.DS_Store
Thumbs.db

# ----------------------------------------------------------
# Python Packaging
# ----------------------------------------------------------
build/
dist/
*.egg-info/

# ----------------------------------------------------------
# Testing / Coverage
# ----------------------------------------------------------
.pytest_cache/
.coverage
htmlcov/
```

4. **Staging & Conventional Commits**:

- Stage your modifications using `git add`.

- Commit using the _Conventional Commits_ specification (e.g., `feat(git): add .gitignore and initial project structure`).

	4.1: Example of situation, for select which file will be commited and which ignored:

                 ┌───────────────────────────────┐
                 │      Working Tree             │
                 │ (Local files)          │
                 │                               │
                 │ sample.ipynb                  │
                 │ sample2.ipynb                 │
                 │ .gitignore                    │
                 └───────────────┬───────────────┘
                                 │
                          git add file
                                 │
                                 ▼
                 ┌───────────────────────────────┐
                 │        Staging Area           │
                 │   (Next commit)            │
                 └───────────────┬───────────────┘
                                 │
                            git commit
                                 │
                                 ▼
                 ┌───────────────────────────────┐
                 │      Git Repository           │
                 │ (Permanent History log)       │
                 └───────────────────────────────┘

	- We have sample.ipynb with !Hello world the one we need to commit, and update the remote repository, and sample2.ipynb who will be ignored for the commit, staying in our local workspace using the .gitignore mechanic.
	
	
# git add files has priority and exclusivity on the next commit, so you use this command to select and ignore files you want to keep in local workspace.


***Bash
```
# First of all we make a file sample.ipynb in notebook folder,
#  then we type /DataScienceCourse/notebooks/sample.ipynb/'!hello world'
#  also we create sample2 empty, sample will be commited and sample2 ignored.

#Step 1: Edit .gitignore: sample2.ipynb

#Step 2: We only add to commit .gitignore as 
[****@cachyos-**** DataScienceCourse]$
❯'git add .gitignore'

#Step 3: Time to add to commit sample.ipynb
[****@cachyos-**** DataScienceCourse]$
❯'git add sample.ipynb'

#Step 4:
[****@cachyos-**** DataScienceCourse]$
❯'git commit -m "chore(git): ignore sample2 notebook"'
[Module3.1 50db125] chore(git): ignore sample2 notebook
2 files changed, 21 insertions(+)
create mode 100644 notebooks/sample.ipynb

```


5. **Temporary State Management (`git stash`)**:

- Modify a text file or notebook cell locally without committing.

- Stash your uncommitted changes using `git stash`.

- Verify a clean working directory with `git status`.

- Restore stashed changes back using `git stash pop`.

  #5.1: We make an example making a sample3.ipynb with Bye Bye World! in a markdown cell inside.
***Bash
```
#Step 1: using 'git stash' we temporally block the file to be commited, it will be saved only in the local repository. First of all lets check which changes are
without commit

[****@cachyos-**** DataScienceCourse]$
❯'git status'
[****@cachyos-**** DataScienceCourse]$ git status
En la rama Module3.1
Tu rama está actualizada con 'origin/Module3.1'.

Archivos sin seguimiento:
  (usa "git add <archivo>..." para incluirlo a lo que será confirmado)
        notebooks/sample3.ipynb

no hay nada agregado al commit pero hay archivos sin seguimiento presentes (usa "git add" para hacerles seguimiento)

#Step 2: Let's stash this file to avoid the commit temporally, still the file
is working properly.
[****@cachyos-**** DataScienceCourse]$
❯'git stash push -u -m "WIP: sample3 notebook exercise"'
Directorio de trabajo y estado de índice On Module3.1: WIP: sample3 notebook exercise guardados

#Step 3: Lets recover the stashed file with git stash pop
[****@cachyos-**** DataScienceCourse]$
❯'git stash pop'
Ya está actualizado.
En la rama Module3.1
Tu rama está actualizada con 'origin/Module3.1'.

Archivos sin seguimiento:
  (usa "git add <archivo>..." para incluirlo a lo que será confirmado)
        notebooks/sample3.ipynb

no hay nada agregado al commit pero hay archivos sin seguimiento presentes (usa "git add" para hacerles seguimiento)
Descartado refs/stash@{0} (Hexadecimal code)
```

6. **Remote Synchronization**:

- Push your feature branch to GitHub (`git push -u origin Module3.1`).

***Bash
```
#Step 1: Lets track the Module3.1 branch

[****@cachyos-**** DataScienceCourse]$
❯'git push -u origin Module3.1'
rama 'Module3.1' configurada para rastrear 'origin/Module3.1'.
Everything up-to-date

#Step 2: Add and commit the remaining files.

[****@cachyos-**** DataScienceCourse]$
❯'git add ./notebooks/sample3.ipynb'

[****@cachyos-**** DataScienceCourse]$
❯git commit -m "AllWorkDone"
[Module3.1 b8dc6da] AllWorkDone
 1 file changed, 19 insertions(+)
 create mode 100644 notebooks/sample3.ipynb

```
7. **Directory Structure Setup**: Build the following folder hierarchy and include a `.gitkeep` file in empty directories to enforce tracking:

├── data/

│ ├── raw/ <-- Untracked raw datasets (ignored via .gitignore)

│ └── processed/ <-- Derived & cleaned datasets

├── notebooks/ <-- Module Jupyter Notebooks (.ipynb)

├── src/ <-- Helper Python scripts (.py)

├── .gitignore <-- Exclusions

└── README.md <-- Main documentation

My .gitkeep config:

DataScienceCourse/
│
├── data/
│   ├── .gitkeep
│   ├── raw/
│   │   └── None, ill prefer to keep them only in local, with .gitignore setup.
│   ├── processed/
│   │   └── .gitkeep
│   └── external/
│       └── .gitkeep
│
├── notebooks/	
│        └── .gitkeep
├── src/
│       └── .gitkeep
└── README.md
  

8. **Notebook Version Control Practice**:

- Create a dummy notebook at `notebooks/03_1_git_test.ipynb`.

- Clear cell outputs before committing to avoid committing large JSON/metadata diffs, or examine how cell output changes affect your `git diff`.

#STEP1: Create the notebook:

notebooks/
└── 03_1_git_test.ipynb

Type in a code cell: 

***Python
```
print("Git notebook test")
```

***Bash
```
#Step2: Let's check if git detects the changes

[****@cachyos-**** DataScienceCourse]$
❯'git diff'
<>JSON
{
  "cells":[
      {
          "cell_type":"code",
          "source":[
              "print(\"Git notebook test\")"
          ],
          "outputs":[
              {
                  ...
              }
          ],
          "execution_count":1
      }
  ]
}
#Step3: Lets clean cell outputs and restart python kernel.
#execute git diff again.

[****@cachyos-**** DataScienceCourse]$
❯'git diff'
<>JSON
"outputs": [...]
```