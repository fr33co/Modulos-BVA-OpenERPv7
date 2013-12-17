from openerp.osv import osv, fields

class parroquias(osv.Model):
	_name = "parroquias"
	_order = 'parroquia'
	_rec_name = 'parroquia'
	_columns = {
		#'ciudad' :fields.many2one('ciudades', 'Ciudad'),
		'estado' : fields.related('municipio','estado', type ='many2one', relation ='estados', string = 'Estado', required=True),
		'municipio': fields.many2one('municipios', 'Municipio', required=True),
		#'municipio' : fields.char(string="Municipio", size=25, required=True),
		'parroquia' : fields.char(string="Parroquia", size=25, required=True),
		'codigo_p' : fields.char(string="Codigo de Parroquia", size=3, required=True),
	}