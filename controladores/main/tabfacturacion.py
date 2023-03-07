import os
from datetime import datetime

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from controladores import modales

from bbdd import VehiculoRepository, ClienteRepository, ServicioRepository, Servicio
from bbdd.factura import FacturaRepository
from bbdd.modelos.factura import Factura
from controladores.dialogos import DialogoAbrir
from controladores.main import cargar
from controladores.ventmain import Main
from negocio import informes, Informes


def init_tab(self: Main):
	limpiar(self)
	load_facturas(self)

	# Configurar las columnas editables de la tabla de servicios
	self.ventMain.tablaFacturaServicios.setItemDelegate(Delegate(self))
	self.ventMain.tablaFacturasActuales.currentItemChanged.connect(
		lambda: load_factura(self)
	)

	self.ventMain.cmbFactCli.currentTextChanged.connect(lambda: load_vehiculos(self))

	self.ventMain.tabWidget.currentChanged.connect(lambda: limpiar(self))
	self.ventMain.btnLimpiarFactura.clicked.connect(lambda: limpiar(self))
	self.ventMain.btnImprimirFactura.clicked.connect(lambda: imprimir_factura(self))
	self.ventMain.btnGuardarFactura.clicked.connect(lambda: guardar_factura(self))
	self.ventMain.btnBuscaFact.clicked.connect(lambda: buscar_factura(self))


def load_clientes(self: Main):
	self.ventMain.cmbFactCli.clear()
	self.ventMain.cmbFactCli.addItems(
		f"{c.dni} - {c.nombre}" for c in
		ClienteRepository.get_all(False)
	)


def load_vehiculos(self: Main):
	self.ventMain.cmbFactCar.clear()
	self.ventMain.cmbFactCar.addItems(
		f"{v.matricula} - {v.marca} {v.modelo}" for v in
		VehiculoRepository.get_by_dni(
			self.ventMain.cmbFactCli.currentText()[0:9]
		)
	)


def load_facturas(self: Main):
	facturas = FacturaRepository.get_all()
	if self.ultima_busqueda_fact is not None or self.ultima_busqueda_fact != "":
		facturas = [
			fac for fac in facturas if
			fac.matricula.__contains__(self.ultima_busqueda_fact) or
			fac.nif.__contains__(self.ultima_busqueda_fact) or
			str(fac.fid).__contains__(self.ultima_busqueda_fact)
		]

	self.ventMain.tablaFacturasActuales.setRowCount(len(facturas))

	for idx, fact in enumerate(facturas):
		self.ventMain.tablaFacturasActuales \
			.setItem(idx, 0, QtWidgets.QTableWidgetItem(str(fact.fid)))
		self.ventMain.tablaFacturasActuales \
			.setItem(idx, 1, QtWidgets.QTableWidgetItem(fact.nif))

	for i in range(0, self.ventMain.tablaFacturasActuales.columnCount()):
		if i < 1:
			self.ventMain.tablaFacturasActuales \
				.horizontalHeader() \
				.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
		else:
			self.ventMain.tablaFacturasActuales \
				.horizontalHeader() \
				.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)


def load_servicios(self: Main):
	servicios = ServicioRepository.get_all(False)
	self.ventMain.tablaFacturaServicios.setRowCount(len(servicios))

	for idx, serv in enumerate(servicios):
		self.ventMain.tablaFacturaServicios \
			.setItem(idx, 0, QtWidgets.QTableWidgetItem(str(serv.sid)))
		self.ventMain.tablaFacturaServicios \
			.setItem(idx, 1, QtWidgets.QTableWidgetItem(serv.nombre))
		self.ventMain.tablaFacturaServicios \
			.setItem(idx, 3, QtWidgets.QTableWidgetItem(str(0)))

		self.ventMain.tablaFacturaServicios \
			.setItem(idx, 2, QtWidgets.QTableWidgetItem(f"{float(serv.precio_unitario):.2f} €"))
		self.ventMain.tablaFacturaServicios \
			.setItem(idx, 4, QtWidgets.QTableWidgetItem(f"{float(0):.2f} €"))

	for i in range(0, self.ventMain.tablaFacturaServicios.columnCount()):
		if i < 1:
			self.ventMain.tablaFacturaServicios \
				.horizontalHeader() \
				.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
		else:
			self.ventMain.tablaFacturaServicios \
				.horizontalHeader() \
				.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)


def load_servicios_factura(self: Main, factura: Factura):
	load_servicios(self)
	for i in range(0, self.ventMain.tablaFacturaServicios.rowCount()):
		servicio = self.ventMain.tablaFacturaServicios.item(i, 0).text()
		cantidad = FacturaRepository.get_cantidad_producto_factura(factura.fid, int(servicio))
		cantidad = 0 if cantidad is None else cantidad
		self.ventMain.tablaFacturaServicios.item(i, 3).setText(str(cantidad))


def guardar_factura(self: Main):
	factura = Factura(
		None,
		self.ventMain.cmbFactCli.currentText()[0:9],
		self.ventMain.cmbFactCar.currentText().split(" - ")[0],
		self.ventMain.txtFechaFactura.date().toString("yyyy-MM-dd"),
		1 if self.ventMain.chkFormalizarFactura.isChecked() else 0
	)

	servicios = []
	for i in range(0, self.ventMain.tablaFacturaServicios.rowCount()):
		servicios.append(
			(
				self.ventMain.tablaFacturaServicios.item(i, 0).text(),
				self.ventMain.tablaFacturaServicios.item(i, 3).text()
			)
		)

	FacturaRepository.guardar_factura(factura, servicios)
	load_facturas(self)
	limpiar(self)


def actualizar_subtotales(self: Main):
	acumulador = 0
	for i in range(0, self.ventMain.tablaFacturaServicios.rowCount()):
		unitario = float(self.ventMain.tablaFacturaServicios.item(i, 2).text()[:-2])
		cantidad = float(self.ventMain.tablaFacturaServicios.item(i, 3).text())

		if cantidad == 0:
			continue

		self.ventMain.tablaFacturaServicios \
			.setItem(i, 4, QtWidgets.QTableWidgetItem(f"{(unitario * cantidad):.2f} €"))
		acumulador += unitario * cantidad

	self.ventMain.lblSubtotal.setText(f"{acumulador :.2f} €")
	self.ventMain.lblSubtotalIva.setText(f"{acumulador * 0.21 :.2f} €")
	self.ventMain.lblSubtotalTotal.setText(f"{acumulador * 1.21 :.2f} €")


def limpiar(self: Main):
	load_servicios(self)
	load_clientes(self)
	load_vehiculos(self)

	self.ventMain.txtFactId.setText("NUEVA")
	self.ventMain.txtFechaFactura.setDate(datetime.now())
	self.ventMain.tablaFacturaServicios.setEnabled(True)
	self.ventMain.cmbFactCar.setEnabled(True)
	self.ventMain.cmbFactCli.setEnabled(True)
	self.ventMain.txtFechaFactura.setEnabled(True)

	self.ventMain.chkFormalizarFactura.setEnabled(True)
	self.ventMain.chkFormalizarFactura.setChecked(False)

	self.ventMain.btnGuardarFactura.setEnabled(True)
	self.ventMain.btnImprimirFactura.setEnabled(False)
	actualizar_subtotales(self)


def load_factura(self: Main):
	try:
		factura = recuperar_factura(self)

		editable = False if factura.emitida == 1 else True
		self.ventMain.tablaFacturaServicios.setEnabled(editable)
		self.ventMain.cmbFactCli.setEnabled(editable)
		self.ventMain.txtFactId.setText(str(factura.fid))
		# Busca el índice del cliente en el combo con el DNI de la factura
		idx = self.ventMain.cmbFactCli.findText(factura.nif, Qt.MatchFlag.MatchStartsWith)
		self.ventMain.cmbFactCli.setCurrentIndex(idx)

		self.ventMain.cmbFactCar.setEnabled(editable)
		idx = self.ventMain.cmbFactCar.findText(factura.matricula, Qt.MatchFlag.MatchStartsWith)
		self.ventMain.cmbFactCar.setCurrentIndex(idx)

		self.ventMain.txtFechaFactura.setDate(datetime.strptime(factura.fecha, "%Y-%m-%d"))
		self.ventMain.txtFechaFactura.setEnabled(editable)
		self.ventMain.chkFormalizarFactura.setEnabled(editable)
		self.ventMain.btnGuardarFactura.setEnabled(editable)

		self.ventMain.btnImprimirFactura.setEnabled(True)
		load_servicios_factura(self, factura)
		actualizar_subtotales(self)
	except Exception as e:
		print(e)
		pass


def recuperar_factura(self):
	factura_id = self.ventMain.tablaFacturasActuales.item(
		self.ventMain.tablaFacturasActuales.currentRow(), 0).text()
	factura = FacturaRepository.get_by_id(int(factura_id))
	return factura


def imprimir_factura(self: Main):
	"""
	Imprime la factura seleccionada en la tabla de facturas actuales

	:param self:  La ventana principal para detectar la factura seleccionada
	:return: None
	"""
	try:
		factura = recuperar_factura(self)
		servicios = ServicioRepository.get_all(False)

		srvs: list[tuple[Servicio, int]] = []

		dialogo = DialogoAbrir()
		directorio, _ = dialogo.getSaveFileName(
			self,
			"Guardar factura", "",
			"Portable Document Format (*.pdf)"
		)

		if directorio == "":
			return

		if not(directorio.endswith(".pdf")):
			directorio += ".pdf"


		for servicio in servicios:
			cantidad = FacturaRepository.get_cantidad_producto_factura(factura.fid, servicio.sid)
			if cantidad is not None and cantidad > 0:
				srvs.append((servicio, cantidad))

		Informes.factura(factura, srvs, directorio)
		os.startfile(directorio)
	except Exception as e:
		print("Error al imprimir factura: ", e)


def buscar_factura(self: Main):
	input_dlg = QtWidgets.QInputDialog()
	if self.ultima_busqueda_fact is None or self.ultima_busqueda_fact == "":
		self.ultima_busqueda_fact = ""

	texto, ok = input_dlg.getText(
		self,
		"Búsqueda de facturas", "Nº de factura, matrícula o DNI",
		QtWidgets.QLineEdit.EchoMode.Normal,
		self.ultima_busqueda_car
	)
	if not ok:
		return

	self.ultima_busqueda_fact = texto

	load_facturas(self)


class Delegate(QtWidgets.QStyledItemDelegate):
	def __init__(self, main: Main):
		super().__init__()
		self.main = main

	def createEditor(self, parent, option, index):
		if index.column() == 3:
			return super(Delegate, self).createEditor(parent, option, index)

	def destroyEditor(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
		super().destroyEditor(editor, index)
		actualizar_subtotales(self.main)
