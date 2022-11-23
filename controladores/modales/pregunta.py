from PyQt6 import QtWidgets


class CuadroPreguntaSiNo:

	def __init__(self, titulo, mensaje):
		self.titulo = titulo
		self.mensaje = mensaje

	def mostrar(self) -> bool:
		box = QtWidgets.QMessageBox()

		result = QtWidgets.QMessageBox.question(None, self.titulo, self.mensaje) == QtWidgets.QMessageBox.StandardButton.Yes
		return result