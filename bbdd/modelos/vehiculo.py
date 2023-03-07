class Vehiculo:
	"""
	Representa el modelo Vehiculo de la base de datos
	"""
	def __init__(self, matricula, cliente, marca, modelo, motor, fecha_baja=None):
		self.matricula = matricula
		self.dni = cliente
		self.marca = marca
		self.modelo = modelo
		self.motor = motor
		self.fecha_baja = fecha_baja