# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import fields, osv

class Empleado(osv.Model):
	
	'''Herenciando a hr_applicant (empleados)'''
	
	#_order = "empleado"
	
	_inherit = 'hr.applicant'

	
	_columns = {
		'hola' : fields.char(string="hola", size = 50, required=False),
	}
	
	_defaults = {
		#'date_now': lambda *a: time.strftime("(%d) días del mes %B del año %Y"),# formato corecto al español
		
	} 
