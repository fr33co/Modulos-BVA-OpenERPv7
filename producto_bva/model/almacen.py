# -*- coding: utf-8 -*-
import time
from openerp.osv import osv, fields
from datetime import datetime, timedelta

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

	_columns = {
		'codigo' : fields.char(string="Código", required=False),
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
	}