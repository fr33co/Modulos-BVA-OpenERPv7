from openerp.osv import osv, fields

class ciudades(osv.Model):
	_name = "ciudades"	
	_order = 'ciudad'
	_rec_name = 'ciudad'
	_columns = {
		'ciudad' : fields.char(string="Ciudad", size=25, required=True),
		'codigo_c' : fields.char(string="Codigo de Ciudad", size=3, required=True),
		'estado' :fields.many2one('estados', 'Estado'),
	}
	_sql_constraints = [
        ('ciudad_unique','UNIQUE(ciudad)','Ya existe esa ciudad'),
    ]