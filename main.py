import os
import sys

from PyQt6.QtGui import QFontDatabase

from qt_material import apply_stylesheet

from controladores.ventmain import Main
from PyQt6 import QtWidgets, QtGui

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
