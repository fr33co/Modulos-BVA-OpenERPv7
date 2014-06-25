# -*- coding: utf-8 -*-}
from openerp.osv import fields, osv, orm
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import tools
from openerp.osv import osv, fields

class producto_bva(osv.Model):

	_inherit = "product.product"
	_columns = {
		'g' : fields.char(string="G", size=2, required=True),
		'sg' : fields.char(string="S/G", size=2, required=True),
		's' : fields.char(string="S", size=2, required=True),
		'estado' : fields.selection((('1','Bueno'), ('2','Malo')),'Status', required=True),
		'codigo':fields.many2one('codigos.bva', 'Código',required=True),
		#'codigo' : fields.selection((('BBV','BBV'), ('BVA','BVA'), ('BE','BE'), ('No se codifica','No se codifica')),'Código Bien Nacional', required=True),
		'numero' : fields.char(string="Número del Bien", size=20),
		'nombre_des' : fields.char(string="Nombre y Descripción del Elemento"),
		'union' : fields.char(string="Relación"),
		'nidentificacion' : fields.char(string="N de Identificacion", size=20),
		'v_unitario' : fields.float(string="Valor Unitario Bs.", size=20, required=True),
		'v_total' : fields.float(string="Valor Total Bs.", size=20, required=True),
		'serial' : fields.char(string="Serial", required=False),
		'donacion' : fields.boolean("Donación"),
		'ubicacion' : fields.many2one('stock.location', 'Ubicación Actual', required=False),
		#'incorporacion': fields.many2one('procesos.incorporaciones', 'Incorporación por', required=False),
	}
	
	_defaults = {
		'sale_ok': False,
		'type': 'product',
		}

	"""    
	Este metodo valida que de ser seleccionado en el codigo del bien el parametro "No se codifica"
	automaticamente envia al campo invisible (nidentificacion) el parametro "No se codifica" 
	para se mostrado en el registro
	"""
	
	def on_change_codigo(self, cr, uid, ids, codigo, numero, name, nombre_des, serial, context=None):
		values = {}
		datos = self.pool.get('codigos.bva')
		variable = datos.browse(cr, uid, codigo, context=context)
		rd_id        = datos.read(cr, uid, variable.id, ['codigo'], context=context)
		c_bien = rd_id['codigo']
		
		if c_bien == 'No se codifica':
			
			codigo_id2 = 'No se codifica'
			num = ""
		else:
			codigo_id2 = c_bien
			num = ""
		if c_bien == 'Ilegible':
			
			codigo_id2 = 'Ilegible'
			num = ""
		else:
			codigo_id2 = c_bien
			num = ""
		
		n_descrip = str(nombre_des)+' Serial:'+str(serial)
		relacion =  str(n_descrip)+' '+str(codigo_id2)
			
		values.update({'nidentificacion' : codigo_id2, 'union' : relacion, 'name' : n_descrip,'numero' : num,})
		return {'value' : values}

	"""
	Metodo ubicado en el campo status a modo que una vez que se seleccione el status del bien
	automaticamente genere la concatenación de los campos nombre_des codigo y numero en un solo
	campo invisible el cual se somete a un sqlcontraing a modo de evitar duplicidad de los 
	registros. A su vez une el campo codigo y numero para asi generar el codigo de bien Nacional
	completo.
	"""

	def on_change_identificacion(self, cr, uid, ids, estado, codigo, numero, name, nombre_des, serial, context=None):
		values = {}
		serial2 = ''
		if not estado:
			return values
		
		datos = self.pool.get('codigos.bva')
		variable = datos.browse(cr, uid, codigo, context=context)
		rd_id        = datos.read(cr, uid, variable.id, ['codigo'], context=context)
		c_bien = rd_id['codigo']
		
		if c_bien == 'No se codifica':
			
			codigo_id = str(c_bien)
		else:
			
			codigo_id = str(c_bien)+'-'+str(numero)
			
		if c_bien == 'Ilegible':
			
			codigo_id = str(c_bien)
		else:
			
			codigo_id = str(c_bien)+'-'+str(numero)
			

		n_descrip = str(nombre_des)+' Serial:'+str(serial)
		relacion =  str(n_descrip)+' '+str(codigo_id)
		
		values.update({'nidentificacion' : codigo_id, 'union' : relacion, 'name' : n_descrip,})
		return {'value' : values}

	"""
	Metodo ubicado en el campo status a modo que una vez que se seleccione el status del bien
	automaticamente genere la concatenación de los campos nombre_des codigo y numero en un solo
	campo invisible el cual se somete a un sqlcontraing a modo de evitar duplicidad de los 
	registros. A su vez une el campo codigo y numero para asi generar el codigo de bien Nacional
	completo.
	"""

	def on_change_identificacion_numero(self, cr, uid, ids, codigo, numero, name, nombre_des, serial, context=None):
		values = {}
		serial2 = ''
		if not numero:
			return values
		
		datos = self.pool.get('codigos.bva')
		variable = datos.browse(cr, uid, codigo, context=context)
		rd_id        = datos.read(cr, uid, variable.id, ['codigo'], context=context)
		c_bien = rd_id['codigo']
		
		if c_bien == 'No se codifica':
			
			codigo_id = str(c_bien)
		else:
			
			codigo_id = str(c_bien)+'-'+str(numero)
			
		if c_bien == 'Ilegible':
			
			codigo_id = str(c_bien)
		else:
			
			codigo_id = str(c_bien)+'-'+str(numero)
			

		n_descrip = str(nombre_des)+' Serial:'+str(serial)
		relacion =  str(n_descrip)+' '+str(codigo_id)
		
		values.update({'nidentificacion' : codigo_id, 'union' : relacion, 'name' : n_descrip,})
		return {'value' : values}
	
	"""
	Metodo que dependiendo de la categoria del producto que selecciones trae toda la infomacion
	de la clasificacion del mismo.
	"""

	def on_change_clasificacion(self, cr, uid, ids, categ_id, context=None):
		values = {}
		if not categ_id:
			return values
		datos = self.pool.get('product.category').browse(cr, uid, categ_id, context=context)
		values.update({
			'g' : datos.g,
			'sg' : datos.sg,
			's' : datos.s,
		})
		return {'value' : values}
	
	#Restriccion para que la descripcion del Material sea unica y evitar duplicidad
	#_sql_constraints = [
	#	('descripcion_unique','UNIQUE(union)','Elemento ya registrado con el mismo nombre, serial y código de bien'),
	#]
	


class ubicacion_producto(osv.Model):

	_inherit = "stock.change.product.qty"
	
	def cambiar_producto(self, cr, uid, ids, context=None):
		""" Changes the Product Quantity by making a Physical Inventory.
		@param self: The object pointer.
		@param cr: A database cursor
		@param uid: ID of the user currently logged in
		@param ids: List of IDs selected
		@param context: A standard dictionary
		@return:
		"""
		if context is None:
		    context = {}
	
		rec_id = context and context.get('active_id', False)
		assert rec_id, _('Active ID is not set in Context')
	
		inventry_obj = self.pool.get('stock.inventory')
		inventry_line_obj = self.pool.get('stock.inventory.line')
		prod_obj_pool = self.pool.get('product.product')
	
		res_original = prod_obj_pool.browse(cr, uid, rec_id, context=context)
		for data in self.browse(cr, uid, ids, context=context):
			if data.new_quantity < 0:
			    raise osv.except_osv(_('Warning!'), _('Quantity cannot be negative.'))
			inventory_id = inventry_obj.create(cr , uid, {'name': _('INV: %s') % tools.ustr(res_original.name)}, context=context)
			ubic= data.location_id.id
			prod = res_original.id
			line_data ={
			    'inventory_id' : inventory_id,
			    'product_qty' : data.new_quantity,
			    'location_id' : data.location_id.id,
			    'product_id' : rec_id,
			    'product_uom' : res_original.uom_id.id,
			    'prod_lot_id' : data.prodlot_id.id
			}
			inventry_line_obj.create(cr , uid, line_data, context=context)

			inventry_obj.action_confirm(cr, uid, [inventory_id], context=context)
			inventry_obj.action_done(cr, uid, [inventory_id], context=context)
			
			cr.execute("UPDATE product_product SET ubicacion=%s WHERE id=%s;", (ubic, prod))
			#self.write(cr, uid, ids,{'ubicacion':ubic},context=context)
			#product_obj.write(cr, uid, [id_m_desc], {'cantidad':resta_valor}, context=None)
		return {}
	
	# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
