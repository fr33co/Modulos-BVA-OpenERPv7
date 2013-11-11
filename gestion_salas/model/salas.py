from openerp.osv import osv, fields

class registrar_salas(osv.Model):
	_name = "registrar.salas"
	_order = 'sala_nombre'
	_rec_name = 'sala_nombre'
	_columns = {
		'c_sala' : fields.char(string="Codigo de la Sala", size=8, readonly=False, required=True),
		'sala_nombre' : fields.char(string="Nombre de la Sala", size=35, required=True),
		'sede' : fields.many2one('sedes', 'Sede'),
		'estado' : fields.char(string="Estado", size=25),
		'ciudad' : fields.char(string="Ciudad", size=25),
		'municipio' : fields.char(string="Municipio", size=25),
		'parroquia' : fields.char(string="Parroquia", size=25),
		'sector' : fields.char(string="Sector", size=25),
		'direccion' : fields.char(string="Direccion", size=100, required=True),
		'observaciones' : fields.char(string="Observaciones"),		
	}