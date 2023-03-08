import os
import shutil
import sys

from PyQt6 import QtSql
from controladores import modales

from controladores.modales import aviso


def abrir():
	"""
	Abre la conexión de QtSql con SQLite

	:return: True si se pudo abrir la conexión, False en caso contrario
	"""
	if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
		dbfile = "C:\\Program Files (x86)\\TalleresTeis\\bbdd.sqlite"
		if not os.path.exists(dbfile):
			# Copia el archivo de la carpeta de instalación
			# a la carpeta de la aplicación
			shutil.copyfile(os.path.join(sys._MEIPASS, 'bbdd.sqlite'), dbfile)
	else:
		dbfile = os.path.join(os.path.dirname(__file__), '..', 'bbdd.sqlite')

	dbfile = os.path.abspath(dbfile)

	modales.info("Base de datos", "Se abrirá la base de datos: " + dbfile)

	db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
	db.setDatabaseName(dbfile)
	if not db.open():
		aviso.error("Error abriendo base de datos", "No se pudo abrir la base de datos")
		return False
	else:
		print("Conexión establecida")
		return True
