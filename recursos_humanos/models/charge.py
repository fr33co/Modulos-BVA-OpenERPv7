# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import fields, osv

class Cargo_empleado(osv.Model):

	'''Herenciando a hr.job (Cargo)'''

	_inherit = 'hr.job'

	_columns = {
		'asignacion' : fields.char(string="Asignacion", size = 20),

	}

	_defaults = {
		# 'fecha_actual': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al espa?ol
	}


