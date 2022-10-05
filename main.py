from dialogsalir import DialogSalir
from ui.ventMain import *
from dni import validar as validar_dni


class Main(QtWidgets.QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		self.ventMain = Ui_ventMain()
		self.ventMain.setupUi(self)
		self.dialogSalir = DialogSalir()

		# Configurar que hacer cuando se pulsa salir
		self.ventMain.actionSalir.triggered.connect(self.on_press_salir)
		self.ventMain.toolbarSalir.triggered.connect(self.on_press_salir)

		# Configur evento cuando se pulsa 'Enter' en el campo DNI
		self.ventMain.txtDni.editingFinished.connect(self.on_dni_comprobar)

		# Configurar evento a llamar cuando se seleccione un radioButton de motor
		self.ventMain.btnGroupMotorizacion.buttonClicked.connect(self.on_motoroption_change)

	def on_motoroption_change(self):
		try:
			print(self.ventMain.btnGroupMotorizacion.checkedButton().text())
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
			print("Error mostrando marcado validez DNI: ", error)

	def on_press_salir(self):
		self.dialogSalir.mostrar_salir()