from PyQt6 import QtWidgets


class DialogoAbrir(QtWidgets.QFileDialog):
	def __init__(self):
		super(DialogoAbrir, self).__init__()