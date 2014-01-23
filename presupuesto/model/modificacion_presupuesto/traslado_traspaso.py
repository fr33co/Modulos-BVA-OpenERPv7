from openerp.osv import osv, fields
class Traslado(osv.Model):
    """
     Crear el objeto 'presupuesto.accion'
    """

    _name = "presupuesto.traslado"

    _order    ='id_tipo_doc'
    _rec_name ='id_tipo_doc'

    """
        Declaracion de las Columnas para el xmly la base de datos
    """

    _columns = {
        # Campo que genera una lista desplegable del los Tipos de documento generados en el modulo de Tipos de documento
        'id_tipo_doc' : fields.many2one('presupuesto.documento','Tipo Doc',ondelete='cascade',required=True,domain=[('tipo', '=', '1')]),
        'numero' : fields.char(string="Numero:",size=100, required=True),
        'fecha' : fields.date(string="Fecha:", required=True),
        'oficio' : fields.char(string="# Oficio:", required=True),
        'fecha_resolucion' : fields.date(string="Fecha de Resolucion:", required=True),
        'motivo' : fields.char(string="Motivo:", required=True),
        'codigo_proyecto_accion' : fields.char(string="Proyecto Accion:", size=8,required=True),
        # Campo que genera una lista desplegable del Proyecto Accion generados en el modulo de  Proyecto Accion
        'id_proyecto_accion' : fields.many2one('presupuesto.accion','Consulta Proyecto Accion:',ondelete='cascade',required=True),
        'cod_presupuesto' : fields.char(string="Cod Presupuestario:", required=True),
        'par_presu' : fields.char(string="Partida Presupuestaria:",readonly=True),
        'aumen_dism': fields.selection([('1','Aumentar'),('2','Disminuir')],'Aumentar/Disminuir'),
        'aumentar' : fields.float(string="Aumentar:",),
        'disminuir' : fields.float(string="Disminuir:"),
        'disponibilidad' : fields.char(string="Disponibilidad:"),

    }

    """
    Metodo para obtener el ultimo numero segun el documento seleccionado 
    en el combo o lista desplegable
    """
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

    """
    Metodo para obtener el el codigo de accion o el nombre de la accion, 
    segun el criterio de busqueda si busca el el cmapo de texto,
    'codigo_proyecto_accion' obtendra el el combo lista el nombre de la
    accion y si busca en la lista accion obtendra el codigo de la accion
    """ 
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
            # si selecciona en la lista buscamos solamente el codigo de de la accion seleccionada
            brw_accion  = sfl_accion.browse(cr, uid, accion, context=context)
            if brw_accion != False:
                id_accion = brw_accion.codigo_accion
            valores   = {'codigo_proyecto_accion' : id_accion}

        values.update(valores)
        return {'value' : values,'warning':mensaje}

    """
    Metodo para obtener el el el nombre de la partida
    y el monto
    """ 
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
        valores = {'par_presu' : partida_presupuestaria,'disponibilidad':monto}

        values.update(valores)
        return {'value' : values,'warning':mensaje}

    def on_change_montomovi(self, cr, uid, ids, monto, context=None):
        values = {}
        valores = {'monto_movi1' : monto}
        values.update(valores)
        return {'value' : values}

    def on_change_get_row(self, cr, uid, ids, numero,id_tipo_doc, context=None):
        values  = {}
        valores = {}

        valores = {
        'fecha': None,
        'oficio': None,
        'fecha_resolucion':None,
        'motivo': None,
        'categoria': None,
        'consulta_categoria': 0,
        'monto_movi': 0.00,
        'aumen_dism': None,
        }

        if not numero:
            return values

        sfl_get_row   = self.pool.get('presupuesto.traslado')

        srcnt_get_row = sfl_get_row.search_count(cr,uid,[('id_tipo_doc','=',id_tipo_doc),('numero','=',numero)], context=None)

        if srcnt_get_row > 0:
            srch_get_row = sfl_get_row.search(cr,uid,[('id_tipo_doc','=',id_tipo_doc),('numero','=',numero)])
            rd_get_row   = sfl_get_row.read(cr, uid, srch_get_row,context=context)
            valores = {
            'fecha': rd_get_row[0]['fecha'],
            'oficio': rd_get_row[0]['oficio'],
            'fecha_resolucion': rd_get_row[0]['fecha_resolucion'],
            'motivo': rd_get_row[0]['motivo'],
            'codigo_proyecto_accion': rd_get_row[0]['codigo_proyecto_accion'],
            'cod_presupuesto': rd_get_row[0]['cod_presupuesto'],
            }

        values.update(valores)
        return {'value' : values}