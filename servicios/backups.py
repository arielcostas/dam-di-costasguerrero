import zipfile
import xlwt
from PyQt6 import QtSql


class ServicioBackup:
	def restaurar_copia(self, ruta: str) -> bool:
		zipf = zipfile.ZipFile(ruta, 'r')
		zipf.extractall()
		zipf.close()
		return True

	def hacer_copia(self, ruta: str) -> bool:
		zipf = zipfile.ZipFile(ruta, 'w', zipfile.ZIP_DEFLATED)
		zipf.write("bbdd.sqlite")
		zipf.close()
		return True

	def exportar_excel(self, ruta: str) -> bool:
		try:
			wb = xlwt.Workbook()
			hoja_clientes = wb.add_sheet("Clientes")
			hoja_clientes.write(0, 0, "DNI")
			hoja_clientes.write(0, 1, "Nombre")
			hoja_clientes.write(0, 2, "Fecha alta")
			hoja_clientes.write(0, 3, "Direccion")
			hoja_clientes.write(0, 4, "Provincia")
			hoja_clientes.write(0, 5, "Municipio")
			hoja_clientes.write(0, 6, "Formas de pago")

			query = QtSql.QSqlQuery()
			query.prepare("SELECT * FROM clientes ORDER BY alta")
			if query.exec():
				fila = 1
				while query.next():
					hoja_clientes.write(fila, 0, query.value(0))
					hoja_clientes.write(fila, 1, query.value(1))
					hoja_clientes.write(fila, 2, query.value(2))
					hoja_clientes.write(fila, 3, query.value(3))
					hoja_clientes.write(fila, 4, query.value(4))
					hoja_clientes.write(fila, 5, query.value(5))

					metodosPago = []
					if query.value(6) == 1:
						metodosPago.append("Efectivo")
					if query.value(7) == 1:
						metodosPago.append("Factura")
					if query.value(8) == 1:
						metodosPago.append("Transferencia")
					hoja_clientes.write(fila, 6, ", ".join(metodosPago))
					fila += 1

			wb.save(ruta)
			return True
		except Exception as error:
			print("Error al exportar a excel: ", error)
			return False
