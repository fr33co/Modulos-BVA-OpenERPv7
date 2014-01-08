from openerp.osv import osv, fields
import random
class Proyecto(osv.Model):
    _name = "presupuesto.proyecto"



    _columns = {
        'codigo_proyecto' : fields.char(string="Codigo del Proyecto",size=100, required=True),
        'proyecto' : fields.char(string="Nombre del Proyecto",size=100, required=True),
        'monto' : fields.float(string="Monto",size=100, required=True),
        'descripcion' : fields.text(string="Descripcion",size=300, required=True),
    }


    _order='proyecto'
    _rec_name='proyecto'

