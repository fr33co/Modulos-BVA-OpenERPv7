# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Sede(osv.Model):
	_name="hr.concepts"

	_order = 'concepto'
	
	_rec_name = 'concepto'


	def search_code_hr_concepts(self, cr, uid, ids, codigo, context=None):

		values = {}
		mensaje = {}
		
		if not codigo:
			return values
		obj_dp = self.pool.get('hr.concepts')

		busqueda = obj_dp.search(cr, uid, [('codigo','=',codigo)])

		datos = obj_dp.read(cr,uid,busqueda,context=context)
		

		if int(datos[0]['codigo']):
			
			mensaje = {
					'title'   : "Codigo de Concepto",
					'message' : "Disculpe este codigo ya esta asignado al concepto "+datos[0]['concepto']+", intente de nuevo...",
			}

			values.update({
				
				'codigo' : None,

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



