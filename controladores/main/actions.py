from datetime import datetime

import conexion
from controladores import modal
from controladores.dlgTipoExportacion import DialogoTipoExportacion
from controladores.dlgabrir import DialogoAbrir
from controladores.dlgsalir import DialogSalir
from controladores.ventmain import Main


def salir():
	dialog_salir = DialogSalir()
	dialog_salir.mostrar_salir()


def exportar_copia(self: Main):
	try:
		dialogo = DialogoAbrir()

		fecha = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
		copia = f"{fecha}_backup.zip"
		directorio, filename = dialogo.getSaveFileName(self, "Guardar copia de seguridad",
													   copia, "Zip (*.zip)")

		if directorio and self.servicioBackup.hacer_copia(directorio):
			modal.aviso("Aviso", "Copia de seguridad realizada correctamente")

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

			modal.aviso("Aviso", "Se ha restaurado la copia de seguridad correctamente")
	except Exception as error:
		print(f"Error restaurando copia: {error}")


def exportar_excel(self: Main):
	try:
		dialogo_exportacion = DialogoTipoExportacion()
		if dialogo_exportacion.exec():
			if not dialogo_exportacion.ui.checkboxCoches.isChecked() and not dialogo_exportacion.ui.checkboxClientes.isChecked():
				modal.error("Aviso", "Debes seleccionar al menos una opción")
				exportar_excel(self)
				return
			dialogo_abrir = DialogoAbrir()
			directorio = dialogo_abrir.getSaveFileName(self, "Exportar a Excel", "",
													   "Excel (*.xls)")
			if directorio[0]:
				self.servicioBackup.exportar_excel(directorio[0],
												   dialogo_exportacion.ui.checkboxClientes.isChecked(),
												   dialogo_exportacion.ui.checkboxCoches.isChecked())
				modal.aviso("Aviso", "Se ha exportado a Excel correctamente")
	except Exception as error:
		print(f"Error exportando excel: {error}")


def importar_excel(self: Main):
	try:
		dialogo = DialogoAbrir()
		directorio, filename = dialogo.getOpenFileName(self, "Importar Excel", "",
													   "Excel (*.xls)")
		if directorio and self.servicioBackup.importar_excel(directorio):
			import cargar
			cargar.tabla_vehiculos(self)
			modal.aviso("Aviso", "Se ha importado de Excel correctamente")
	except Exception as error:
		print(f"Error importando excel: {error}")
