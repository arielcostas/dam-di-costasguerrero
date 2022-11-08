from datetime import *

from PyQt6 import QtWidgets, QtCore

from ui.dlgCalendario import Ui_dlgCalendario


class DialogCalendar(QtWidgets.QDialog):
	def __init__(self):
		super(DialogCalendar, self).__init__()
		self.dialogCalendar = Ui_dlgCalendario()
		self.dialogCalendar.setupUi(self)
		a = datetime.now()
		self.dialogCalendar.calendarWidget.setSelectedDate(QtCore.QDate(a.day, a.month, a.year))
