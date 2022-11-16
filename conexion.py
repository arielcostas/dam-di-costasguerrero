from PyQt6 import QtWidgets, QtSql

from controladores import modal


class Conexion:
	def iniciar_conexion(self):
		dbfile = 'bbdd.sqlite'
		db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
		db.setDatabaseName(dbfile)
		if not db.open():
			modal.error("Error abriendo base de datos", "No se pudo abrir la base de datos")
			return False
		else:
			print("Conexión establecida")
			return True

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
			query.prepare(
				"SELECT municipio FROM municipios LEFT JOIN provincias p on p.id = municipios.provincia_id WHERE p.provincia = :prov")
			query.bindValue(':prov', provincia)
			if query.exec():
				resultados = [""]
				while query.next():
					resultados.append(query.value(0))
				return resultados


		except Exception as error:
			print(f"Error recuperando municipios de {provincia}: {error}")

	def cargar_vehiculos(self):
		try:
			query = QtSql.QSqlQuery()
			query.prepare("SELECT dnicli, matricula, marca, modelo, motor FROM coches")
			if query.exec():
				resultados = []
				while query.next():
					resultados.append([query.value(0), query.value(1), query.value(2), query.value(3), query.value(4)])
				return resultados
		except Exception as error:
			print(f"Error recuperando vehiculos: {error}")

	def guardar_cliente(self, cliente):
		try:
			query = QtSql.QSqlQuery()
			query.prepare(
				"INSERT OR REPLACE INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
			)
			query.addBindValue(cliente.get("dni"))
			query.addBindValue(cliente.get("nombre"))
			query.addBindValue(cliente.get("alta"))
			query.addBindValue(cliente.get("direccion"))
			query.addBindValue(cliente.get("provincia"))
			query.addBindValue(cliente.get("municipio"))
			query.addBindValue(int(cliente.get("efectivo")))
			query.addBindValue(int(cliente.get("factura")))
			query.addBindValue(int(cliente.get("transferencia")))
			print(query.lastError().text())
			return query.exec()
		except Exception as error:
			print(f"Error guardando cliente: {error}")

	def guardar_vehiculo(self, vehiculo):
		try:
			query = QtSql.QSqlQuery()
			query.prepare("INSERT INTO coches VALUES (?,?,?,?,?)")
			query.addBindValue(vehiculo.get("matricula"))
			query.addBindValue(vehiculo.get("cliente"))
			query.addBindValue(vehiculo.get("marca"))
			query.addBindValue(vehiculo.get("modelo"))
			query.addBindValue(vehiculo.get("motor"))

			return query.exec()
		except Exception as error:
			print(f"Error guardando vehiculo: {error}")
