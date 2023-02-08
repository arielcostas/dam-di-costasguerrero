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
				doc.setFont("Helvetica-Bold", 16)
				doc.drawString(50, 720, "Informe de clientes")
				doc.setFont("Courier", 9)

				doc.line(30, 700, 570, 700)
				doc.setFont("Courier-Bold", 12)
				doc.drawString(30, 685, "DNI")
				doc.drawString(100, 685, "Nombre")
				doc.drawString(240, 685, "Dirección")
				doc.drawString(390, 685, "Municipio")
				doc.drawString(480, 685, "Provincia")
				doc.setFont("Helvetica", 12)
				doc.line(30, 680, 570, 680)

			cabecera_tabla()

			h = 665
			for cli in clientes:
				if h < 80:
					doc.showPage()
					Informes.cabecera(doc)
					cabecera_tabla()
					Informes.pie(doc)
					h = 665
				doc.setFont("Courier", 11)
				doc.drawString(30, h, "*****" + cli.dni[-4:-1] + "*")
				doc.drawString(100, h, cli.nombre)
				doc.drawString(240, h, cli.direccion)
				doc.drawString(390, h, cli.municipio)
				doc.drawString(480, h, cli.provincia)
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
				doc.setFont("Helvetica-Bold", 16)
				doc.drawString(50, 720, "Informe de vehículos")
				doc.setFont("Courier", 9)

				doc.line(30, 700, 570, 700)
				doc.setFont("Courier-Bold", 12)
				doc.drawString(30, 685, "Matrícula")
				doc.drawString(130, 685, "DNI dueño")
				doc.drawString(230, 685, "Marca")
				doc.drawString(350, 685, "Modelo")
				doc.drawString(480, 685, "Motorización".rjust(10, " "))
				doc.setFont("Helvetica", 12)
				doc.line(30, 680, 570, 680)

			cabecera_tabla()

			h = 665
			for veh in vehiculos:
				if h < 80:
					doc.showPage()
					Informes.cabecera(doc)
					cabecera_tabla()
					Informes.pie(doc)
					h = 665
				doc.setFont("Courier", 11)
				doc.drawString(30, h, veh.matricula)
				doc.drawString(130, h, "*****" + veh.dni[-4:-1] + "*")
				doc.drawString(230, h, veh.marca)
				doc.drawString(350, h, veh.modelo)
				doc.drawString(500, h, veh.motor.rjust(10, " "))
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

			clinom = cli.nombre
			clinif = "NIF: " + factura.nif
			clidir = cli.direccion
			climun = cli.municipio + " - " + cli.provincia

			maximo = max(clinom, clinif, clidir, climun)
			
			doc.drawString(460, 715, clinom.rjust(len(maximo)))
			doc.drawString(460, 705, clinif.rjust(len(maximo)))
			doc.drawString(460, 695, clidir.rjust(len(maximo)))
			doc.drawString(460, 685, climun.rjust(len(maximo)))

			def cabecera_tabla():
				doc.setFont("Helvetica", 12)
				doc.line(30, 670, 570, 670)
				doc.setFont("Courier-Bold", 12)

				doc.drawString(50, 656, "Nº")
				doc.drawString(100, 656, "Producto")
				doc.drawString(250, 656, "Precio unitario")
				doc.drawString(390, 656, "Cantidad")
				doc.drawString(500, 656, "Subtotal".rjust(10))
				doc.setFont("Helvetica", 12)
				doc.line(30, 650, 570, 650)

			cabecera_tabla()

			precio_total = 0
			h = 635
			i = 1
			for serv in servicios:
				if h < 80:
					doc.showPage()
					Informes.cabecera(doc)
					cabecera_tabla()
					Informes.pie(doc)
					h = 635
				doc.setFont("Courier", 11)
				doc.drawString(50, h, f"{i}")
				doc.drawString(100, h, serv[0].nombre)
				doc.drawString(250, h, f"{serv[0].precio_unitario:.2f}".rjust(10))
				doc.drawString(390, h, f"{serv[1]:.2f}".rjust(5))
				doc.drawString(500, h, f"{serv[0].precio_unitario * serv[1]:.2f} €".rjust(10))

				h -= 15
				i += 1
				precio_total += serv[0].precio_unitario * serv[1]

			iva = precio_total * 0.21

			doc.setFont("Helvetica", 11)
			doc.drawString(420, 95, "Subtotal: ")
			doc.setFont("Courier-Bold", 11)
			doc.drawString(480, 95, f"{precio_total:.2f} €".rjust(10))
			doc.setFont("Helvetica", 11)
			doc.drawString(420, 80, "IVA (21%): ")
			doc.setFont("Courier-Bold", 11)
			doc.drawString(480, 80, f"{iva:.2f} €".rjust(10))
			doc.setFont("Helvetica", 11)
			doc.drawString(420, 65, "Total: ")
			doc.setFont("Courier-Bold", 11)
			doc.drawString(480, 65, f"{precio_total + iva:.2f} €".rjust(10))

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
