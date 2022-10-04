import var


class Clientes:
	def validar_dni(self, dni):
		'''
		Módulo para validar el DNI
		:return:
		'''
		try:
			tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
			dig_ext = 'XYZ'
			reemplazar_dig_ext = {"X": 0, "Y": 1, "Z": 2}
			numeros = "1234567890"
			if len(dni) == 9:
				digito_control = dni[8]
				dni = dni[:8]
				if dni[0] in dig_ext:  # Es extranjero
					dni = dni.replace(dni[0], reemplazar_dig_ext[dni[0]])
				return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == digito_control
			return False
		except Exception as error:
			print(f"Error validando DNI: {error}", )

	def mostrar_valido_dni(self=None):
		try:
			dni = var.ui.txtDni.text()
			if Clientes.validar_dni(self, dni):
				var.ui.lblValidardni.setStyleSheet('color: green;')
				var.ui.lblValidardni.setText('V')
				var.ui.txtDni.setText(dni.upper())
				var.ui.txtDni.setStyleSheet('background-color: white;')
			else:
				var.ui.lblValidardni.setStyleSheet('color: red;')
				var.ui.lblValidardni.setText('X')
				var.ui.txtDni.setText(dni.upper())
				var.ui.txtDni.setStyleSheet('background-color: pink;')

		except Exception as error:
			print("Error mostrando marcado validez DNI: ", error)

	def selMotor(self=None):
		try:
			#var.motor = (var.ui.radioButtonGasolina, var.ui.radioButtonDiesel, var.ui.radioButtonHibrido,
			#			 var.ui.radioButtonElectrico)
			#for i in var.motor:
			#	i.toggled.connect(Clientes.checkMotor)
			var.ui.btnGroupMotorizacion.buttonClicked.connect(Clientes.checkMotor)
		except Exception as error:
			print(f"Error selección motor {error}")

	def checkMotor(self=None):
		try:
			#print(var.ui.btnGroupMotorizacion.checkedButton().text())
			if var.ui.radioButtonGasolina.isChecked():
				print("Gasolina")
			elif var.ui.radioButtonGasolina.isChecked():
				print("Diesel")
			elif var.ui.radioButtonHibrido.isChecked():
				print("Hibrido")
			elif var.ui.radioButtonElectrico.isChecked():
				print("Electrico")
			else:
				pass
		except Exception as error:
			print(f"Error seleccionando motor: {error}")
