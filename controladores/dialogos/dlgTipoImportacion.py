from PyQt6 import QtWidgets

from ui.dlgTipoImportacion import Ui_dialogoTipoImportacion


class DialogoTipoImportacion(QtWidgets.QDialog):
	"""
	Dialogo para seleccionar los tipos de importación.
	"""
	def __init__(self, clientes: bool, vehiculos: bool):
		super(DialogoTipoImportacion, self).__init__()
		self.ui = Ui_dialogoTipoImportacion()
		self.ui.setupUi(self)

		self.ui.checkboxClientes.setEnabled(clientes)
		self.ui.checkboxCoches.setEnabled(vehiculos)

		self.ui.buttonImportar.clicked.connect(self.accept)
		self.ui.buttonCancelar.clicked.connect(self.reject)
