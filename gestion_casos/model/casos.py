# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
import MySQLdb as sql
import random # Imporatacion a la 
import re
import os


class Casos(osv.Model): # Creacion del Modelo Monitor de Casos

	_name = "monitor.caso"
	
	
	'''
	|-----------------------------------------------------------------------------------------
	|        Método public para listar los numeros provenientes para los tipos de casos()
	|-----------------------------------------------------------------------------------------
	'''
	def _listar_destination_number(self, cr, uid, ids, context=None):
		
		local = "localhost"
		usu   = "root"
		pwd   = "123"
		bd    = "kalkun"
		
		result = ()
		
		db=sql.connect(host=local, user=usu, passwd=pwd, db=bd)
		cursor=db.cursor()
		query='SELECT SenderNumber FROM inbox'
		cursor.execute(query)
		resultado=cursor.fetchall()
			
		for datos in resultado:
			result = result + ((datos[0], datos[0]),) # anidamos todos los campos de
											  # la tupla como a tuplas hijas
		return result
		
	'''
	|-----------------------------------------------------------------------------------------
	|        Método public para listar los numeros provenientes para los tipos de casos()
	|-----------------------------------------------------------------------------------------
	'''
	def onchage_datos_casos(self, cr, uid, ids, tlf, context=None):
		
		local = "localhost"
		usu   = "root"
		pwd   = "123"
		bd    = "kalkun"

		db=sql.connect(host=local, user=usu, passwd=pwd, db=bd)
		
		
		values = {}
		
		if not tlf:
			return values
		query='SELECT * FROM inbox'
		cursor=db.cursor()
		cursor.execute(query)
		resultado=cursor.fetchall()
		
		values.update({
			'descripcion' : resultado.TextDecoded,
			#~ 'ciudad' : direccion.ciudad,
			#~ 'municipio' : direccion.municipio,
			})
		return {'value' : values}
	
	'''
	|-----------------------------------------------------------------------------------------
	|                           Método private para tipo de casos (1)
	|-----------------------------------------------------------------------------------------
	'''
	def _filtro_caso(self, cr, user_id, context=None):
		cr.execute('SELECT caso FROM tipos_caso')
		t = () # declaramos una tupla vacía
		for datos in cr.fetchall():
			t = t + ((datos[0], datos[0]),) # anidamos todos los camps de
											  # la tupla como a tuplas hijas
		return t

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
	|                Método public onchange para validar campos solo caracteres
	|-----------------------------------------------------------------------------------------
	'''
	def validar(self, cr, uid, ids, parametro):
		valida = {}
		id_filtro=re.compile("[a-z]")
		if id_filtro.match(parametro):
			valida['warning'] = {'title': 'Disculpe!!!','message': 'Correcto',}
			return valida
		else:
			valida['warning'] = {'title': 'Disculpe!!!','message': 'solo se permiten numeros',}
			return valida
	
	'''
	|-----------------------------------------------------------------------------------------
	|                          Método public onchange para validar fechas
	|-----------------------------------------------------------------------------------------
	'''
	def onchange_fecha(self, cr, uid, ids, fecha, context=None):
		validar_fecha = {}
		now = datetime.now().strftime('%Y-%m-%d')
		if fecha < now:
			validar_fecha['warning'] = {'title': 'Disculpe!!!','message': 'Disculpe, no debe seleccionar una fecha anterior al actual',}
			return validar_fecha
		return validar_fecha
		
	'''
	|-----------------------------------------------------------------------------------------
	'''
	
	_columns = {
		'cedula' : fields.char(string="Cédula", size=8, required=True, translate=True),
		'nombres' : fields.char(string="Nombres", size=256, required=True),
		'apellidos' : fields.char(string="Apellidos", size=256, required=True),
		#~ 'tlf' : fields.integer(string="Celúlar", size=20, required=True),
		'tlf' : fields.selection(_listar_destination_number,'Celúlar', required=True),
		'urbanizacion' : fields.char(string="Urbanización", size=256, required=True),
		'estado': fields.related('municipio','estado', type = 'many2one',relation = 'configuracion.estado',string = 'Estado', required=True, select="0"),
		'municipio' :  fields.related('parroquia','municipio', type = 'many2one',relation = 'configuracion.municipio',string = 'Municipio', required=True, select="0"),
		'parroquia' : fields.many2one("configuracion.parroquia","Parroquia", required=True, select="1"),
		'sector' : fields.char(string="Sector", size=256, required=True, select="1"),
		'tlf_local' : fields.integer(string="Local", size=30),
		'casa' : fields.char(string="Casa/Apt/Local/Galpón", size=256, required=True),
		'nro_caso' : fields.char(string="Nro de Caso", size=20, required=True),
		'fecha' : fields.date(string="Fecha de Registro"),
		'caso' : fields.selection(_filtro_caso,'Caso', required=True),
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
		
		
		
		
	
