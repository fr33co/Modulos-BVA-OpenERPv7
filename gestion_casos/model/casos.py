# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
import MySQLdb
import random


class Casos(osv.Model): # Creacion del Modelo Monitor de Casos

	_name = "monitor.caso"
	
	'''
	|-----------------------------------------------------------------------------------------
	|                               Método private para status (1)
	|-----------------------------------------------------------------------------------------
	'''
	def _filtro_estatus(self, cr, user_id, context=None):
		cr.execute('SELECT status FROM configuracion_caso')
		t = () # declaramos una tupla vacía
		for datos in cr.fetchall():
			t = t + ((datos[0], datos[0]),) # anidamos todos los camps de
											  # la tupla como a tuplas hijas
		return t
	
	'''
	|-----------------------------------------------------------------------------------------
	'''
	_columns = {
		'cedula' : fields.char(string="Cédula", size=8, required=True, translate=True),
		'nombres' : fields.char(string="Nombres", size=256, required=True),
		'apellidos' : fields.char(string="Apellidos", size=256, required=True),
		'tlf' : fields.integer(string="Teléfono", size=20, required=True),
		'urbanizacion' : fields.char(string="Urbanización", size=256, required=True),
		#'estado' : fields.many2one("estados","Estado", required=True, select="1"),
		'estado': fields.related('municipio','estado', type = 'many2one',relation = 'configuracion.estado',string = 'Estado', required=True, select="0"),
		'municipio' :  fields.related('parroquia','municipio', type = 'many2one',relation = 'configuracion.municipio',string = 'Municipio', required=True, select="0"),
		'parroquia' : fields.many2one("configuracion.parroquia","Parroquia", required=True, select="1"),
		'sector' : fields.char(string="Sector", size=256, required=True, select="1"),
		'tlf_local' : fields.integer(string="Teléfono Local", size=20),
		'casa' : fields.char(string="Casa/Apt/Local/Galpón", size=256, required=True),
		'nro_caso' : fields.char(string="Nro de Caso", size=20, required=True),
		'fecha' : fields.date(string="Fecha de Registro"),
		#'caso' : fields.char(string="Caso", size=256, required=True),
		'caso' : fields.selection((('1','Alumbrado'),('2','Vialidad'),('3','Salud'),('4','Vivienda'),('5','Aseo'),('6','Educación')),'Caso', required=True),
		'descripcion' : fields.char(string="Descripción del Caso", size=256, required=True),
		'ub_municipio' :  fields.related('parroquia','municipio', type = 'many2one',relation = 'configuracion.municipio',string = 'Municipio', required=True, select="0"),
                'ub_parroquia' : fields.many2one("configuracion.parroquia","Parroquia", required=True, select="0"),
		'ub_sector' : fields.char(string="Sector", size=256, required=True),
		'ub_residencia' : fields.char(string="Urb/Barrio/Residencia", size=256, required=True),
		'ub_calle' : fields.char(string="Calle/Av", size=256, required=True),
		'ub_casa' : fields.char(string="Casa/Apt/Local/Galpón", size=256, required=True),
		'estatus' : fields.selection(_filtro_estatus,'estatus'),
		'nro_seguimiento' : fields.char(string="Nro de Seguimiento", size=100, required=True),
		'operador' : fields.char(string="Operador del Caso", size=150, required=True),
		'comp_intitucional' : fields.char(string="Competencia Institucional", size=256, required=True),
	}
	
	_defaults = { # Valores aleatorios
    'nro_seguimiento' : lambda *a: str(random.randint(111,999)) + "-Seg",
    'nro_caso' : lambda *a: str(random.randint(111,999)) + "-caso",
	} 


class Seguimiento(osv.Model):
	_name="preguntas.caso"

	_columns = {
	'tlf_seguimiento' : fields.char(string="Teléfono", size=11),
	'pregunta' : fields.char(string="Formular Pregunta", size=256),
	}
		
		
		
		
	
