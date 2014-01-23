from openerp.osv import osv, fields
import random
class CreditosAdiconales(osv.Model):
    _name = "presupuesto.creditos"

    _order='id_tipo_doc'
    _rec_name='id_tipo_doc'

    _columns = {
        'id_tipo_doc' : fields.many2one('presupuesto.documento','Tipo Doc',ondelete='cascade',required=True,domain=[('tipo', '=', '2')]),
        'numero' : fields.char(string="Numero:",size=100, required=True),
        'fecha' : fields.date(string="Fecha:", required=True),
        'oficio' : fields.char(string="# Oficio:", required=True),
        'fecha_oficion' : fields.date(string="Fecha de Oficio:", required=True),
        'observacion' : fields.char(string="Motivo:", required=True),
        'proyecto_accion' : fields.char(string="Proyecto Accion",size=100, required=True),
        'id_proyecto_accion' : fields.many2one('presupuesto.accion','Consulta Proyecto Accion:',ondelete='cascade',required=True),
        'cod_presupuesto' : fields.char(string="Cod Presupuestario",size=100, required=True),
        'desc_presupuesto' : fields.char(string="Desc Presupuesto:",size=100),
        'disponibilidad' : fields.char(string="Disponibilidad:"),
    }

    def get_last_numero(self, cr, uid, ids, id_tipo_doc, context = None):
        values = {}
        vlores = {}
        if not id_tipo_doc:
            return values

        sfl_last_num   = self.pool.get('presupuesto.creditos')
        srch_last_num  = sfl_last_num.search(cr,uid,[('id_tipo_doc','=',id_tipo_doc)],offset=0,limit=1,order='numero desc')
        rd_last_num    = sfl_last_num.read(cr, uid, srch_last_num,['numero'],context=context)
        
        if not rd_last_num:
            str_number = '1'
            last_num   = str_number.rjust(7,'0')
        else :
            last_num   = rd_last_num[0]['numero']
            last_num   = last_num.lstrip('0')
            str_number = str(int(last_num) + 1)
            last_num   = str_number.rjust(7,'0')

        valores = {'numero' : last_num}

        values.update(valores)

        return {'value' : values}

    def on_change_accion(self, cr, uid, ids, accion,tipo,context=None):
        values    = {}
        valores   = {}
        id_accion = 0
        mensaje   = ''
        if not accion:
            return values

        # obtener los registros del modelo
        sfl_accion = self.pool.get('presupuesto.accion')

        if tipo == 'cod_accion':
            #validar si viene por el campo de texto 'codigo_proyecto_accion'
            
            #verificar si exusten registros segun el crieterio de busqueda
            srcnt_accion = sfl_accion.search_count(cr, uid, [('codigo_accion','=', accion)], context=None)
            if srcnt_accion  > 0:
                #buscar los registros segun el criterio de busqueda 
                srch_accion = sfl_accion.search(cr, uid, [('codigo_accion','=', accion)])

                #leer los registros obtenidos a traves del metodo search
                rd_accion   = sfl_accion.read(cr, uid, srch_accion, context=context)
                id_accion   = rd_accion[0]['id']
            else:
                # si no existen registro generar un error 
                mensaje = {'title':'ERROR','message':'Este codigo de proyecto no esta registrado indique un codigo registrado'}

            valores   = {'id_proyecto_accion' : id_accion}
        else:
            print accion
            # si selecciona en la lista buscamos solamente el codigo de de la accion seleccionada
            brw_accion  = sfl_accion.browse(cr, uid, accion, context=context)
            if brw_accion != False:
                id_accion = brw_accion.codigo_accion
            valores   = {'proyecto_accion' : id_accion}

        values.update(valores)
        return {'value' : values,'warning':mensaje}

    def on_change_partida(self, cr, uid, ids, partida, context=None):
        valores = {}
        values  = {}
        id_part = 0
        partida_presupuestaria = False
        monto = 0.00
        mensaje = ''
        if not partida:
            return values
       
        sfl_distribucion   = self.pool.get('presupuesto.distribucion')

        srcnt_distribucion = sfl_distribucion.search_count(cr, uid, [('partida','=', partida)], context=None)
 
        if srcnt_distribucion > 0:

            srch_distribucion = sfl_distribucion.search(cr, uid, [('partida','=', partida)])
            rd_distribucion   = sfl_distribucion.read(cr, uid, srch_distribucion,['monto_pre'], context=context)

            monto = rd_distribucion[0]['monto_pre']

            sfl_partida   = self.pool.get('presupuesto.partidas')

            srcnt_partida = sfl_partida.search_count(cr, uid, [('codigo','=', partida)], context=None)

            if srcnt_partida > 0:
                srch_partida = sfl_partida.search(cr, uid, [('codigo','=', partida)])
                rd_partida   = sfl_partida.read(cr, uid, srch_partida, context=context)

                partida_presupuestaria = rd_partida[0]['descripcion']

                rd_descripcion    = sfl_distribucion.read(cr, uid, srch_distribucion,['monto_pre'], context=context)

        else:
            mensaje = {'title':'ERROR','message':'La Partida Presupuestaria no existe o no tiene fondos suficientes'}        
        valores = {'desc_presupuesto' : partida_presupuestaria,'disponibilidad':monto}

        values.update(valores)
        return {'value' : values,'warning':mensaje}