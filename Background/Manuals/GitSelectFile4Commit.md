Un flujo profesional suele ser:
1. Configuro las reglas del repositorio (.gitignore)
            │
            ▼
2. Git ya sabe qué archivos locales no deben versionarse
            │
            ▼
3. Empiezo a añadir únicamente los archivos que sí quiero subir

# 1. Crear o modificar .gitignore
nano .gitignore

# 2. Comprobar el estado
git status

# 3. Añadir únicamente lo que quieres versionar
git add .gitignore
git add README.md
git add src/
git add notebooks/sample2.ipynb

# 4. Verificar el Stage
git status

# 5. Commit
git commit -m "chore(git): configure repository ignore rules"


                WORKING TREE
                     │
                     ▼
              ┌─────────────┐
              │ .gitignore  │
              └─────────────┘
                 │       │
              Ignora   Permite
                 │       │
                 ▼       ▼
              Descartado  Staging Area
                              │
                              ▼
                          git commit
                              │
                              ▼
                          Repository