from openerp.osv import osv, fields
import random
class Partidas(osv.Model):
    _name = "presupuesto.partidas"



    _columns = {
        'codigo' : fields.char(string="Codigo",size=20, required=True),
        'descripcion' : fields.text(string="Descripcion",size=300, required=True),

    }


    _order='codigo'
    _rec_name='descripcion'

