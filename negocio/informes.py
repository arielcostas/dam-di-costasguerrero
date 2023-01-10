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

			# Header
			doc.line(30, 820, 570, 820)
			doc.drawString(50, 805, "Talleres de Teis, S.L.")
			doc.setFont("Helvetica", 7)
			doc.drawString(50, 785, "CIF: 12345678A")
			doc.drawString(50, 775, "Avenida de Galicia, 101")
			doc.drawString(50, 765, "36208 Vigo - España")
			doc.drawString(50, 755, "Teléfono: 986 986 986")
			doc.drawString(50, 745, "a21arielcg@iesteis.es")
			doc.line(30, 740, 570, 740)

			doc.setFont("Helvetica", 12)

			tabla = Table(data)
			tabla.setStyle([
				("GRID", (0, 0), (-1, -1), 1, colors.black),
				("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)
			])

			doc.save()
			#doc.build([header, tabla])
		except Exception as e:
			print(e)
			return False