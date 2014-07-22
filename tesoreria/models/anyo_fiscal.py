# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class AnyoFiscal(osv.Model):
	_name = "tesoreria.anyofiscal"
	
	_order = "anyo_fiscal"
	
	_rec_name = "anyo_fiscal"

	_columns = {
		'anyo_fiscal': fields.date(string = "Año Fiscal", required = True),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]





