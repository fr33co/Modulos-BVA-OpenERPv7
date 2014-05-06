# -*- coding: utf-8 -*-
import time
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class movimientos_bva(osv.Model):

	_inherit = "stock.move"

	"""
	Metodo que genera el codigo 
	"""

	def _get_id_movimientos(self, cr, uid, ids, context = None):
	
		sfl_id       = self.pool.get('stock.move')
		srch_id      = sfl_id.search(cr,uid,[])
		rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
		

		if rd_id:
			id_documento = rd_id[-1]['correlativo']
			codigo = id_documento[3:]
			last_id      = codigo.lstrip('0')
			str_number   = str(int(last_id) + 1)
			codigo      = str_number.rjust(4,'0')
			print codigo
		else :
			str_number = '1'
			last_id      = str_number.rjust(4,'0')
			codigo      = last_id
		return codigo

	_columns = {
		'enviado' : fields.char(string="Responsable", size=50, required=False),
		'recibido' : fields.char(string="Responsable", size=50, required=False),
		'vigilante' : fields.char(string="Vigilante de Guardia", size=50, required=False),
		'g' : fields.char(string="G", required=False),
		'sg' : fields.char(string="S/G", required=False),
		's' : fields.char(string="S", required=False),
		'bva' : fields.char(string="N de Identificacion"),
		'estado' : fields.char(string="Status", required=False),
		'v_total' : fields.char(string="Valor Unitario Bs.", required=False),
		'nota' : fields.text(string="Nota", required=False),
		'correlativo' : fields.char(string="Correlativo", required=False),
		'justificacion' : fields.char(string="Justificación", required=False),
		'f_correlativo': fields.char('Fecha', required=False),
		'tipo_envio' : fields.selection((('Interno','Interno'), ('Externo','Externo')),'Tipo de Envio', required=False),
	}
	_defaults = {
		'f_correlativo': lambda *a: time.strftime("%Y"),
		'correlativo' : _get_id_movimientos,
	}
	
	def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False, loc_dest_id=False, partner_id=False):
		""" On change of product id, if finds UoM, UoS, quantity and UoS quantity.
		@param prod_id: Changed Product id
		@param loc_id: Source location id
		@param loc_dest_id: Destination location id
		@param partner_id: Address id of partner
		@return: Dictionary of values
		"""
		if not prod_id:
		    return {}
		user = self.pool.get('res.users').browse(cr, uid, uid)
		lang = user and user.lang or False
		if partner_id:
		    addr_rec = self.pool.get('res.partner').browse(cr, uid, partner_id)
		    if addr_rec:
			lang = addr_rec and addr_rec.lang or False
		ctx = {'lang': lang}
	
		product = self.pool.get('product.product').browse(cr, uid, [prod_id], context=ctx)[0]
		uos_id  = product.uos_id and product.uos_id.id or False
		if product.estado == '1':
			val = 'Bueno'
		else:
			val = 'Malo'
		print val
		result = {
			'product_uom': product.uom_id.id,
			'product_uos': uos_id,
			'product_qty': 1.00,
			'product_uos_qty' : self.pool.get('stock.move').onchange_quantity(cr, uid, ids, prod_id, 1.00, product.uom_id.id, uos_id)['value']['product_uos_qty'],
			'prodlot_id' : False,
			's': product.s,
			'g' : product.g,
			'sg' : product.sg,
			'estado' : val,
			'bva' : product.nidentificacion,
			#'cantidad' : datos.cantidad,
			'v_total' : product.v_total,
		}
		if not ids:
		    result['name'] = product.partner_ref
		if loc_id:
		    result['location_id'] = loc_id
		if loc_dest_id:
		    result['location_dest_id'] = loc_dest_id
		return {'value': result}