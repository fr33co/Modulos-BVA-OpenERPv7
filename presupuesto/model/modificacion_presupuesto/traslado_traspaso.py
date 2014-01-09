from openerp.osv import osv, fields
import random
class Traslado(osv.Model):
    _name = "presupuesto.traslado"

    _order='tipo_doc'
    _rec_name='tipo_doc'

    _columns = {
        'tipo_doc' : fields.many2one('presupuesto.documento','Tipo Doc',ondelete='cascade',required=True,domain=[('tipo', '=', '1')]),
        'numero' : fields.char(string="Numero:",size=100, required=True),
        'fecha' : fields.date(string="Fecha:", required=True),
        'oficio' : fields.char(string="# Oficio:", required=True),
        'fecha_resolucion' : fields.date(string="Fecha de Resolucion:", required=True),
        'motivo' : fields.char(string="Motivo:", required=True),
        'categoria' : fields.char(string="Categoria:", required=True),
        'consulta_categoria' : fields.char(string="Consulta de Categoria:", required=True),
        'cod_presupuesto' : fields.char(string="Cod Presupuesto:", required=True),
        'monto_movi' : fields.float(string="Monto Movimiento:", required=True),
        'monto_movi1' : fields.float(string="Monto Movimiento:"),
        'aumen_dism': fields.selection([('aumento','Aumentar'),('disminuye','Disminuir')],'Aumentar Disminuir'),
        'disponibilidad' : fields.char(string="Disponibilidad:"),
    }

    def get_last_numero(self, cr, uid, ids, tipo_doc, context = None):
        values = {}
        if not tipo_doc:
            return values

        sfl_id   = self.pool.get('presupuesto.traslado')
        srch_id  = sfl_id.search(cr,uid,[('tipo_doc','=',tipo_doc)])
        rd_id    = sfl_id.read(cr, uid, srch_id, context=context)

        if not rd_id:
            str_number = '1'
            last_num = str_number.rjust(7,'0')
        else :
            last_num = rd_id[-1]['numero']
            last_num = last_num.lstrip('0')
            str_number = str(int(last_num) + 1)
            last_num = str_number.rjust(7,'0')

        values.update({'numero' : last_num})

        return {'value' : values}
