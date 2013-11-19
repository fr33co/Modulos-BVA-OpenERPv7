# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
import MySQLdb

class Estado(osv.Model):
    _name = "configuracion.estado"

    _columns = {
        'estado' : fields.char(string="Estado",size=100, required=True),
    }
    _order='estado'
    _rec_name='estado'

class Municipio(osv.Model):
    _name = "configuracion.municipio"
    _columns = {
        'estado' : fields.many2one('configuracion.estado','Estado',ondelete='cascade',required=True),
        'municipio' : fields.char(string="Municipio",size=100, required=True),
    }
    _order='estado'
    _rec_name='municipio'

class Parroquia(osv.Model):
    _name    = "configuracion.parroquia"
    _columns = {
    'estado': fields.related('municipio','estado', type = 'many2one',relation = 'configuracion.estado',string = 'Estado'),
    'municipio':  fields.many2one('configuracion.municipio', 'Municipio'),
    'parroquia' : fields.char(string="Parroquia",size=100, required=True),
    }
    _order='municipio'
    _rec_name='parroquia'

class Casos(osv.Model): # Creacion del Modelo Monitor de Casos

	_name = "monitor.caso"
	
	'''
	|-----------------------------------------------------------------------------------------
	|                               Método private para estado (1)
	|-----------------------------------------------------------------------------------------
	'''
	def _filtro_estados_1(self, cr, user_id, context=None):
		cr.execute('SELECT estado FROM configuracion_estado')
		t = () # declaramos una tupla vacía
		for datos in cr.fetchall():
			t = t + ((datos[0], datos[0]),) # anidamos todos los camps de
											  # la tupla como a tuplas hijas
		return t
	
	'''
	|-----------------------------------------------------------------------------------------
	|                               Método private para estado (2)
	|-----------------------------------------------------------------------------------------
	'''
	def _filtro_estados_2(self, cr, user_id, context=None):
		cr.execute('SELECT estado FROM configuracion_estado')
		t = () # declaramos una tupla vacía
		for datos in cr.fetchall():
			t = t + ((datos[0], datos[0]),) # anidamos todos los camps de
											  # la tupla como a tuplas hijas
		return t
		res['warning'] = {
		'title'   : "Warning: problems",
		'message' : "You need more seats for this session",
		}
		return res


	
	'''
	|-----------------------------------------------------------------------------------------
	|                              Método public select dependiente (2)
	|-----------------------------------------------------------------------------------------
	'''
	def onchange_mun(self, cr, uid, ids, estado, context=None):
		cr.execute('SELECT estado FROM configuracion_municipio WHERE estado = \'%s\'' % estado)
		mun = () # declaramos una tupla vacía
		for datos in cr.fetchall():
			mun = mun + ((datos[0], datos[0]),) # anidamos todos los camps de
											  # la tupla como a tuplas hijas
		return t
		
	def onchange_campo(self, cr, uid, ids, estado):
		val = {'estado':''}
		if estado:
			cr.execute('SELECT estado FROM configuracion_municipio WHERE estado = \'%s\'' % estado)
			valor_campo = cr.fetchone()[0] # Recuperamos el campo para autocompletar
			if valor_campo is None :
				val = {'estado':'',} # si no existe asignamos un valor vacío
			else : 
				val = {'estado':valor_campo,}
		return {'value':val} # retornamos el diccionario de valors per que 
											 # se actualice todo el form
		
	'''------------------------------------------------------------------------------------'''
	

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
		'nro_caso' : fields.integer(string="Nro de Caso", size=20, required=True),
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
		'estatus' : fields.selection((('1','Atentido'),('2','No atentido')),'Estatus', required=True),
		'nro_seguimiento' : fields.char(string="Nro de Seguimiento", size=100, required=True),
		'operador' : fields.char(string="Operador del Caso", size=150, required=True),
		'comp_intitucional' : fields.char(string="Competencia Institucional", size=256, required=True),
	}


class Seguimiento(osv.Model):
	_name="preguntas.caso"

	_columns = {
	'tlf_seguimiento' : fields.char(string="Teléfono", size=11),
	'pregunta' : fields.char(string="Formular Pregunta", size=256),
	}
		
		
		
		
	
