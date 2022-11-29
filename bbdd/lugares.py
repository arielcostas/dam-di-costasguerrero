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
