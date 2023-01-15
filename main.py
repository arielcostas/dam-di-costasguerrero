import os
import sys

from PyQt6.QtGui import QFontDatabase

from controladores.ventmain import Main
from PyQt6 import QtWidgets, QtGui

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	icon = QtWidgets.QFileIconProvider()
	app.setWindowIcon(QtGui.QIcon("img/logo.png"))
	app.setApplicationName("Talleres Teis")
	app.setOrganizationName("Teis")
	app.setApplicationDisplayName("Talleres Teis")

	for font in os.listdir("fonts"):
		QFontDatabase.addApplicationFont(f"fonts/{font}")
	app.setFont(QtGui.QFont("Manrope", 9))
	window = Main()
	window.show()
	sys.exit(app.exec())