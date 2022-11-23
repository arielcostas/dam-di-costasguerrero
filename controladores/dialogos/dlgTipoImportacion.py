from PyQt6 import QtWidgets

from ui.dlgTipoExportacion import Ui_dialogoTipoExportacion


class DialogoTipoImportacion(QtWidgets.QDialog):
	def __init__(self, clientes: bool, vehiculos: bool):
		super(DialogoTipoImportacion, self).__init__()
		self.ui = Ui_dialogoTipoExportacion()
		self.ui.setupUi(self)

		self.ui.checkboxClientes.setEnabled(clientes)
		self.ui.checkboxCoches.setEnabled(vehiculos)

		self.ui.buttonGuardar.clicked.connect(self.accept)
		self.ui.buttonCancelar.clicked.connect(self.reject)
