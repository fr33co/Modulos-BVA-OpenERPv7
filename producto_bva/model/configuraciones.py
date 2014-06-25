# -*- coding: utf-8 -*-
import time
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class codigos_bva(osv.Model):

	_name = "codigos.bva"
	_order = 'codigo'
	_rec_name = 'codigo'
	
	"""
	Modelo para agregar codigos de bien nacional y que verifica que no se repitan.
	"""
	_columns = {
		'codigo' : fields.char(string="Código", required=False),
		'descripcion' : fields.text(string="Descripción", required=False),
	}

	_sql_constraints = [
        ('codigo_unique','UNIQUE(codigo)','Código ya registrado'),
    ]

class incorporaciones_bva(osv.Model):

	_name = "procesos.incorporaciones"
	_order = 'incorporaciones'
	_rec_name = 'incorporaciones'
	"""
	Modelo para agregar los procesos de incorporacion.
	"""
	_columns = {
		'incorporaciones' : fields.char(string="Incorporado por:", required=False),
		'descripcion' : fields.text(string="Descripción", required=False),
	}

	_sql_constraints = [
        ('procesoi_unique','UNIQUE(incorporaciones)','Proceso ya registrado'),
    ]

class desincorporaciones_bva(osv.Model):

	_name = "procesos.desincorporacion"
	_order = 'desincorporaciones'
	_rec_name = 'desincorporaciones'
	"""
	Modelo para agregar los procesos de desincorporacion.
	"""
	_columns = {
		'desincorporaciones' : fields.char(string="Desincorporado por:", required=False),
		'descripcion' : fields.text(string="Descripción", required=False),
	}

	_sql_constraints = [
        ('procesod_unique','UNIQUE(desincorporaciones)','Proceso ya registrado'),
    ]