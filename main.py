import clientes
from ventMain import *
import sys, var, events
from PyQt6 import *


class Main(QtWidgets.QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		var.ui = Ui_ventMain()
		var.ui.setupUi(self)
		'''
		Listados de eventos
		'''
		var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
		var.ui.txtDni.editingFinished.connect(lambda: clientes.Clientes.mostrar_valido_dni())
		'''
		Seleccionar motor
		'''
		clientes.Clientes.selMotor()


if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	window = Main()
	window.show()
	sys.exit(app.exec())
