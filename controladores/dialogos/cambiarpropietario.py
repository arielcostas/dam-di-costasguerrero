from PyQt6 import QtWidgets

from bbdd.modelos import Cliente, Vehiculo
from ui.dlgCambiarPropietario import Ui_dialogoCambiarPropietario


class DialogoCambiarPropietario(QtWidgets.QDialog):
	def __init__(self, clientes: list[Cliente], vehiculos: list[Vehiculo]):
		super().__init__()
		self.ui = Ui_dialogoCambiarPropietario()
		self.ui.setupUi(self)

		for cliente in clientes:
			self.ui.cliente.addItem(cliente.dni + " - " + cliente.nombre)

		for vehiculo in vehiculos:
			self.ui.vehiculo.addItem(vehiculo.matricula + " (" + vehiculo.marca + " " + vehiculo.modelo + ")")

		self.ui.buttonCambiar.clicked.connect(self.accept)
		self.ui.buttonCancelar.clicked.connect(self.reject)