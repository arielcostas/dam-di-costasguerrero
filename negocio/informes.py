from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, PageTemplate

from bbdd import Cliente


class Informes:
	@staticmethod
	def informe_clientes(clientes: list[Cliente], ruta: str) -> bool:
		data = [["DNI", "Nombre", "Fecha de alta", "Efectivo", "Factura", "Transferencia"]]
		for cliente in clientes:
			data.append([
				cliente.dni,
				cliente.nombre,
				cliente.fecha_alta,
				"Si" if cliente.efectivo else "No",
				"Si" if cliente.factura else "No",
				"Si" if cliente.transferencia else "No"
			])

		try:
			doc = SimpleDocTemplate(ruta, pagesize=A4)
			header = Paragraph("Listado de clientes", style="h1")

			tabla = Table(data)
			tabla.setStyle([
				("GRID", (0, 0), (-1, -1), 1, colors.black),
				("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)
			])


			doc.build([header, tabla])
		except Exception as e:
			print(e)
			return False