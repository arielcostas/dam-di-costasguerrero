from PyQt6 import QtSql

from bbdd import Servicio
from bbdd.modelos.factura import Factura


class FacturaRepository:
	@staticmethod
	def get_all() -> list[Factura]:
		'''
		Obtiene todas las facturas de la base de datos y las devuelve
		:return: un listado de facturas
		'''
		query = QtSql.QSqlQuery()
		query.prepare('SELECT * FROM facturas')
		query.exec()
		facturas = []
		while query.next():
			cliente = Factura(
				query.value(0),
				query.value(1),
				query.value(2),
				query.value(3),
				query.value(4)
			)

			facturas.append(cliente)
		return facturas

	@staticmethod
	def get_by_id(factura_id: int) -> Factura:
		query = QtSql.QSqlQuery()
		query.prepare('SELECT * FROM facturas WHERE id=? LIMIT 1')
		query.addBindValue(factura_id)

		if query.exec():
			query.next()
			return Factura(
				query.value(0),
				query.value(1),
				query.value(2),
				query.value(3),
				query.value(4)
			)

	@staticmethod
	def get_cantidad_producto_factura(factura: int, servicio_id: int) -> int:
		'''
		Obtiene cuántos productos de un tipo hay en una factura
		:param factura: factura de la que obtener
		:param servicio_id: id del producto
		:return: cantidad
		'''
		query = QtSql.QSqlQuery()
		query.prepare(
			"SELECT cantidad FROM facturas_servicios WHERE factura_id=? AND "
			"servicio_id=?"
		)
		query.addBindValue(factura)
		query.addBindValue(servicio_id)
		if query.exec():
			query.next()
			return query.value(0)
		else:
			return 0

	@staticmethod
	def guardar_factura(factura: Factura, servicios: list[(int, int)]):
		try:
			query = QtSql.QSqlQuery()
			query.prepare(
				"INSERT OR REPLACE INTO facturas (nif, matricula, fecha, emitida) VALUES (?, ?, ?, ?)"
			)

			query.addBindValue(factura.nif)
			query.addBindValue(factura.matricula)
			query.addBindValue(factura.fecha)
			query.addBindValue(factura.emitida)

			if not query.exec():
				print(query.lastError().text())
				return False

			query2 = QtSql.QSqlQuery()
			query2.prepare(
				"INSERT OR REPLACE INTO facturas_servicios (factura_id, servicio_id, cantidad) VALUES (?, ?, ?)"
			)

			id_factura = query.lastInsertId()
			for servicio, cantidad in servicios:

				query2.addBindValue(id_factura)
				query2.addBindValue(int(servicio))
				query2.addBindValue(int(cantidad))
				if not query2.exec():
					print(query2.lastError().text())
					return False
		except Exception as e:
			print(e)
			return False