# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class metas_financieras(osv.Model):

	_name = "metas.financieras"
	
	#Función para el cálculo de la cantidad de cada meta de un proyecto
	def suma_trimestres(self, cr, uid, ids, trim1, trim2, trim3, trim4, context=None):
		
			cantidad_meta = {}
			
			resultado = {}
			
			sumatotal = trim1+trim2+trim3+trim4
			
			cantidad_meta.update({'total_meta':sumatotal,})
			
			resultado = {'value':cantidad_meta}
			
			return resultado
			

	_columns = {
		'metas_ids':fields.many2one('proyecto.conaplan', 'metas_financieras', ondelete='cascade', select=False),
		'nom_accion_metas' : fields.char(string="Nombre de la Acción Específica", required=False),
		'trim_1' : fields.float(string="Trimestre I", required=False),
		'trim_2' : fields.float(string="Trimestre II", required=False),
		'trim_3' : fields.float(string="Trimestre III", required=False),
		'trim_4' : fields.float(string="Trimestre IV", required=False),
		'total_meta' : fields.float(string="Cantidad", required=False),
	}

