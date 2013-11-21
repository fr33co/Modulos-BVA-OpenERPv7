from openerp.osv import osv, fields

class Estado(osv.Model):
    _name = "configuracion.estado"

    _columns = {
        'estado' : fields.char(string="Estado",size=100, required=True),
    }
    _order='estado'
    _rec_name='estado'
