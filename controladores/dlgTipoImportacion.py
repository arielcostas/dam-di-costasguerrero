from PyQt6 import QtWidgets

from ui.dlgTipoImportacion import Ui_dialogoTipoImportacion


class DialogoTipoImportacion(QtWidgets.QDialog):
	def __init__(self):
		super(DialogoTipoImportacion, self).__init__()
		self.ui = Ui_dialogoTipoImportacion()
		self.ui.setupUi(self)

		self.ui.buttonImportar.clicked.connect(self.accept)
		self.ui.buttonCancelar.clicked.connect(self.reject)