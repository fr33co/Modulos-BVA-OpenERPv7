# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Banco(osv.Model):
	_name = "becados.bancos"
	
	_order = "banco"
	
	_rec_name = "banco"
	
	_columns = {
		'codigo' : fields.char(string="Código", size=10, required=False),
		'banco' : fields.char(string="Entidad Bancaria", size=50, required=False),
	}

