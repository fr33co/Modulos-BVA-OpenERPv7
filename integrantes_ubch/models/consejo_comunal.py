# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class ConsejoComunal(osv.Model):
	_name = "integrante.consejocomunal"
	
	_order = "consejo_comunal"
	
	_rec_name = "consejo_comunal"

	_columns ={
		'codigo': fields.char(string = "Código", size = 9, required = False, help="Código del consejo comunal"),
		'consejo_comunal' : fields.char(string="Consejo Comunal", help="Ingrese el consejo comunal", required = True),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]

