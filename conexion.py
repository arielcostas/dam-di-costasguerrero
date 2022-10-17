from PyQt6 import QtWidgets, QtSql


class Conexion():
	def iniciarConexion(self):
		dbfile = 'bbdd.sqlite'
		db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
		db.setDatabaseName(dbfile)
		if not db.open():
			QtWidgets.QMessageBox.critical(None, "No se puede abrir la base de datos", "Conexión no establecida",
										   QtWidgets.QMessageBox.StandardButton.Cancel)
			return False
		else:
			print("Conexión establecida")

	def cargar_provincias(self):
		try:
			query = QtSql.QSqlQuery()
			query.prepare("SELECT provincia FROM provincias")
			if query.exec():
				resultados = [""]
				while query.next():
					resultados.append(query.value(0))
				return resultados
			else:
				return ["else!"]


		except Exception as error:
			print(f"Error recuperando provincias: {error}")

	def cargar_municipios(self, provincia):
		try:
			query = QtSql.QSqlQuery()
			query.prepare("SELECT municipio FROM municipios LEFT JOIN provincias p on p.id = municipios.provincia_id WHERE p.provincia = :prov")
			query.bindValue(':prov', provincia)
			if query.exec():
				resultados = [""]
				while query.next():
					resultados.append(query.value(0))
				return resultados


		except Exception as error:
			print(f"Error recuperando municipios de {provincia}: {error}")

	def guardarCliente(self):
		pass