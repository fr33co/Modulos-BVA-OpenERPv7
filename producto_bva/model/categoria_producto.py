# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class categoria_producto_bva(osv.Model):

	_inherit = "product.category"
	_columns = {
		'g' : fields.char(string="G", size=2, required=True),
		'sg' : fields.char(string="S/G", size=2, required=True),
		's' : fields.char(string="S", size=2, required=True),		
	}