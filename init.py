import sys

from main import Main
from PyQt6 import QtWidgets

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	window = Main()
	window.show()
	sys.exit(app.exec())