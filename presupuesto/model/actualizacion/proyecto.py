#-*- coding:utf-8 -*-
###########################################################
#
# Clase para crear el proyecto del modulo de presupuesto
#
###########################################################
import time
from datetime import date
from openerp.osv import osv, fields
class Proyecto(osv.Model):

    """
     Crear el objeto 'presupuesto.proyecto'
    """
    _name = "presupuesto.proyecto"

    """
        Ordenar por proyecto y llamar el nombre del proyecto
    """
    _order='proyecto'
    _rec_name='proyecto'

    """
        Declaracion de las Columnas para el xmly la base de datos
    """
    _columns = {
        'codigo_proyecto' : fields.char(string="Código del Proyecto:",size=3, required=True,help="Prueba"),
        'proyecto' : fields.char(string="Nombre del Proyecto:",size=100, required=True),
        'monto' : fields.float(string="Monto:",size=12, digits=(12,2) ,required=True),
        'descripcion' : fields.text(string="Descripción:",size=300, required=True),
        #'proyecto_treee' : fields.one2many("presupuesto.proyecto","codigo_proyecto",string="Carga Familiar",readonly=True),
    }

     # Metodo para Validar ununicocodigo de proyecto por año
   
    def on_change_codigo_proyecto(self, cr, uid, ids, codigo ,context={}):
        values = {}
        if not codigo:
            values.update({'codigo_proyecto' : ''})
            return {'value' : values}
            
        cr.execute("SELECT COUNT(codigo_proyecto) FROM presupuesto_proyecto WHERE to_char(create_date, 'YYYY') = to_char(CURRENT_DATE, 'YYYY') AND codigo_proyecto=%s", (codigo,))
        existe_cod = cr.fetchone()[0]
        if existe_cod > 0:
            mensaje = {'title':'ERROR','message':'Este codigo de proyecto se encuentra registrado para este año'}
            values.update({'codigo_proyecto' : ''})
            return {'value' : values,'warning':mensaje}
        return True
