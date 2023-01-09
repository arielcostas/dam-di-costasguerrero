from PyQt6 import QtSql


class ServicioPropietarios:
	def cambiar_propietario(self, id_vehiculo: str, id_propietario: str) -> bool:
		try:
			query = QtSql.QSqlQuery()
			query.prepare("UPDATE coches SET dnicli = :id_propietario WHERE matricula = :id_vehiculo")
			query.bindValue(':id_propietario', id_propietario)
			query.bindValue(':id_vehiculo', id_vehiculo)

			return query.exec()
		except Exception as error:
			print(f"Error cambiando propietario: {error}")
			return False