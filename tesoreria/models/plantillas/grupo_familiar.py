# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Grupo_familiar(osv.Model):
	_name = "grupo.familiar"

	#~ def on_change_datos_personales(self, cr, uid, ids, becado, context=None):
		#~ values = {}
		#~ if not becado:
			#~ return values
		#~ obj_dp = self.pool.get('hr.employee')
#~ 
#~ 
		#~ busqueda = obj_dp.search(cr, uid, [('id','=',becado)])
#~ 
		#~ busqueda_read = obj_dp.read(cr,uid,busqueda,context=context)
#~ 
		#~ values.update({
			#~ 'primer_nombre' : busqueda_read[0]['primer_nombre'],
			#~ 'segundo_nombre' : busqueda_read[0]['segundo_nombre'],
			#~ 'primer_apellido' : busqueda_read[0]['primer_apellido'],
			#~ 'segundo_apellido' : busqueda_read[0]['segundo_apellido'],
			#~ 'nombre_completo' : busqueda_read[0]['name_related'],
#~ 
			#~ })
		#~ return {'value' : values}

	
	_columns ={
		#Identificador del integrante
		'integrante' : fields.many2one('integrantes.ubch','Integrante', required=False),
		#Sección II (Datos del Familiar)
		'cedula': fields.char(string = "Cédula Familiar", size = 9, required = False, help="Cédula del familiar"),
		'nombre_apellido' : fields.char(string="Nombre y Apellido", help="Ingrese el nombre y el apellido del Familiar", required = True),
		'telefono' : fields.char(string="Teléfono", size = 11, required=False),
		'ocupacion' : fields.many2one("integrante.ocupacion", "Ocupación", required=False),
		'edad' : fields.integer(string="Edad", size=3, required = True),
		'parentesco' : fields.selection((('1','Padre'),('2','Madre'),('3','Conyugue'),('4','Hijo(a)')), "Parentesco", required = True),
		'discapacidad' : fields.selection((('1','Sí'),('2','No')),"¿Discapacidad?", required = True),
		'situacion_medica' : fields.char(string="Situación Médica", size=15, required=False),
		'observacion' : fields.char(string="Observación", size=20, required=False),		
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]

