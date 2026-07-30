# --- GESTIÓN DE ENTORNOS VIRTUALES (venv) ---

# 1. Crear un nuevo entorno virtual (carpeta .venv)
python3 -m venv .venv

# 2. Activar el entorno virtual
source .venv/bin/activate

# 3. Desactivar el entorno virtual
deactivate

# 4. Eliminar completamente el entorno virtual (si está corrupto o quieres resetear)
# Nota: Primero asegúrate de estar fuera del entorno (deactivate)
rm -rf .venv


# --- GESTIÓN DE PAQUETES (pip) ---

# 5. Instalar una dependencia
pip install nombre_paquete

# 6. Eliminar una dependencia (útil para resolver conflictos/interdependencias)
pip uninstall nombre_paquete

# 7. Eliminar varias dependencias a la vez
pip uninstall paquete1 paquete2 paquete3

# 8. Listar paquetes instalados y sus versiones
pip list

# 9. Exportar dependencias a un archivo requirements.txt
pip freeze > requirements.txt

# 10. Instalar desde requirements.txt
pip install -r requirements.txt


# --- LIMPIEZA DE CACHE Y REPARACIÓN ---

# 11. Limpiar la caché de pip (soluciona errores de descarga o instalación corrupta)
pip cache purge

# 12. Ver información de la caché de pip
pip cache info


# --- SOLUCIÓN DE PROBLEMAS EN VSCODIUM ---

# 13. Si VSCodium no detecta el intérprete:
#     a) Activa el entorno en la terminal integrada: source .venv/bin/activate
#     b) Abre la paleta de comandos (Ctrl+Shift+P)
#     c) Ejecuta: "Python: Select Interpreter"
#     d) Elige la ruta que apunta a .venv/bin/python

# 14. Si la terminal se "buggea" o no responde bien tras activar/desactivar:
#     - Cierra la terminal integrada en VSCodium (icono de basura o Ctrl+Shift+C)
#     - Abre una nueva terminal (Ctrl+Shift+` o Terminal > New Terminal)
#     - Vuelve a activar: source .venv/bin/activate

# 15. Resetear extensión de Python en VSCodium (desde terminal, recarga la ventana)
#     Ejecuta esto en la paleta de comandos, no en bash: "Developer: Reload Window"   