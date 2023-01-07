from datetime import datetime

from PyQt6 import QtSql

from bbdd.modelos import Servicio


class ServicioRepository:
	@staticmethod
	def get_all(historico: bool)-> list[Servicio]:
		try:
			query = QtSql.QSqlQuery()
			if historico:
				query.prepare("SELECT * FROM servicios")
			else:
				query.prepare("SELECT * FROM servicios WHERE fechaBaja IS NULL")
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
					))
				return servicios
			else:
				raise Exception(query.lastError().text())
		except Exception as error:
			print(f"Error recuperando servicios: {error}")

	@staticmethod
	def get_by_id(sid: str) -> Servicio:
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
			)

	@staticmethod
	def nuevo_servicio(nombre: str, precio_unitario: float) -> bool:
		try:
			query = QtSql.QSqlQuery()
			query.prepare("INSERT INTO servicios(nombre, precioUnitario, fechaAlta, fechaModificacion) VALUES (?,?,?,?)")

			query.addBindValue(nombre)
			query.addBindValue(precio_unitario)
			query.addBindValue(datetime.now().strftime("%Y-%m-%d"))
			query.addBindValue(datetime.now().strftime("%Y-%m-%d"))

			return query.exec()
		except Exception as error:
			print(f"Error creando servicio: {error}")

	@staticmethod
	def modificar_servicio(sid, nombre, precio_unitario) -> bool:
		try:
			query = QtSql.QSqlQuery()
			query.prepare("UPDATE servicios SET nombre=?, precioUnitario=?, fechaModificacion=? WHERE id=?")

			query.addBindValue(nombre)
			query.addBindValue(precio_unitario)
			query.addBindValue(datetime.now().strftime("%Y-%m-%d"))
			query.addBindValue(sid)

			return query.exec()
		except Exception as error:
			print(f"Error modificando servicio: {error}")

	@staticmethod
	def eliminar_servicio(sid: str) -> bool:
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
					))
				return servicios
			else:
				raise Exception(query.lastError().text())
		except Exception as error:
			print(f"Error recuperando servicios: {error}")
