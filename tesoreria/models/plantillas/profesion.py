# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Profesion(osv.Model):
	_name = "integrante.profesion"
	
	_order = "profesion"
	
	_rec_name = "profesion"

	_columns ={
		'codigo': fields.char(string = "Código", size = 9, required = False, help="Código de la profesión"),
		'profesion' : fields.char(string="Profesión", help="Ingrese la profesión", required = True),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]

