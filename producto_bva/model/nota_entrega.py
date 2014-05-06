# -*- coding: utf-8 -*-
import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class nota_de_entrega(osv.Model):

	_name = "nota.entrega"
	_columns = {
		#'area' : fields.char(string="Área Solicitante:", required=True),
		'area' : fields.many2one('stock.location', 'Área Solicitante', required=True),
		'fecha': fields.char('Fecha:', readonly=True,  required=True),
		'nombre' : fields.char(string="Nota de Entrega:", required=True),
		'almacen': fields.one2many('materiales.bva', 'materiales_id', string='Materiales'),
		'entregado' : fields.char(string="Entregador por:", required=True),
		'recibido' : fields.char(string="Recibido por:", required=True),
		#'ids' : fields.char(string="Transcriptor:", size=5, required=True),
		'c_nota' : fields.char(string="Correlativo:", size=6, readonly=True, required=True),
		't_materiales' : fields.selection((('Limpieza','Limpieza'), ('Oficina','Oficina'), ('Otros','Otros')),'Tipo de Material:', required=True),

	}
	def _get_last_id(self, cr, uid, ids, context = None):

                sfl_id       = self.pool.get('nota.entrega')
                srch_id      = sfl_id.search(cr,uid,[])
                rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
                if rd_id:
                    id_documento = rd_id[-1]['c_nota']
                    c_nota = id_documento[2:]
                    last_id      = c_nota.lstrip('0')
                    str_number   = str(int(last_id) + 1)
                    last_id      = str_number.rjust(4,'0')
                    codigo      = last_id
                else :
                    str_number = '1'
                    last_id      = str_number.rjust(4,'0')
                    codigo      = last_id
                return codigo

	_defaults = {
		'fecha': lambda *a: time.strftime("%d de %m de %Y"),
		'c_nota' : _get_last_id
	} 

class materiales_bva(osv.Model):

	_name = "materiales.bva"
	_columns = {
		'materiales_id':fields.many2one('nota.entrega', 'almacen', ondelete='cascade', select=False),
		'cantidad' : fields.char(string="Cantidad", required=True),
		#'unidad':fields.many2one('product.uom', 'Unidad de Medida',required=True),
		'descripcion':fields.many2one('materiales.almacen', 'Descripción del Material',required=True),
	}

	# def on_change_materiales(self, cr, uid, ids, descripcion, context=None):
	# 	values = {}
	# 	if not descripcion:
	# 		return values
	# 	datos = self.pool.get('materiales.almacen')
	# 	variable = datos.browse(cr, uid, descripcion, context=context)
	# 	rd_id        = datos.read(cr, uid, variable.id, ['unidad'], context=context)
	# 	u_material = rd_id['unidad']
	# 	values.update({
	# 		'unidad' : u_material,
	# 	})
	# 	return {'value' : values}