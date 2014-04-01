# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Eje(osv.Model):
	_name="becados.ejes"

	_order = 'eje'
	
	_rec_name = 'eje'
	
	_columns = {
		'eje': fields.char(string = "Eje", size = 150, required = True),
	}
