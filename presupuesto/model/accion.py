from openerp.osv import osv, fields
import random
class Estado(osv.Model):
    _name = "presupuesto.accion"



    _columns = {
    'proyecto' : fields.many2one('presupuesto.proyecto','Proyecto',ondelete='cascade',required=True),
    #'codigo_proyecto' : fields.char(string="Codigo del Proyecto",size=100, readonly=True),
    'codigo_accion' : fields.char(string="Codigo de Accion",size=100, required=True),
    'siglas' : fields.char(string="Siglas",size=300, required=True),
    'descripcion' : fields.text(string="Descripcion",size=300, required=True),
    'unidad' : fields.char(string="Unidad Ejecutora",size=100, required=True),
    'monto' : fields.float(string="Monto",size=100, required=True),
    }

    def on_change_proyecto(self, cr, uid, ids, proyecto, context=None):
        values = {}
        if not proyecto:
            return values
        proyecto = self.pool.get('presupuesto.proyecto').browse(cr, uid, proyecto, context=context)
        values.update({
                'codigo_proyecto' : proyecto.codigo_proyecto+'-',
        })
        return {'value' : values}

    _order='codigo_proyecto'
    _rec_name='proyecto'

