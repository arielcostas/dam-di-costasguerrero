from PyQt6 import QtWidgets

from ui.dlgTipoExportacion import Ui_dialogoTipoExportacion


class DialogoTipoExportacion(QtWidgets.QDialog):
	def __init__(self):
		super(DialogoTipoExportacion, self).__init__()
		self.ui = Ui_dialogoTipoExportacion()
		self.ui.setupUi(self)

		self.ui.buttonGuardar.clicked.connect(self.accept)
		self.ui.buttonCancelar.clicked.connect(self.reject)