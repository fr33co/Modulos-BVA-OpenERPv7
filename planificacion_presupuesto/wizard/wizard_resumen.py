# -*- coding: utf-8 -*-

import hashlib
import itertools
import logging
import os
import re
import class_pdf
import base64
import random
import unicodedata
import sys
from openerp import tools
from openerp.osv import fields,osv
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)
import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring #Necesario para la generación del .xsl
import netsvc
import tools
import logging
import xlwt
from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from xlwt import Borders
import os
import math
import re
import unicodedata
import base64 #Necesario para la generación del .xls

class wizard_resumen(osv.osv_memory):

	_name = "wizard.resumen"
	
	_order = "wizard_resumen"
	
	
	def resumen_de_proyectos(self, cr, uid, ids, context=None): # Generacion de inventario
	
		# Instancia de la clase heredada L es horizontal y P es vertical
		# format A4, A3 o letter que son los formatos de la hoja (oficio, carta, etc)
	
		pdf=class_pdf.PDF2(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Marcel Arcuri')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		#pdf.set_font('Times','',10) # TAMANO Y TIPO DE LETRA DE LA FUENTE
		pdf.set_font('Arial','B',15)
		pdf.set_fill_color(157,188,201) # COLOR DE BORDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		
		resumen = self.browse(cr, uid, ids, context=context)
		for m in resumen:
			fecha = m.year_fiscal
		
		datos = self.pool.get('observacion.proyecto') # Objeto 
		res = datos.search(cr, uid, [('a_fiscal','=',fecha)], context=None)
		resumen_ob = datos.read(cr,uid,res,context=context)
		
		pdf.set_line_width(0.25) #Grosor de la Linea
		pdf.set_draw_color(255,255,255) #Color de las Lineas
		pdf.set_fill_color(11,13,56) #Color de las Celdas
		pdf.set_text_color(255,255,255) #Color del Texto
		pdf.set_font('Arial','B',11) #Fuente de la Letra
		pdf.cell(190,5,"RESUMEN DE PROYECTOS".decode("UTF-8"),'LTBR',1,'C',1)
		
		for x in resumen_ob:
			ids = x['codigo']
			ente = acento (x['ente'][1])
			pro= acento(x['nombre_pro'])
			monto_asi = float(x['monto'])
			monto_sol = float(x['monto_solicitado'])
			
			pdf.set_line_width(0.25) #Grosor de la Linea
			pdf.set_draw_color(255,255,255) #Color de las Lineas
			pdf.set_fill_color(11,13,56) #Color de las Celdas
			pdf.set_text_color(255,255,255) #Color del Texto
			pdf.set_font('Arial','B',11) #Fuente de la Letra
			
			pdf.set_font('Arial','B',8)
			pdf.cell(190,5,ente,'',1,'L',1)
			pdf.cell(25,5,"Proyecto:".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.cell(165,5,"",'LTBR',1,'C',1)
			pdf.multi_cell(194,5,pro,'LTBR','J',1)
			pdf.set_fill_color(191,191,191) #Color de las Celdas
			pdf.set_text_color(0,0,0) #Color del Texto
			pdf.cell(50,5,"Monto Asignado:".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.cell(47,5,str(monto_asi),'LTBR',0,'C',1)
			pdf.set_fill_color(191,191,191) #Color de las Celdas
			pdf.set_text_color(0,0,0) #Color del Texto
			pdf.cell(50,5,"Monto Solicitado:".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.cell(47,5,str(monto_sol),'LTBR',1,'C',1)
			pdf.ln(1)
			
			pdf.set_draw_color(255,255,255) #Color de las Lineas
			pdf.set_fill_color(11,13,56) #Color de las Celdas
			pdf.set_text_color(255,255,255) #Color del Texto
			
		nom = "Resumen de Proyectos"+"-"+str(fecha)+'.pdf'
		pdf.output('openerp/addons/planificacion_presupuesto/reportes/'+nom,'F')
	
	def resumen_sectores(self, cr, uid, ids, context=None): # Generacion de inventario
	
		# Instancia de la clase heredada L es horizontal y P es vertical
		# format A4, A3 o letter que son los formatos de la hoja (oficio, carta, etc)
	
		pdf=class_pdf.PDF2(orientation='L',unit='mm',format='letter') #HORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Marcel Arcuri')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION

		pdf.set_margins(12,10,10) # MARGENE DEL DOCUMENTO
		pdf.set_font('Times','B',11)
		pdf.set_fill_color(255,255,255) #Color de las Celdas
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		
		resumen = self.browse(cr, uid, ids, context=context)
		for m in resumen:
			fecha = m.year_fiscal
			#sector = m.sector.id
			a = "Formulación Planificación y Presupuesto ".decode("UTF-8")
			b = ". Monto por categoría de planificación, según clasificación sectorial del gasto.".decode("UTF-8")
			titulo = a+str(fecha)+b

			datos = self.pool.get('organos.sectores') # Objeto
			result = datos.search(cr, uid, [], context=None)
			sectores = datos.read(cr,uid,result,context=context)
			pdf.set_line_width(0.25)
			pdf.cell(255,10,titulo,'',1,'C',1)
			pdf.set_draw_color(255,255,255)
			pdf.set_fill_color(11,13,56)
			pdf.set_text_color(255,255,255)
			
			pdf.set_font('Times','B',9)
			pdf.cell(85,18,"Clasificación sectorial del gasto".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.set_y(48)
			pdf.set_x(97)
			pdf.cell(170,5,"Categoría de planificación".decode("UTF-8"),'LTR',0,'C',1)
			pdf.set_y(53)
			pdf.set_x(97)
			pdf.cell(57,8,"Acción Centralizada".decode("UTF-8"),'LTR',0,'C',1)
			pdf.cell(56,8,"Proyecto".decode("UTF-8"),'LTR',0,'C',1)
			pdf.cell(57,8,"Total".decode("UTF-8"),'LTR',0,'C',1)
			pdf.set_y(61)
			pdf.set_x(97)
			pdf.cell(57,5,"Bs.".decode("UTF-8"),'LTR',0,'R',1)
			pdf.cell(56,5,"Bs.".decode("UTF-8"),'LTR',0,'R',1)
			pdf.cell(57,5,"Bs.".decode("UTF-8"),'LTR',1,'R',1)
			pdf.set_fill_color(255,255,255) # COLOR DE BOLDE DE LA CELDA
			pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
			i = 0
			
			for s in sectores:
				sectores = s['sectores']
				id_sector = s['id']
				#print sectores
				#print id_sector
			
				datos = self.pool.get('proyecto.conaplan') # Objeto
				res = datos.search(cr, uid, [('year_fiscal','=',fecha),('sector','=',sectores)], context=None)
				#res = datos.search(cr, uid, [('sector','=',sector)], context=None)
				resumen_sec = datos.read(cr,uid,res,context=context)
				sumatoria = 0.0
				total = 0.0
				
				for x in resumen_sec:
					#print 'Id'+str(x['c_solicitud'])
					#print 'Siglas'+str(x['siglas'])
					#print 'Monto'+str(x['costo_proyecto'])
					#print 'Sectores'+str(x['sector'])
					sector_res = x['sector']
					sumatoria += float(x['costo_proyecto'])
					
					
				#print ""+str(sumatoria)
					pdf.set_fill_color(255,255,255) # COLOR DE BOLDE DE LA CELDA
					if i % 2 == 0:
						pdf.set_fill_color(191,191,191) # COLOR DE LA CELDA
						
					pdf.set_font('Times','B',8)
					pdf.cell(85,5,acento(sectores).upper(),'LTBR',0,'L',1)
					pdf.set_font('Times','',8)
					pdf.cell(57,5,"0.0".decode("UTF-8"),'LTR',0,'R',1)
					pdf.cell(56,5,str(sumatoria),'LTR',0,'R',1)
					pdf.cell(57,5,"0.0".decode("UTF-8"),'LTR',1,'R',1)
					print i
					i = i +1
				total += float(sumatoria)
			
			pdf.set_font('Times','B',8)
			pdf.set_fill_color(97,97,97)
			pdf.set_text_color(255,255,255)
			pdf.cell(85,5,"Total".decode("UTF-8"),'LTBR',0,'L',1)
			pdf.cell(57,5,"189489984".decode("UTF-8"),'LTR',0,'R',1)
			pdf.cell(56,5,str(total),'LTR',0,'R',1)
			pdf.cell(57,5,"189489984".decode("UTF-8"),'LTR',1,'R',1)
	
		nom = "Planificación y Presupuesto "+str(fecha)+", según clasificación sectorial"+'.pdf'
		pdf.output('openerp/addons/planificacion_presupuesto/reportes/'+nom,'F')
			
	_columns = {
		#'acciones_ids':fields.many2one('proyecto.conaplan', 'acciones_especificas', ondelete='cascade', select=False),
		'year_fiscal': fields.selection([(num, str(num)) for num in range(2014, (datetime.now().year)+30 )], 'Año Fiscal', required=False),
		'sector':fields.many2one('organos.sectores', 'Sector', ondelete='cascade', select=False, required=False),

	}
def acento(cadena):
	result = cadena.encode('UTF-8').decode('UTF-8')# INSTITUCION
	return result
wizard_resumen()
	
