def validar(dni):
	'''
	Función para comprbar si un DNI es válido
	:return: Si el DNI es válido
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
		print(f"Error validando DNI: {error}")