# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Onchange_status(osv.Model):
	_name="hr.onchange.status"

	_order = 'cedula_employee'
	
	_rec_name = 'cedula_employee'

	# MÉTODO DE BUSQUEDA PARA CAMBIO DE ESTÁTUS


	def search_onchange_status(self, cr, uid, ids, argument_search, context=None):

		values = {}
		mensaje = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('hr.employee')
		
		#======================== Busqueda por código ============================

		search_obj_code = obj_dp.search(cr, uid, [('cedula','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		
		#=========================================================================

		if not datos_code:
			
			mensaje = {
					'title'   : "Cambio de estátus",
					'message' : "Disculpe el registro no existe, intente de nuevo...",
			}

			values.update({
				
				'cedula_employee' : None,
				'nom' : None,
				'charge' : None,
				'status' : None,

				})

		else:

			values.update({
				
				'nom' : datos_code[0]['name'],
				'charge' : datos_code[0]['job_id'],
				'status' : datos_code[0]['status'],

				})

			
		return {'value' : values,'warning' : mensaje}

	
	def reason_change_read(self, cr, uid, ids, context=None):

		status_model = self.pool.get('hr.employee')
		status_browse = self.browse(cr, uid, ids, context=None)
		
		for many_load_id in status_browse:

			id_fill = many_load_id.status
			#print "ESTE ES EL ESTATUS: "+str(id_fill)
			cedula = many_load_id.cedula_employee

			cr.execute("UPDATE hr_employee SET status=%s WHERE cedula=%s;", (id_fill, cedula))
			
		return True
	
	
	_columns = {
		'cedula_employee': fields.char(string = "Cédula", size = 9, required = True),
		'nom': fields.char(string = "Nombres", size = 256, required = False),
		'charge': fields.many2one("hr.job", "Cargo", required = False),
		#'status': fields.many2one("becados.status", "Estátus", required = True),
		'status' : fields.selection((('1','Activo'),('2','Periódo de gracia'),('3','Permiso de reposo'),('4','Permiso no remunerado'),('5','Suspendido'),('6','Vacaciones')), "Estatus", required = False),
		'date_onchange': fields.date(string = "Fecha", required = True),
		'reason_change': fields.text(string = "Descripción", size = 256, required = True),
	}

	_defaults = {
		#'codigo' : 
	}


