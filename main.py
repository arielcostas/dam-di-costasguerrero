from ventMain import *
import sys,var,events


class Main(QtWidgets.QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		var.ui = Ui_ventMain()
		var.ui.setupUi(self)
		'''
		Listados de eventos
		'''
		var.ui.actionSalir.triggered.connect(events.Eventos.Salir)


if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	window = Main()
	window.show()
	sys.exit(app.exec())
