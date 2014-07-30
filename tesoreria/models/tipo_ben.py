
# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class TiposBeneficiario(osv.Model):
	_name = "tesoreria.tipobeneficiario"
	
	_order = "descripcion"
	
	_rec_name = "descripcion"

	_columns = {
		'codigo': fields.char(string = "Código", size = 2, required = True, help="Indique el código del tipo de beneficiario"),
		'descripcion' : fields.char(string="Descripción", help="Ingrese la descripción", required = True),
		'secuenciador' : fields.char(string="Secuenciador", required = False),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]



