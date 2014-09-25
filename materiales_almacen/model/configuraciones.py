# -*- coding: utf-8 -*-
import time
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class codigos_gba(osv.Model):

	_name = "codigos.gba"
	_order = 'codigo'
	_rec_name = 'codigo'
	
	"""
	Modelo para agregar codigos de bien nacional y que verifica que no se repitan.
	"""
	_columns = {
		'codigo' : fields.char(string="Código", required=True),
		'descripcion' : fields.text(string="Descripción", required=False),
	}

	_sql_constraints = [
		('codigo_unique','UNIQUE(codigo)','Código ya registrado'),
	]
	