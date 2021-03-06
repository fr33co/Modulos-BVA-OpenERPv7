from openerp.osv import osv, fields
class CreditosMovimientos(osv.Model):
    """
     Crear el objeto 'presupuesto.creditos_movimientos'
    """

    _name = "presupuesto.creditos_movimientos"
     

    _order    ='cod_presupuesto'
    _rec_name ='cod_presupuesto'

    """
        Declaracion de las Columnas para el xmly la base de datos
    """

    _columns = {
        # Campo que genera una lista desplegable del Proyecto Accion generados en el modulo de  Proyecto Accion
        'credito' : fields.many2one("presupuesto.creditos","Creditos",required=False),
        'cod_presupuesto' : fields.char(string="Cod Presupuestario:", required=True),
        'par_presu' : fields.many2one('presupuesto.partidas','Partida',ondelete='cascade',required=True,),
        'monto' : fields.float(string="Monto:",),
        'disponibilidad' : fields.char(string="Disponibilidad:",readonly=True),
    }
    
    def on_change_partida(self, cr, uid, ids, partida,tipo, context=None):
        valores = {}
        values  = {}
        id_part = 0
        partida_presupuestaria = False
        monto = 0.00
        mensaje = ''
        if not partida:
            return values

        sfl_distribucion = self.pool.get('presupuesto.distribucion')
        sfl_partida      = self.pool.get('presupuesto.partidas')

        if tipo == 'cod_presupuesto':

            srcnt_partida = sfl_partida.search_count(cr, uid, [('codigo','=', partida)], context=None)
            if srcnt_partida > 0:
                srch_partida = sfl_partida.search(cr, uid, [('codigo','=', partida)])
                rd_partida   = sfl_partida.read(cr, uid, srch_partida, context=context)
                id_partida   = rd_partida[0]['id']

                srcnt_istribucion = sfl_distribucion.search_count(cr, uid, [('partida','=', partida)], context=None)
                if srcnt_istribucion > 0:
                    srch_distribucion = sfl_distribucion.search(cr, uid, [('partida','=', partida)])
                    rd_distribucion   = sfl_distribucion.read(cr, uid, srch_distribucion,['monto_pre'], context=context)
                    monto             = rd_distribucion[0]['monto_pre']

                    valores = {'par_presu' : id_partida,'disponibilidad':monto}
                    values.update(valores)

                else:
                    mensaje = {'title':'ERROR','message':'La Partida Presupuestaria no existe o no contiene fondos '}        
                    valores = {'par_presu' : id_part,'disponibilidad':monto}
                    values.update(valores)
        else:
            brw_partida    = sfl_partida.browse(cr, uid, partida, context=context)
            rd_partida     = sfl_partida.read(cr, uid, brw_partida.id,['codigo'], context=context)
            codigo_partida = rd_partida['codigo']

            srcnt_distribucion = sfl_distribucion.search_count(cr, uid, [('partida','=', codigo_partida)], context=None)
            if srcnt_distribucion > 0:
                srch_distribucion = sfl_distribucion.search(cr, uid, [('partida','=', codigo_partida)])
                rd_distribucion   = sfl_distribucion.read(cr, uid, srch_distribucion,['monto_pre'], context=context)
                monto             = rd_distribucion[0]['monto_pre']

                valores = {'cod_presupuesto' : codigo_partida,'disponibilidad':monto}
                values.update(valores)
            else:
                mensaje = {'title':'ERROR','message':'La Partida Presupuestaria no contiene fondos '}        
                valores = {'cod_presupuesto' : '','disponibilidad':monto}
                values.update(valores)
        return {'value' : values,'warning':mensaje}