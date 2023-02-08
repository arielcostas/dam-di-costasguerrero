from datetime import datetime

from bbdd import ClienteRepository, conexion, VehiculoRepository
from controladores.dialogos.cambiarpropietario import DialogoCambiarPropietario
from controladores.main import cargar
from controladores.modales import aviso
from controladores.dialogos import DialogoAbrir, DialogoSalir, DialogoTipoExportacion, \
	DialogoTipoImportacion
from controladores.ventmain import Main
from negocio.informes import Informes


def salir():
	dialog_salir = DialogoSalir()
	dialog_salir.mostrar_salir()


def exportar_copia(self: Main):
	try:
		dialogo = DialogoAbrir()

		fecha = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
		copia = f"{fecha}_backup.zip"
		directorio, filename = dialogo.getSaveFileName(self, "Guardar copia de seguridad",
													   copia, "Zip (*.zip)")

		if directorio and self.servicioBackup.hacer_copia(directorio):
			aviso.info("Aviso", "Copia de seguridad realizada correctamente")

	except Exception as error:
		print(f"Error haciendo copia: {error}")


def importar_copia(self: Main):
	try:
		dialogo = DialogoAbrir()
		directorio, filename = dialogo.getOpenFileName(
			self,
			"Restaurar copia de seguridad", "",
			"Archivo comprimido en ZIP (*.zip)"
		)
		if directorio and self.servicioBackup.restaurar_copia(directorio):
			conexion.abrir()
			import cargar
			cargar.tabla_vehiculos(self)

			aviso.info("Aviso", "Se ha restaurado la copia de seguridad correctamente")
	except Exception as error:
		print(f"Error restaurando copia: {error}")


def exportar_excel(self: Main):
	try:
		dialogo_exportacion = DialogoTipoExportacion()
		if dialogo_exportacion.exec():
			if not dialogo_exportacion.ui.checkboxCoches.isChecked() \
				and not dialogo_exportacion.ui.checkboxClientes.isChecked() \
				and not dialogo_exportacion.ui.checkBoxServicios.isChecked():
				aviso.error("Aviso", "Debes seleccionar al menos una opción")
				exportar_excel(self)
				return
			dialogo_abrir = DialogoAbrir()
			directorio = dialogo_abrir.getSaveFileName(
				self, "Exportar a Excel", "",
				"Hoja de cálculo de Excel (*.xlsx)"
			)
			if directorio[0]:
				self.servicioBackup.exportar_excel(
					directorio[0],
					dialogo_exportacion.ui.checkboxClientes.isChecked(),
					dialogo_exportacion.ui.checkboxCoches.isChecked(),
					dialogo_exportacion.ui.checkBoxServicios.isChecked(),
					dialogo_exportacion.ui.checkboxIncluirHistorico.isChecked()
				)
				aviso.info("Aviso", "Se ha exportado a Excel correctamente")
	except Exception as error:
		print(f"Error exportando excel: {error}")


def importar_excel(self: Main):
	try:
		# Elegir el archivo de donde lee
		dialogo = DialogoAbrir()
		directorio, filetype = dialogo.getOpenFileName(
			self, "Importar Excel", "",
			"Hoja de cálculo de Excel (*.xlsx)"
		)
		if directorio:
			# Comprobar si el excel tiene tabla de clientes, coches o ambas
			puede_cargar_clientes, puede_cargar_coches = \
				self.servicioBackup.comprobar_tipos_importables_excel(directorio)

			# El excel contiene tabla de clientes o coches
			if puede_cargar_clientes or puede_cargar_coches:
				# Mostrar diálogo para elegir que tablas de las disponibles se cargan
				dialogo_importar = DialogoTipoImportacion(
					puede_cargar_clientes,
					puede_cargar_coches
				)
				if dialogo_importar.exec():
					if not dialogo_importar.ui.checkboxCoches.isChecked() and not dialogo_importar.ui.checkboxClientes.isChecked():
						aviso.error("Aviso", "Debes seleccionar al menos una opción")
						# importar_excel(self)
						return
					# Cargar las tablas elegidas
					self.servicioBackup.importar_excel(
						directorio,
						dialogo_importar.ui.checkboxClientes.isChecked(),
						dialogo_importar.ui.checkboxCoches.isChecked()
					)
					aviso.info("Aviso", "Se ha importado correctamente")

					from controladores.main import cargar
					cargar.tabla_vehiculos(self)
			else:
				aviso.error("Error", "El archivo no contiene tablas de clientes ni de coches")

	except Exception as error:
		print(f"Error importando excel: {error}")


def cambiar_propietario(self: Main):
	try:
		clientes = ClienteRepository().get_all()
		vehiculos = VehiculoRepository.get_all(True)
		dcp = DialogoCambiarPropietario(clientes, vehiculos)
		if dcp.exec():
			matricula = dcp.ui.vehiculo.currentText().split(" (")[0]
			dni = dcp.ui.cliente.currentText().split(" - ")[0]

			if self.servicioPropietarios.cambiar_propietario(matricula, dni):
				cargar.tabla_vehiculos(self)
				aviso.info("Aviso", "Se ha cambiado el propietario correctamente")
			else:
				aviso.error("Error", "No se ha podido cambiar el propietario")


	except Exception as error:
		print(f"Error cambiando propietario: {error}")


def informe_clientes(self):
	# Obtiene todos los clientes
	clientes = ClienteRepository.get_all(False)

	# Pregunta al usuario dónde quiere guardar
	dialogo_abrir = DialogoAbrir()
	directorio = dialogo_abrir.getSaveFileName(
		self, "Informe de clientes", "",
		"(*.pdf)"
	)
	if directorio[0]:
		# Usa la ruta especificada
		ruta = directorio[0]
	else:
		# Sale porque el usuario ha cancelado
		return

	# genera el informe y lo guarda
	Informes.informe_clientes(clientes, ruta)

def informe_vehiculos(self):
	vehiculos = VehiculoRepository.get_all(False)

	dialogo_abrir = DialogoAbrir()
	directorio = dialogo_abrir.getSaveFileName(
		self, "Informe de vehículos", "",
		"(*.pdf)"
	)
	if directorio[0]:
		ruta = directorio[0]
	else:
		return

	Informes.informe_vehiculos(vehiculos, ruta)
