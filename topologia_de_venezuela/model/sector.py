from openerp.osv import osv, fields

class sectores(osv.Model):
	_name = "sectores"
	_order = 'sector'
	_rec_name = 'sector'
	_columns = {
		'estado' : fields.related('municipio','estado', type ='many2one', relation ='estados', string = 'Estado', required=True),
		'ciudad' :fields.many2one('ciudades', 'Ciudad', required=True),
		'municipio' : fields.related('parroquia','municipio', type ='many2one', relation ='municipios', string = 'Municipio', required=True),
		'parroquia' : fields.char(string="Parroquia", size=25, required=True),
		'sector' : fields.char(string="sector", size=25, required=True),
		'codigo_s' : fields.char(string="Codigo del Sector", size=3, required=True),
	}