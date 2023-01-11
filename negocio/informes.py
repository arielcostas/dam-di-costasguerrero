from datetime import datetime

from reportlab.graphics.shapes import Line, Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph

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
			doc = canvas.Canvas(ruta)
			doc.setPageSize(A4)

			Informes.cabecera(doc)

			doc.setFont("Helvetica-Bold", 12)
			doc.drawString(50, 720, "Informe de clientes")
			doc.setFont("Helvetica", 12)

			doc.line(30, 700, 570, 700)
			doc.drawString(50, 685, "DNI")
			doc.drawString(120, 685, "Nombre")
			doc.drawString(220, 685, "Dirección")
			doc.drawString(330, 685, "Municipio")
			doc.drawString(410, 685, "Provincia")
			doc.line(30, 680, 570, 680)

			h = 660
			for cli in clientes:
				if h < 80:
					doc.showPage()
					Informes.cabecera(doc)
					h = 670
				doc.drawString(50, h, cli.dni)
				doc.drawString(120, h, cli.nombre)
				doc.drawString(220, h, cli.direccion)
				doc.drawString(330, h, cli.municipio)
				doc.drawString(410, h, cli.provincia)
				h -= 15

			doc.save()
		except Exception as e:
			print(e)
			return False

	@staticmethod
	def cabecera(doc: canvas.Canvas):
		doc.setFont("Helvetica", 12)
		doc.line(30, 820, 570, 820)
		doc.drawString(50, 805, "Talleres de Teis, S.L.")
		doc.setFont("Helvetica", 7)
		doc.drawString(50, 785, "CIF: 12345678A")
		doc.drawString(50, 775, "Avenida de Galicia, 101")
		doc.drawString(50, 765, "36208 Vigo - España")
		doc.drawString(50, 755, "Teléfono: 986 986 986")
		doc.drawString(50, 745, "a21arielcg@iesteis.es")
		doc.line(30, 740, 570, 740)
