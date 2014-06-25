# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class acciones_especificas(osv.Model):

	_name = "acciones.especificas"
	
	_order = "nombre_accion"
	
	_rec_name = "nombre_accion"
	
	#Función para el cálculo de la cantidad de cada acción de un proyecto
	def suma_trimestres(self, cr, uid, ids, trim1, trim2, trim3, trim4, context=None):
		
		cantidad_meta = {}
		
		resultado = {}
		
		sumatotal = trim1+trim2+trim3+trim4
		
		cantidad_meta.update({'total':sumatotal,})
		
		resultado = {'value':cantidad_meta}
		
		return resultado
			

	_columns = {
		'acciones_ids':fields.many2one('proyecto.conaplan', 'acciones_especificas', ondelete='cascade', select=False),
		'nombre_accion' : fields.char(string='Nombre de la Acción Específica', size=40, required=False),
		'unidad_medida' : fields.char(string="Unidad de Medida", size=25, required=False),
		'medio' : fields.char(string="Medio de Verificación", size=25, required=False),
		'trim_i' : fields.integer(string="Trimestre I", required=False),
		'trim_ii' : fields.integer(string="Trimestre II", required=False),
		'trim_iii' : fields.integer(string="Trimestre III", required=False),
		'trim_iv' : fields.integer(string="Trimestre IV", required=False),
		'total' : fields.integer(string="Total", required=False),
	}
