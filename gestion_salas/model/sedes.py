from openerp.osv import osv, fields

class registrar_sede(osv.Model):
	_name = "sedes2"
	_order = 'sede'
	_rec_name = 'sede'
	_columns = {
        'c_sede' : fields.char(string="Codigo de Sede", size=25, readonly=True, required=True),
        'sede' : fields.char(string="Sede", size=45, required=True),
        #'estado' : fields.many2one('estados', 'Estado', size=25, required=False),
        #'ciudad' : fields.many2one('ciudades', 'Ciudad', required=False),
        'municipio' : fields.char('Municipio', readonly=False,  required=True),
        'parroquia' : fields.char(string="Parroquia", size=25, required=False),
        'sector' : fields.char(string="Sector", size=25, required=False),
        'direccion' : fields.char(string="Direccion", size=150, required=True),
        'descripcion_s' : fields.text(string="Descripcion de la Sede"),
        'ciudad' : fields.char(string="Ciudad", size=25, required=True),
        'estado' : fields.char(string="Estado", size=25, required=True),
        'telefono' : fields.char(string="Telefono", size=11),
        }
        _defaults= {
        'c_sede': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'sedes2'),
        } 