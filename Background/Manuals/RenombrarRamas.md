Para renombrar una rama local y sincronizar el cambio con el repositorio remoto, se deben ejecutar los siguientes comandos en secuencia:

Renombrar localmente:
Si estás en la rama a renombrar: git branch -m <nuevo-nombre>
Si estás en otra rama: git branch -m <nombre-antiguo> <nuevo-nombre>
Nota: Usa -M en lugar de -m si el sistema de archivos no distingue mayúsculas de minúsculas o si el nuevo nombre ya existe localmente. 
Eliminar la rama antigua en el remoto: git push origin --delete <nombre-antiguo> 
Enviar la nueva rama y configurar el upstream: git push -u origin <nuevo-nombre> 
Una vez realizado este proceso, cualquier colaborador que tenga una copia local del repositorio deberá actualizar su configuración para reflejar el nuevo nombre, ejecutando git fetch origin, git branch -m <nombre-antiguo> <nuevo-nombre> (si aún tienen la rama antigua local) y git branch -u origin/<nuevo-nombre> <nuevo-nombre>. 