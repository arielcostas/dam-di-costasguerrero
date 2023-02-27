from datetime import datetime

from PyQt6 import QtSql

from bbdd.modelos import Vehiculo


class VehiculoRepository:
	@staticmethod
	def get_all(historico: bool = False)-> list[Vehiculo]:
		"""
		Recupera todos los vehiculos de la base de datos

		:param historico: Si es True, recupera todos los vehiculos, si es False, solo los activos

		:return: Una lista con todos los vehiculos
		"""
		try:
			query = QtSql.QSqlQuery()
			if historico:
				query.prepare("SELECT * FROM coches")
			else:
				query.prepare("SELECT * FROM coches WHERE coches.fecha_baja IS NULL")
			if query.exec():
				vehiculos: list[Vehiculo] = []
				while query.next():
					vehiculos.append(Vehiculo(
						query.value(0),
						query.value(1),
						query.value(2),
						query.value(3),
						query.value(4),
						query.value(5),
					))
				return vehiculos
			else:
				raise Exception(query.lastError().text())
		except Exception as error:
			print(f"Error recuperando vehiculos: {error}")


	@staticmethod
	def get_by_dni(dni: str)-> list[Vehiculo]:
		"""
		Recupera todos los vehiculos de la base de datos

		:param historico: Si es True, recupera todos los vehiculos, si es False, solo los activos

		:return: Una lista con todos los vehiculos
		"""
		try:
			query = QtSql.QSqlQuery()
			query.prepare("SELECT * FROM coches WHERE coches.dnicli = :dni")
			query.bindValue(':dni', dni)

			if query.exec():
				vehiculos: list[Vehiculo] = []
				while query.next():
					vehiculos.append(Vehiculo(
						query.value(0),
						query.value(1),
						query.value(2),
						query.value(3),
						query.value(4),
						query.value(5),
					))
				return vehiculos
			else:
				raise Exception(query.lastError().text())
		except Exception as error:
			print(f"Error recuperando vehiculos: {error}")

	@staticmethod
	def get_by_id(matricula: str) -> Vehiculo:
		"""
		Recupera un vehiculo de la base de datos

		:param matricula: La matricula del vehiculo a recuperar

		:return: El vehiculo recuperado o None si no se ha encontrado
		"""
		query = QtSql.QSqlQuery()
		query.prepare("SELECT * FROM coches WHERE matricula = ? LIMIT 1")
		query.addBindValue(matricula)

		if query.exec():
			query.next()
			return Vehiculo(
				query.value(0),
				query.value(1),
				query.value(2),
				query.value(3),
				query.value(4),
				query.value(5),
			)
		else:
			return None

	@staticmethod
	def insert(vehiculo: Vehiculo) -> bool:
		"""
		Inserta un vehiculo en la base de datos

		:param vehiculo: El vehiculo a insertar

		:return: True si se ha insertado correctamente, False si ha habido un error
		"""
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

	@staticmethod
	def delete(matricula: str) -> bool:
		"""
		Elimina un vehiculo de la base de datos

		:param matricula: La matricula del vehiculo a eliminar

		:return: True si se ha eliminado correctamente, False si ha habido un error
		"""
		try:
			query = QtSql.QSqlQuery()
			query.prepare("UPDATE coches SET fecha_baja = CURRENT_TIMESTAMP WHERE matricula = ?")
			query.addBindValue(matricula)

			return query.exec()
		except Exception as error:
			print(f"Error eliminando vehiculo: {error}")

	@staticmethod
	def delete_by_dni(dni: str) -> bool:
		"""
		Elimina todos los vehiculos de un cliente

		:param dni: DNI del cliente

		:return: True si se ha eliminado correctamente, False si ha habido un error
		"""
		try:
			query = QtSql.QSqlQuery()
			query.prepare("UPDATE coches SET fecha_baja=:fecha_baja WHERE dnicli = :dni")
			query.bindValue(':fecha_baja', datetime.now().strftime("%Y-%m-%d"))
			query.bindValue(':dni', dni)

			return query.exec()
		except Exception as error:
			print(f"Error eliminando vehiculos: {error}")