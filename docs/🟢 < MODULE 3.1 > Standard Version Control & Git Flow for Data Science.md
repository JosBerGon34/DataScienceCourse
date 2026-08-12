### 🎯 Context & Objectives

In Data Science, version control is essential not only for managing code changes but also for **auditing experiments**, isolating feature engineering developments, and preventing large or sensitive raw datasets (e.g., raw `.csv` files or database credentials) from polluting the repository.

In this exercise, you will set up a professional workflow (_Git Flow_) using standard CLI operations to structure the project workspace and manage feature branches (`MOD3.1_gitflow`).

### 📑 Exercise Instructions

#### 1. Syntactic / Terminal Operations (`git` CLI)

Execute the following standard and advanced CLI sequence in your local environment (Bash/Zsh):

1. **Initialization & Global/Local Configuration**:
    
    - Verify or set up your local user signature (`user.name` and `user.email`).
        
    - Ensure default branch naming is set to `main`.
        
2. **Branching & Isolation (_Feature Branch_)**:
    
    - Create and switch to a new branch named `MOD3.1_gitflow` branching off from `main`.
        
3. **Ignored Files Management (`.gitignore`)**:
    
    - Create or update a `.gitignore` file at the root of your repository.
        
    - Configure rules to ignore:
        
        - Heavy/local datasets (`*.csv`, `*.parquet`, `*.sqlite`), preserving only small sample files.
            
        - Jupyter Notebook checkpoints (`.ipynb_checkpoints/`).
            
        - Virtual environments, cache, and sensitive environment keys (`.env`, `.venv/`, `__pycache__/`).
            
4. **Staging & Conventional Commits**:
    
    - Stage your modifications using `git add`.
        
    - Commit using the _Conventional Commits_ specification (e.g., `feat(git): add .gitignore and initial project structure`).
        
5. **Temporary State Management (`git stash`)**:
    
    - Modify a text file or notebook cell locally without committing.
        
    - Stash your uncommitted changes using `git stash`.
        
    - Verify a clean working directory with `git status`.
        
    - Restore stashed changes back using `git stash pop`.
        
6. **Remote Synchronization**:
    
    - Push your feature branch to GitHub (`git push -u origin MOD3.1_gitflow`).
        

#### 2. Applied Data Science Architecture

Apply these operations directly to your project workspace:

1. **Directory Structure Setup**: Build the following folder hierarchy and include a `.gitkeep` file in empty directories to enforce tracking:
├── data/
│   ├── raw/            <-- Untracked raw datasets (ignored via .gitignore)
│   └── processed/      <-- Derived & cleaned datasets
├── notebooks/          <-- Module Jupyter Notebooks (.ipynb)
├── src/                <-- Helper Python scripts (.py)
├── .gitignore          <-- Exclusions
└── README.md           <-- Main documentation

2. **Notebook Version Control Practice**:
    
    - Create a dummy notebook at `notebooks/03_1_git_test.ipynb`.
        
    - Clear cell outputs before committing to avoid committing large JSON/metadata diffs, or examine how cell output changes affect your `git diff`.
        

### 🌐 Official References for Documentation

- **Git Official Documentation**: [Git Reference Manual](https://git-scm.com/docs)
    
- **GitHub Docs - Ignoring Files**: [Ignoring Files - GitHub Docs](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files)
    
- **Conventional Commits Standard**: [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
    

### 📚 Recommended Manuals & CheatSheets

- **GitHub Official Git Cheat Sheet**: [GitHub Git Cheat Sheet (PDF)](https://education.github.com/git-cheat-sheet-education.pdf)
    
- **Pro Git Book by Scott Chacon & Ben Straub**: [Pro Git Book (Free Online)](https://git-scm.com/book/en/v2)
    

💻 **Your Challenge**: Execute this workflow on your terminal and set up your repository layout. When you are ready or if you encounter any CLI issues, let me know to move on to **Exercise 3.2: Modern Web Scraping for Data Science**.