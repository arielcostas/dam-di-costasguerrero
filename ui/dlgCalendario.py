# Form implementation generated from reading ui file 'C:/Users/a21arielcg/PycharmProjects/costasguerrero/ui/dlgCalendario.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgCalendario(object):
    def setupUi(self, dlgCalendario):
        dlgCalendario.setObjectName("dlgCalendario")
        dlgCalendario.resize(280, 175)
        dlgCalendario.setMinimumSize(QtCore.QSize(280, 175))
        dlgCalendario.setMaximumSize(QtCore.QSize(280, 175))
        self.centralwidget = QtWidgets.QWidget(dlgCalendario)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 280, 175))
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 280, 175))
        self.calendarWidget.setMinimumSize(QtCore.QSize(280, 175))
        self.calendarWidget.setMaximumSize(QtCore.QSize(280, 175))
        self.calendarWidget.setFirstDayOfWeek(QtCore.Qt.DayOfWeek.Monday)
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendarWidget.setObjectName("calendarWidget")

        self.retranslateUi(dlgCalendario)
        QtCore.QMetaObject.connectSlotsByName(dlgCalendario)

    def retranslateUi(self, dlgCalendario):
        _translate = QtCore.QCoreApplication.translate
        dlgCalendario.setWindowTitle(_translate("dlgCalendario", "Calendario"))
