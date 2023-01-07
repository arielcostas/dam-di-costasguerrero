from PyQt6.QtWidgets import QMessageBox

from bbdd import ClienteRepository, conexion, VehiculoRepository
from controladores.modales import aviso
from controladores.dialogos import DialogoCalendario
from bbdd.modelos import Cliente, Vehiculo
from servicios import ServicioBackup, validar as validar_dni, ServicioPropietarios
from ui.ventMain import *


class Main(QtWidgets.QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		self.servicioBackup = ServicioBackup()
		self.servicioPropietarios = ServicioPropietarios()

		self.ventMain = Ui_ventMain()
		self.ventMain.setupUi(self)

		self.dialogCalendar = DialogoCalendario()

		# Guarda todos los campos de texto para uso en otros métodos
		self.campos_texto = [self.ventMain.txtDni, self.ventMain.txtNombre,
							 self.ventMain.txtDireccionCliente,
							 self.ventMain.txtFechaAltaCliente, self.ventMain.txtMatricula,
							 self.ventMain.txtMarca,
							 self.ventMain.txtModelo]

		# Botones de la barra de herramientas
		from .main import actions, cargar, tabservicios

		self.ventMain.actionSalir.triggered.connect(lambda: actions.salir())
		self.ventMain.actionHacerCopia.triggered.connect(lambda: actions.exportar_copia(self))
		self.ventMain.actionRestaurarCopia.triggered.connect(lambda: actions.importar_copia(self))
		self.ventMain.actionExportarExcel.triggered.connect(lambda: actions.exportar_excel(self))
		self.ventMain.actionImportarExcel.triggered.connect(lambda: actions.importar_excel(self))
		self.ventMain.actionCambiarPropietario.triggered.connect(lambda: actions.cambiar_propietario(self))
		self.ventMain.actionBajaCliente.triggered.connect(self.on_borrar_cliente_coche)

		# Se pulsa enter en DNI
		self.ventMain.txtDni.editingFinished.connect(self.on_dni_comprobar)

		# Guardar y eliminar clientes
		self.ventMain.buttonGuardarCliente.clicked.connect(self.on_guardar_cliente)
		self.ventMain.buttonEliminarCliente.clicked.connect(self.on_borrar_coche)

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

		conexion.abrir()
		cargar.lista_provincias(self)
		cargar.tabla_vehiculos(self)

		self.ventMain.comboProvinciaCliente.currentTextChanged.connect(
			lambda: cargar.lista_municipios(self)
		)

		# Al selecionar una fila de la tabla
		self.ventMain.tablaClientes.currentItemChanged.connect(self.on_item_seleccionado)

		self.ventMain.checkMostrarHistorico.stateChanged.connect(lambda: cargar.tabla_vehiculos(self))

		tabservicios.init_tab(self)



	def on_item_seleccionado(self, item: QtWidgets.QTableWidgetItem):
		if item is not None:
			dni = self.ventMain.tablaClientes.item(item.row(), 0)
			matricula = self.ventMain.tablaClientes.item(item.row(), 1)
			self.cargar_datos_cliente(dni.text())
			self.cargar_datos_vehiculo(matricula.text())

	def cargar_datos_cliente(self, dni: str):
		try:
			cliente: Cliente = ClienteRepository.get_by_dni(dni)
			self.ventMain.txtDni.setText(cliente.dni)
			self.ventMain.txtDni.setDisabled(True)
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
			vehiculo = VehiculoRepository.get_by_id(matricula)
			self.ventMain.txtMatricula.setText(vehiculo.matricula)
			self.ventMain.txtMatricula.setDisabled(True)
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
		self.ventMain.lblValidardni.setText('✅')
		self.ventMain.txtDni.setText(dni.upper())

	def set_dni_invalido(self, dni: str):
		self.ventMain.lblValidardni.setText('❌')
		self.ventMain.txtDni.setText(dni.upper())

	def on_dni_comprobar(self):
		try:
			dni = self.ventMain.txtDni.text()
			if validar_dni(dni):
				self.set_dni_valido(dni)
			else:
				self.set_dni_invalido(dni)
		except Exception as error:
			print(f"Error mostrando marcado validez DNI: {error}")

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

			if not validar_dni(cliente.dni):
				self.set_dni_invalido(cliente.dni)
				aviso.error("Error guardando", "DNI no válido")
				return

			guardado = ClienteRepository.insert(cliente) and VehiculoRepository.insert(vehiculo)

			if guardado:
				self.limpiar()

				from controladores.main import cargar
				cargar.tabla_vehiculos(self)

				aviso.info("Guardado correctamente", "Se han guardado los datos correctamente")
			else:
				aviso.error("Error guardando", "No se han podido guardar los datos")

		except Exception as error:
			print(f"Error guardando: {error}")
			aviso.error("Error guardando", "No se han podido guardar los datos")

	def on_borrar_coche(self):
		from controladores.main import cargar
		try:
			matricula = self.ventMain.txtMatricula.text()
			# TODO: Mover a otro sitio
			borrar = QMessageBox.question(None, 'Borrar vehículo',
										  f"¿Estás seguro de borrar el vehículo {matricula}?",
										  QMessageBox.StandardButton.Yes |
										  QMessageBox.StandardButton.No,
										  QMessageBox.StandardButton.No)

			if borrar == QMessageBox.StandardButton.Yes:
				if VehiculoRepository.delete(matricula):
					self.limpiar()
					cargar.tabla_vehiculos(self)
					aviso.info("Borrado correctamente", "Se ha borrado el vehículo correctamente")
		except Exception as error:
			print(f"Error borrando coche: {error}")

	def on_borrar_cliente_coche(self):
		from controladores.main import cargar
		try:
			dni = self.ventMain.txtDni.text()
			# TODO: Mover a otro sitio
			borrar = QMessageBox.question(None, 'Borrar vehículo',
										  f"¿Estás seguro de borrar al cliente {dni} y todos sus vehículos?",
										  QMessageBox.StandardButton.Yes |
										  QMessageBox.StandardButton.No,
										  QMessageBox.StandardButton.No)

			if borrar == QMessageBox.StandardButton.Yes:
				q1e = VehiculoRepository.delete_by_dni(dni)
				q2e = ClienteRepository.delete_by_dni(dni)

				if q1e and q2e:
					self.limpiar()
					cargar.tabla_vehiculos(self)
					aviso.info("Borrado correctamente", "Se ha borrado el cliente y sus vehículos correctamente")
		except Exception as error:
			print(f"Error borrando cliente y coches: {error}")

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

			self.ventMain.txtMatricula.setDisabled(False)
			self.ventMain.txtDni.setDisabled(False)
			self.ventMain.comboProvinciaCliente.setCurrentIndex(0)

			for btn in self.ventMain.buttonGroupMotorizacion.buttons():
				btn.setChecked(False)

			self.ventMain.radioButtonGasolina.setChecked(True)
		except Exception as error:
			print(f"Error limpiando cliente: {error}")
