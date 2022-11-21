from PyQt6 import QtWidgets, QtSql

from controladores import modal
from modelos import Vehiculo, Cliente


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

	def cargar_vehiculos(self) -> list[Vehiculo]:
		try:
			query = QtSql.QSqlQuery()
			query.prepare("SELECT dnicli, matricula, marca, modelo, motor FROM coches")
			if query.exec():
				resultados: list[Vehiculo] = list()

				while query.next():
					resultados.append(Vehiculo(query.value(1), query.value(0), query.value(2), query.value(3), query.value(4)))
				return resultados
		except Exception as error:
			print(f"Error recuperando vehiculos: {error}")

	def guardar_cliente(self, cliente: Cliente) -> bool:
		try:
			query = QtSql.QSqlQuery()
			query.prepare(
				"INSERT OR REPLACE INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
			)
			query.addBindValue(cliente.dni)
			query.addBindValue(cliente.nombre)
			query.addBindValue(cliente.alta)
			query.addBindValue(cliente.direccion)
			query.addBindValue(cliente.provincia)
			query.addBindValue(cliente.municipio)
			query.addBindValue(int(cliente.efectivo))
			query.addBindValue(int(cliente.factura))
			query.addBindValue(int(cliente.transferencia))
			print(query.lastError().text())
			return query.exec()
		except Exception as error:
			print(f"Error guardando cliente: {error}")

	def guardar_vehiculo(self, vehiculo: Vehiculo) -> bool:
		try:
			query = QtSql.QSqlQuery()
			query.prepare("INSERT INTO coches VALUES (?,?,?,?,?)")
			query.addBindValue(vehiculo.matricula)
			query.addBindValue(vehiculo.dni)
			query.addBindValue(vehiculo.marca)
			query.addBindValue(vehiculo.modelo)
			query.addBindValue(vehiculo.motor)

			return query.exec()
		except Exception as error:
			print(f"Error guardando vehiculo: {error}")

	def cargar_vehiculo(self, matricula: str) -> Vehiculo:
		try:
			query = QtSql.QSqlQuery()
			query.prepare("SELECT dnicli, matricula, marca, modelo, motor FROM coches WHERE matricula = :mat")
			query.bindValue(':mat', matricula)
			if query.exec():
				while query.next():
					return Vehiculo(query.value(0), query.value(1), query.value(2), query.value(3), query.value(4))
		except Exception as error:
			print(f"Error recuperando vehiculo: {error}")

	def cargar_cliente(self, dni: str) -> Cliente:
		try:
			query = QtSql.QSqlQuery()
			query.prepare("SELECT * FROM clientes WHERE dni = :dni")
			query.bindValue(':dni', dni)
			if query.exec():
				while query.next():
					return Cliente(query.value(1), query.value(0), query.value(2), query.value(3), query.value(4), query.value(5), query.value(6), query.value(7), query.value(8))
		except Exception as error:
			print(f"Error recuperando cliente: {error}")