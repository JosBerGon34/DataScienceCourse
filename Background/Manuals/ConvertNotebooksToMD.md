🛠️ Opción A: Línea de Comandos (Recomendada para Automatización)
Esta es la opción más robusta. Utiliza la herramienta jupyter nbconvert que se instala junto con Jupyter. 

Requisito previo:

pip install nbconvert   

1. Exportar CON Assets (Imágenes)
Por defecto, nbconvert extrae las imágenes y crea una carpeta adjunta.

# Sintaxis
jupyter nbconvert --to markdown tu_notebook.ipynb #Clicando encima del notebook para crear la ventana de terminal, si el notebook ya tiene salidas outputcells se imprimen en el md.
jupyter nbconvert --to markdown Ex3.2.ipynb

# Output generado:
# 1. tu_notebook.md
# 2. Carpeta: tu_notebook_files/ (contiene todas las imágenes .png, .jpg, etc.)  
El archivo .md tendrá referencias relativas tipo ![imagen](tu_notebook_files/imagen.png). 

2. Exportar SIN Assets (Solo texto y código)
Para evitar que se genere la carpeta de imágenes y obtener un archivo .md limpio (útil para documentación rápida o repositorios ligeros), debes excluir las salidas que contienen imágenes.

No existe un flag único --no-images, pero puedes lograrlo excluyendo las celdas de salida o filtrando por tipos de datos si usas una plantilla custom. La forma más rápida "nativa" es excluir los outputs visuales:

# Excluye todos los outputs (gráficos y resultados de texto), dejando solo código y markdown
jupyter nbconvert --to markdown --TemplateExporter.exclude_output=True tu_notebook.ipynb

# Opción intermedia: Excluir solo inputs (código) pero mantener outputs (imágenes)
# jupyter nbconvert --to markdown --TemplateExporter.exclude_input=True tu_notebook.ipynb  

Nota técnica: Si necesitas un .md con código y texto, pero sin las imágenes incrustadas ni la carpeta _files, la solución más limpia es usar un script de post-procesamiento o una plantilla personalizada, ya que nbconvert tiende a guardar cualquier output gráfico como archivo externo. Sin embargo, para la mayoría de casos, excluir el output (--TemplateExporter.exclude_output=True) es el método estándar para eliminar los assets visuales.

3. Mover a otra carpeta (Tu caso de uso)
Puedes especificar el directorio de salida para los archivos y la carpeta de assets con --output-dir y --FilesExporter.output_files_dir.

# Exporta el .md y la carpeta de assets dentro de la carpeta 'docs'
jupyter nbconvert --to markdown tu_notebook.ipynb --output-dir ./docs  

🖱️ Opción B: Extensiones en VSCodium (Uso Manual)
Si prefieres hacerlo con clics dentro del editor, instala una de estas extensiones desde el Marketplace (funcionan igual en VSCodium):

"Jupyter To Markdown" (Recomendada):
Instalación: Busca Leytton.jupyter-to-markdown en extensiones.
Uso: Click derecho sobre el archivo .ipynb en el explorador → "Convert To Markdown".
Comportamiento: Ejecuta nbconvert internamente. Generará el .md y la carpeta _files en el mismo directorio.
Limitación: No suele permitir configurar fácilmente "sin assets" desde la UI; para eso es mejor la terminal. 
"Project To Markdown":
Útil si quieres unir todo tu proyecto (varios archivos) en un solo .md, pero menos específica para notebooks individuales con gestión de assets. 
📋 Resumen para tu Repositorio (Cheatsheet)
Objetivo	Comando / Acción	Resultado de Assets
Estándar	jupyter nbconvert --to markdown nota.ipynb	✅ Crea carpeta nota_files/ con imágenes. 
Solo Texto/Código	jupyter nbconvert --to markdown --TemplateExporter.exclude_output=True nota.ipynb	❌ Sin imágenes ni carpeta extra. 
Mover de carpeta	jupyter nbconvert --to markdown nota.ipynb --output-dir ./docs	✅ Crea docs/nota.md y docs/nota_files/. 
VSCodium (Click)	Ext: Jupyter To Markdown → Click Derecho	✅ Igual que el estándar (crea carpeta). 

Flujo de trabajo sugerido para tu caso:
Ejecuta el comando en la terminal integrada de VSCodium (Ctrl + ñ o Ctrl + `).
Usa el comando estándar para tener el backup completo con gráficos.
Si necesitas una versión ligera para leer en GitHub sin descargar imágenes, usa el flag --TemplateExporter.exclude_output=True.


fuentes:

[text](https://stackoverflow.com/questions/37423380/ignore-markdown-cells-in-jupyter-nbconvert-with-to-script)

[text](https://discourse.jupyter.org/t/how-to-avoid-image-embedding-when-nbconverting-to-md/23441)