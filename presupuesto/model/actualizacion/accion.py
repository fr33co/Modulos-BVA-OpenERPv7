#-*- coding:utf-8 -*-
###############################################################################################
#
# Clase para crear las acciones presupuestarias dependientes del proyecto del modulo de presupuesto
#
###############################################################################################
from openerp.osv import osv, fields
import re
class Accion(osv.Model):

    """
     Crear el objeto 'presupuesto.accion'
    """
    _name = "presupuesto.accion"

    """
        Ordenar por proyecto y llamar el nombre del proyecto
    """
    _order='codigo_accion'
    _rec_name='descripcion'
    
    """
        Declaracion de las Columnas para el xmly la base de datos
    """

    def _proyec_accion(self, cr, uid, ids, name, arg, context={}):    
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
            res[r.id] = r.codigo_proyecto+'-'+ r.codigo_accion
        return res

    _columns = {
    # Campo que genera una lista desplegable del los proyectos generados en el modulo de proyecto
    'proyecto_id' : fields.many2one('presupuesto.proyecto','Proyecto:',ondelete='cascade',required=True),
    'codigo_proyecto' : fields.char(string="Codigo de Accion:",size=2,required=True),
    'codigo_accion' : fields.char(string="Codigo de Accion:",size=8, required=True,help="El formato valido para el codigo de la accion deberia ser Ej.00-00-00"),
    'siglas' : fields.char(string="Siglas",size=6, required=True),
    'descripcion' : fields.text(string="Descripcion:",size=300, required=True),
    'unidad' : fields.char(string="Unidad Ejecutora:",size=100,readonly=True),
    'monto' : fields.float(string="Monto",size=100, required=True),
    'cod_proyect_accion' : fields.function(_proyec_accion, method=True, type='char', readonly=True, string='Codigo Proyecto'),
    }

    
    def on_cod_proyecacc(self, cr, uid, ids, proyecto,accion, context=None):
        values  = {}
        mensaje = ''
       
        sls_cod_accion    = self.pool.get('presupuesto.accion')
        srcnt_proyect_acc = sls_cod_accion.search_count(cr,uid, [('codigo_proyecto','=', proyecto),('codigo_accion','=',accion)])
        if srcnt_proyect_acc > 0:
            mensaje = {'title':'ERROR','message':'Este codigo de accion ya se encuentra registrado para este proyecto'}
           
        return {'warning':mensaje}



    def _check_codigo_accion(self, cr, uid, ids, context=None):
        """
        Constraints para validar que que el codigo de la accion
        sea en formato 00-00-00  
        """
        for codigo in self.read(cr, uid, ids, ['codigo_accion'], context=context): 
            patron = re.compile('^[0-9]{2}-[0-9]{2}-[0-9]{2}$') 
            if not re.match(patron, codigo['codigo_accion']):
                    return False
        return True

    _constraints = [
        (_check_codigo_accion, 'Error! El Codigo de la acion no es correcto!',['Codigo de Accion']),
    ]

    # Asignar un valor por defecto en un campo del xml
    _defaults = {
        'unidad' : 'PLANIF.PRESUPUESTO'
    }

    """
    Metodo para buscar el codigo del proyecto seleccionado en el combo list,
    y asi generar el codigo del proyecto
    """

    def on_change_proyecto(self, cr, uid, ids, proyecto,tipo, context=None):
        
        values  = {}
        mensaje = ''
        if not proyecto:
            values.update({'codigo_proyecto' : ''})
            return {'value' : values}

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