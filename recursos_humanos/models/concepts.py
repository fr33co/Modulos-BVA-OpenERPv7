# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Sede(osv.Model):
	_name="hr.concepts"

	_order = 'concepto'
	
	_rec_name = 'concepto'

	# MÉTODO DE BUSQUEDA PARA CONCEPTOS
	
	def search_hr_concepts(self, cr, uid, ids, argument_search, context=None):

		values = {}
		mensaje = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('hr.concepts')
		
		#======================== Busqueda por código ============================

		search_obj_code = obj_dp.search(cr, uid, [('codigo','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		
		#======================= Busqueda por descripcion ========================
		
		search_obj_concept = obj_dp.search(cr, uid, [('concepto','=',argument_search)])

		datos_concept = obj_dp.read(cr,uid,search_obj_concept,context=context)
		
		#=========================================================================		

		if datos_code:
			
			mensaje = {
					'title'   : "Código de Concepto",
					'message' : "Disculpe este codigo ya esta asignado al concepto "+datos_code[0]['concepto']+", intente de nuevo...",
			}

			values.update({
				
				'codigo' : None,

				})
								
		elif datos_concept:
			
			mensaje = {
					'title'   : "Descripción del Concepto",
					'message' : "Disculpe esta descripcion ya esta asignado al concepto "+datos_concept[0]['codigo']+", intente de nuevo...",
			}

			values.update({
				
				'concepto' : None,

				})
			
		return {'value' : values,'warning' : mensaje}
	
	_columns = {
		'codigo': fields.char(string = "Código", size = 4, required = True),
		'concepto': fields.text(string = "Concepto", size = 256, required = True),
		'formula': fields.char(string = "Fórmula", size = 200, required = True),
	}

	_defaults = {
		#'codigo' : 
	}



