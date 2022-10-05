import sys

from PyQt6 import QtWidgets

from ui.dlgSalir import Ui_dlgSalir


class DialogSalir(QtWidgets.QDialog):
	def __init__(self):
		super(DialogSalir, self).__init__()
		self.dialogSalir = Ui_dlgSalir()
		self.dialogSalir.setupUi(self)

		self.dialogSalir.buttonSalir.clicked.connect(self.confirm_salir)  # Al confirmar que quiere salir
		self.dialogSalir.buttonCancelar.clicked.connect(self.cancel_salir)  # Al cancelar que quiere salir

	def mostrar_salir(self):
		self.show()

	def cancel_salir(self):
		self.hide()

	def confirm_salir(self):
		sys.exit()
