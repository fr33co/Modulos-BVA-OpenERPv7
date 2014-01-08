# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Novedades(osv.Model):
	_name = "novedades.becados"
	_order = 'encargado'
	_rec_name = 'encargado'
	
	_columns = {
		'encargado' : fields.char(string="Encargado de Eje:", size=256, required=True),
		'eje' : fields.selection((('1','Eje metro'),('2','Eje sur'),('3','Eje este'),('4','Eje centro'),('5','Eje costa')), "Eje", required = True),
		'fecha_actual' : fields.date(string="Fecha de Actual", required=True, readonly=True),
		'nombres' : fields.char(string="Nombres", size=256, required=True),
		'apellidos' : fields.char(string="Apellidos", size=256, required=True),
		'ci' : fields.char(string="C.I", size=256, required=True),
		'novedad' : fields.char(string="Novedad", size=256, required=True),
		'observacion' : fields.char(string="Observación", size=256, required=True),
		'observacion_general' : fields.text(string="Observación General", size=256, required=True),
		'direccion' : fields.char(string="Dirección", size=256, required=True),
		'tlf_movil' : fields.char(string="Teléfono movil", size=256, required=True),
		'correo' : fields.char(string="Correo", size=256, required=True),
		'duration' : fields.char(string="Duración", size=256, required=False),
		
	}

	_sql_constraints = [
    ('ci_unique','UNIQUE(ci)','Disculpe esta cedula ya tiene asignada una novedad'),
	]


	_defaults = {
		'fecha_actual': lambda *a: time.strftime('%Y-%m-%d'),
	} 

