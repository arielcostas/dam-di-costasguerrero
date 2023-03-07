from PyQt6 import QtWidgets


class CuadroPreguntaSiNo:
	"""
	Hace una pregunta al usuario de Sí o No y espera una respuesta
	"""
	def __init__(self, titulo, mensaje):
		self.titulo = titulo
		self.mensaje = mensaje

	def mostrar(self) -> bool:
		"""
		Muestra el cuadro de pregunta y espera una respuesta
		:return: True si la respuesta es afirmativa, False en caso contrario
		"""
		return QtWidgets.QMessageBox.question(
			None, self.titulo,
			self.mensaje
		) == QtWidgets.QMessageBox.StandardButton.Yes
