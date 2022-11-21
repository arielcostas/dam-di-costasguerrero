import conexion
from controladores import modal
from controladores.dlgcalendario import DialogCalendar
from modelos import Cliente, Vehiculo
from servicios import ServicioBackup, validar as validar_dni
from ui.ventMain import *


class Main(QtWidgets.QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		self.servicioBackup = ServicioBackup()

		self.ventMain = Ui_ventMain()
		self.ventMain.setupUi(self)

		self.dialogCalendar = DialogCalendar()

		# Guarda todos los campos de texto para uso en otros métodos
		self.campos_texto = [self.ventMain.txtDni, self.ventMain.txtNombre,
							 self.ventMain.txtDireccionCliente,
							 self.ventMain.txtFechaAltaCliente, self.ventMain.txtMatricula,
							 self.ventMain.txtMarca,
							 self.ventMain.txtModelo]

		# Botones de la barra de herramientas
		from .main import actions

		self.ventMain.actionSalir.triggered.connect(lambda: actions.salir(self))
		self.ventMain.actionHacerCopia.triggered.connect(lambda: actions.exportar_copia(self))
		self.ventMain.actionRestaurarCopia.triggered.connect(lambda: actions.importar_copia(self))
		self.ventMain.actionExportarExcel.triggered.connect(lambda: actions.exportar_excel(self))
		self.ventMain.actionImportarExcel.triggered.connect(lambda: actions.importar_excel(self))

		# Se pulsa enter en DNI
		self.ventMain.txtDni.editingFinished.connect(self.on_dni_comprobar)

		# Guardar cliente
		self.ventMain.buttonGuardarCliente.clicked.connect(self.on_guardar_cliente)

		# Al seleccionar en el calendario, obtener fecha
		self.ventMain.buttonFechaAltaCliente.clicked.connect(self.on_abrir_calendario)
		self.dialogCalendar.dialogCalendar.calendarWidget.clicked.connect(self.on_seleccionar_fecha)

		# Limpiar
		self.ventMain.buttonLimpiarVehiculo.clicked.connect(self.limpiar)

		# Poner mayúsculas a todos
		self.camposMayusculas = [self.ventMain.txtMarca, self.ventMain.txtModelo,
								 self.ventMain.txtNombre, self.ventMain.txtDireccionCliente,
								 self.ventMain.txtDni]

		for campo in self.camposMayusculas:
			campo.editingFinished.connect(self.mayuscula_palabra)

		self.ventMain.txtMatricula.editingFinished.connect(self.mayuscula_palabra)

		self.bbdd = conexion.Conexion()
		self.bbdd.iniciar_conexion()
		self.cargar_provincias()
		self.cargar_tabla_vehiculos()

		# Al seleccionar una provincia, cargar sus municipios
		self.ventMain.comboProvinciaCliente.currentTextChanged.connect(self.cargar_municipios)

		# Al selecionar una fila de la tabla
		self.ventMain.tablaClientes.currentItemChanged.connect(self.on_item_seleccionado)

	def on_item_seleccionado(self, item: QtWidgets.QTableWidgetItem):
		dni = self.ventMain.tablaClientes.item(item.row(), 0)
		matricula = self.ventMain.tablaClientes.item(item.row(), 1)
		self.cargar_datos_cliente(dni.text())
		self.cargar_datos_vehiculo(matricula.text())

	def cargar_datos_cliente(self, dni: str):
		try:
			cliente: Cliente = self.bbdd.cargar_cliente(dni)
			self.ventMain.txtDni.setText(cliente.dni)
			self.ventMain.txtNombre.setText(cliente.nombre)
			self.ventMain.txtDireccionCliente.setText(cliente.direccion)
			self.ventMain.txtFechaAltaCliente.setText(cliente.alta)
			self.ventMain.comboProvinciaCliente.setCurrentText(cliente.provincia)
			self.ventMain.comboMunicipioCliente.setCurrentText(cliente.municipio)
			self.ventMain.checkEfectivo.setChecked(cliente.efectivo == 1)
			self.ventMain.checkFactura.setChecked(cliente.factura == 1)
			self.ventMain.checkTransferencia.setChecked(cliente.transferencia == 1)
		except Exception as error:
			print(f"Error cargando datos del cliente: {error}")

	def cargar_datos_vehiculo(self, matricula: str):
		try:
			vehiculo = self.bbdd.cargar_vehiculo(matricula)
			self.ventMain.txtMatricula.setText(vehiculo.matricula)
			self.ventMain.txtMarca.setText(vehiculo.marca)
			self.ventMain.txtModelo.setText(vehiculo.modelo)
			if vehiculo.motor == "Gasolina":
				self.ventMain.radioButtonGasolina.setChecked(True)
			elif vehiculo.motor == "Diesel":
				self.ventMain.radioButtonDiesel.setChecked(True)
			elif vehiculo.motor == "Híbrido":
				self.ventMain.radioButtonHibrido.setChecked(True)
			elif vehiculo.motor == "Eléctrico":
				self.ventMain.radioButtonElectrico.setChecked(True)
		except Exception as error:
			print(f"Error cargando datos del vehículo: {error}")

	def get_motor(self):
		try:
			return self.ventMain.buttonGroupMotorizacion.checkedButton().text()
		except Exception as error:
			print(f"Error seleccionando motor: {error}")

	def set_dni_valido(self, dni: str):
		self.ventMain.lblValidardni.setStyleSheet('color: green;')
		self.ventMain.lblValidardni.setText('V')
		self.ventMain.txtDni.setText(dni.upper())
		self.ventMain.txtDni.setStyleSheet('background-color: white;')

	def set_dni_invalido(self, dni: str):
		self.ventMain.lblValidardni.setStyleSheet('color: red;')
		self.ventMain.lblValidardni.setText('X')
		self.ventMain.txtDni.setText(dni.upper())
		self.ventMain.txtDni.setStyleSheet('background-color: pink;')

	def on_dni_comprobar(self):
		try:
			dni = self.ventMain.txtDni.text()
			if validar_dni(dni):
				self.set_dni_valido(dni)
			else:
				self.set_dni_invalido(dni)
		except Exception as error:
			print(f"Error mostrando marcado validez DNI: {error}")

	def on_press_salir(self):
		self.dialogSalir.mostrar_salir()

	def on_guardar_cliente(self):
		try:
			vm = self.ventMain
			cliente = Cliente(vm.txtDni.text(), vm.txtNombre.text(), vm.txtFechaAltaCliente.text(),
							  vm.txtDireccionCliente.text(), vm.comboProvinciaCliente.currentText(),
							  vm.comboMunicipioCliente.currentText(), vm.checkEfectivo.isChecked(),
							  vm.checkFactura.isChecked(), vm.checkTransferencia.isChecked())

			vehiculo = Vehiculo(vm.txtMatricula.text(), cliente.dni, vm.txtMarca.text(),
								vm.txtModelo.text(),
								self.get_motor())

			guardado = self.bbdd.guardar_cliente(cliente) and self.bbdd.guardar_vehiculo(vehiculo)

			if guardado:
				self.limpiar()
				self.cargar_tabla_vehiculos()
				modal.aviso("Guardado correctamente", "Se han guardado los datos correctamente")
			else:
				modal.aviso("Error guardando", "No se han podido guardar los datos")

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
		for campo in self.campos_texto:
			campo.setText(campo.text().title())
		self.ventMain.txtMatricula.setText(self.ventMain.txtMatricula.text().upper())

	def limpiar(self):
		try:
			for campo in self.campos_texto:
				campo.setText("")

			self.ventMain.comboProvinciaCliente.setCurrentIndex(0)

			for btn in self.ventMain.buttonGroupMotorizacion.buttons():
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

	def cargar_tabla_vehiculos(self):
		try:
			self.ventMain.tablaClientes.clearContents()
			datos = self.bbdd.cargar_vehiculos()
			self.ventMain.tablaClientes.setRowCount(len(datos))
			for idx, el in enumerate(datos):
				self.ventMain.tablaClientes.setItem(idx, 0, QtWidgets.QTableWidgetItem(el.dni))
				self.ventMain.tablaClientes.setItem(idx, 1,
													QtWidgets.QTableWidgetItem(el.matricula))
				self.ventMain.tablaClientes.setItem(idx, 2, QtWidgets.QTableWidgetItem(el.marca))
				self.ventMain.tablaClientes.setItem(idx, 3, QtWidgets.QTableWidgetItem(el.modelo))
				self.ventMain.tablaClientes.setItem(idx, 4, QtWidgets.QTableWidgetItem(el.motor))

			for i in range(0, self.ventMain.tablaClientes.columnCount()):
				self.ventMain.tablaClientes.horizontalHeader().setSectionResizeMode(i,
																					QtWidgets.QHeaderView.ResizeMode.Stretch)
				if i < 2:
					self.ventMain.tablaClientes.horizontalHeader().setSectionResizeMode(i,
																						QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
		except Exception as error:
			print(f"Error cargando tabla vehiculos: {error}")
