# Guía Técnica: Sincronizar Carpetas Específicas de una Rama Secundaria a `main`

Este manual documenta el procedimiento estándar para traer modificaciones hechas en carpetas específicas (por ejemplo, `./Background` o `./docs`) desde una rama de desarrollo hacia la rama principal (`main`), sin realizar un *merge* completo de toda la rama.

---

## ⚠️ Requisito Previo Fundamental

Para evitar errores como `error: ruta especificada no concordó con ningún archivo`, **asegúrate siempre de estar posicionado en la raíz del repositorio Git** antes de ejecutar estos comandos:

```bash
# Ir a la raíz del repositorio local
cd "$(git rev-parse --show-toplevel)"



🚀 Flujo de Trabajo Paso a Paso
1. Guardar o enviar cambios en la rama de trabajo
Asegúrate de que la rama secundaria (por ejemplo, Module2.1 o mi-rama) tiene todos sus cambios guardados y confirmados (committed) o subidos (pushed):

#Bash:
# En tu rama de trabajo
git add .
git commit -m "docs: guarda cambios locales en carpetas Background y docs"
git push origin nombre-de-la-rama

2. Cambiar a la rama principal (main)

#Bash:
git checkout main
git pull origin main

3. Extraer carpetas específicas desde la rama de trabajo
Puedes extraer una o múltiples carpetas conjuntamente en un solo comando pasando sus rutas separadas por espacio.

#Bash:

#Sincroniza múltiples carpetas en un solo paso
git checkout nombre-de-la-rama -- Background docs

💡 ¿Qué hace exactamente este comando? > Extrae el estado exacto de los directorios especificados en nombre-de-la-rama 
y los copia directamente al Staging Area (Índice) de tu rama actual (main). 
No es necesario ejecutar git add posteriormente, ya que Git los deja preparados automáticamente para el commit.

4. Confirmar y subir los cambios en main

# Confirmar los cambios en local
git commit -m "docs: sync Background y docs desde nombre-de-la-rama"

# Subir al repositorio remoto
git push origin main

5. Regresar a tu rama de trabajo

git checkout nombre-de-la-rama

🛠️ Resumen de Atajos y Casos EspecialesSituaciónComando 
Recomendado
Paso rápido desde subcarpeta: git checkout nombre-de-la-rama -- :/Background :/docs (El prefijo :/ indica la raíz de Git)
Traer un solo archivo: git checkout nombre-de-la-rama -- Background/Manual.md
Ver qué se va a commitear: git status