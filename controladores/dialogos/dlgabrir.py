from PyQt6 import QtWidgets


class DialogoAbrir(QtWidgets.QFileDialog):
	"""
	Dialogo para seleccionar ficheros.
	"""
	def __init__(self):
		super(DialogoAbrir, self).__init__()