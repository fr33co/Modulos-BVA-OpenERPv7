from openerp.osv import osv, fields

class estado(osv.Model):
	_name = "estados"
	_order = 'estado'
	_rec_name = 'estado'
	_columns = {
		'estado' : fields.char(string="Estado", size=25, required=True),
		'codigo_e' : fields.char(string="Codigo del Estado", size=2, required=True),
	}
	
	_sql_constraints = [
        ('estado_unique','UNIQUE(estado)','Ese Estado ya existe'),
    ]