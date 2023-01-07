from datetime import datetime

from PyQt6 import QtSql

from bbdd.modelos import Cliente


class ClienteRepository:
	@staticmethod
	def get_all(incluir_eliminados: bool = False) -> list[Cliente]:
		'''
		Obtiene todos los clientes de la base de datos y los devuelve
		:param incluir_eliminados: Si es True, incluye los clientes eliminados
		:return: un listado de clientes
		'''
		query = QtSql.QSqlQuery()
		if incluir_eliminados:
			query.prepare('SELECT * FROM clientes')
		else:
			query.prepare('SELECT * FROM clientes WHERE fecha_baja IS NULL ORDER BY dni')
		query.exec()
		clientes = []
		while query.next():
			cliente = Cliente(
				query.value(0),
				query.value(1),
				query.value(2),
				query.value(3),
				query.value(4),
				query.value(5),
				query.value(6),
				query.value(7),
				query.value(8),
			)

			clientes.append(cliente)
		return clientes

	@staticmethod
	def get_by_dni(dni: str) -> Cliente | None:
		'''
		Obtiene el cliente cuyo DNI coincida
		:return: el cliente que coincida con el DNI
		'''
		query = QtSql.QSqlQuery()
		query.prepare('SELECT * FROM clientes WHERE dni = :id_cliente')
		query.bindValue(':id_cliente', dni)
		query.exec()
		if not query.next():
			return None

		return Cliente(
			query.value(0),
			query.value(1),
			query.value(2),
			query.value(3),
			query.value(4),
			query.value(5),
			query.value(6),
			query.value(7),
			query.value(8),
		)

	@staticmethod
	def delete_by_dni(dni: str) -> bool:
		'''
		Elimina el cliente cuyo DNI coincida
		:return: True si se ha eliminado correctamente, False si no
		'''
		query = QtSql.QSqlQuery()
		query.prepare("UPDATE clientes SET fecha_baja=:fecha_baja WHERE dni = :dni")
		query.bindValue(':fecha_baja', datetime.now().strftime("%Y-%m-%d"))
		query.bindValue(':dni', dni)
		return query.exec()

	@staticmethod
	def insert(cliente: Cliente) -> bool:
		try:
			query = QtSql.QSqlQuery()
			query.prepare(
				"INSERT OR REPLACE INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)"
			)
			query.addBindValue(cliente.dni)
			query.addBindValue(cliente.nombre)
			query.addBindValue(cliente.fecha_alta)
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
