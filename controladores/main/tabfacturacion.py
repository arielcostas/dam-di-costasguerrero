from bbdd import VehiculoRepository, ClienteRepository
from controladores.ventmain import Main


def init_tab(self: Main):
	load_clientes(self)
	load_vehiculos(self)

def load_clientes(self: Main):
	self.ventMain.cmbFactCli.clear()
	self.ventMain.cmbFactCli.addItems(f"{c.dni} - {c.nombre}" for c in
									  ClienteRepository.get_all(False))

def load_vehiculos(self: Main):
	self.ventMain.cmbFactVeh.clear()
	self.ventMain.cmbFactCar.addItems(f"{v.matricula } - {v.marca} {v.modelo}" for v in
									  VehiculoRepository.get_all())
