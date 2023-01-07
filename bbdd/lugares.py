from PyQt6 import QtSql


class LugaresRepository:
	@staticmethod
	def get_provincias() -> list[str]:
		query = QtSql.QSqlQuery()
		query.prepare("SELECT provincia FROM provincias")
		if query.exec():
			resultados = [""]
			while query.next():
				resultados.append(query.value(0))
			return resultados
		else:
			return [""]

	@staticmethod
	def get_municipios(provincia: str) -> list[str]:
		"""
		Recupera los municipios de una provincia dado su nombre
		:param provincia: El nombre de la provincia a buscar
		:return: Una lista con los nombres de los municipios
		"""
		query = QtSql.QSqlQuery()
		query.prepare(
			"SELECT municipio FROM municipios LEFT JOIN provincias p on p.id = "
			"municipios.provincia_id WHERE p.provincia = ?"
		)

		query.addBindValue(provincia)
		if query.exec():
			resultados = [""]
			while query.next():
				resultados.append(query.value(0))
			return resultados
		else:
			return [""]
