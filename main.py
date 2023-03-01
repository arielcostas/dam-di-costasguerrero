import sys

from PyQt6 import QtWidgets, QtGui

from controladores.ventmain import Main

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	icon = QtWidgets.QFileIconProvider()
	app.setWindowIcon(QtGui.QIcon("img/logo.png"))
	app.setApplicationName("Talleres Teis")
	app.setOrganizationName("Teis")
	app.setApplicationDisplayName("Talleres Teis")

	window = Main()

	window.show()
	sys.exit(app.exec())
