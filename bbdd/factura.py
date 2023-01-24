from PyQt6 import QtSql

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
