from openerp.osv import osv, fields
import random
class Distribucion(osv.Model):
    _name = "presupuesto.distribucion"



    _columns = {
        'proyecto': fields.related('accion','proyecto', type = 'many2one',relation = 'presupuesto.proyecto',string = 'Proyecto',required=True,),
        'codigo_accion' : fields.char(string="Codigo del Accion",size=2,readonly=True),
        'accion' : fields.many2one('presupuesto.accion','',ondelete='cascade',required=True),
        'partida' : fields.char(string="Partida Presupuestaria",size=12, required=True),
        'descripcion' : fields.char(string="",size=300, required=True),
        'monto_pre' : fields.float(string="Monto del Presupuesto",size=12, required=True),
        'aceptar' : fields.selection((('1','Ambos'), ('2','Compras'), ('3', 'Servicios')),'Aceptar orden de', required=True),
        'fecha' : fields.date(string="Fecha Apertura", required=True),
        'disponibilidad' : fields.integer(string="Disponibilidad Actual"),
    }


    def on_change_accion(self, cr, uid, ids, accion, context=None):
        values = {}
        if not accion:
            return values
        obj_accion = self.pool.get('presupuesto.accion').browse(cr, uid, accion, context=context)

        values.update({
                'codigo_accion' : obj_accion.codigo_accion,
        })
        values.update({
                'disponibilidad' : obj_accion.monto,
        })

        return {'value' : values}

    def on_change_partida(self, cr, uid, ids, partida, context=None):
        values = {}
        if not partida:
            return values
        obj_partida  = self.pool.get('presupuesto.partidas')
        srch_partida =  obj_partida.search(cr, uid, [('codigo','=', partida)])
        rd_partida   = obj_partida.read(cr, uid, srch_partida, context=context)
        descripcion  = rd_partida[0]['descripcion']
        values.update({
                'descripcion' : descripcion,
        })
        return {'value' : values}

    _order='codigo_accion'
    _rec_name='descripcion'

