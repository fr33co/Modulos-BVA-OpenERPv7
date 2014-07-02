# -*- coding: utf-8 -*-
import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class tipo_acciones_centralizadas(osv.Model):

	_name = "tipo.accion.centralizada"
	
	_rec_name ="a_centralizada"
	_order = "a_centralizada"
	_columns = {
		
		'a_centralizada' : fields.char(string="Acción Centralizada", required=False),
		
	}
	
class tipo_acciones_especificas(osv.Model):

	_name = "tipo.accion.especifica"

	_rec_name ="a_especifica"
	_columns = {
		
		'a_especifica' : fields.char(string="Acción Específica", required=False),
		'a_centralizada': fields.many2one('tipo.accion.centralizada', 'Acción Centralizada', required=True),
	}

class partidas_centralizadas(osv.Model):

	_name = "partida.centralizada"

	_rec_name ="partida"
	_columns = {
		
		'partida' : fields.many2one('partida.presupuestaria', 'Partida Presupuestaria', required=False),
		'codigo' : fields.char(string="codigo", required=False),
		'a_centralizada': fields.many2one('tipo.accion.centralizada', 'Acción Centralizada', required=True),
		
	}
	
	def on_change_partida(self, cr, uid, ids, argument_search,item, context=None):

		values = {}
		mensaje = {}

		if not argument_search:
			return values
		
		obj_dp = self.pool.get('partida.presupuestaria')

		if item == "1":
			#======================== Busqueda por cargo ============================
			search_id = obj_dp.search(cr, uid, [('id','=',argument_search)])
			datos_id = obj_dp.read(cr,uid,search_id,context=context)
			#========================================================================
			if datos_id:
				values.update({
					'codigo' : datos_id[0]['codigo'],
					})
		elif item == "2":
			#======================== Busqueda por cargo ============================
			search_cod = obj_dp.search(cr, uid, [('codigo','=',argument_search)])
			datos_cod = obj_dp.read(cr,uid,search_cod,context=context)
			#========================================================================
			if datos_cod:
				values.update({
					'partida' : datos_cod[0]['id'],
					})
		return {'value' : values,'warning' : mensaje}


class partidas_presupuestaria(osv.Model):

	_name = "partida.presupuestaria"

	_rec_name ="partida"
	_columns = {
		
		'partida_padre' : fields.many2one('partida.presupuestaria', 'Partida padre', required=False),
		'codigo' : fields.char(string="Código", required=True),
		'partida' : fields.char(string="Nombre de la partida", required=True),
	}