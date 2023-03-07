import sys

from PyQt6 import QtWidgets, QtGui

from controladores.ventmain import Main


def main():
	"""
	Método principal de la aplicación

	:return: None
	"""
	app = QtWidgets.QApplication([])
	icon = QtGui.QIcon("img/logo.png")
	app.setWindowIcon(icon)
	app.setApplicationName("Talleres Teis")
	app.setOrganizationName("Teis")
	app.setApplicationDisplayName("Talleres Teis")

	window = Main()
	window.setWindowIcon(icon)

	window.show()
	sys.exit(app.exec())


if __name__ == "__main__":
	main()
