#-*- coding:utf-8 -*-
#########################################
#
# Clase para asignar el monto a las partidas presupuestarias
#
#########################################

from openerp.osv import osv, fields
import random
import time
from datetime import datetime, timedelta
class Distribucion(osv.Model):
    """
     Crear el objeto 'presupuesto.distribucion'
    """
    _name = "presupuesto.distribucion"

    """
        Ordenar por proyecto y llamar el nombre del proyecto
    """
    _order    ='partida'
    _rec_name ='descripcion'
    

    def _proyec_accion(self, cr, uid, ids, name, arg, context={}):    
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
            res[r.id] = r.codigo_proyecto+'-'+ r.codigo_accion
        return res

    _columns = {
        #  "proyecto_id" campo que genera un combo dependiente  el cualla relacion seria
        #  proyecto=>accion  el cual la tabla accion depende de la tabla proyecto
        'proyecto_id': fields.related('accion','proyecto_id', type = 'many2one',relation = 'presupuesto.proyecto',string = 'Proyecto',required=True),
        'codigo_proyecto' : fields.char(string="Codigo de Accion:",size=2,required=True),
        'codigo_accion' : fields.char(string="Codigo del Accion",size=8,required=True),
        'accion' : fields.many2one('presupuesto.accion','Accion',ondelete='cascade',required=True,domain="[('proyecto_id','=',proyecto_id)]"),
        'partida' : fields.char(string="Partida Presupuestaria",size=13, required=True),
        'descripcion' : fields.many2one('presupuesto.partidas','Partidad',ondelete='cascade',required=True),
        'monto_pre' : fields.float(string="Monto del Presupuesto",size=12, required=True),
        'aceptar' : fields.selection((('1','Ambos'), ('2','Compras'), ('3', 'Servicios')),'Aceptar orden de'),
        'fecha' : fields.date(string="Fecha Apertura", required=True),
        'disponibilidad' : fields.float(string="Disponibilidad Actual",readonly=True),
        'monto_proyecto' : fields.float(string="Monto del Proyecto",readonly=True),
        'cod_proyect_accion' : fields.function(_proyec_accion, method=True, type='char', readonly=True, string='Codigo Proyecto Accion'),
    }




    """
    Metodo para buscar el codigo del proyecto seleccionado en el combo list,
    y asi generar el codigo del proyecto
    """

    def on_change_proyecto(self, cr, uid, ids, proyecto,tipo, context=None):
        
        values  = {}
        mensaje = ''
        if not proyecto:
            return values

        sls_cod_proyect = self.pool.get('presupuesto.proyecto')
        if tipo == 'proyecto_id':
            brw_cod_proyect = sls_cod_proyect.browse(cr, uid,proyecto, context=context)
            values.update({'codigo_proyecto' : brw_cod_proyect.codigo_proyecto,})
        else:
            srcnt_acod_proyect = sls_cod_proyect.search_count(cr,uid, [('codigo_proyecto','=', proyecto)])
            if srcnt_acod_proyect > 0:
                srch_id_proyect = sls_cod_proyect.search(cr,uid,[('codigo_proyecto','=', proyecto)])
            
                # funcion que obtiene los registros de que genero el search 
                rd_id_proyect   = sls_cod_proyect.read(cr, uid, srch_id_proyect,context=context)
              
                values.update({'proyecto_id' : rd_id_proyect[0]['id']})
            else:
                mensaje = {'title':'ERROR','message':'Este codigo de proyecto no esta registrado indique un codigo registrado'}
                values.update({'proyecto_id' : 0})
            
        return {'value' : values,'warning':mensaje}


    """
     Metodo para buscar  la accion del proyecto segun el metodo de busqueda,
     puede ser a traves del campo de texto 'codigo_accion' o a traves de la lista o combo
     desplegable 'accion'.
    """
    def on_change_accion(self, cr, uid, ids, accion,proyecto_id,tipo,context=None):
        values = {}
        if not accion:
            return values

        id_accion  = 0
        mensaje    = ''
        print accion
        if proyecto_id == False:
            mensaje = {'title':'ERROR','message':'Por favor debe Seleccionar un proyecto en el combo'}
        else:
            sfl_accion = self.pool.get('presupuesto.accion')# hacer referencia a la tabla a buscar ej: 'presupuesto.accion'
            if tipo == 'cod_accion':
                # validar segun el tipo aqui se buscamos por la caja de texto 'codigo_accion'
                # para llenar la lista o combo desplegable 'accion' con el valor a buscar

                tamano = len(accion)

                if tamano > 2:
                    # validar que el tamañodel codigo sea mayor a 2 
                    # si es mayor buscamos registrossegun el criterio de busqueda
                    
                    # funcion search_count para saber si hay registros el la tabla 'presupuesto.accion',
                    # segun el criterio de busqueda
                    srcnt_accion = sfl_accion.search_count(cr,uid, [('codigo_accion','=', accion)])
                    # si existen registros en la tabla
                    if srcnt_accion > 0:

                    # funcion para buscar los registros en la tabla
                    # segun el criterio de busqueda
                        srch_accion = sfl_accion.search(cr, uid, [('codigo_accion','=', accion)])

                        # funcion para obtener los registros de la tabla
                        # despues de la busqueda
                        rd_accion   = sfl_accion.read(cr, uid, srch_accion, context=context)

                        # selecciono el registro segun indice y clave
                        #id_accion   = rd_accion[0]['id']
                        # selecciono el registro segun indice y clave
                        id_accion   = rd_accion[0]['id']

                        #actualizo el campo el la vista
                        values.update({'accion' : id_accion})
                                 
                    else:
                        #validar si no hay registros y si el codigo es tamaño de la accion es mayor a 2
                        mensaje = {'title':'ERROR','message':'Este codigo de la accion no se encuentra registrado indique un codigo registrado '}
                        values.update({'accion' : 0})

                        
            else:
                # se busca cuando se seleciona el la lista o el combo desplegable un elemento
                brw_accion  = sfl_accion.browse(cr, uid, accion, context=context)
                if brw_accion != False:
                    # valido de que no sea falso la busqueda

                    # obtengo el valor que necesito de la tabla
                    id_accion = brw_accion.codigo_accion

                    #actualizo el campo el la vista
                    values.update({'codigo_accion' : id_accion})

                # llenar restos de los campos de la viista segun el criterio de busqueda
                # campos a llenar son 'disponibilidad' y 'monto'
                monto_disponible = brw_accion.monto
                id_proyecto      = brw_accion.proyecto_id

                obj_proyecto     = self.pool.get('presupuesto.proyecto')
                srch_proyecto    = obj_proyecto.search(cr, uid, [('id','=',id_proyecto.id)])
                rd_proyecto      = obj_proyecto.read(cr, uid, srch_proyecto, context=context)
                monto_proyecto   = rd_proyecto[0]['monto']

                #actualizo la vista
                values.update({'disponibilidad' : monto_disponible,'monto_proyecto':monto_proyecto})
        return {'value' : values,'warning':mensaje}   

    """
     Metodo para buscar  la partida del proyecto segun el metodo de busqueda,
     puede ser a traves del campo de texto 'partida' o a traves de la lista o combo
     desplegable 'descripcion'.
    """
    def on_change_partida(self, cr, uid, ids, partida,tipo='select', context=None):

        values  = {}
        id_part = 0
        mensaje = ''
        if not partida:
            return values

        sfl_partida  = self.pool.get('presupuesto.partidas')# hacer referencia a la tabla a buscar ej: 'presupuesto.partidas'

        if tipo == 'cod_partida':

            # validar segun el tipo  aqui se buscar por la caja de texto 'partida'
            # para llenar la lista o combo desplegable 'descripcion' con el valor a buscar


            # funcion search_count para saber si hay registros el la tabla 'presupuesto.partidas',
            # segun el criterio de busqueda
            srcnt_partida = sfl_partida.search_count(cr,uid, [('codigo','=', partida)])

            if srcnt_partida > 0:
                # valido si hay registros

                # funcion para buscar los registros en la tabla,
                # segun el criterio de busqueda
                srch_partida =  sfl_partida.search(cr, uid, [('codigo','=', partida)])

                # funcion para obtener los registros de la tabla,
                # despues de la busqueda
                rd_partida   = sfl_partida.read(cr, uid, srch_partida, context=context)

                # selecciono el registro segun indice y clave
                id_part      = rd_partida[0]['id']
            else:
                mensaje = {'title':'ERROR','message':'Este codigo de partida no esta registrado indique un codigo registrado'}
            #actualizo el campo el la vista
            values.update({'descripcion' : id_part})
        else:
            brw_partida  = sfl_partida.browse(cr, uid, partida, context=context)
            if brw_partida != False:
                # valido de que no sea falso la busqueda

                # obtengo el valor que necesito de la tabla
                codigo = brw_partida.codigo
            #actualizo el campo el la vista
            values.update({'partida' : codigo})

        return {'value' : values,'warning':mensaje}