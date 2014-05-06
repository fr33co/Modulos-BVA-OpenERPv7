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
        #'cosulta_proyecto_accion' : fields.char(string="Consulta de Proyecto Accion:",size=100, required=True),
        'cosulta_proyecto_accion' :fields.many2one('presupuesto.accion','Consulta proyecto Accion:',ondelete='cascade',required=True),
        'movimientos_creditos' : fields.one2many('presupuesto.creditos_movimientos', 'credito', string="Creditos"),
    }
    
    
    
    def get_last_numero(self, cr, uid, ids, id_tipo_doc, context = None):
        values = {}
        vlores = {}
        if not id_tipo_doc:
            return values

        # funcion para obtener los registros de la tabla 'presupuesto.traslado'
        sfl_last_num   = self.pool.get('presupuesto.traslado')

        # funcion para obtener los registros de la tabla,
        # segun el criterio de busqueda ej:'id_tipo_doc'
        
        brw_accion     = sfl_last_num.browse(cr, uid, id_tipo_doc, context=context)
        
        # funcion que nos permite saber si la tabla tiene registro segun el criterio de busqueda ej:'id_tipo_doc',
        # la busqueda se realiza con 'brw_accion.id',
        # para obtener todos los registros de la tabla segun el criterio "'id_tipo_doc','=', brw_accion.id"
        srcnt_last_num = sfl_last_num.search_count(cr, uid, [('id_tipo_doc','=', brw_accion.id)], context=None)
        

        if srcnt_last_num > 0:
            # verificar si existe registros en la tabla 
             
            """
            Con esta funcion obtenemos el ultimo regsitro de la tabla,
            para luego sumar '1' y asi generar un correlativo con ceros adelante de '7' digistos
            """
            # buscar el registro segun el criterio de busqueda
            # offset de que fila empezara a obtener los registros
            # limit cantidad d registros a obtener 
            # order por que columna realizara el ordenamiento y si es descendente o ascendente 
            srch_last_num = sfl_last_num.search(cr,uid,[('id_tipo_doc','=',brw_accion.id)],offset=0,limit=1,order='numero desc')
            
            # funcion que obtiene los registros de que genero el search 
            rd_last_num   = sfl_last_num.read(cr, uid, srch_last_num,['numero'],context=context)
            
            # obtener el registro por indice y clave
            last_num      = rd_last_num[0]['numero']

            # funcion para eliminar los '0' a la derecha 
            last_num      = last_num.lstrip('0')
            # sumar '1' al registro obtenido
            str_number    = str(int(last_num) + 1)

            # agregar '0' a la derecha en este caso son '7' 
            last_num      = str_number.rjust(7,'0')
        else:
            #si no existen registros solamente agregar ceros a la variable 'str_number'
            str_number = '1'
            last_num   = str_number.rjust(7,'0')
        
        # agregar el valor generado en 'last_num' a a un arreglo,
        # para luego actualizar el campo de la vista, 
        # 'numero'
        valores = {'numero' : last_num}

        values.update(valores)

        return {'value' : values}
    
    
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
    
    
    def on_change_accion(self, cr, uid, ids, accion,tipo,context=None):
        values    = {}
        valores   = {}
        id_accion = 0

        if not accion:
            return values

        sfl_accion = self.pool.get('presupuesto.accion')
    
        if tipo == 'cod_accion':

            srcnt_accion = sfl_accion.search_count(cr, uid, [('codigo_accion','=', accion)], context=None)
            if srcnt_accion  > 0:
                srch_accion = sfl_accion.search(cr, uid, [('codigo_accion','=', accion)])
                rd_accion   = sfl_accion.read(cr, uid, srch_accion, context=context)
                id_accion   = rd_accion[0]['id']
            valores   = {'cosulta_proyecto_accion' : id_accion}
        else:
                
            
            brw_accion  = sfl_accion.browse(cr, uid, accion, context=context)
            if brw_accion != False:
                id_accion = brw_accion.codigo_accion
                print id_accion
            valores   = {'proyecto_accion' : id_accion}

        values.update(valores)
        return {'value' : values}
    
    
    