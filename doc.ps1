# Genera la documentación con Sphinx
# Si al ejecutarlo da un problema de ExecutionPolicy, ejecutar:
# Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
# o copiar el contenido del script y pegarlo en la consola

New-Item -ItemType Directory -Name docs -ErrorAction SilentlyContinue > $null

sphinx-apidoc.exe -o docs . > $null
sphinx-build.exe -b html -d _build/doctrees . docs/html

Remove-Item -Path _build -Recurse -Force
