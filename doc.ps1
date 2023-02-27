# genera la documentación con Sphinx
# Si el parámetro 0 es "api" genera la documentación de la API


New-Item -ItemType Directory -Name docs -ErrorAction SilentlyContinue > $null

sphinx-apidoc.exe -o docs . > $null
sphinx-build.exe -b html -d _build/doctrees . docs/html

Remove-Item -Path _build -Recurse -Force
