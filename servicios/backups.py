import zipfile

import xlrd
import xlwt
from PyQt6 import QtSql
from xlrd.sheet import Sheet
from xlwt import Workbook

from modelos import Vehiculo, Cliente


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

	def exportar_excel(self, ruta: str, clientes: bool, coches: bool) -> bool:
		try:
			wb = Workbook()
			if clientes:
				self.exportar_clientes_excel(wb)
			if coches:
				self.exportar_coches_excel(wb)
			wb.save(ruta)
		except Exception as error:
			print("Error al exportar a excel: ", error)
			return False

	def exportar_clientes_excel(self, wb: Workbook) -> bool:
		try:
			hoja_clientes = wb.add_sheet("clientes")
			elementos = ["DNI", "Nombre", "Fecha alta", "Direccion", "Provincia", "Municipio",
						 "Admite efectivo", "Admite factura", "Admite transferencia"]
			for i, e in enumerate(elementos):
				hoja_clientes.write(0, i, e)

			query = QtSql.QSqlQuery()
			query.prepare("SELECT * FROM clientes ORDER BY alta")
			if query.exec():
				fila = 1
				while query.next():
					for i in range(0, 9):
						hoja_clientes.write(fila, i, query.value(i))
					fila += 1

			return True
		except Exception as error:
			print("Error al exportar a excel: ", error)
			return False

	def exportar_coches_excel(self, wb: Workbook) -> bool:
		try:
			hoja_coches = wb.add_sheet("coches")
			hoja_coches.write(0, 0, "Matricula")
			hoja_coches.write(0, 1, "DNI cliente")
			hoja_coches.write(0, 2, "Marca")
			hoja_coches.write(0, 3, "Modelo")
			hoja_coches.write(0, 4, "Tipo motor")

			query = QtSql.QSqlQuery()
			query.prepare("SELECT * FROM coches ORDER BY matricula")
			if query.exec():
				fila = 1
				while query.next():
					hoja_coches.write(fila, 0, query.value(0))
					hoja_coches.write(fila, 1, query.value(1))
					hoja_coches.write(fila, 2, query.value(2))
					hoja_coches.write(fila, 3, query.value(3))
					hoja_coches.write(fila, 4, query.value(4))
					fila += 1
			return True
		except Exception as error:
			print("Error al exportar a excel: ", error)
			return False

	def comprobar_tipos_importables_excel(self, ruta) -> [bool, bool]:
		try:
			book = xlrd.open_workbook(ruta)
			hojas = book.sheets()

			# resultado = NoClientes y NoCoches
			resultado = (False, False)

			for hoja in hojas:
				if hoja.name == "clientes":
					# resultado = SiClientes y LoqueseaCoches
					resultado = (True, resultado[1])
				if hoja.name == "coches":
					# resultado = LoqueseaClientes y SiCoches
					resultado = (resultado[0], True)
			return resultado
		except Exception as error:
			print("Error al comprobar tipos importables: ", error)
			return False, False

	def importar_excel(self, ruta: str, clientes: bool, coches: bool) -> bool:
		try:
			book = xlrd.open_workbook(ruta)
			if clientes:
				self.importar_clientes_excel(book.sheet_by_name("clientes"))
			if coches:
				self.importar_coches_excel(book.sheet_by_name("coches"))
		except Exception as error:
			print("Error al exportar a excel: ", error)
			return False

	def importar_clientes_excel(self, sheet: Sheet) -> bool:
		try:
			filas: list[Cliente] = []
			for fila in range(1, sheet.nrows):  # Empieza en 1 para saltarse la cabecera
				filas.append(Cliente(
					sheet.cell_value(fila, 0),
					sheet.cell_value(fila, 1),
					sheet.cell_value(fila, 2),
					sheet.cell_value(fila, 3),
					sheet.cell_value(fila, 4),
					sheet.cell_value(fila, 5),
					sheet.cell_value(fila, 6),
					sheet.cell_value(fila, 7),
					sheet.cell_value(fila, 8)
				))

		except Exception as error:
			print("Error al importar clientes excel: ", error)
			return False

	def importar_coches_excel(self, sheet: Sheet) -> bool:
		try:
			filas: list[Vehiculo] = []
			for fila in range(1, sheet.nrows):  # Empieza en 1 para saltarse la cabecera
				matricula = sheet.cell_value(fila, 0)
				dni = sheet.cell_value(fila, 1)
				marca = sheet.cell_value(fila, 2)
				modelo = sheet.cell_value(fila, 3)
				tipo_motor = sheet.cell_value(fila, 4)
				filas.append(Vehiculo(matricula, dni, marca, modelo, tipo_motor))

			query = QtSql.QSqlQuery()
			query.prepare(
				"INSERT INTO coches (matricula, dnicli, marca, modelo, motor) VALUES (?, ?, ?, ?, ?)")

			for fila in filas:
				query.addBindValue(fila.matricula)
				query.addBindValue(fila.dni)
				query.addBindValue(fila.marca)
				query.addBindValue(fila.modelo)
				query.addBindValue(fila.motor)
				query.exec()

			return True
		except Exception as error:
			print("Error al importar de excel: ", error)
			return False
