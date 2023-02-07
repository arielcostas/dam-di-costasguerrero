from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from bbdd import Cliente, Vehiculo, Servicio, ClienteRepository
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
	def informe_vehiculos(vehiculos: list[Vehiculo], ruta: str) -> bool:
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
		cli = ClienteRepository.get_by_dni(factura.nif)

		try:
			doc = canvas.Canvas(ruta)
			doc.setPageSize(A4)

			Informes.cabecera(doc)
			Informes.pie(doc)

			doc.setFont("Helvetica-Bold", 16)
			doc.drawString(50, 700, "Factura #" + str(factura.fid))
			doc.setFont("Courier", 9)
			doc.drawString(460, 715, cli.nombre)
			doc.drawString(460, 705, "NIF: " + factura.nif)
			doc.drawString(460, 695, cli.direccion)
			doc.drawString(460, 685, cli.municipio + " - " + cli.provincia)

			def cabecera_tabla():
				doc.setFont("Helvetica", 12)
				doc.line(30, 670, 570, 670)
				doc.setFont("Courier-Bold", 12)

				doc.drawString(50, 655, "Nº")
				doc.drawString(100, 655, "Producto")
				doc.drawString(250, 655, "Precio unitario")
				doc.drawString(390, 655, "Cantidad")
				doc.drawString(480, 655, "Subtotal")
				doc.setFont("Helvetica", 12)
				doc.line(30, 650, 570, 650)

			cabecera_tabla()

			precio_total = 0
			h = 630
			i = 1
			for serv in servicios:
				if h < 80:
					doc.showPage()
					Informes.cabecera(doc)
					cabecera_tabla()
					Informes.pie(doc)
					h = 670
				doc.setFont("Courier", 11)
				doc.drawString(50, h, f"{i}")
				doc.drawString(100, h, serv[0].nombre)
				doc.drawString(250, h, f"{serv[0].precio_unitario:.2f}".rjust(10))
				doc.drawString(390, h, f"{serv[1]:.2f}".rjust(5))
				doc.drawString(480, h, f"{serv[0].precio_unitario * serv[1]:.2f}".rjust(10))

				h -= 15
				i += 1
				precio_total += serv[0].precio_unitario * serv[1]

			doc.setFont("Courier-Bold", 11)
			doc.drawString(480, 85, f"{precio_total:.2f} €".rjust(10))
			doc.setFont("Helvetica", 11)

			doc.save()
		except Exception as e:
			print("Error al generar el informe de clientes", e)
			return False

	@staticmethod
	def cabecera(doc: canvas.Canvas):
		doc.line(30, 820, 570, 820)
		doc.setFont("Times-Bold", 15)
		doc.drawString(50, 800, "Talleres de Teis, S.L.")
		doc.setFont("Helvetica", 8)
		doc.drawString(50, 790, "CIF: 12345678A")
		doc.drawString(50, 780, "Avenida de Galicia, 101")
		doc.drawString(50, 770, "36208 Vigo - España")
		doc.drawString(50, 760, "Teléfono: 986 986 986")
		doc.drawString(50, 750, "a21arielcg@iesteis.es")
		doc.drawImage("img/logo_fondo.png", 510, 750, 50, 50)
		doc.line(30, 740, 570, 740)

	@staticmethod
	def pie(doc: canvas.Canvas):
		doc.setFont("Helvetica", 8)
		doc.line(30, 50, 570, 50)
		doc.drawString(50, 35, "Talleres de Teis, S.L.")
		doc.drawString(280, 35, "Página %d" % doc.getPageNumber())
		doc.drawString(500, 35, "Fecha: %s" % datetime.now().strftime("%d/%m/%Y"))
