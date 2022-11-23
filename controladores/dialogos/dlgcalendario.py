from datetime import *

from PyQt6 import QtWidgets, QtCore

from ui.dlgCalendario import Ui_dlgCalendario


class DialogoCalendario(QtWidgets.QDialog):
	def __init__(self):
		super(DialogoCalendario, self).__init__()
		self.dialogCalendar = Ui_dlgCalendario()
		self.dialogCalendar.setupUi(self)
		a = datetime.now()
		self.dialogCalendar.calendarWidget.setSelectedDate(QtCore.QDate(a.day, a.month, a.year))
