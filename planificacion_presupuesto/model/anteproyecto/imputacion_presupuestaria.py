# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class imputacion_presupuestaria(osv.Model):

	_name = "imputacion.presupuestaria"
	
	#Función para el cálculo de la cantidad de cada partida presupuestaria de un proyecto
	def suma_trimestres(self, cr, uid, ids, trim1, trim2, trim3, trim4, context=None):
		
		cantidad_meta = {}
		
		resultado = {}
		
		sumatotal = trim1+trim2+trim3+trim4
		
		cantidad_meta.update({'total_impu':sumatotal,})
		
		resultado = {'value':cantidad_meta}
		
		return resultado
			
	
	def on_change_partidas(self, cr, uid, ids, partida_presu, context=None):
		values = {}
		if not partida_presu:
			return values
		datos = self.pool.get('partida.presupuestaria').browse(cr, uid, partida_presu, context=context)

		values.update({
			'codigo' : datos.codigo,

		})
		return {'value' : values}
	
	def on_change_codigos(self, cr, uid, ids, codigo, context=None):
		values = {}
		if not codigo:
			return values
		
		sfl_get_row    = self.pool.get('partida.presupuestaria')
		search_direccion = sfl_get_row.search(cr,uid,[('id','=',codigo)])
	        rd_get_row    = sfl_get_row.read(cr, uid, search_direccion,context=context)
		print rd_get_row
		#cod = self.pool.get('partida.presupuestaria').browse(cr, uid, codigo, context=context)
		#print cod
		#values.update({
		#	'partida_presu' : cod.partida.id,
		#
		#})
		return {'value' : values}

	_columns = {
		'imputacion_ids':fields.many2one('proyecto.conaplan', 'imputacion_presupuestaria', ondelete='cascade', select=False),
		'partida_presu' : fields.many2one('partida.presupuestaria', 'Partida Presupuestaria', required=False),
		'codigo' : fields.char(string="Código", required=False),
		#'partida_presu' : fields.char(string="Partida Presupuestaria", required=False),
		'trim_1' : fields.float(string="Trimestre I", required=False),
		'trim_2' : fields.float(string="Trimestre II", required=False),
		'trim_3' : fields.float(string="Trimestre III", required=False),
		'trim_4' : fields.float(string="Trimestre IV", required=False),
		'total_impu' : fields.float(string="Cantidad", required=False),
	}
