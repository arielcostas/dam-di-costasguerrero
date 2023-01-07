class Cliente:
	def __init__(self, dni, nombre, alta, direccion, provincia, municipio, efectivo, factura, transferencia):
		self.dni: str = dni
		self.nombre: str = nombre
		self.fecha_alta: str = alta
		self.direccion: str = direccion
		self.provincia: str = provincia
		self.municipio: str = municipio
		self.efectivo: bool = efectivo
		self.factura: bool = factura
		self.transferencia: bool = transferencia
