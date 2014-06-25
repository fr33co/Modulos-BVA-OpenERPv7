# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class metas_accion_especifica(osv.Model):

	_name = "metas.especificas"
	
	#Función para el cálculo del total de cada meta
	def suma_trimestres(self, cr, uid, ids, trim1, trim2, trim3, trim4, context=None):
		
		cantidad_meta = {}
		
		resultado = {}
		
		sumatotal = trim1+trim2+trim3+trim4
		
		cantidad_meta.update({'total_trim':sumatotal,})
		
		resultado = {'value':cantidad_meta}
		
		return resultado


	_columns = {
		'metas_acc_espec':fields.many2one('accion.centralizada', 'metas_accion_especifica', ondelete='cascade', select=False),
		'actividades' : fields.char(string="Actividades", required=False),
		'trim_1' : fields.float(string="I Trimestre", required=False),
		'trim_2' : fields.float(string="II Trimestre", required=False),
		'trim_3' : fields.float(string="III Trimestre", required=False),
		'trim_4' : fields.float(string="IV Trimestre", required=False),
		'total_trim' : fields.float(string="TOTAL", required=False),

	}