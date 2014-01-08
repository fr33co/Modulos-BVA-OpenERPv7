from openerp.osv import osv, fields
import random
class Documento(osv.Model):
    _name = "presupuesto.documento"

    _order='id_documento'
    _rec_name='documento'

    _columns = {
        'id_documento' : fields.char(string="Codigo del Documento:",size=100, required=True),
        'siglas' : fields.char(string="siglas del Documento:",size=6, required=True),
        'documento' : fields.char(string="Tipo de Documento:",size=100, required=True),
    }

    def on_change_documento(self, cr, uid, ids, id_documento, context=None):
        values = {}
        if not id_documento:
            return False
        sf_documento   = self.pool.get('presupuesto.documento')
        srch_documento = sf_documento.search(cr, uid, [('id_documento','=', id_documento)])
        rd_documento   = sf_documento.read(cr, uid, srch_documento, context=context)
        if not rd_documento:
            values.update({'siglas' : '','documento':''})
        else:
            siglas         = rd_documento[0]['siglas']
            documento      = rd_documento[0]['documento']
            values.update({'siglas' : siglas,'documento':documento})
        return {'value' : values}

    _defaults = {
           'id_documento': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'presupuesto.documento'),
    }