# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class municipios(osv.Model):
	_name = "municipio"
	_order = 'municipio'
	_rec_name = 'municipio'
	_columns = {
		'municipio' : fields.char(string="Municipio", size=45, required=True),
	}