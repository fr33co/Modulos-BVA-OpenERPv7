# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class categoria_bienes_gba(osv.Model):

	"""
	Herencia de la clase categoria de producto, para poder agregarle los campos Grupo(g), Sub-Grupo(s)
	Sector(s).
	"""


	_inherit = "product.category"
	_columns = {
		'g' : fields.char(string="G", size=2, required=True),
		'sg' : fields.char(string="S/G", size=2, required=True),
		's' : fields.char(string="S", size=2, required=True),		
	}