# -*- coding: utf-8 -*-
import time
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class desincorporaciones_bva(osv.Model):

	_name = "desincorporaciones.bva"
	_order = 'descripcion'
	_rec_name = 'descripcion'

	"""
	Metodo que genera el codigo se solicitud donde se busca el ultimo valor encontrado en la BD
	y se le suma 1.
	"""

	def _get_id_desincorporaciones(self, cr, uid, ids, context = None):

		sfl_id       = self.pool.get('desincorporaciones.bva')
		srch_id      = sfl_id.search(cr,uid,[])
		rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
		if rd_id:
			id_documento = rd_id[-1]['codigo']
			codigo = id_documento[3:]
			last_id      = codigo.lstrip('0')
			str_number   = str(int(last_id) + 1)
			last_id      = str_number.rjust(4,'0')
			codigo      = 'DES'+last_id
		else :
			str_number = '1'
			last_id      = str_number.rjust(4,'0')
			codigo      = 'DES'+last_id
		return codigo
	
	def on_change_cedula_presidente(self, cr, uid, ids, cedula_p, context=None):
	        values  = {}
	        valores = {}

	        valores = {
				'presidente' : None,
			}

	        if not cedula_p:
	            return values

	        sfl_get_row    = self.pool.get('desincorporaciones.bva')
	        srcnt_get_row = sfl_get_row.search_count(cr,uid,[('cedula_p','=',cedula_p)], context=None)

	        if srcnt_get_row > 0:
	            srch_get_row = sfl_get_row.search(cr,uid,[('cedula_p','=',cedula_p)])
	            rd_get_row    = sfl_get_row.read(cr, uid, srch_get_row,context=context)
	            valores = {
	                                'presidente': rd_get_row[0]['presidente'],
	                        }

	        values.update(valores)
	        return {'value' : values}
	
	def on_change_cedula_desincorporador(self, cr, uid, ids, cedula_b, context=None):
	        values  = {}
	        valores = {}

	        valores = {
				'desincorporado' : None,
			}

	        if not cedula_b:
	            return values

	        sfl_get_row    = self.pool.get('desincorporaciones.bva')
	        srcnt_get_row = sfl_get_row.search_count(cr,uid,[('cedula_b','=',cedula_b)], context=None)

	        if srcnt_get_row > 0:
	            srch_get_row = sfl_get_row.search(cr,uid,[('cedula_b','=',cedula_b)])
	            rd_get_row    = sfl_get_row.read(cr, uid, srch_get_row,context=context)
	            valores = {
	                                'desincorporado': rd_get_row[0]['desincorporado'],
	                        }

	        values.update(valores)
	        return {'value' : values}
	
	def on_change_cedula_administrador(self, cr, uid, ids, cedula_a, context=None):
	        values  = {}
	        valores = {}

	        valores = {
				'administradora' : None,
			}

	        if not cedula_a:
	            return values

	        sfl_get_row    = self.pool.get('desincorporaciones.bva')
	        srcnt_get_row = sfl_get_row.search_count(cr,uid,[('cedula_a','=',cedula_a)], context=None)

	        if srcnt_get_row > 0:
	            srch_get_row = sfl_get_row.search(cr,uid,[('cedula_a','=',cedula_a)])
	            rd_get_row    = sfl_get_row.read(cr, uid, srch_get_row,context=context)
	            valores = {
	                                'administradora': rd_get_row[0]['administradora'],
	                        }

	        values.update(valores)
	        return {'value' : values}

	_columns = {
		'codigo' : fields.char(string="Código", required=False),
		'desincorporado' : fields.char(string="Desincorporado por:", required=True),
		#'usuario_login': fields.many2one('res.users', 'Desincorporado por:', readonly=True),
		#'grupo': fields.many2one('res.groups', 'grupo:', readonly=False),
		'f_solicitud': fields.char('Fecha de Solicitud', readonly=True, required=True),
		'cedula_p': fields.char('Cedula del Presidente', readonly=False, required=True, size=8),
		'presidente': fields.char('Presidente (ACBBVVA)', readonly=False, required=True),
		'administradora': fields.char('Administrador (ACBBVVA):', readonly=False, required=True),
		'cedula_a': fields.char('Cedula de Administrador ', readonly=False, required=True, size=8),
		'cedula_b': fields.char('Cedula Jefe de Bienes', readonly=False, required=True, size=8),
		'f_solicitudr': fields.char('Fecha de Solicitud', readonly=True, required=True),
		'descripcion' : fields.text(string="Descripción de la desincorporación", required=True),
		't_desincorporacion': fields.many2one('procesos.desincorporacion', 'Proceso de Desincorporación:', required=True),
		#'jefa_bienes': fields.many2one('res.user', 'Jefa Unidad de Bienes', required=True),
		'bienes':fields.one2many('bienes.desincorporacion', 'inventario_ids',required=True),
		
		
	}

	_defaults = {
	    'codigo': _get_id_desincorporaciones,
	    #'usuario_login': lambda s, cr, uid, c: uid,
	    #'grupo': lambda s, cr, uid, c: uid,
	    'f_solicitud': lambda *a: time.strftime("%d/%B/%Y"),
	    'f_solicitudr': lambda *a: time.strftime("a los %d días del mes de %B del año %Y"),
	}

class bienes_desincorporar(osv.Model):

	_name = "bienes.desincorporacion"

	"""
	Metodo que de a cuerdo al elemento seleccionado trae de BD toda la informacion
	que contiene. 
	"""
	
	def on_change_bienes(self, cr, uid, ids, nidentificacion, context=None):
		values = {}
		if not nidentificacion:
			return values
		datos = self.pool.get('product.product').browse(cr, uid, nidentificacion, context=context)
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
		'inventario_ids':fields.many2one('desincorporaciones.bva', 'bienes', ondelete='cascade', select=False),
		'ubicacion' : fields.many2one('stock.location', 'Ubicacion', required=True),
		'nidentificacion' : fields.many2one('product.product', 'Nombre del Elemento',required=True),
		'g' : fields.char(string="G", required=False),
		'sg' : fields.char(string="S/G", required=False),
		's' : fields.char(string="S", required=False),
		'bva' : fields.char(string="N de Identificacion", size=20),
		'estado' : fields.char(string="Status", required=False),
		'v_unitario' : fields.char(string="Valor Unitario Bs.", required=False),
		'v_total' : fields.char(string="Valor Unitario Bs.", required=False),
		'cantidad' : fields.char(string="Cantidad", required=False),
	}