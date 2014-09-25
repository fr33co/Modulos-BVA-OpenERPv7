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
from openerp.tools.translate import _
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
	
		pdf=class_pdf.PDF2(orientation='P',unit='mm',format='letter') #ORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Marcel Arcuri')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		#pdf.set_font('Times','',10) # TAMANO Y TIPO DE LETRA DE LA FUENTE
		pdf.set_font('Arial','B',15)
		pdf.set_fill_color(157,188,201) # COLOR DE BORDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		pdf.set_margins(10,10,10)
		pdf.set_line_width(0.25) #Grosor de la Linea
		pdf.set_draw_color(255,255,255) #Color de las Lineas
		pdf.set_fill_color(11,13,56) #Color de las Celdas
		pdf.set_text_color(255,255,255) #Color del Texto
		pdf.set_font('Arial','B',11) #Fuente de la Letra
		#pdf.cell(190,5,"RESUMEN DE PROYECTOS"+str(fecha).decode("UTF-8"),'LTBR',1,'C',1)
		resumen = self.browse(cr, uid, ids, context=context)
		fecha = 0
		for m in resumen:
			fecha = m.year_fiscal
			pdf.set_draw_color(255,255,255) #Color de las Lineas
			pdf.set_fill_color(97,97,97)
			pdf.set_text_color(255,255,255)
			pdf.cell(190,5,"RESUMEN DE PROYECTOS - "+str(fecha).decode("UTF-8"),'LTBR',1,'C',1)
			datos = self.pool.get('observacion.proyecto') # Objeto 
			res = datos.search(cr, uid, [('a_fiscal','=',fecha)], context=None)
			resumen_ob = datos.read(cr,uid,res,context=context)
			
		total_soli = 0.0
		total_asig = 0.0
		monto_sol  = 0.0
		monto_asi  = 0.0
		total_so   = 0.0
		total_as   = 0.0
		
		cr.execute('select s.id, s.sectores from organos_sectores as s inner join organos_entes as os on s.id=os.sector inner join proyecto_conaplan as pc on os.id=pc.organismo inner join observacion_proyecto as op on pc.id=op.codigo  where op.a_fiscal = \''+str(fecha)+'\' group by  s.codigo,s.id order by s.codigo')
		
		for arr_sector in cr.fetchall():					
			id_sec   = arr_sector[0]
			sectores = arr_sector[1]

			
			pdf.set_draw_color(255,255,255) #Color de las Lineas
			pdf.set_fill_color(224,224,224)
			pdf.set_text_color(0,0,0)
			pdf.set_font('Arial','B',10)
			pdf.multi_cell(190,5,sectores,'LTBR','J',1)
			
			tot_proyec = 0
			cr.execute('select os.id,btrim(os.nombre_ente,\' \') from organos_sectores as s inner join organos_entes as os on s.id=os.sector inner join proyecto_conaplan as pc on os.id=pc.organismo inner join observacion_proyecto as op on pc.id=op.codigo where op.a_fiscal =\''+str(fecha)+'\' AND os.sector = '+str(id_sec)+' group by os.nombre_ente,os.id') 
			for arr_ente in cr.fetchall():
				id_ente     = arr_ente[0]
				nombre_ente = arr_ente[1]
				pdf.set_font('Arial','B',8)
				pdf.set_fill_color(237,237,237)
				pdf.cell(190,5,nombre_ente.upper(),'',1,'L',1)
				pdf.cell(25,5,"Proyectos:".decode("UTF-8"),'LTBR',0,'C',1)
				
				
				
				cr.execute('select DISTINCT op.nombre_pro, op.monto, op.monto_solicitado from organos_sectores as s  inner join organos_entes as os on s.id=os.sector inner join proyecto_conaplan as pc on os.id=pc.organismo  inner join observacion_proyecto as op on pc.id=op.codigo where op.a_fiscal = \''+str(fecha)+'\' AND os.id='+str(id_ente)+' ORDER BY op.monto, op.monto_solicitado DESC') 
				for arr_proyecto in cr.fetchall():
					nomb_proy   = arr_proyecto[0]
					monto_proye = arr_proyecto[1]
					monto_solic = arr_proyecto[2]
					
					pdf.set_font('Arial','',8)
					pdf.set_fill_color(255,255,255)
					pdf.set_text_color(24,29,31)
					pdf.cell(165,5,"",'LTBR',1,'C',1)
					pdf.multi_cell(190,5,nomb_proy.capitalize(),'LTBR','J',1)
					#pdf.set_fill_color(191,191,191) #Color de las Celdas
					pdf.set_text_color(0,0,0) #Color del Texto
					pdf.set_font('Arial','B',8)
					pdf.cell(50,5,"Monto Asignado:".decode("UTF-8"),'LTBR',0,'L',1)
					pdf.set_fill_color(255,255,255)
					pdf.set_text_color(24,29,31)
					pdf.cell(47,5,str(monto_proye),'LTBR',0,'R',1)
					#pdf.set_fill_color(191,191,191) #Color de las Celdas
					pdf.set_text_color(0,0,0) #Color del Texto
					pdf.cell(50,5,"Monto Solicitado:".decode("UTF-8"),'LTBR',0,'R',1)
					pdf.set_fill_color(255,255,255)
					pdf.set_text_color(24,29,31)
					pdf.cell(43,5,str(monto_solic),'LTBR',1,'R',1)
				
				print id_ente
				total_asig = 0.0
				total_soli = 0.0
				cr.execute('select SUM(op.monto), SUM(op.monto_solicitado) from organos_sectores as s inner join organos_entes as os on s.id=os.sector inner join proyecto_conaplan as pc on os.id=pc.organismo inner join observacion_proyecto as op on pc.id=op.codigo where op.a_fiscal = \''+str(fecha)+'\' AND os.id='+str(id_ente)+'') 
				for subtotal in cr.fetchall():
					total_asig   = subtotal[0]
					total_soli   = subtotal[1]
				pdf.cell(190,5,"________________________________________________________________________________________________________________________".decode("UTF-8"),'LTBR',1,'L',1)
				pdf.cell(50,5,"Sub Total Asignado:".decode("UTF-8"),'LTBR',0,'L',1)	
			        pdf.cell(47,5,str(total_asig),'LTBR',0,'R',1)	
				pdf.cell(50,5,"Sub Total Solicitado:".decode("UTF-8"),'LTBR',0,'R',1)	
			        pdf.cell(43,5,str(total_soli),'LTBR',1,'R',1)
			        	
				pdf.ln(5)
		
		pdf.set_draw_color(255,255,255) #Color de las Lineas
		pdf.set_fill_color(11,13,56) #Color de las Celdas
		pdf.set_text_color(255,255,255) #Color del Texto
		
		pdf.set_draw_color(255,255,255) #Color de las Lineas
		pdf.set_fill_color(97,97,97)
		pdf.set_text_color(255,255,255)
		cr.execute('select SUM(op.monto), SUM(op.monto_solicitado) from organos_sectores as s inner join organos_entes as os on s.id=os.sector inner join proyecto_conaplan as pc on os.id=pc.organismo inner join observacion_proyecto as op on pc.id=op.codigo where op.a_fiscal = \''+str(fecha)+'\'') 
		for total in cr.fetchall():
			total_as   = total[0]
			total_so   = total[1]
		pdf.cell(80,5,"Totales:".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.cell(40,5,"Montos Asignados:".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,5,"Bs. "+str(total_as),'LTBR',1,'R',1)
		pdf.cell(40,5,"Montos Solicitados:".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,5,"Bs. "+str(total_so),'LTBR',1,'R',1)
			
		nom = "Resumen de Proyectos"+"-"+str(fecha)+'.pdf'
	
		pdf.output('/home/jdaponte/openerp7/openerp/addons/planificacion_presupuesto/reportes/'+nom,'F')
		#pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')
		archivo = open('/home/jdaponte/openerp7/openerp/addons/planificacion_presupuesto/reportes/'+nom)
		#archivo = open('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom)
		r_archivo = self.pool.get('reportes.generales').create(cr, uid, {
		    'name' : nom,
		    'res_name' : nom,
		    'datas' : base64.encodestring(archivo.read()),
		    'datas_fname' : nom,
		    'res_model' : 'wizard.resumen',
		    'registro': 'Resumen de proyectos',
		},context=context)
	
	def resumen_sectores(self, cr, uid, ids, context=None): # Generacion de inventario
	
		# Instancia de la clase heredada L es horizontal y P es vertical
		# format A4, A3 o letter que son los formatos de la hoja (oficio, carta, etc)
	
		pdf=class_pdf.PDF(orientation='L',unit='mm',format='letter') #ORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Marcel Arcuri')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION

		pdf.set_margins(12,10,10) # MARGENE DEL DOCUMENTO
		pdf.set_font('Times','B',11)
		pdf.set_fill_color(255,255,255) #Color de las Celdas
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		resumen = self.browse(cr, uid, ids, context=context)
		campo = self.read(cr, uid, ids, context=context)[0] # Lectura del objeto propio
		
		for m in resumen:
			fecha = m.year_fiscal
			
			if not campo['year_fiscal']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe seleccionar el Año Fiscal"))
			else:
				
				cr.execute('select count(s.sectores)from organos_sectores as s inner join organos_entes as os on s.id=os.sector inner join proyecto_conaplan as pc on os.id=pc.organismo inner join accion_centralizada as ac on os.id=ac.organismo where year_fiscal ='+str(fecha))
				for resumen in cr.fetchall():
					prueba = resumen[0]
				
				if prueba == 0:
					raise osv.except_osv(_("Warning!"), _("Disculpe NO hay Registros para el Año Fiscal Seleccionado"))
				
				cr.execute("select s.sectores, sum(pc.costo_proyecto), sum(ac.total_metas), sum(pc.costo_proyecto) + sum(ac.total_metas) as suma_tot, CASE WHEN sum(pc.costo_proyecto)=0 THEN 'Bs.0,00' ELSE to_char(sum(pc.costo_proyecto),'FML9G999G999G999G999G999D00') END as total_proyectos, CASE WHEN sum(ac.total_metas)=0 THEN 'Bs.0,00' ELSE to_char(sum(ac.total_metas),'FML9G999G999G999G999G999D00') END as total_acciones, CASE WHEN sum(pc.costo_proyecto) + sum(ac.total_metas)=0 THEN 'Bs.0,00'ELSE to_char(sum(pc.costo_proyecto) + sum(ac.total_metas),'FML9G999G999G999G999G999D00')  END as total_montos, s.codigo from organos_sectores as s inner join organos_entes as os on s.id=os.sector inner join proyecto_conaplan as pc on os.id=pc.organismo inner join accion_centralizada as ac on os.id=ac.organismo where year_fiscal ="+str(fecha)+" group by s.sectores,s.codigo order by s.codigo")
				print cr.execute

				a = "Formulación Planificación y Presupuesto ".decode("UTF-8")
				b = ". Monto por categoría de planificación, según clasificación sectorial del gasto.".decode("UTF-8")
				titulo = a+str(fecha)+b
				
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
				total_acc = 0.0
				total_pro = 0.0
				total_global = 0.0
				for resumen in cr.fetchall():
					
					#print "Sectores para organismos: "+str(resumen[0].encode("UTF-8"))
					#print float(resumen[1])
					sector = resumen[0]
					total_sec_pro = resumen[1]
					total_sec_acc = resumen[2]
					total_final = resumen[3]

					monto_pro = resumen[4]
					monto_acc = resumen[5]
					monto_final = resumen[6]
					codigo = resumen[7]
					
					pdf.set_fill_color(255,255,255) # COLOR DE BOLDE DE LA CELDA
					if i % 2 == 0:
						pdf.set_fill_color(191,191,191) # COLOR DE LA CELDA
						
					pdf.set_font('Times','B',8)
					pdf.cell(85,5,acento(sector).upper(),'LTBR',0,'L',1)
					pdf.set_font('Times','',8)
					pdf.cell(57,5,str(monto_acc),'LTR',0,'R',1)
					pdf.cell(56,5,str(monto_pro),'LTR',0,'R',1)
					pdf.cell(57,5,str(monto_final),'LTR',1,'R',1)
					#print i
					i = i +1
					total_pro += float(total_sec_pro)
					total_acc += float(total_sec_acc)
					total_global += float(total_final)
				pdf.set_font('Times','B',8)
				pdf.set_fill_color(97,97,97)
				pdf.set_text_color(255,255,255)
				pdf.cell(85,5,"Total".decode("UTF-8"),'LTBR',0,'L',1)
				pdf.cell(57,5,"Bs. "+addComa(str(total_acc)),'LTR',0,'R',1)
				pdf.cell(56,5,"Bs. "+addComa(str(total_pro)),'LTR',0,'R',1)
				pdf.cell(57,5,"Bs. "+addComa(str(total_global)),'LTR',1,'R',1)
			
				nom = "Planificación y Presupuesto "+str(fecha)+" según clasificación sectorial"+'.pdf'
				
				
				#rutausuario =  os.getcwd()
				#rutax       = os.path.split(rutausuario+'planificacion_presupuesto')
				#rutadir     = rutax[0]
				
				
				ruta_fun = ruta('')
				
				pdf.output(ruta_fun+'/reportes/'+nom,'F')
				#pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')
				archivo = open(ruta_fun+'/reportes/'+nom)
				
				
				#pdf.output('openerp/addons/planificacion_presupuesto/reportes/'+nom,'F')
				#pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')
				#archivo = open('openerp/addons/planificacion_presupuesto/reportes/'+nom)
				#archivo = open('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom)
				r_archivo = self.pool.get('reportes.generales').create(cr, uid, {
				'name' : nom,
				'res_name' : nom,
				'datas' : base64.encodestring(archivo.read()),
				'datas_fname' : nom,
				'res_model' : 'wizard.resumen',
				'registro': 'Resumen de sectores',
				},context=context)
				
	_columns = {
		#'acciones_ids':fields.many2one('proyecto.conaplan', 'acciones_especificas', ondelete='cascade', select=False),
		'year_fiscal': fields.selection([(num, str(num)) for num in range(2014, (datetime.now().year)+30 )], 'Año Fiscal', required=False),
		'sector':fields.many2one('organos.sectores', 'Sector', ondelete='cascade', select=False, required=False),

	}
def acento(cadena):
	result = cadena.encode('UTF-8').decode('UTF-8')# INSTITUCION
	return result
wizard_resumen()
	
def addComa( snum ):
    "Adicionar comas como separadores de miles a n. n debe ser de tipo string"
    s = snum;
    i = s.index('.') # Se busca la posición del punto decimal
    while i > 3:
        i = i - 3
        s = s[:i] +  '#' + s[i:]
	
    n = s.replace(".", ",", 5);
    t = n.replace("#", ".", 5);
    return t

def ruta( usuario ):
    ruta = '/home'
    if usuario == 'administrador':
        ruta = '/home/administrador/openerp70/modules/planificacion_presupuesto'

    return ruta
