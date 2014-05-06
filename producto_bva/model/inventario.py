# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class inventario_bva(osv.Model):

	_inherit = "stock.inventory"

	_columns = {
		'usuario_login': fields.many2one('res.users', 'Registrado por:', readonly=True),
		'ubicacion' : fields.many2one('stock.location', 'Área Solicitante', required=True),
		't_inventario' : fields.selection((('Bienes','Bienes'), ('Materiales','Materiales')),'Tipo de Inventario', required=False),
		'almacen': fields.one2many('inventario.materiales', 'inventario_id', string='Materiales'),
		't_materiales' : fields.selection((('1','Limpieza'), ('2','Oficina'), ('Otros','Otros')),'Tipo de Material', required=False),	
	}

	_defaults = {
		'usuario_login': lambda s, cr, uid, c: uid,
	} 

class almacen_bva(osv.Model):

	_name = "inventario.materiales"

	_columns = {
		'inventario_id':fields.many2one('stock.inventory', 'inventario', ondelete='cascade', select=False),
		# 'id' : fields.char(string="Item", required=False),
		'cantidad' : fields.char(string="Cantidad", required=True),
		'unidad':fields.many2one('product.uom', 'Unidad de Medida',required=True),
		'descripcion':fields.many2one('materiales.almacen', 'Descripción del Material',required=True),
	}

	def on_change_materiales(self, cr, uid, ids, descripcion, context=None):
		values = {}
		if not descripcion:
			return values
		datos = self.pool.get('materiales.almacen')
		variable = datos.browse(cr, uid, descripcion, context=context)
		rd_id        = datos.read(cr, uid, variable.id, ['unidad'], context=context)
		u_material = rd_id['unidad']
		values.update({
			'unidad' : u_material,
		})
		return {'value' : values}
	
class inventario_bva2(osv.Model):

 	#_name = "bva.inventario"
 	_inherit = "stock.inventory.line"
	
	"""
	Metodo que de a cuerdo al elemento seleccionado trae de BD toda la informacion
	que contiene. 
	"""
	
	def on_change_productos(self, cr, uid, ids, product_id, context=None):
		values = {}
		if not product_id:
			return values
		datos = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
		print datos.estado
		if datos.estado == '1':
			val = 'Bueno'
		else:
			val = 'Malo'
		print val
		values.update({
			'g' : datos.g,
			'sg' : datos.sg,
			's' : datos.s,
			'estado' : val,
			'bva' : datos.nidentificacion,
			#'cantidad' : datos.cantidad,
			'v_unitario' : datos.v_unitario,
			'v_total' : datos.v_total,
		})
		return {'value' : values}
	
	_columns = {

 		'g' : fields.char(string="G", required=False),
 		'sg' : fields.char(string="S/G", required=False),
 		's' : fields.char(string="S", required=False),
 		'nidentificacion' : fields.char(string="N de Identificacion", required=True),
 		'estado' : fields.char(string="Status", required=False),
 		'v_unitario' : fields.char(string="Valor Unitario Bs.", required=False),
 		'v_total' : fields.char(string="Valor Unitario Bs.", required=False),
 	}

