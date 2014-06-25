# -*- coding: utf-8 -*-
import time
from openerp.osv import osv, fields, orm
from datetime import datetime, timedelta
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import tools

class almacen_bva(osv.Model):

	_name = "materiales.almacen"
	_order = 'descripcion'
	_rec_name = 'descripcion'

	"""
	Metodo que genera el codigo se solicitud donde se busca el ultimo valor encontrado en la BD
	y se le suma 1.
	"""

	def _get_id_material(self, cr, uid, ids, context = None):

		sfl_id       = self.pool.get('materiales.almacen')
		srch_id      = sfl_id.search(cr,uid,[])
		rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
		if rd_id:
			id_documento = rd_id[-1]['codigo']
			codigo = id_documento[1:]
			last_id      = codigo.lstrip('0')
			str_number   = str(int(last_id) + 1)
			last_id      = str_number.rjust(4,'0')
			codigo      = 'M'+last_id
		else :
			str_number = '1'
			last_id      = str_number.rjust(4,'0')
			codigo      = 'M'+last_id
		return codigo
	
	#def cantidad_materiales(self, cr, uid, ids, context=None):
	#	if context is None:
	#	    context = {}
	#
	#	#rec_id = context and context.get('active_id', False)
	#	#assert rec_id, _('Active ID is not set in Context')
	#
	#	inventry_obj = self.pool.get('inventario.almacen') #se llama al objeto donde daremos la cantidad y ubicacion
	#	inventry_line_obj = self.pool.get('inventario.materiales') #se llama al objeto que contiene el one2many
	#	prod_obj_pool = self.pool.get('materiales.almacen') #El objeto de donde se esta haciendo el cambio
	#
	#	#res_original = prod_obj_pool.browse(cr, uid, rec_id, context=context)
	#	for data in self.browse(cr, uid, ids, context=context):
	#		if data.cantidad < 0: #Validacion de que la cantidad no puede ser menor a 0
	#			raise osv.except_osv(_('Atencion!'), _('Las cantidades no pueden ser negativas'))
	#	
	#		inventory_id = inventry_obj.create(cr , uid, {'nombre': _('INV: %s')}, context=context)
	#		print data.descripcion
	#		line_data ={
	#			'inventario_id' : inventory_id,
	#			'cantidad' : data.cantidad,
	#			'gerencia' : data.location_id.id,
	#			'descripcion' : data.id,
	#			'unidad' : data.unidad.id
	#		}
	#		inventry_line_obj.create(cr , uid, line_data, context=context)
	#
	#	return {}

	_columns = {
		'codigo' : fields.char(string="Código", required=False, readonly=True),
		'fecha': fields.char('Fecha:', readonly=True,  required=True),
		'user_register': fields.many2one('res.users', 'Registrado por:', readonly=True),
		't_materiales' : fields.selection((('Limpieza','Limpieza'), ('Oficina','Oficina'), ('Otros','Otros')),'Tipo de Material', required=False),
		'unidad':fields.many2one('product.uom', 'Unidad de Medida',required=True),
		'descripcion' : fields.char(string="Descripción del Material", required=True),
	}
	
	#Restriccion para que la descripcion del Material sea unica y evitar duplicidad
	_sql_constraints = [
	('descripcion_unique','UNIQUE(descripcion)','Material ya registrado'),
	]
	
	"""
	Por Defecto:
		- El campo codigo genera un codigo unico que incrementa con cada registro.
		- El campo user_register muestra automaticamente el usuario logeado.
	"""
	_defaults = {
		'codigo': _get_id_material,
		'user_register': lambda s, cr, uid, c: uid,
		'fecha': lambda *a: time.strftime("%d/%m/%Y"),
	}