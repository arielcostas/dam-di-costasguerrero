from datetime import datetime
from typing import List

from PyQt6 import QtSql

from modelos import Vehiculo
from modelos.servicio import Servicio


class VehiculoRepository:
	@staticmethod
	def get_all(historico: bool)-> list[Vehiculo]:
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
	def get_by_id(sid: str) -> Vehiculo:
		query = QtSql.QSqlQuery()
		query.prepare("SELECT * FROM servicios WHERE id = ? LIMIT 1")
		query.addBindValue(sid)

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

