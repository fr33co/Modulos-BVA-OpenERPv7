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
        # _defaults= {
        # 'c_sede': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'sedes2'),
        # } 

        def _get_last_id(self, cr, uid, ids, context = None):

                sfl_id       = self.pool.get('sedes2')
                srch_id      = sfl_id.search(cr,uid,[])
                rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
                if rd_id:
                    id_documento = rd_id[-1]['c_sede']
                    c_sede = id_documento[2:]
                    last_id      = c_sede.lstrip('0')
                    str_number   = str(int(last_id) + 1)
                    last_id      = str_number.rjust(5,'0')
                    codigo      = 'BV'+last_id
                else :
                    str_number = '1'
                    last_id      = str_number.rjust(5,'0')
                    codigo      = 'BV'+last_id
                return codigo

        _defaults = {
                'c_sede' : _get_last_id
        }