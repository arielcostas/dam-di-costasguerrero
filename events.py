import sys


class Eventos:
	def Salir(self):
		try:
			sys.exit()
		except Exception as e:
			print(f"Error al aslir {str(e)}")
