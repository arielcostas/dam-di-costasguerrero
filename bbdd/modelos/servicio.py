class Servicio:
	"""
	Representa el modelo Servicio de la base de datos
	"""
	def __init__(self, sid: int, nombre: str, precio_unitario: str, fecha_alta: str, fecha_modificacion: str, fecha_baja: str, stock: int, almacenable: bool):
		self.sid = sid
		self.nombre = nombre
		self.precio_unitario = precio_unitario
		self.fecha_alta = fecha_alta
		self.fecha_modificacion = fecha_modificacion
		self.fecha_baja = fecha_baja
		self.stock = stock
		self.almacenable = almacenable

	def __str__(self):
		return f"Servicio: {self.nombre} - {self.precio_unitario} - {self.fecha_alta}"