from PyQt6 import QtWidgets

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
		self.ventMain.txtMarca.editingFinished.connect(self.mayuscula_palabra)
		self.ventMain.txtModelo.editingFinished.connect(self.mayuscula_palabra)
		self.ventMain.txtNombre.editingFinished.connect(self.mayuscula_palabra)
		self.ventMain.txtDireccionCliente.editingFinished.connect(self.mayuscula_palabra)
		self.ventMain.txtDni.editingFinished.connect(self.mayuscula_palabra)

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
			cliente = [
				self.ventMain.txtDni.text(),
				self.ventMain.txtMatricula.text(),
				self.ventMain.txtMarca.text(),
				self.ventMain.txtModelo.text(),
				self.get_motor()
			]

			tabla = self.ventMain.tablaClientes
			row_position = tabla.rowCount()
			tabla.insertRow(row_position)
			tabla.setItem(row_position, 0, QtWidgets.QTableWidgetItem(cliente[0]))
			tabla.setItem(row_position, 1, QtWidgets.QTableWidgetItem(cliente[1]))
			tabla.setItem(row_position, 2, QtWidgets.QTableWidgetItem(cliente[2]))
			tabla.setItem(row_position, 3, QtWidgets.QTableWidgetItem(cliente[3]))
			tabla.setItem(row_position, 4, QtWidgets.QTableWidgetItem(cliente[4]))

		except Exception as error:
			print(f"Error en carga cliente: {error}")

	def on_abrir_calendario(self):
		print(self.dialogCalendar)
		self.dialogCalendar.show()

	def on_seleccionar_fecha(self):
		qDate = self.dialogCalendar.dialogCalendar.calendarWidget.selectedDate()
		try:
			data = f"{qDate.day()}/{qDate.month()}/{qDate.year()}"
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


	def on_limpiar(self):
		try:
			self.ventMain.txtDni.setText("")
			self.ventMain.txtDni.setText("")
			self.ventMain.txtFechaAltaCliente.setText("")
			self.ventMain.txtDireccionCliente.setText("")
			self.ventMain.txtMatricula.setText("")
			self.ventMain.txtMarca.setText("")
			self.ventMain.txtModelo.setText("")

			self.ventMain.comboMunicipioCliente.setCurrentIndex(0)
			self.ventMain.comboProvinciaCliente.setCurrentIndex(0)

			for btn in self.ventMain.btnGroupPago.buttons():
				btn.setChecked(False)

			self.ventMain.radioButtonGasolina.setChecked(True)
		except Exception as error:
			print(f"Error limpiando cliente: {error}")