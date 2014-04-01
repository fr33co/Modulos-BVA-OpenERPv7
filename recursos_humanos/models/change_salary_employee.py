# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
from datetime import date

from openerp.osv import osv, fields

class Onchange_salary(osv.Model):
	_name="hr.change.salary"

	_order = 'salary'
	
	_rec_name = 'salary'

	
	def reason_change_salary(self, cr, uid, ids, context=None):

		salary_browse = self.browse(cr, uid, ids, context=None)
		
		for many_load_salary in salary_browse:
			experience 	= many_load_salary.experience
			salary_id 	= many_load_salary.salary
			charge_id 	= many_load_salary.charge.id
			degree_id 	= many_load_salary.degree_instruction.id

			print "Año de experiencia :"+str(experience)

			if int(experience)==0: # Bloque de código para validar si el año de experencia no tiene valor

				cr.execute("UPDATE hr_employee SET asignacion=%s WHERE job_id=%s AND grado_instruccion=%s;", (salary_id,charge_id,degree_id))
				
			elif int(experience)!=0: #Bloque de código para validar si el año de experencia tiene valor

				cr.execute("UPDATE hr_employee SET asignacion=%s WHERE job_id=%s AND grado_instruccion=%s AND ano_antiguedad=%s;", (salary_id,charge_id,degree_id,experience))
			
			return True

	def search_hr_data(self, cr, uid, ids, argument_search,item, context=None):

		values = {}
		mensaje = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('hr.employee')

		if item == "1":
		
			#======================== Busqueda por cargo ============================
			search_job_id = obj_dp.search(cr, uid, [('job_id','=',argument_search)])

			datos_job_id = obj_dp.read(cr,uid,search_job_id,context=context)
			#========================================================================
			
			if not datos_job_id:
				
				mensaje = {
						'title'   : "Cédula",
						'message' : "Disculpe no se encuentra registrado el cargo, intente de nuevo...",
				}

				values.update({
					
					'charge' : None,

					})

		elif item == "2":
			#========================================================================
			search_instruction = obj_dp.search(cr, uid, [('grado_instruccion','=',argument_search)])

			datos_instruction = obj_dp.read(cr,uid,search_instruction,context=context)
			#========================================================================

			if not datos_instruction:

				mensaje = {
						'title'   : "Cédula",
						'message' : "Disculpe no se encuentra registrado el Grado  de Instruccion, intente de nuevo...",
				}

				values.update({
					
					'degree_instruction' : None,

					})

		elif item == '3':

			now = datetime.now().strftime('%Y-%m-%d')
			if argument_search < now:
				
				mensaje = {
						'title'   : "Cambio de estátus",
						'message' : "Disculpe, no puede seleccionar una fecha anterior al actual, intente de nuevo...",
				}

				values.update({
					'date_onchange' : None,
					})

		return {'value' : values,'warning' : mensaje}
	
	
	_columns = {
		'salary': fields.char(string = "Sueldo", size = 7, required = True),
		'charge': fields.many2one("hr.job", "Cargo", required = True),
		'degree_instruction': fields.many2one("becados.gradoinstruccion", "Grado de Instruccción", required = True),
		'date_now': fields.date(string = "Fecha", required = True),
		'change_salary': fields.text(string = "Motivo del cambio", size = 256, required = False),
		'experience' : fields.char(string="Año de experiencia", size=2, required=False),
		'item' : fields.boolean(string=""),
	}

	_defaults = {
		'salary' : "0.000",
	}



