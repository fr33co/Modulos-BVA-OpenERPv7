# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class parroquias(osv.Model):
	_name = "parroquia"
	_order = 'parroquia'
	_rec_name = 'parroquia'
	_columns = {
		'municipio': fields.many2one('municipio', 'Municipio', required=True),
		'parroquia' : fields.char(string="Parroquia", size=25, required=True),
	}