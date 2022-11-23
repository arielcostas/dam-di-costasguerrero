from datetime import datetime

import conexion
from controladores.modales import aviso
from controladores.dialogos import DialogoAbrir, DialogoSalir, DialogoTipoExportacion, DialogoTipoImportacion
from controladores.ventmain import Main


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
		directorio, filename = dialogo.getOpenFileName(self, "Restaurar copia de seguridad", "",
													   "Zip (*.zip)")
		if directorio and self.servicioBackup.restaurar_copia(directorio):
			self.bbdd = conexion.Conexion()
			self.bbdd.iniciar_conexion()
			import cargar
			cargar.tabla_vehiculos(self)

			aviso.info("Aviso", "Se ha restaurado la copia de seguridad correctamente")
	except Exception as error:
		print(f"Error restaurando copia: {error}")


def exportar_excel(self: Main):
	try:
		dialogo_exportacion = DialogoTipoExportacion()
		if dialogo_exportacion.exec():
			if not dialogo_exportacion.ui.checkboxCoches.isChecked() and not dialogo_exportacion.ui.checkboxClientes.isChecked():
				aviso.error("Aviso", "Debes seleccionar al menos una opción")
				exportar_excel(self)
				return
			dialogo_abrir = DialogoAbrir()
			directorio = dialogo_abrir.getSaveFileName(self, "Exportar a Excel", "",
													   "Excel (*.xls)")
			if directorio[0]:
				self.servicioBackup.exportar_excel(directorio[0],
												   dialogo_exportacion.ui.checkboxClientes.isChecked(),
												   dialogo_exportacion.ui.checkboxCoches.isChecked())
				aviso.info("Aviso", "Se ha exportado a Excel correctamente")
	except Exception as error:
		print(f"Error exportando excel: {error}")


def importar_excel(self: Main):
	try:
		# Elegir el archivo de donde lee
		dialogo = DialogoAbrir()
		directorio, filetype = dialogo.getOpenFileName(self, "Importar Excel", "",
													   "Excel (*.xls)")
		if directorio:
			# Comprobar si el excel tiene tabla de clientes, coches o ambas
			puedeCargarClientes, puedeCargarCoches = self.servicioBackup.comprobar_tipos_importables_excel(
				directorio)

			# El excel contiene tabla de clientes o coches
			if puedeCargarClientes or puedeCargarCoches:
				# Mostrar diálogo para elegir que tablas de las disponibles se cargan
				dialogo_importar = DialogoTipoImportacion(puedeCargarClientes, puedeCargarCoches)
				if dialogo_importar.exec():
					if not dialogo_importar.ui.checkboxCoches.isChecked() and not dialogo_importar.ui.checkboxClientes.isChecked():
						aviso.error("Aviso", "Debes seleccionar al menos una opción")
						#importar_excel(self)
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
