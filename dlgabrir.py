from PyQt6 import QtWidgets


class FileDialogAbrir(QtWidgets.QFileDialog):
	def __init__(self):
		super(FileDialogAbrir, self).__init__()