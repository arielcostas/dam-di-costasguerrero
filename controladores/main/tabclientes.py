from PyQt6 import QtWidgets

from controladores.main import cargar
from controladores.ventmain import Main


def init_tab(self: Main):
	self.ventMain.btnBusCar.clicked.connect(lambda: buscar_cli(self))


def buscar_cli(self: Main):
	input_dlg = QtWidgets.QInputDialog()
	if self.ultima_busqueda_car is None or self.ultima_busqueda_car == "":
		self.ultima_busqueda_car = ""

	texto, ok = input_dlg.getText(self, "Búsqueda de clientes", "Matrícula a buscar", QtWidgets.QLineEdit.EchoMode.Normal, self.ultima_busqueda_car)
	if not ok:
		return

	self.ultima_busqueda_car = texto

	cargar.tabla_vehiculos(self)