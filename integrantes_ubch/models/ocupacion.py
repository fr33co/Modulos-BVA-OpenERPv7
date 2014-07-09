# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Ocupacion(osv.Model):
	_name = "integrante.ocupacion"
	
	_order = "ocupacion"
	
	_rec_name = "ocupacion"

	_columns ={
		'codigo': fields.char(string = "Código", size = 9, required = False, help="Código de la ocupación"),
		'ocupacion' : fields.char(string="Ocupación", size = 30, help="Ingrese la ocupación", required = True),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]

