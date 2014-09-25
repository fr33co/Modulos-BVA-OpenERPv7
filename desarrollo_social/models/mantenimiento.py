# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class ClassName(osv.Model):
	_name="becados.mantenimiento"

	_columns = {

		
		'estado_civil': fields.char(string = "Estado Civil", size = 150, required = True),
	}

	_defaults = {

	}