from datetime import datetime

from PyQt6 import QtSql

from bbdd.modelos import Servicio


class ServicioRepository:
	@staticmethod
	def get_all(historico: bool) -> list[Servicio]:
		"""
		Obtiene todos los servicios de la base de datos y los devuelve

		:param historico: Si es True, incluye los servicios eliminados
		:return: un listado de servicios
		"""
		try:
			query = QtSql.QSqlQuery()
			if historico:
				query.prepare("SELECT * FROM servicios")
			else:
				query.prepare("SELECT * FROM servicios WHERE fechaBaja IS NULL")

			if query.exec():
				servicios: list[Servicio] = []
				while query.next():
					servicio = Servicio(query.value(0), query.value(1), query.value(2),
										query.value(3), query.value(4), query.value(5),
										query.value(6), True if query.value(7) == 1 else False)
					servicios.append(servicio)
				return servicios
			else:
				raise Exception(query.lastError().text())
		except Exception as error:
			print(f"Error recuperando servicios: {error}")

	@staticmethod
	def get_by_id(sid: str) -> Servicio:
		"""
		Obtiene el servicio cuyo ID coincida

		:param sid: El ID del servicio
		:return: El servicio que coincida con el ID
		"""
		query = QtSql.QSqlQuery()
		query.prepare("SELECT * FROM servicios WHERE id = ? LIMIT 1")
		query.addBindValue(sid)

		if query.exec():
			query.next()
			return Servicio(
				query.value(0),
				query.value(1),
				query.value(2),
				query.value(3),
				query.value(4),
				query.value(5),
				query.value(6),
				True if query.value(7) == 1 else False
			)

	@staticmethod
	def nuevo_servicio(nombre: str, precio_unitario: float, stock: int, almacenable: bool) -> bool:
		"""
		Crea un nuevo servicio en la base de datos

		:param nombre: El nombre del servicio
		:param precio_unitario: El precio unitario del servicio
		:return: True si se ha creado correctamente, False en caso contrario
		"""
		try:
			query = QtSql.QSqlQuery()
			query.prepare(
				"INSERT INTO servicios(nombre, precioUnitario, fechaAlta, fechaModificacion, stock, almacenable) VALUES (?,?,?,?,?,?)")

			query.addBindValue(nombre)
			query.addBindValue(precio_unitario)
			query.addBindValue(datetime.now().strftime("%Y-%m-%d"))
			query.addBindValue(datetime.now().strftime("%Y-%m-%d"))
			query.addBindValue(stock if almacenable else 0)
			query.addBindValue(1 if almacenable else 0)

			return query.exec()
		except Exception as error:
			print(f"Error creando servicio: {error}")

	@staticmethod
	def modificar_servicio(sid, nombre, precio_unitario, stock) -> bool:
		"""
		Modifica un servicio en la base de datos

		:param sid: El ID del servicio
		:param nombre: El nuevo nombre del servicio
		:param precio_unitario:  El nuevo precio unitario del servicio
		:return: True si se ha modificado correctamente, False en caso contrario
		"""
		try:
			query = QtSql.QSqlQuery()
			query.prepare(
				"UPDATE servicios SET nombre=?, precioUnitario=?, fechaModificacion=?, stock=? WHERE id=?")

			query.addBindValue(nombre)
			query.addBindValue(precio_unitario)
			query.addBindValue(datetime.now().strftime("%Y-%m-%d"))
			query.addBindValue(stock)
			query.addBindValue(sid)

			return query.exec()
		except Exception as error:
			print(f"Error modificando servicio: {error}")

	@staticmethod
	def eliminar_servicio(sid: str) -> bool:
		"""
		Elimina un servicio de la base de datos

		:param sid: El ID del servicio
		:return:  True si se ha eliminado correctamente, False en caso contrario
		"""
		try:
			query = QtSql.QSqlQuery()
			query.prepare("UPDATE servicios SET fechaModificacion=?, fechaBaja=? WHERE id=?")

			query.addBindValue(datetime.now().strftime("%Y-%m-%d"))
			query.addBindValue(datetime.now().strftime("%Y-%m-%d"))
			query.addBindValue(sid)

			return query.exec()
		except Exception as error:
			print(f"Error eliminando servicio: {error}")

	@staticmethod
	def buscar(term):
		"""
		Busca servicios por nombre

		:param term: El término a buscar
		:return: Una lista de servicios que coincidan con el término
		"""
		try:
			query = QtSql.QSqlQuery()
			query.prepare("SELECT * FROM servicios WHERE fechaBaja IS NULL AND nombre LIKE ?")
			query.addBindValue(f"%{term}%")

			if query.exec():
				servicios: list[Servicio] = []
				while query.next():
					servicios.append(Servicio(
						query.value(0),
						query.value(1),
						query.value(2),
						query.value(3),
						query.value(4),
						query.value(5),
						query.value(6),
						True if query.value(7) == 1 else False
					))
				return servicios
			else:
				raise Exception(query.lastError().text())
		except Exception as error:
			print(f"Error recuperando servicios: {error}")
