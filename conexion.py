from datetime import datetime

from PyQt6 import QtSql

from bbdd import ClienteRepository
from controladores.modales import aviso
from modelos import Vehiculo, Cliente


class Conexion:
	def iniciar_conexion(self):
		dbfile = 'bbdd.sqlite'
		db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
		db.setDatabaseName(dbfile)
		if not db.open():
			aviso.error("Error abriendo base de datos", "No se pudo abrir la base de datos")
			return False
		else:
			print("Conexión establecida")
			return True

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

	def cargar_vehiculos(self, historico: bool = False) -> list[Vehiculo]:
		try:
			query = QtSql.QSqlQuery()
			if historico:
				query.prepare("SELECT dnicli, matricula, marca, modelo, motor, fecha_baja FROM coches")
			else:
				query.prepare("SELECT dnicli, matricula, marca, modelo, motor, fecha_baja FROM coches WHERE fecha_baja IS NULL")
			if query.exec():
				resultados: list[Vehiculo] = list()

				while query.next():
					resultados.append(Vehiculo(query.value(1), query.value(0), query.value(2), query.value(3), query.value(4), query.value(5)))
				return resultados
		except Exception as error:
			print(f"Error recuperando vehiculos: {error}")

	def guardar_cliente(self, cliente: Cliente) -> bool:
		try:
			query = QtSql.QSqlQuery()
			query.prepare(
				"INSERT OR REPLACE INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)"
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
			query.prepare("INSERT OR REPLACE INTO coches VALUES (?,?,?,?,?, NULL)")
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
			query.prepare("SELECT matricula, dnicli, marca, modelo, motor FROM coches WHERE matricula = :mat AND fecha_baja IS NULL")
			query.bindValue(':mat', matricula)
			if query.exec():
				while query.next():
					return Vehiculo(query.value(0), query.value(1), query.value(2), query.value(3), query.value(4))
		except Exception as error:
			print(f"Error recuperando vehiculo: {error}")

	@staticmethod
	def eliminar_cliente_coches(dni: str) -> bool:
		"""
		Elimina todos los coches de un cliente, y luego el propio cliente
		:param dni: El DNI del cliente a eliminar
		:return: True si se ha eliminado correctamente, False si ha habido algún error
		"""
		try:
			query1 = QtSql.QSqlQuery()
			query1.prepare("UPDATE coches SET fecha_baja=:fecha_baja WHERE dnicli = :dni")
			query1.bindValue(':fecha_baja', datetime.now().strftime("%Y-%m-%d"))
			query1.bindValue(':dni', dni)
			q1e = query1.exec()

			q2e = ClienteRepository.delete_by_dni(dni)

			return q1e and q2e
		except Exception as error:
			print(f"Error eliminando cliente: {error}")

	@staticmethod
	def eliminar_vehiculo(matricula: str) -> bool:
		"""
		Elimina un vehículo de un cliente
		:param matricula: La matrícula del vehículo a eliminar
		:return: True si se ha eliminado correctamente, False si ha habido algún error
		"""
		try:
			query = QtSql.QSqlQuery()
			query.prepare("UPDATE coches SET fecha_baja=:fecha_baja WHERE matricula = :mat")
			query.bindValue(':fecha_baja', datetime.now().strftime("%Y-%m-%d"))
			query.bindValue(':mat', matricula)
			return query.exec()
		except Exception as error:
			print(f"Error eliminando vehiculo: {error}")

	def cargar_vehiculos_incluye_eliminados(self):
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
