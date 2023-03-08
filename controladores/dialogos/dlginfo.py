import sys

from PyQt6 import QtWidgets

from ui.dlgAcercaDe import Ui_dlgAcercaDe
from ui.dlgSalir import Ui_dlgSalir


class DialogoInfo(QtWidgets.QDialog):
	"""
	Diálogo para mostrar información del programa
	"""
	def __init__(self):
		super(DialogoInfo, self).__init__()
		self.dialogoInfo = Ui_dlgAcercaDe()
		self.dialogoInfo.setupUi(self)

		self.dialogoInfo.buttonAceptar.clicked.connect(lambda: self.accept())
