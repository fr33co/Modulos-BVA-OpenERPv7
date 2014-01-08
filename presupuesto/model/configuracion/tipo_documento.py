from openerp.osv import osv, fields
import random
class Documento(osv.Model):
    _name = "presupuesto.documento"

    _order='id_documento'
    _rec_name='documento'

    _columns = {
        'id_documento' : fields.char(string="Codigo del Documento:",size=100),
        'siglas' : fields.char(string="Siglas del Documento:",size=6, required=True),
        'documento' : fields.char(string="Tipo de Documento:",size=100, required=True),
        'tipo' : fields.selection((('1','Traspaso/Traslado'), ('2','Creditos Adiconales')),'Tipo', required=True),
    }

    def _get_last_id(self, cr, uid, ids, context = None):

        cr.execute("SELECT LTRIM(MAX(id_documento),'0') AS ultimo_id  FROM presupuesto_documento")
        last_id = cr.fetchone()[0]
        if last_id is None :
             str_number = str(1)
             last_id = str_number.rjust(6,'0')
             return last_id
        else :
             str_number = str(int(last_id) + 1)
             last_id = str_number.rjust(6,'0')
             return last_id
    _defaults = {
        'id_documento' : _get_last_id
    }