# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class distribucion_actividades_trimestrales(osv.Model):

	_name = "actividades.trimestrales"
	
	#Función para el cálculo del total de cada actividad
	def suma_trimestres(self, cr, uid, ids, trim1, trim2, trim3, trim4, context=None):
		
		total_actividad = {}
		
		resultado = {}
		
		sumatotal = trim1+trim2+trim3+trim4
		
		total_actividad.update({'total_trim':sumatotal,})
		
		resultado = {'value':total_actividad}
		
		return resultado
	
	

	_columns = {
		'act_trimestral_ids':fields.many2one('accion.centralizada', 'actividades_trimestrales', ondelete='cascade', select=False),
		'actividades' : fields.char(string="Actividades", required=False),
		'trim_1' : fields.integer(string="I Trimestre", required=False),
		'trim_2' : fields.integer(string="II Trimestre", required=False),
		'trim_3' : fields.integer(string="III Trimestre", required=False),
		'trim_4' : fields.integer(string="IV Trimestre", required=False),
		'total_trim' : fields.integer(string="TOTAL", required=False),

	}