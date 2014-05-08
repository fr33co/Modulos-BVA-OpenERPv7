# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import class_pdf
import time
import base64
from time import gmtime, strftime
from datetime import datetime, timedelta

class almacen_bva(osv.Model):

	_name = "inventario.almacen"

	_columns = {
		'nombre' : fields.char(string="Nombre de Referencia", required=True),
                'usuario_login': fields.many2one('res.users', 'Registrado por:', readonly=False),
		'ubicacion' : fields.many2one('stock.location', 'Área Solicitante', required=False),
                'date': fields.datetime('Fecha de Creación', required=True, ),
		'almacen': fields.one2many('inventario.materiales', 'inventario_id', string='Materiales'),
                't_materiales' : fields.selection((('1','Limpieza'), ('2','Oficina'), ('Otros','Otros')),'Tipo de Material', required=False),
	}
        _defaults = {
            'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
	    'usuario_login': lambda s, cr, uid, c: uid,
        }



class inventario_materiales(osv.Model):

	_name = "inventario.materiales"

	_columns = {
		'inventario_id':fields.many2one('inventario.almacen', 'inventario', ondelete='cascade', select=False),
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