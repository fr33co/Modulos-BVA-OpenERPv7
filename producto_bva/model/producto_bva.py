# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class producto_bva(osv.Model):

	_inherit = "product.product"
	_columns = {
		'g' : fields.char(string="G", size=2, required=True),
		'sg' : fields.char(string="S/G", size=2, required=True),
		's' : fields.char(string="S", size=2, required=True),
		'estado' : fields.selection((('1','Bueno'), ('2','Malo')),'Status', required=True),
		'codigo' : fields.selection((('BBV','BBV'), ('BVA','BVA'), ('BE','BE'), ('No se codifica','No se codifica')),'Código Bien Nacional', required=True),
		'numero' : fields.char(string="N de Identificacion", size=20),
		'nidentificacion' : fields.char(string="N de Identificacion", size=20),
		'v_unitario' : fields.float(string="Valor Unitario Bs.", size=20, required=True),
		'v_total' : fields.float(string="Valor Total Bs.", size=20, required=True),
	}

	def on_change_codigo(self, cr, uid, ids, codigo, context=None):
		values = {}

		if codigo == 'No se codifica': 
			codigo_id2 = 'No se codifica'
		else: 
			codigo_id2 = ''

		values.update({'nidentificacion' : codigo_id2,})
		return {'value' : values}

	def on_change_identificacion(self, cr, uid, ids, numero, codigo, context=None):
		values = {}
		if not numero:
			return values

		codigo_id = codigo+'-'+numero

		values.update({'nidentificacion' : codigo_id,})
		return {'value' : values}        		
