from PyQt6 import QtWidgets

from bbdd.servicio import ServicioRepository
from controladores import modales
from controladores.ventmain import Main
from bbdd.modelos import Servicio

NUEVO_PRODUCTO_ID = "NUEVO"


def init_tab(self: Main):
	"""
	Inicializa la pestaña de servicios

	:param self: Ventana principal
	:return: None
	"""
	cargar_tabla(self)

	self.ventMain.textId.setText(NUEVO_PRODUCTO_ID)
	self.ventMain.btnEliminarServicio.setDisabled(True)

	self.ventMain.btnGuardarServicio.clicked.connect(lambda: on_guardar_servicio(self))
	self.ventMain.btnEliminarServicio.clicked.connect(lambda: on_eliminar_servicio(self))

	self.ventMain.checkHistoricoServicios.stateChanged.connect(lambda: cargar_tabla(self))
	self.ventMain.textNombreServicio.editingFinished.connect(
		lambda: on_nombre_servicio_editado(self))

	self.ventMain.tablaServicios.currentItemChanged.connect(lambda: cargar_servicio(self))
	self.ventMain.btnLimpiarServicio.clicked.connect(lambda: on_limpiar(self))
	self.ventMain.btnBuscarServicio.clicked.connect(lambda: on_buscar(self))


def cargar_servicio(self: Main):
	"""
	Carga el servicio seleccionado en la tabla

	:param self: Ventana principal
	:return: None
	"""
	try:
		row = self.ventMain.tablaServicios.currentRow()
		if row is not None:
			sid = self.ventMain.tablaServicios.item(row, 0).text()
			serv = ServicioRepository.get_by_id(sid)

			on_limpiar(self)
			self.ventMain.textId.setText(str(serv.sid))
			self.ventMain.textNombreServicio.setText(serv.nombre)
			self.ventMain.textPrecioUnitario.setValue(serv.precio_unitario)

			self.ventMain.textStockServicio.setValue(serv.stock)
			if not serv.almacenable:
				self.ventMain.textStockServicio.setEnabled(False)

			self.ventMain.btnEliminarServicio.setDisabled(False)
	except Exception as error:
		print(f"Error cargando servicio: {error}")


def on_buscar(self: Main):
	"""
	Busca servicios por nombre

	:param self: Ventana principal
	:return: None
	"""
	try:
		dlg = QtWidgets.QInputDialog(self)
		dlg.setWindowTitle("Buscar servicios")
		dlg.setLabelText("Introduzca el término a buscar")
		dlg.exec()
		term = dlg.textValue()
		filas = ServicioRepository.buscar(term)
		insertar_tabla(self, filas)
	except Exception as error:
		print(f"error buscando {error}")


def on_guardar_servicio(self: Main):
	"""
	Guarda el servicio

	:param self: Ventana principal
	:return: None
	"""
	id = self.ventMain.textId.text()
	nombre = self.ventMain.textNombreServicio.text()
	precio_unitario = self.ventMain.textPrecioUnitario.value()

	stock = self.ventMain.textStockServicio.value()
	stockbd = stock
	almacenable = stock != -1
	if stock == -1:
		stockbd = 0

	if id == NUEVO_PRODUCTO_ID:
		if ServicioRepository.nuevo_servicio(nombre, precio_unitario, stockbd, almacenable):
			cargar_tabla(self)
			on_limpiar(self)
			modales.info("Guardado de servicios", "Se ha creado el servicio")
		else:
			modales.error("Guardado de servicios", "Hubo un error creando el servicio")
	else:
		if ServicioRepository.modificar_servicio(id, nombre, precio_unitario, stockbd):
			cargar_tabla(self)
			modales.info("Guardado de servicios", "Se ha actualizado el servicio")
		else:
			modales.error("Guardado de servicios", "Hubo un error actualizando el servicio")


def on_eliminar_servicio(self: Main):
	"""
	Elimina el servicio seleccionado

	:param self: Ventana principal
	:return: None
	"""
	id = self.ventMain.textId.text()
	eliminado = ServicioRepository.eliminar_servicio(id)
	if eliminado:
		cargar_tabla(self)
		modales.info("Guardado de servicios", "Se ha eliminado el servicio")
	else:
		modales.error("Guardado de servicios", "No se pudo eliminar el servicio")


def on_nombre_servicio_editado(self: Main):
	"""
	Formatea el nombre del servicio

	:param self: Ventana principal
	:return: None
	"""
	self.ventMain.textNombreServicio.setText(
		self.ventMain.textNombreServicio.text().capitalize()
	)


def cargar_tabla(self: Main):
	"""
	Carga la tabla de servicios

	:param self: Ventana principal
	:return: None
	"""
	cargar_historico = self.ventMain.checkHistoricoServicios.isChecked()
	filas = ServicioRepository.get_all(cargar_historico)
	insertar_tabla(self, filas)


def insertar_tabla(self: Main, filas: list[Servicio]):
	"""
	Inserta los datos de los servicios en la tabla

	:param self: Ventana principal
	:param filas: Lista de servicios
	:return: None
	"""
	self.ventMain.tablaServicios.clearContents()
	self.ventMain.tablaServicios.setRowCount(len(filas))
	for idx, el in enumerate(filas):
		self.ventMain.tablaServicios \
			.setItem(idx, 0, QtWidgets.QTableWidgetItem(str(el.sid)))
		self.ventMain.tablaServicios \
			.setItem(idx, 1, QtWidgets.QTableWidgetItem(el.nombre))
		self.ventMain.tablaServicios \
			.setItem(idx, 2, QtWidgets.QTableWidgetItem(str(el.precio_unitario)))
		self.ventMain.tablaServicios \
			.setItem(idx, 3, QtWidgets.QTableWidgetItem(el.fecha_alta))
		self.ventMain.tablaServicios \
			.setItem(idx, 4, QtWidgets.QTableWidgetItem(el.fecha_modificacion))

		if el.almacenable:
			self.ventMain.tablaServicios \
				.setItem(idx, 5, QtWidgets.QTableWidgetItem(str(el.stock)))
		else:
			self.ventMain.tablaServicios \
				.setItem(idx, 5, QtWidgets.QTableWidgetItem("N/A"))

		self.ventMain.tablaServicios \
			.setItem(idx, 6, QtWidgets.QTableWidgetItem(el.fecha_baja))


	for i in range(0, self.ventMain.tablaServicios.columnCount()):
		self.ventMain.tablaServicios \
			.horizontalHeader() \
			.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
		if i < 2:
			self.ventMain.tablaServicios \
				.horizontalHeader() \
				.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)


def on_limpiar(self: Main):
	"""
	Limpia los campos de la pestaña de servicios

	:param self: Ventana principal
	:return: None
	"""
	self.ventMain.textId.setText(NUEVO_PRODUCTO_ID)
	self.ventMain.textNombreServicio.setText("")
	self.ventMain.textPrecioUnitario.setValue(0.00)
	self.ventMain.btnEliminarServicio.setDisabled(True)
	self.ventMain.textStockServicio.setValue(0)
	self.ventMain.textStockServicio.setEnabled(True)
