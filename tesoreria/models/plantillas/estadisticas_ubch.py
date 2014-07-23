# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
import os
import commands
from openerp.tools.translate import _
from openerp.osv import fields, osv
import base64#Necesario para la generación del .txt
import estadistica_ubch_reporte
import estadistica_ubch_reporte2
#~ import pdf_nominas
import unicodedata

class EstadisticasUBCH(osv.Model):

	_name = 'integrantes.estadisticas'
	
	#~ _rec_name = 'anyo'
	
	#Método para generar las estadísticas generales de los centros electorales
	def estadisticas_centros(self, cr, uid, ids, context=None):
		
		nom = "vacio"
		archivo = "vacio"
		
		browse_id = self.browse(cr, uid, ids, context=context)
		
		for estadistica in browse_id:
			id_est = estadistica.id
			todo = estadistica.todo
			estado = estadistica.estado.id
			municipio = estadistica.municipio.id
			nom_municipio = estadistica.municipio.name
			#~ print "Estadísticas de los centros electorales"
			
			if (todo == True):
				#Obtención de los valores retornados por la función que genera el archivo	de reporte de estadísticas
				nom, archivo = estadistica_ubch_reporte.gen_est_centros(cr, estado)
			else:
				if not municipio:
					#Obtención de los valores retornados por la función que genera el archivo	de reporte de estadísticas
					nom, archivo = estadistica_ubch_reporte.gen_est_centros(cr, estado)
				else:
					nom_municipio = estadistica.municipio.name.encode("UTF-8").decode("UTF-8")
					#Obtención de los valores retornados por la función que genera el archivo	de reporte de estadísticas
					nom, archivo = estadistica_ubch_reporte2.gen_est_centros_mun(cr, municipio)	
			
			if nom != "vacio" and archivo != "vacio":	
				#Registro del archivo de reporte en la base de datos
				id_att = self.pool.get('ir.attachment').create(cr, uid, {
					'estadistica_id': id_est, 
					'name': nom,
					'res_name': nom,
					#~ 'municipio' : nom_municipio,
					'datas': base64.encodestring(archivo.read()),
					'datas_fname': nom,
					'res_model': 'integrantes.estadisticas',
					}, context=context)
			else:
				raise osv.except_osv(_("Warning!"), _("No se generó el documento, no hay integrantes para el municipio selccionado."))
					
		return "Vacío"
	
	
	#Definición de las columnas del modelo----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	_columns = {
		'todo' : fields.boolean(string="Todos los municipios",required=False,help="Marque esta casilla para un reporte general"),
		'country_id' : fields.many2one("res.country", "País", required=True),
		'estado' : fields.many2one("res.country.state", "Estado", required = True, select="0"),
		'municipio' : fields.many2one("res.country.municipality", "Municipio", required = False, select="0"),
		'fecha_creacion' : fields.date(string="Fecha de creación", required = True),
	}
	
	_defaults = {
		'todo' : False,
		'country_id' : 240,
		'estado' : 55,
		'fecha_creacion' : lambda *a: time.strftime("%Y-%m-%d"),# formato corecto al español
	}
