"""
Script para limpiar y compilar el proyecto
"""

import os, shutil
from PyQt6 import uic


def limpiar_pycache():
	"""
	Elimina recursivamente los directorios __pycache__
	"""
	for root, dirs, files in os.walk("."):
		for dir in dirs:
			if dir == "__pycache__":
				print("limpiar_pycache: Eliminando", os.path.join(root, dir))
				shutil.rmtree(os.path.join(root, dir))


def limpiar_ui():
	"""
	Elimina los archivos compilados de los archivos .ui en el directorio `ui`
	"""
	for root, dirs, files in os.walk("ui"):
		for file in files:
			if file.endswith(".py"):
				print("limpiar_ui: Eliminando", os.path.join(root, file))
				os.remove(os.path.join(root, file))


def compilar_ui():
	"""
	Compila los archivos .ui en el directorio `ui` con PyQt6.uic.pyuic
	"""
	for root, dirs, files in os.walk("ui"):
		for file in files:
			if file.endswith(".ui"):
				print("compilar_ui: Compilando", os.path.join(root, file))
				uic.compileUi(
					os.path.join(root, file),
					open(os.path.join(root, file[:-3] + ".py"), "w", encoding="utf-8"),
				)


if __name__ == "__main__":
	limpiar_pycache()
	limpiar_ui()
	compilar_ui()
