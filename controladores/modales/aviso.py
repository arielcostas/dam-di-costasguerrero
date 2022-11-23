from PyQt6 import QtWidgets


def info(titulo: str, texto: str) -> None:
	msg = QtWidgets.QMessageBox()
	msg.setModal(True)
	msg.setWindowTitle(titulo)
	msg.setIcon(msg.Icon.Information)
	msg.setText(texto)
	msg.exec()


def error(titulo: str, texto: str) -> None:
	msg = QtWidgets.QMessageBox()
	msg.setModal(True)
	msg.setWindowTitle(titulo)
	msg.setIcon(msg.Icon.Critical)
	msg.setText(texto)
	msg.exec()
