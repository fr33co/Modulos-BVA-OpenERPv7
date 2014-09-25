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

class wizard_resumen_inventario(osv.osv_memory):

	_name = "wizard.resumen.inventario"
	
	#_order = "wizard_resumen"
	
	def format_fecha(self, fecha):
		date = fecha.split("-")
		nueva_fecha = date[2]+"-"+date[1]+"-"+date[0]
		return nueva_fecha
	
	def buscar_tipo_material(self, cr, uid, ids, t_materiales, context=None): # Proceso de busqueda de tipo de material

		values = {}
		mensaje = {}
		
		if not t_materiales:
		    
		    return values
		obj_dp = self.pool.get('inventario.materiales')
		
		#======================== Busqueda por id ============================
		id_mate     = obj_dp.search(cr, uid, [('t_materiales','=',t_materiales)])
	
		t_material  = obj_dp.read(cr,uid,id_mate,context=context)
		#=========================================================================
		
		if not t_material:
			mensaje = {
				'title'   : "Busqueda por Tipo de Material",
				'message' : "Disculpe, no hay materiales inventariados a esta categoria, intente de nuevo...",
			}
	
			values.update({
				't_materiales' : None,
			})
	
		return {'value' : values,'warning' : mensaje}
	
	
	def generar_inventario_almacen(self, cr, uid, ids, context=None): # Generacion de inventario
		# Instancia de la clase heredada L es horizontal y P es vertical
		
		pdf=class_pdf.PDF3(orientation='P',unit='mm',format='letter' ) #HORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Marcel Arcuri')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		pdf.set_font('Arial','B',10)
		pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		pdf.set_margins(20,10,10) # MARGENE DEL DOCUMENTO
		#pdf.ln(20) # Saldo de linea
		# 10 y 50 eje x y y 200 dimencion
		#pdf.line(10, 40, 200, 40) Linea
		
		resumen = self.browse(cr, uid, ids, context=context)
		
		mate = ""
		for m in resumen:
			material = m.t_materiales
			fecha = self.format_fecha(m.fecha)
			if int(material) == 1:
				mate = "Limpieza"
			elif int(material) == 2:
				mate = "Oficina"
			elif int(material) == 3:
				mate = "Servicios Generales"
			elif int(material) == 4:
				mate = "Tecnológico"
		
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',12)
			pdf.set_y(10)
			pdf.set_x(60)
			pdf.write(50,"Inventario de Materiales de "+mate+" al "+fecha)
			pdf.set_y(15)
			pdf.set_x(75)
			pdf.write(50,"Unidad de Bienes y Suministros")
			pdf.set_y(20)
			pdf.set_x(80)
			pdf.write(50,"A. C. Biblioteca Virtuales")
			pdf.ln(30)
			
			pdf.cell(15,5,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(25,5,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(140,5,"Descripción del Material".decode("UTF-8"),'LTBR',1,'C',1)
		
		datos = self.pool.get('inventario.materiales') # Objeto 
		res = datos.search(cr, uid, [('t_materiales','=',material)], context=None)
		resumen_por_tipo = datos.read(cr,uid,res,context=context)

		k = 0
		j = 0
		item = 0
		for x in resumen_por_tipo:
			descrip = acento(x['descripcion'][1])
			cantidad= int(x['cantidad'])
			unidad = str(x['unidad'][0])
			
			if j == 25:
				
				pdf.add_page()
				pdf.ln(8)
				pdf.set_fill_color(255,255,255)
				pdf.set_font('Arial','B',12)
				pdf.set_y(10)
				pdf.set_x(60)
				pdf.write(50,"Inventario de Materiales de "+mate+" al "+fecha)
				pdf.set_y(15)
				pdf.set_x(80)
				pdf.write(50,"Unidad de Bienes y Suministros")
				pdf.set_y(20)
				pdf.set_x(85)
				pdf.write(50,"A. C. Biblioteca Virtuales")
				pdf.ln(10)
				
				pdf.cell(15,5,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(25,5,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(127,5,"Descripción del Material".decode("UTF-8"),'LTBR',1,'C',1)
		
		
				# Fin Cabezera
				j=0
			
			# Filas que vienen de la BD
			item = int(item) + 1
			if unidad == "11":
				unid = "Lt"
			else:
				unid = ""
			if unidad == "3":
				unid = "Kg"
			else:
				unid = ""
			
			pdf.set_font('Arial','',10)
			pdf.cell(15,5,str(item).decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(25,5,str(cantidad)+" "+unid,'LTBR',0,'C',1)
			pdf.cell(140,5,descrip,'LTBR',1,'L',1)

		
			if k == 24 : 
				pdf.ln(5)
				pdf.set_font('Arial','B',12)
				pdf.cell(90,6,"REALIZADO POR",'LTBR',0,'C',0)
				pdf.cell(90,6,"SOLICITANTE",'LTBR',1,'C',1)
				
		
				pdf.cell(90,6,"Realizado por: ",'LTBR',0,'L',0)
				pdf.cell(90,6,"Recibido por: ",'LTBR',1,'L',1)
				
		
				pdf.cell(90,6,"Fecha: ",'LTBR',0,'L',0)
				pdf.cell(90,6,"Fecha: ",'LTBR',1,'L',1)
				
				pdf.cell(90,6,"Firma:",'LTBR',0,'L',0)
				pdf.cell(90,6,"Firma:",'LTBR',1,'L',1)
			
			# pdf.set_font('Arial','',8) # TAMANO DE LA FUENTE
				k = 0
			
			k = k+1
			j =j+1
			
		pdf.ln(5)
		pdf.set_font('Arial','B',12)
		pdf.cell(90,6,"REALIZADO POR",'LTBR',0,'C',0)
		pdf.cell(90,6,"SOLICITANTE",'LTBR',1,'C',1)
		

		pdf.cell(90,6,"Realizado por: ",'LTBR',0,'L',0)
		pdf.cell(90,6,"Recibido por: ",'LTBR',1,'L',1)
		

		pdf.cell(90,6,"Fecha: ",'LTBR',0,'L',0)
		pdf.cell(90,6,"Fecha: ",'LTBR',1,'L',1)
		
		pdf.cell(90,6,"Firma:",'LTBR',0,'L',0)
		pdf.cell(90,6,"Firma:",'LTBR',1,'L',1)
		
		tipo = acento(mate)
		nom = "Inventario de Materiales de "+tipo+" al "+fecha+'.pdf' #Nombre del archivo .pdf
		#
		#
		pdf.output('openerp/addons/materiales_almacen/reportes/'+nom)
		#pdf.output('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom,'F')
		
		archivo = open('openerp/addons/materiales_almacen/reportes/'+nom)
		#archivo = open('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom)
		
		#nom = nombre_r+" "+fecha+'.pdf' #Nombre del archivo .pdf
		#
		tipo_repor = "Inventario de "+tipo
		r_archivo = self.pool.get('reporte.inventario').create(cr, uid, {
		 	'name' : nom,
		 	'res_name' : nom,
		 	'datas' : base64.encodestring(archivo.read()),
		 	'datas_fname' : nom,
		 	'res_model' : 'wizard.resumen.inventario',
			'tipo_reporte': tipo_repor,
		},context=context)
		
		return r_archivo
				
	_columns = {
		'fecha': fields.date('Fecha de Creación', required=True, ),
		't_materiales' : fields.selection((('1','Limpieza'), ('2','Oficina'), ('3','Servicios Generales'), ('4','Tecnológico')),'Tipo de Material', required=True),
	
	}
def acento(cadena):
	result = cadena.encode('UTF-8').decode('UTF-8')# INSTITUCION
	return result
wizard_resumen_inventario()
	
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

