from PyQt6 import QtWidgets

import conexion
from dlgcalendario import DialogCalendar
from dlgsalir import DialogSalir
from ui.ventMain import *
from dni import validar as validar_dni


class Main(QtWidgets.QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		self.ventMain = Ui_ventMain()
		self.ventMain.setupUi(self)
		self.dialogSalir = DialogSalir()
		self.dialogCalendar = DialogCalendar()

		# Se pulsa salir en una barra de herramientas
		self.ventMain.actionSalir.triggered.connect(self.on_press_salir)
		self.ventMain.toolbarSalir.triggered.connect(self.on_press_salir)

		# Se pulsa enter en DNI
		self.ventMain.txtDni.editingFinished.connect(self.on_dni_comprobar)

		# Guardar cliente
		self.ventMain.buttonGuardarCliente.clicked.connect(self.on_guardar_cliente)

		# Al seleccionar en el calendario, obtener fecha
		self.ventMain.buttonFechaAltaCliente.clicked.connect(self.on_abrir_calendario)
		self.dialogCalendar.dialogCalendar.calendarWidget.clicked.connect(self.on_seleccionar_fecha)

		# Limpiar
		self.ventMain.buttonLimpiarVehiculo.clicked.connect(self.on_limpiar)

		# Poner mayúsculas a todos
		self.camposMayusculas = [self.ventMain.txtMarca, self.ventMain.txtModelo,
								 self.ventMain.txtNombre, self.ventMain.txtDireccionCliente, self.ventMain.txtDni]

		for campo in self.camposMayusculas:
			campo.editingFinished.connect(self.mayuscula_palabra)

		self.ventMain.txtMatricula.editingFinished.connect(self.mayuscula_palabra)

		self.bbdd = conexion.Conexion()
		self.bbdd.iniciarConexion()
		self.cargar_provincias()
		self.cargar_tablaVehiculos()

		# Al seleccionar una provincia, cargar sus municipios
		self.ventMain.comboProvinciaCliente.currentTextChanged.connect(self.cargar_municipios)

	def get_motor(self):
		try:
			return self.ventMain.btnGroupMotorizacion.checkedButton().text()
		except Exception as error:
			print(f"Error seleccionando motor: {error}")

	def on_dni_comprobar(self):
		try:
			dni = self.ventMain.txtDni.text()
			if validar_dni(dni):
				self.ventMain.lblValidardni.setStyleSheet('color: green;')
				self.ventMain.lblValidardni.setText('V')
				self.ventMain.txtDni.setText(dni.upper())
				self.ventMain.txtDni.setStyleSheet('background-color: white;')
			else:
				self.ventMain.lblValidardni.setStyleSheet('color: red;')
				self.ventMain.lblValidardni.setText('X')
				self.ventMain.txtDni.setText(dni.upper())
				self.ventMain.txtDni.setStyleSheet('background-color: pink;')
		except Exception as error:
			print(f"Error mostrando marcado validez DNI: {error}")

	def on_press_salir(self):
		self.dialogSalir.mostrar_salir()

	def on_guardar_cliente(self):
		try:
			vm = self.ventMain
			cliente = {
				"dni": vm.txtDni.text(),
				"nombre": vm.txtNombre.text(),
				"alta": vm.txtFechaAltaCliente.text(),
				"direccion": vm.txtDireccionCliente.text(),
				"provincia": vm.comboProvinciaCliente.currentText(),
				"municipio": vm.comboMunicipioCliente.currentText(),
				"efectivo": vm.checkEfectivo.isChecked(),
				"factura": vm.checkFactura.isChecked(),
				"transferencia": vm.checkTransferencia.isChecked(),
			}

			vehiculo = {
				"matricula": vm.txtMatricula.text(),
				"cliente": cliente.get("dni"),
				"marca": vm.txtMarca.text(),
				"modelo": vm.txtModelo.text(),
				"motor": self.get_motor(),
			}

			guardado = self.bbdd.guardar_cliente(cliente) and self.bbdd.guardar_vehiculo(vehiculo)
			msg = QtWidgets.QMessageBox()
			if guardado:
				msg.setText("Guardado correctamente")
				msg.setIcon(msg.Icon.Information)
				msg.setText("Se han guardado los datos de cliente y coche correctamente")
			else:
				msg.setText("Error al guardar")
				msg.setIcon(msg.Icon.Critical)
				msg.setText("Hubo un problema al guardar los datos")
			msg.exec()
		except Exception as error:
			print(f"Error en carga cliente: {error}")

	def on_abrir_calendario(self):
		self.dialogCalendar.show()

	def on_seleccionar_fecha(self):
		qdate = self.dialogCalendar.dialogCalendar.calendarWidget.selectedDate()
		try:
			data = f"{qdate.day()}/{qdate.month()}/{qdate.year()}"
			self.ventMain.txtFechaAltaCliente.setText(data)
			self.dialogCalendar.hide()
		except Exception as error:
			print(f"Error cargando fecha cliente: {error}")

	def mayuscula_palabra(self):
		self.ventMain.txtMarca.setText(self.ventMain.txtMarca.text().title())
		self.ventMain.txtModelo.setText(self.ventMain.txtModelo.text().title())
		self.ventMain.txtNombre.setText(self.ventMain.txtNombre.text().title())
		self.ventMain.txtDireccionCliente.setText(self.ventMain.txtDireccionCliente.text().title())
		self.ventMain.txtDni.setText(self.ventMain.txtDni.text().title())
		self.ventMain.txtMatricula.setText(self.ventMain.txtMatricula.text().upper())

	def on_limpiar(self):
		try:
			self.ventMain.txtDni.setText("")
			self.ventMain.txtDni.setText("")
			self.ventMain.txtFechaAltaCliente.setText("")
			self.ventMain.txtDireccionCliente.setText("")
			self.ventMain.txtMatricula.setText("")
			self.ventMain.txtMarca.setText("")
			self.ventMain.txtModelo.setText("")

			self.ventMain.comboProvinciaCliente.setCurrentIndex(0)

			for btn in self.ventMain.btnGroupPago.buttons():
				btn.setChecked(False)

			self.ventMain.radioButtonGasolina.setChecked(True)
		except Exception as error:
			print(f"Error limpiando cliente: {error}")

	def cargar_provincias(self):
		self.ventMain.comboProvinciaCliente.clear()
		datos = self.bbdd.cargar_provincias()
		for i in datos:
			self.ventMain.comboProvinciaCliente.addItem(i)

	def cargar_municipios(self):
		self.ventMain.comboMunicipioCliente.clear()
		provincia = self.ventMain.comboProvinciaCliente.currentText()
		datos = self.bbdd.cargar_municipios(provincia)
		for i in datos:
			self.ventMain.comboMunicipioCliente.addItem(i)

	def cargar_tablaVehiculos(self):
		self.ventMain.tablaClientes.clearContents()
		datos = self.bbdd.cargar_vehiculos()
		self.ventMain.tablaClientes.setRowCount(len(datos))
		for idx, el in enumerate(datos):
			for idx2, el2 in enumerate(el):
				item = QtWidgets.QTableWidgetItem(str(el2))
				item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
				self.ventMain.tablaClientes.setItem(idx, idx2, item)
		for i in range(0, self.ventMain.tablaClientes.columnCount()):
			self.ventMain.tablaClientes.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
