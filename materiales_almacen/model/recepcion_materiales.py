# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

import time # Necesario para las funciones de Fecha
import pdf_class # Llamada de las clases DPF
import base64 
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final

from openerp.osv import osv, fields

class Solicitud_materiales(osv.Model):
    _name="compras.wizard"

    _order = 'nombre'
    
    _rec_name = 'nombre'


    # METODO PARA TRAER EL NUMERO DE CORRELATIVO COMO PEDIDO DE SOLICITUD DE MATERIALES (COMPRAS)
    def search_solicitud_m(self, cr, uid, ids, argument_search, context=None): # Proceso de busqueda de un manager(Gerente)

        values = {}
        sms    = {}
        
        if not argument_search:
            
            return values
        obj_dp = self.pool.get('comp.solicitud')
        
        #======================== Busqueda por código ============================

        search_obj_code = obj_dp.search(cr, uid, [('nombre','=',argument_search)])

        datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
    
        #=========================================================================
        if not datos_code:
            
            sms = {
                        'title'   : 'Solicitud de Materiales',
                        'message' : "Disculpe el número de Solicitud de materiales no se encuentra asignado como pedido de unidad solicitante, intente de nuevo...",
                }

            values.update({
                'nombre' : None,
                'solicitante' : None,
                'papeleria' : None,
                })
        
        else:
            
            values.update({
                
                'solicitante' : datos_code[0]['solicitante'],
                'papeleria'   : datos_code[0]['papeleria'],
                })
        
        return {'value' : values,'warning' : sms}
    
    # EMITIR SOLICITUD DE MATERIALES DE CADA UNIDAD SOLICITANTE, REMITIDA A COMPRAS PARA EL PROCESO DE LLENADO DE LA ORDEN DE COMPRAS, ASDJUNTADA CON LAS PARTIDAS PRESUPUESTARIAS DE CADA MATERIAL
    def emitir_solicitud_material(self, cr, uid, ids, context=None):
        
        for s in self.browse(cr, uid, ids, context=None):
            model_id        = s.id
            correlativo     = s.nombre
            fecha_solicitud = s.fecha
            solicitante     = s.solicitante.id
            item            = s.item
            observaciones   = s.observaciones

            print "CORRELATIVO: "+str(correlativo)

        # Guardamos la data de solicicitud de materiales en el proceso de SOLICITUD DE MATERIALES, EQUIPOS Y SERVICIOS
        self.pool.get('purchase.entrada.materiales').create(cr, uid, {
            'nombre': correlativo,
            'fecha': fecha_solicitud,
            'solicitante': solicitante,
            'item' : item,
            'observaciones': observaciones,
            }, context=context)
        
    ######################################################################################  
    # METODO PARA LA GENERACION DE CORRELATIVO (ELEMENTO DE IDENTIFICACION)
    ######################################################################################
    def _generacion_correlativo(self, cr, uid, ids, context = None):
        
        ano  = time.strftime('%Y') # AÑO ACTUAL DEL SISTEMA
        
        obj_solicitud       = self.pool.get('compras.wizard')
        obj_search          = obj_solicitud.search(cr,uid,[])
        read_obj            = obj_solicitud.read(cr, uid, obj_search, context=context)
        if read_obj:
            id_documento = read_obj[-1]['nombre']
            c_nota = id_documento[5:]
            last_id      = c_nota.lstrip('0')
            str_number   = str(int(last_id) + 1)
            last_id      = str_number.rjust(4,'0')
            codigo      = last_id
        else :
            str_number = '1'
            last_id      = str_number.rjust(4,'0')
            codigo      = last_id

        return str(codigo)+"-"+str(ano)
    ######################################################################################
    
    _columns = {
            # Compras Solicitud
        'solicitante' : fields.many2one('stock.location','Area Solicitante',required=True),
        'nombre': fields.char(string="Nombre de referencia", size=100, required=True),
        'limpieza' : fields.boolean(string="Limpieza"),
        'servicios' : fields.boolean(string="Servicios"),
        'papeleria' : fields.boolean(string="Papeleria"),
        'tecnologico' : fields.boolean(string="Tecnologico"),
        'otros' : fields.boolean(string="Otros"),
        'material_id': fields.one2many('purchase.material', 'materiales_id', string='Materiales'),
        'user': fields.many2one('res.users', 'Registrado por:', readonly=True),
        'fecha' : fields.date(string = "Fecha", required = True),
        'observaciones' :  fields.text(string="Observaciones", size=256, required=False),
        'item' : fields.selection([('limpieza','Limpieza'),('servicios','Servicios Generales'),('papeleria','Papelería'),('tecnologico','Tecnológico'),('otros','Otros')], string="Tipo de Material", required=True),
    }

    _defaults = {
        'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
        'fecha': lambda *a: time.strftime("%Y-%m-%d"),
        # 'nombre': _generacion_correlativo,
    }

# Clase para los materiales de compras (Solicitud Directa)

class solicitud_material(osv.Model):

    _name = "purchase.material"
    
    # Metodo para traer las especificaciones de los materiales
    def search_materiales(self, cr, uid, ids, argument_search, context=None): # Proceso de busqueda de un manager(Gerente)

        values = {}
        
        if not argument_search:
            
            return values
        obj_dp = self.pool.get('materiales.almacen')
        
        #======================== Busqueda por código ============================

        search_obj_code = obj_dp.search(cr, uid, [('id','=',argument_search)])

        datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
        
        print "hola mundo: "+str(datos_code)
        #=========================================================================
        if not datos_code:
            
            values.update({
                
                'tipo' : None,
                'unidad' : None,
                })
        
        else:
            
            values.update({
                
                'tipo' : datos_code[0]['t_materiales'],
                'unidad' : datos_code[0]['unidad'],
                })
        
        return {'value' : values}
    
    # COLUMNAS PARA LA LISTA DE MATERIALES DE SOLICITUD
    _columns = {
        'materiales_id':fields.many2one('compras.wizard', 'material_id', ondelete='cascade', select=False),
        'cantidad' : fields.char(string="Cantidad", required=True),
        'tipo' : fields.selection([('Limpieza','Limpieza'),('Oficina','Oficina'),('Otros','Otros')], string="Tipo de Material", required=True),
        'descripcion':fields.many2one('materiales.almacen', 'Descripción del Material',required=True),
        'unidad' : fields.many2one('product.uom', 'Unidad de Medida', required=True),
        'modelo' : fields.char(string="Modelo", required=False),
        'marca'  : fields.char(string="Marca", required=True),
        'foto_referencial' : fields.binary("Foto Referencial",help="Foto Referencial"),
        'partida' : fields.many2one('presupuesto.partidas','Partida Presupuestaria',required=False),
        'cod_part' : fields.char(string="Código", required=False),
        'cod_part_g' : fields.char(string="General", required=False),
        'cod_part_e' : fields.char(string="Específica", required=False),
    }
###################
# METODOS GLOBALES
###################
def acento(cadena):
    result = cadena.encode('UTF-8').decode('UTF-8') # INSTITUCION
    return result

# Metodo global para fechas
def fecha(fecha):
    date = fecha.split("-")
    nueva_fecha = date[2]+"/"+date[1]+"/"+date[0]
    return nueva_fecha

# Metodo global para redondear
def decimal(cadena):
    salida = "%.2f" % round(cadena,2)
    return salida


