from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from bbdd import Cliente, Vehiculo, Servicio
from bbdd.modelos.factura import Factura


class Informes:
	@staticmethod
	def informe_clientes(clientes: list[Cliente], ruta: str) -> bool:
		try:
			doc = canvas.Canvas(ruta)
			doc.setPageSize(A4)

			Informes.cabecera(doc)
			Informes.pie(doc)

			def cabecera_tabla():
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

			cabecera_tabla()

			h = 660
			for cli in clientes:
				if h < 80:
					doc.showPage()
					Informes.cabecera(doc)
					cabecera_tabla()
					Informes.pie(doc)
					h = 670
				doc.setFont("Helvetica", 11)
				doc.drawString(50, h, "*****" + cli.dni[-4:-1] + "*")
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
	def informe_vehiculos(vehiculos: list[Vehiculo], servicios: list[Servicio], ruta: str) -> bool:
		try:
			doc = canvas.Canvas(ruta)
			doc.setPageSize(A4)

			Informes.cabecera(doc)
			Informes.pie(doc)

			def cabecera_tabla():
				doc.setFont("Helvetica-Bold", 12)
				doc.drawString(50, 720, "Informe de vehículos")
				doc.setFont("Helvetica", 12)

				doc.line(30, 700, 570, 700)
				doc.drawString(50, 685, "Matrícula")
				doc.drawString(120, 685, "DNI dueño")
				doc.drawString(220, 685, "Marca")
				doc.drawString(330, 685, "Modelo")
				doc.drawString(410, 685, "Motorización")
				doc.line(30, 680, 570, 680)

			cabecera_tabla()

			h = 660
			for veh in vehiculos:
				if h < 80:
					doc.showPage()
					Informes.cabecera(doc)
					cabecera_tabla()
					Informes.pie(doc)
					h = 670
				doc.setFont("Helvetica", 11)
				doc.drawString(50, h, veh.matricula)
				doc.drawString(120, h, "*****" + veh.dni[-4:-1] + "*")
				doc.drawString(220, h, veh.marca)
				doc.drawString(330, h, veh.modelo)
				doc.drawString(410, h, veh.motor)
				h -= 15

			doc.save()
		except Exception as e:
			print(e)
			return False

	@staticmethod
	def factura(factura: Factura, servicios: list[tuple[Servicio, int]], ruta: str) -> bool:
		try:
			doc = canvas.Canvas(ruta)
			doc.setPageSize(A4)

			Informes.cabecera(doc)
			Informes.pie(doc)

			def cabecera_tabla():
				doc.setFont("Helvetica-Bold", 12)
				doc.drawString(50, 720, "Factura")
				doc.setFont("Helvetica", 12)

				doc.line(30, 700, 570, 700)
				doc.drawString(50, 685, "Nº")
				doc.drawString(120, 685, "Producto")
				doc.drawString(220, 685, "Cantidad")
				doc.drawString(330, 685, "Precio unitario")
				doc.drawString(410, 685, "Subtotal")
				doc.line(30, 680, 570, 680)

			cabecera_tabla()

			h = 660
			i = 1
			for serv in servicios:
				if serv[1] == 0:
					continue

				if h < 80:
					doc.showPage()
					Informes.cabecera(doc)
					cabecera_tabla()
					Informes.pie(doc)
					h = 670
				doc.setFont("Helvetica", 11)
				doc.drawString(50, h, str(i))
				doc.drawString(120, h, serv[0].nombre)
				doc.drawString(270, h, str(serv[0].precio_unitario))
				doc.drawString(330, h, str(serv[1]))
				doc.drawString(410, h, str(serv[0].precio_unitario * serv[1]))

				h -= 15
				i += 1

			doc.save()
		except Exception as e:
			print("Error al generar el informe de clientes", e)
			return False

	@staticmethod
	def cabecera(doc: canvas.Canvas):
		doc.setFont("Helvetica-Bold", 13)
		doc.line(30, 820, 570, 820)
		doc.drawString(50, 795, "Talleres de Teis, S.L.")
		doc.setFont("Helvetica", 7)
		doc.drawString(50, 785, "CIF: 12345678A")
		doc.drawString(50, 775, "Avenida de Galicia, 101")
		doc.drawString(50, 765, "36208 Vigo - España")
		doc.drawString(50, 755, "Teléfono: 986 986 986")
		doc.drawString(50, 745, "a21arielcg@iesteis.es")
		doc.drawImage("img/logo_fondo.png", 510, 750, 50, 50)
		doc.line(30, 740, 570, 740)

	@staticmethod
	def pie(doc: canvas.Canvas):
		doc.setFont("Helvetica", 7)
		doc.line(30, 50, 570, 50)
		doc.drawString(50, 35, "Talleres de Teis, S.L.")
		doc.drawString(280, 35, "Página %d" % doc.getPageNumber())
		doc.drawString(500, 35, "Fecha: %s" % datetime.now().strftime("%d/%m/%Y"))