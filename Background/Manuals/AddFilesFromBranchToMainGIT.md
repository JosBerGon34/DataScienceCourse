🛠️ Paso a Paso en la Terminal

1. Guarda y confirma los cambios en tu rama actual
Asegúrate de estar en tu rama de trabajo (supongamos que se llama mi-rama o el módulo en el que estés) y tener confirmados los cambios de la carpeta:

git add ./Background
git commit -m "docs: update cheatsheets and templates in ./Background"

2. Cámbiate a la rama main

git checkout main

3. Actualiza y estira la carpeta de tu rama de trabajo hacia main
Este comando trae exactamente el contenido de ./Background tal como está en mi-rama y lo coloca listo para ser subido en main:

git checkout mi-rama -- Background

(Sustituye mi-rama por el nombre exacto de la rama en la que has trabajado, ej. MOD1.PREWORKREVIEW o similar).


4. Confirma y sube los cambios a main (Local y Remoto)

git commit -m "docs: sync ./Background folder from mi-rama"
git push origin main

5. Regresa a tu rama de trabajo para continuar

git checkout mi-rama

💡 ¿Qué hace exactamente git checkout <branch> -- <path>?
Extrae el estado de ese directorio específico de la otra rama y lo coloca en el staging area de tu rama actual (main). De esta manera, solo afectan a main los archivos que estén dentro de ./Background, dejando el resto del código de main intacto.