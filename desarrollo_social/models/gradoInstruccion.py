# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class gradoInstruccion(osv.Model):
	_name="becados.gradoinstruccion"

	_columns = {
		'grado_instruc': fields.char(string = "Grado de Instrucción", size = 150, required = True),
	}


