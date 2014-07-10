# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
import os
from openerp.tools.translate import _
from openerp.osv import fields, osv
import base64#Necesario para la generación del .txt
import estadistica_ubch_reporte
#~ import pdf_nominas
import unicodedata

class EstadisticasUBCH(osv.Model):

	_name = 'integrantes.estadisticas'
	
	#~ _rec_name = 'anyo'
	
	#Método para generar las estadísticas generales de los centros electorales
	def estadisticas_centros(self, cr, uid, ids, context=None):
		
		browse_id = self.browse(cr, uid, ids, context=context)
		
		for estadistica in browse_id:
			id_est = estadistica.id
			todo = estadistica.todo
			estado = estadistica.estado.id
			municipio = estadistica.municipio.id
			#~ print "Estadísticas de los centros electorales"
			
			#~ print str(todo)
			#Obtención de los valores retornados por la función que genera el archivo	de reporte de estadísticas
			nom, archivo = estadistica_ubch_reporte.gen_est_centros(cr, todo, municipio)
			#Registro del archivo de reporte en la base de datos
			id_att = self.pool.get('ir.attachment').create(cr, uid, {
				'integrante_id': id_est, 
				'name': nom,
				'res_name': nom,
				'datas': base64.encodestring(archivo.read()),
				'datas_fname': nom,
				'res_model': 'integrantes.estadisticas',
				}, context=context)
					
		return "Vacío"
	
	
	#Definición de las columnas del modelo----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	_columns = {
		'todo' : fields.boolean(string="Todo",required=False),
		'country_id' : fields.many2one("res.country", "País", required=True),
		'estado' : fields.many2one("res.country.state", "Estado", required = True, select="0"),
		'municipio' : fields.many2one("res.country.municipality", "Municipio", required = False, select="0"),
		'fecha_creacion' : fields.date(string="Fecha de creación", required = True),
	}
	
	_defaults = {
		'todo' : True,
		'country_id' : 240,
		'estado' : 55,
		'fecha_creacion' : lambda *a: time.strftime("%Y-%m-%d"),# formato corecto al español
	}
