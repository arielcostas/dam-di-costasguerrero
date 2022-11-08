import sys

from controladores.ventmain import Main
from PyQt6 import QtWidgets, QtGui

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	icon = QtWidgets.QFileIconProvider()
	app.setWindowIcon(QtGui.QIcon("img/logo.png"))
	window = Main()
	window.show()
	sys.exit(app.exec())