from PyQt6 import QtWidgets

from bbdd import LugaresRepository, VehiculoRepository
from controladores.ventmain import Main


def lista_provincias(self: Main):
	self.ventMain.comboProvinciaCliente.clear()
	datos = LugaresRepository.get_provincias()
	for i in datos:
		self.ventMain.comboProvinciaCliente.addItem(i)


def lista_municipios(self: Main):
	self.ventMain.comboMunicipioCliente.clear()
	provincia = self.ventMain.comboProvinciaCliente.currentText()
	datos = LugaresRepository.get_municipios(provincia)
	for i in datos:
		self.ventMain.comboMunicipioCliente.addItem(i)


def tabla_vehiculos(self: Main):
	historico = self.ventMain.checkMostrarHistorico.isChecked()
	try:
		self.ventMain.tablaClientes.clearContents()
		datos = VehiculoRepository.get_all(historico)
		if self.ultima_busqueda_car is not None and self.ultima_busqueda_car != "":
			datos = [
				d for d in datos if d.matricula.__contains__(self.ultima_busqueda_car)
			]

		self.ventMain.tablaClientes.setRowCount(len(datos))
		for idx, el in enumerate(datos):
			self.ventMain.tablaClientes \
				.setItem(idx, 0, QtWidgets.QTableWidgetItem(el.dni))
			self.ventMain.tablaClientes \
				.setItem(idx, 1, QtWidgets.QTableWidgetItem(el.matricula))
			self.ventMain.tablaClientes \
				.setItem(idx, 2, QtWidgets.QTableWidgetItem(el.marca))
			self.ventMain.tablaClientes \
				.setItem(idx, 3, QtWidgets.QTableWidgetItem(el.modelo))
			self.ventMain.tablaClientes \
				.setItem(idx, 4, QtWidgets.QTableWidgetItem(el.motor))
			self.ventMain.tablaClientes \
				.setItem(idx, 5, QtWidgets.QTableWidgetItem(el.fecha_baja))

		for i in range(0, self.ventMain.tablaClientes.columnCount()):
			self.ventMain.tablaClientes \
				.horizontalHeader() \
				.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
			if i < 2:
				self.ventMain.tablaClientes \
					.horizontalHeader() \
					.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
	except Exception as error:
		print(f"Error cargando tabla vehiculos: {error}")

