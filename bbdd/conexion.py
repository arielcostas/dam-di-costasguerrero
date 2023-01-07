from PyQt6 import QtSql

from controladores.modales import aviso


def abrir():
	dbfile = 'bbdd.sqlite'
	db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
	db.setDatabaseName(dbfile)
	if not db.open():
		aviso.error("Error abriendo base de datos", "No se pudo abrir la base de datos")
		return False
	else:
		print("Conexión establecida")
		return True
