class Factura:
	def __init__(self, fid, dni, matricula, fecha, emitida):
		self.fid = fid
		self.nif = dni
		self.matricula = matricula
		self.fecha = fecha
		self.emitida = emitida

	def __repr__(self):
		return f"Factura({self.fid}, {self.nif}, {self.matricula}, {self.fecha}, {self.emitida})"