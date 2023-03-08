class Factura:
	"""
	Representa el modelo Factura de la base de datos
	"""
	def __init__(self, fid, dni, matricula, fecha, emitida, descuento: float):
		self.fid = fid
		self.nif = dni
		self.matricula = matricula
		self.fecha = fecha
		self.emitida = emitida
		self.descuento = descuento

	def __repr__(self):
		return f"Factura({self.fid}, {self.nif}, {self.matricula}, {self.fecha}, {self.emitida})"