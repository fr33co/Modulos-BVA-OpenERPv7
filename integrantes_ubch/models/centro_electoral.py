# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class CentroElectoral(osv.Model):
	_name = "integrante.centroelectoral"
	
	_order = "centro"
	
	_rec_name = "centro"

	_columns ={
		'codigo': fields.char(string = "Código", size = 9, required = False, help="Código del centro"),
		'centro' : fields.char(string="Centro Electoral", help="Ingrese el centro electoral", required = True),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]


