# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
import os
from datetime import date
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
from openerp.osv import fields, osv
import math
from openerp.tools.translate import _

class Gestion_eventos(osv.Model):
	
	_name = 'gestion.eventos'
	_rec_name = 'actividad'
	# METODO PARA TRAER EL NOMBRE DEL GERENTE ADSCRITO
	def search_ins_geren(self, cr, uid, ids, argument_search, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('gestion.inst.gerencia')
		
		#======================== Busqueda por Gerencia ============================

		search_obj_code = obj_dp.search(cr, uid, [('id','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		#=========================================================================
		if not datos_code[0]['gerente']:
			
			values.update({
				
				'responsable' : None,
				})
		else:
			
			values.update({
				
				'responsable' : datos_code[0]['gerente'],
				})

		return {'value' : values}


	# METODO VALIDADOR PARA ESTABLECER INICIO Y FIN DE LAS FECHAS DEL EVENTO
	def search_date_ini(self, cr, uid, ids, fecha, context=None):
		values = {}
		mensaje = {}
		
		if not fecha:
			
			return values
		
		now = datetime.now().strftime('%Y-%m-%d')
		
		if fecha < now:
			
			mensaje = {
					'title'   : "Eventos",
					'message' : "Disculpe, no puede seleccionar una fecha anterior al actual, intente de nuevo...",
			}

			values.update({
				'fecha_inicio' : None,
				})

		return {'value' : values,'warning' : mensaje}

	def search_date_fin(self, cr, uid, ids, fecha, context=None):
		values = {}
		mensaje = {}
		
		if not fecha:
			
			return values
		
		now = datetime.now().strftime('%Y-%m-%d')
		
		if fecha < now:
			
			mensaje = {
					'title'   : "Eventos",
					'message' : "Disculpe, no puede seleccionar una fecha posterior a la fecha de inicio, intente de nuevo...",
			}

			values.update({
				'fecha_fin' : None,
				})

		return {'value' : values,'warning' : mensaje}

	# ESTATUS REALIZADO
	def gestion_realizado(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': '2'}, context=context)
	# ESTATUS SUSPENDIDO
	def gestion_suspendido(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': '3'}, context=context)
	# ESTATUS REPROGRAMADO
	def gestion_reprogramado(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': '4'}, context=context)
	# ESTATUS ATRASADO
	def gestion_atrasado(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': '5'}, context=context)
	########################################################################
	# ESTATUS CANCELADO
	def gestion_cancelar(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': '6'}, context=context)


	_columns = {
		######################################################################################
		# GESTION DE EVENTOS
		######################################################################################
		'institucion' : fields.many2one("gestion.inst.gerencia", "Institución / Gerencia", required = True),
		'responsable' : fields.char(string="Responsable", size=150, required=False),
		'actividad' : fields.char(string="Actividad", size=256, required=True),
		'fecha_inicio' : fields.date(string="Fecha Inicio", required=True),
		'fecha_fin' : fields.date(string="Fecha Fin", required=True),
		'hora_inicio' : fields.char(string="Hora Inicio", size=25, required=True),
		'hora_fin' : fields.char(string="Hora Fin", size=25, required=True),
		'direccion' : fields.text(string='Dirección', required=False),
		'nacionalidad' : fields.many2one("res.country", "Nacionalidad", required = False),
		'estado' : fields.many2one("res.country.state", "Estado", required = False, select="0"),
		'ciudad' : fields.many2one("res.country.city", "Ciudad", required = False, select="0"),
		'municipio' : fields.many2one("res.country.municipality", "Municipio", required = True, select="0"),
		'parroquia' : fields.many2one("res.country.parish", "Parroquia", required = False, select="0"),
		'participantes' : fields.char(string="Participantes", size=120, required=True),
		'observacion' : fields.text(string='Observación', required=False),
		'recursos': fields.text(string="Recursos", size=500, required=False),
		'status_logistico' : fields.selection([('1','Aprobado totalmente'),('2','Aprobado Parcialmente'),('3','No Aprobado')], string="Estado", required=False),
		'observacion_rl': fields.text(string="Observaciones", size=500, required=False),
		'si' : fields.boolean(string="Si"),
		'no' : fields.boolean(string="No"),
		'user': fields.many2one('res.users', 'Registrado por:', readonly=True), # Usuario logeado
		'descripcion' : fields.text(string='Descripciòn', required=False),
		'motivo' : fields.text(string='Motivo', required=False),
		'rep_event_si' : fields.boolean(string="Si"),
		'rep_event_no' : fields.boolean(string="No"),
		'status' : fields.selection([('1','Pendiente'),('2','Realizado'),('3','Pospuesto'),('4','Reprogramado'),('5','Atrasado'),('6','Cancelado')], string="Acción", required=False),
		'inicio' : fields.selection([('1','AM'),('2','PM')], string="", required=False),
		'fin' : fields.selection([('1','AM'),('2','PM')], string="", required=False),
		######################################################################################
	}
	
	_defaults = {
		'nacionalidad' : 240, # Nacionalidad por defecto
		'estado' : 55, # Estado por defecto
		'ciudad' : 16, # Ciudad por defecto
		'status' : '1', # Estatus por defecto Pendiente
		'hora_inicio' : '00:00',
		'hora_fin' : '00:00',
		'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
	} 
