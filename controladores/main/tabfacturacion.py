from PyQt6 import QtWidgets

from bbdd import VehiculoRepository, ClienteRepository, ServicioRepository
from bbdd.factura import FacturaRepository
from controladores.ventmain import Main


def init_tab(self: Main):
	load_clientes(self)
	load_vehiculos(self)
	load_facturas(self)
	load_servicios(self)

	# Al seleccionar otro cliente, cargar sus vehículos
	self.ventMain.cmbFactCli.currentTextChanged.connect(lambda: load_vehiculos(self))

	# Recargar el listado de clientes cuando se vuelva a la pestaña
	self.ventMain.tabWidget.currentChanged.connect(lambda: load_clientes(self))


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
	self.ventMain.tablaFacturasActuales.setRowCount(len(facturas))

	for idx, fact in enumerate(facturas):
		self.ventMain.tablaFacturasActuales \
			.setItem(idx, 0, QtWidgets.QTableWidgetItem(fact.id))
		self.ventMain.tablaFacturasActuales \
			.setItem(idx, 1, QtWidgets.QTableWidgetItem(fact.dni))
		self.ventMain.tablaFacturasActuales \
			.setItem(idx, 2, QtWidgets.QTableWidgetItem(fact.matricula))
		self.ventMain.tablaFacturasActuales \
			.setItem(idx, 3, QtWidgets.QTableWidgetItem(fact.fecha))

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
			.setItem(idx, 2, QtWidgets.QTableWidgetItem(str(serv.precio_unitario)))
		self.ventMain.tablaFacturaServicios \
			.setItem(idx, 3, QtWidgets.QTableWidgetItem(str(0)))
		self.ventMain.tablaFacturaServicios \
			.setItem(idx, 4, QtWidgets.QTableWidgetItem(str(0)))

	for i in range(0, self.ventMain.tablaFacturaServicios.columnCount()):
		if i < 1:
			self.ventMain.tablaFacturaServicios \
				.horizontalHeader() \
				.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
		else:
			self.ventMain.tablaFacturaServicios \
				.horizontalHeader() \
				.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
