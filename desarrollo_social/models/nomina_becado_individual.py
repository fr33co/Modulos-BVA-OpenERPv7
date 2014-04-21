# -*- coding: utf-8 -*-

import time #Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class NominaBecadoIndividual(osv.Model):
	_name="becados.nominaindividual"

	_order = 'codigo'
	
	_rec_name = 'codigo'
	
	#Función para la carga automática del monto de la asignación correspondiente al becado según el tipo de beca seleccionado
	def carga_asignacion(self, cr, uid, ids, tipo_beca, context=None):
		
		valores = {}	
		
		if not tipo_beca:
			return valores
		
		#~ print tipo_beca
		
		#Seleccionamos el modelo de búsqueda
		modelo = self.pool.get('becados.tipobeca')		
		
		#Verificamos si la nómina individual del becado ya fue generada (se toma en cuenta el código)
		search_tipobeca = modelo.search(cr, uid, [('id','=',tipo_beca)])
		#~ print search_tipobeca
		
		if search_tipobeca:
			leer_tipobeca = modelo.read(cr, uid, search_tipobeca, context=context)
			
			valores.update({
				'asignacion' : leer_tipobeca[0]['asignacion'],
			})
		
		return {'value':valores}
	
	_columns = {
		'nomina' : fields.many2one("becados.nomina", "Nómina", required=False),
		'codigo' : fields.char(string="Código", size=20, required=False),
		'becado': fields.many2one("hr.employee", "Becado", required = True, domain=[('categoria','=','1'),('status','=','1')]),
		'anyo' : fields.char(string="Año",required=True),
		'mes' : fields.selection((('Enero','Enero'),('Febrero','Febrero'),('Marzo','Marzo'),('Abril','Abril'),('Mayo','Mayo'),('Junio','Junio'),('Julio','Julio'),('Agosto','Agosto'),('Septiembre','Septiembre'),('Octubre','Octubre'),('Noviembre','Noviembre'),('Diciembre','Diciembre')),"Mes",required=True),
		'tipo_beca' : fields.many2one("becados.tipobeca", "Tipo de Beca", required=True),
		'asignacion' : fields.float(string="Asignación", required=True) 
	}
	
	_defaults = {
		'anyo' : lambda *a: time.strftime("%Y"),
	}
