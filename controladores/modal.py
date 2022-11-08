from PyQt6 import QtWidgets


def aviso(titulo, texto):
	msg = QtWidgets.QMessageBox()
	msg.setModal(True)
	msg.setWindowTitle(titulo)
	msg.setIcon(msg.Icon.Information)
	msg.setText(texto)
	msg.exec()