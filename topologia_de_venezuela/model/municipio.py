from openerp.osv import osv, fields

class municipios(osv.Model):
	_name = "municipios"
	_order = 'municipio'
	_rec_name = 'municipio'
	_columns = {
		#'estado' : fields.related('ciudad','estado', type ='many2one', relation ='estados', string = 'Estado'),
		#'ciudad' : fields.many2one('ciudades', 'Ciudad'),
		'estado' : fields.many2one('estados', 'Estado', required=True),
		'municipio' : fields.char(string="Municipio", size=35, required=True),
		'codigo_m' : fields.char(string="Codigo del Municipio", size=3, required=True),
	}
