from PyQt6 import QtWidgets

from controladores.ventmain import Main


def lista_provincias(self: Main):
	self.ventMain.comboProvinciaCliente.clear()
	datos = self.bbdd.cargar_provincias()
	for i in datos:
		self.ventMain.comboProvinciaCliente.addItem(i)


def lista_municipios(self: Main):
	self.ventMain.comboMunicipioCliente.clear()
	provincia = self.ventMain.comboProvinciaCliente.currentText()
	datos = self.bbdd.cargar_municipios(provincia)
	for i in datos:
		self.ventMain.comboMunicipioCliente.addItem(i)


def tabla_vehiculos(self: Main):
	try:
		self.ventMain.tablaClientes.clearContents()
		datos = self.bbdd.cargar_vehiculos()
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