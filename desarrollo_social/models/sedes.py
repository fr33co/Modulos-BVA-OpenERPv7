# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Sede(osv.Model):
	_name="becados.sedes"

	_order = 'sede'
	
	_rec_name = 'sede'
	
	_columns = {
		'codigo' : fields.char(string="Código", size=10, required=True),
		'eje' : fields.many2one("becados.ejes", "Eje", required = True),
		'sede': fields.char(string = "Sede", size = 150, required = True),
		'descripcion': fields.char(string = "Descripción", size = 150, required = True),
	}


