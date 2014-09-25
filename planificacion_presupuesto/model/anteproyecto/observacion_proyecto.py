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

class observacion_proyecto(osv.Model):

	_name = "observacion.proyecto"
	
	_order = "codigo"
	
	"""
	Metodo que trae la informacion del proyecto en base al codigo seleccionado.
	"""
	def on_change_proyecto(self, cr, uid, ids, codigo, context=None):
	    values    = {}
	    #codigop01 = ''
	    trim_1p01 = 0.00
	    trim_2p01 = 0.00
	    trim_3p01 = 0.00
	    trim_4p01 = 0.00
	    sumap01   = 0.00
	    
	    
	    trim_1p02 = 0.00
	    trim_2p02 = 0.00
	    trim_3p02 = 0.00
	    trim_4p02 = 0.00
	    sumap02   = 0.00
	    
	    trim_1p03 = 0.00
	    trim_2p03 = 0.00
	    trim_3p03 = 0.00
	    trim_4p03 = 0.00
	    sumap03   = 0.00
	    
	    trim_1p04 = 0.00
	    trim_2p04 = 0.00
	    trim_3p04 = 0.00
	    trim_4p04 = 0.00
	    sumap04   = 0.00
	    
	    trim_1p05 = 0.00
	    trim_2p05 = 0.00
	    trim_3p05 = 0.00
	    trim_4p05 = 0.00
	    sumap05   = 0.00
	    
	    trim_1p07 = 0.00
	    trim_2p07 = 0.00
	    trim_3p07 = 0.00
	    trim_4p07 = 0.00
	    sumap07   = 0.00
	    
	    trim_1p10 = 0.00
	    trim_2p10 = 0.00
	    trim_3p10 = 0.00
	    trim_4p10 = 0.00
	    sumap10   = 0.00
	    
	    trim_1p11 = 0.00
	    trim_2p11 = 0.00
	    trim_3p11 = 0.00
	    trim_4p11 = 0.00
	    sumap11   = 0.00
	    
	    trim_1p12 = 0.00
	    trim_2p12 = 0.00
	    trim_3p12 = 0.00
	    trim_4p12 = 0.00
	    sumap12   = 0.00
	    
	    trim_1p98 = 0.00
	    trim_2p98 = 0.00
	    trim_3p98 = 0.00
	    trim_4p98 = 0.00
	    sumap98   = 0.00
	    
	    suma_tot   = 0.00
	    if not codigo:
		return values
	    datos = self.pool.get('proyecto.conaplan').browse(cr, uid, codigo, context=context)
	    
	    slf_im_pre = self.pool.get('imputacion.presupuestaria')
	    	    
	    src_im_pre_coup1 = slf_im_pre.search_count(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.01')])
	    if src_im_pre_coup1 > 0:
		
		src_im_prep1     = slf_im_pre.search(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.01')], count=False)
		rd_im_prep1      = slf_im_pre.read(cr, uid, src_im_prep1,['trim_1','trim_2','trim_3','trim_4'],context=context)
		
		trim_1p01  = rd_im_prep1[0]['trim_1']
		trim_2p01  = rd_im_prep1[0]['trim_2']
		trim_3p01  = rd_im_prep1[0]['trim_3']
		trim_4p01  = rd_im_prep1[0]['trim_4']
	       
	    sumap01 = trim_1p01 + trim_2p01 + trim_3p01 + trim_4p01
	     
	    
	    src_im_pre_coup2 = slf_im_pre.search_count(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.02')])
	    if src_im_pre_coup2 > 0:
		src_im_prep2     = slf_im_pre.search(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.02')], count=False)
		rd_im_prep2      = slf_im_pre.read(cr, uid, src_im_prep2,['id','trim_1','trim_2','trim_3','trim_4'],context=context)
		
		trim_1p02  = rd_im_prep2[0]['trim_1']
		trim_2p02  = rd_im_prep2[0]['trim_2']
		trim_3p02  = rd_im_prep2[0]['trim_3']
		trim_4p02  = rd_im_prep2[0]['trim_4']
	       
	    sumap02 = trim_1p02 + trim_2p02 + trim_3p02 + trim_4p02
	    
	    src_im_pre_coup3 = slf_im_pre.search_count(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.03')])
	    if src_im_pre_coup3 > 0:
		src_im_prep3     = slf_im_pre.search(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.03')], count=False)
		rd_im_prep3      = slf_im_pre.read(cr, uid, src_im_prep3,['trim_1','trim_2','trim_3','trim_4'],context=context)
		
		trim_1p03  = rd_im_prep3[0]['trim_1']
		trim_2p03  = rd_im_prep3[0]['trim_2']
		trim_3p03  = rd_im_prep3[0]['trim_3']
		trim_4p03  = rd_im_prep3[0]['trim_4']
	       
	    sumap03 = trim_1p03 + trim_2p03 + trim_3p03 + trim_4p03
	    
	    src_im_pre_coup4 = slf_im_pre.search_count(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.04')])
	    if src_im_pre_coup4 > 0:
		src_im_prep4     = slf_im_pre.search(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.04')], count=False)
		rd_im_prep4      = slf_im_pre.read(cr, uid, src_im_prep4,['trim_1','trim_2','trim_3','trim_4'],context=context)
		
		trim_1p04  = rd_im_prep4[0]['trim_1']
		trim_2p04  = rd_im_prep4[0]['trim_2']
		trim_3p04  = rd_im_prep4[0]['trim_3']
		trim_4p04  = rd_im_prep4[0]['trim_4']
	       
	    sumap04 = trim_1p04 + trim_2p04 + trim_3p04 + trim_4p04
	    
	    src_im_pre_coup5 = slf_im_pre.search_count(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.05')])
	    if src_im_pre_coup5 > 0:
		src_im_prep5     = slf_im_pre.search(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.05')], count=False)
		rd_im_prep5      = slf_im_pre.read(cr, uid, src_im_prep5,['trim_1','trim_2','trim_3','trim_4'],context=context)
		
		trim_1p05  = rd_im_prep5[0]['trim_1']
		trim_2p05  = rd_im_prep5[0]['trim_2']
		trim_3p05  = rd_im_prep5[0]['trim_3']
		trim_4p05  = rd_im_prep5[0]['trim_4']
	       
	    sumap05 = trim_1p05 + trim_2p05 + trim_3p05 + trim_4p05
	    
	    src_im_pre_coup7 = slf_im_pre.search_count(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.07')])
	    if src_im_pre_coup7 > 0:
		src_im_prep7     = slf_im_pre.search(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.07')], count=False)
		rd_im_prep7      = slf_im_pre.read(cr, uid, src_im_prep7,['trim_1','trim_2','trim_3','trim_4'],context=context)
		
		trim_1p07  = rd_im_prep7[0]['trim_1']
		trim_2p07  = rd_im_prep7[0]['trim_2']
		trim_3p07  = rd_im_prep7[0]['trim_3']
		trim_4p07  = rd_im_prep7[0]['trim_4']
	       
	    sumap07 = trim_1p07 + trim_2p07 + trim_3p07 + trim_4p07
	    
	    src_im_pre_coup10 = slf_im_pre.search_count(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.10')])
	    if src_im_pre_coup10 > 0:
		src_im_prep10     = slf_im_pre.search(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.10')], count=False)
		rd_im_prep10      = slf_im_pre.read(cr, uid, src_im_prep10,['trim_1','trim_2','trim_3','trim_4'],context=context)
		
		trim_1p10  = rd_im_prep10[0]['trim_1']
		trim_2p10  = rd_im_prep10[0]['trim_2']
		trim_3p10  = rd_im_prep10[0]['trim_3']
		trim_4p10  = rd_im_prep10[0]['trim_4']
	       
	    sumap10 = trim_1p10 + trim_2p10 + trim_3p10 + trim_4p10
	    
	    src_im_pre_coup11 = slf_im_pre.search_count(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.11')])
	    if src_im_pre_coup10 > 0:
		src_im_prep11     = slf_im_pre.search(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.11')], count=False)
		rd_im_prep11      = slf_im_pre.read(cr, uid, src_im_prep11,['trim_1','trim_2','trim_3','trim_4'],context=context)
		
		trim_1p11  = rd_im_prep11[0]['trim_1']
		trim_2p11  = rd_im_prep11[0]['trim_2']
		trim_3p11  = rd_im_prep11[0]['trim_3']
		trim_4p11  = rd_im_prep11[0]['trim_4']
	       
	    sumap11 = trim_1p11 + trim_2p11 + trim_3p11 + trim_4p11
	    
	    src_im_pre_coup12 = slf_im_pre.search_count(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.12')])
	    if src_im_pre_coup12 > 0:
		src_im_prep12     = slf_im_pre.search(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.12')], count=False)
		rd_im_prep12      = slf_im_pre.read(cr, uid, src_im_prep12,['trim_1','trim_2','trim_3','trim_4'],context=context)
		
		trim_1p12  = rd_im_prep12[0]['trim_1']
		trim_2p12  = rd_im_prep12[0]['trim_2']
		trim_3p12  = rd_im_prep12[0]['trim_3']
		trim_4p12  = rd_im_prep12[0]['trim_4']
	       
	    sumap12 = trim_1p12 + trim_2p12 + trim_3p12 + trim_4p12
	    
	    src_im_pre_coup98 = slf_im_pre.search_count(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.98')])
	    if src_im_pre_coup98 > 0:
		src_im_prep98     = slf_im_pre.search(cr, uid, [('imputacion_ids','=',codigo),('codigo','=','4.98')], count=False)
		rd_im_prep98      = slf_im_pre.read(cr, uid, src_im_prep98,['trim_1','trim_2','trim_3','trim_4'],context=context)
		
		trim_1p98  = rd_im_prep98[0]['trim_1']
		trim_2p98  = rd_im_prep98[0]['trim_2']
		trim_3p98  = rd_im_prep98[0]['trim_3']
		trim_4p98  = rd_im_prep98[0]['trim_4']
	       
	    sumap98 = trim_1p98 + trim_2p98 + trim_3p98 + trim_4p98
	    
	    suma_tot = sumap01+ sumap02+ sumap03+ sumap04+ sumap05+ sumap07+ sumap10+ sumap11+ sumap12+ sumap98
	    
	    
	    values.update({
		'nombre_pro' : datos.nombre_pro,
		'a_fiscal' : datos.year_fiscal,
		'monto_solicitado' : suma_tot,
		'siglas' : datos.siglas,
		'partida01s' : sumap01,
		'partida02s' : sumap02,
		'partida03s' : sumap03,
		'partida04s' : sumap04,
		'partida05s' : sumap05,
		'partida07s' : sumap07,
		'partida10s' : sumap10,
		'partida11s' : sumap11,
		'partida12s' : sumap12,
		'partida98s' : sumap98,
	    })
	    return {'value' : values}
	
	"""
	Función para el cálculo de la cantidad de cada partida
	"""
	def suma_partidas(self, cr, uid, ids, partida01, partida02, partida03, partida04, partida05, partida07, partida10, partida11, partida12, partida98, context=None):
		
	    cantidad_partida = {}
	    
	    resultado = {}
	    
	    sumatotal = partida01+partida02+partida03+partida04+partida05+partida07+partida10+partida11+partida12+partida98
	    
	    cantidad_partida.update({'monto':sumatotal,})
	    
	    resultado = {'value':cantidad_partida}
	    
	    return resultado
	
    
	def monto_asignado(self, cr, uid, ids, situado, gestion, fondo, transferencias, part,context=None):
		
	    cantidad_partida = {}
	    
	    resultado = {}
	    
	    monto_asignado= situado+gestion+fondo+transferencias
	    
	    if part == '1':
		cantidad_partida.update({'total_partidas01':monto_asignado,})
	    
	    if part == '2':
		cantidad_partida.update({'total_partidas02':monto_asignado,})
		
	    if part == '3':
		cantidad_partida.update({'total_partidas03':monto_asignado,})
	    if part == '4':
		cantidad_partida.update({'total_partidas04':monto_asignado,})
	    if part == '5':
		cantidad_partida.update({'total_partidas05':monto_asignado,})
	    if part == '7':
		cantidad_partida.update({'total_partidas07':monto_asignado,})
	    if part == '10':
		cantidad_partida.update({'total_partidas10':monto_asignado,})
	    if part == '11':
		cantidad_partida.update({'total_partidas11':monto_asignado,})
	    if part == '12':
		cantidad_partida.update({'total_partidas12':monto_asignado,})
	    if part == '98':
		cantidad_partida.update({'total_partidas98':monto_asignado,})
	    
	    resultado = {'value':cantidad_partida}
	    
	    return resultado
    
    
	"""
	Metodo que cambia el estado de del proyecto de revison --> Para ajuste, donde se envia a la pestaña
	observaciones del modelo proyecto.conaplan las primeras observaciones del proyecto.
	"""
	def action_ajustar(self, cr, uid, ids, context=None):
		obj = self.browse(cr, uid, ids, context=None)
		pest_obser = self.pool.get('proyecto.conaplan')
		observaciones_pro = self.browse(cr, uid, ids)[0]
		for pro in obj:
		    read_pro = pest_obser.read(cr, uid, pro.codigo.id, context=context) #Read al modelo proyecto.conaplan
		    resultado = read_pro['c_solicitud'] #Leemos el codigo del proyecto
		    siglas = read_pro['siglas'] #Leemos las siglas del ente del proyecto
		    
		    #monto  = observaciones_pro.monto
		    revisado = observaciones_pro.revisado.name #Persona que realizo la revision/obervaciones
		    print revisado 
		    observaciones = observaciones_pro.observaciones #Obervaciones Preliminares
		    fecha = observaciones_pro.fecha #Fecha de revision
		    #fuente_fin = observaciones_pro.fuente_fin 
		    estado = '3'
		    self.write(cr, uid, ids, {'estatus':'3'}, context=context)
		    cr.execute("UPDATE proyecto_conaplan SET revisado=%s, fecha_revision=%s, estatus=%s, observaciones=%s WHERE c_solicitud=%s AND siglas=%s;", (revisado, fecha, estado, observaciones, resultado, siglas))

		return True
	
	"""
	Metodo que cambia el estado de del proyecto de Para Ajuste --> Rechazado, donde se envia a la pestaña
	observaciones del modelo proyecto.conaplan notificandole que su proyecto luego de los ajustes aun no
	cumple con lo requerido y por ende es Rechazado.
	"""
	def action_rechasado(self, cr, uid, ids, context=None):
		obj = self.browse(cr, uid, ids, context=None)
		pest_obser = self.pool.get('proyecto.conaplan')
		observaciones_pro = self.browse(cr, uid, ids)[0]
		for pro in obj:
		    read_pro = pest_obser.read(cr, uid, pro.codigo.id, context=context)
		    resultado = read_pro['c_solicitud']
		    siglas = read_pro['siglas']
		    #monto  = observaciones_pro.monto
		    revisado = observaciones_pro.revisado.name
		    observaciones = observaciones_pro.observaciones
		    fecha = observaciones_pro.fecha
		    #fuente_fin = observaciones_pro.fuente_fin
		    estado = '2'
		    self.write(cr, uid, ids, {'estatus':'2'}, context=context)
		    cr.execute("UPDATE proyecto_conaplan SET revisado=%s, fecha_revision=%s, estatus=%s, observaciones=%s WHERE c_solicitud=%s AND siglas=%s;", (revisado, fecha, estado, observaciones, resultado, siglas))
		
		return True
	
	"""
	Metodo que cambia el estado de del proyecto de Para Ajuste --> Aprobado, donde se envia a la pestaña
	observaciones del modelo proyecto.conaplan las ultimas obseraciones si tiene junto a su Monto final
	asignado junto que el monto total que utilizaran por partida.
	"""
	def action_aprobado(self, cr, uid, ids, context=None):
		obj = self.browse(cr, uid, ids, context=None)
		pest_obser = self.pool.get('proyecto.conaplan')
		observaciones_pro = self.browse(cr, uid, ids)[0]
		for pro in obj:
			read_pro = pest_obser.read(cr, uid, pro.codigo.id, context=context)
			resultado = read_pro['c_solicitud']
			siglas = read_pro['siglas']
			monto  = observaciones_pro.monto
			revisado = observaciones_pro.revisado.name
			observaciones = observaciones_pro.observaciones
			fecha = observaciones_pro.fecha
			fuente_fin = observaciones_pro.fuente_fin
			par01 = observaciones_pro.partida01
			par02 = observaciones_pro.partida02
			par03 = observaciones_pro.partida03
			par04 = observaciones_pro.partida04
			par05 = observaciones_pro.partida05
			par07 = observaciones_pro.partida07
			par10 = observaciones_pro.partida10
			par11 = observaciones_pro.partida11
			par12 = observaciones_pro.partida12
			par98 = observaciones_pro.partida98
			estructura = observaciones_pro.estruc_presu
			estado = '4'
			self.write(cr, uid, ids, {'estatus':'4'}, context=context)
			cr.execute("UPDATE proyecto_conaplan SET estatus=%s, fuente_fin=%s, partida01=%s, partida02=%s, partida03=%s, partida04=%s, partida05=%s, partida07=%s, partida10=%s, partida11=%s, partida12=%s, partida98=%s, monto_asignado=%s, estruc_presu=%s, observaciones=%s  WHERE c_solicitud=%s AND siglas=%s;",
				   (estado, fuente_fin, par01, par02, par03, par04, par05, par07, par10, par11,
				    par12, par98, monto, estructura,  observaciones, resultado, siglas))
		
		return True
	
	def action_asignar(self, cr, uid, ids, context=None):
	    
	    slf_im_pre = self.pool.get('imputacion.presupuestaria')	
	    for codigo in self.read(cr, uid, ids, [
						    'codigo',
						    'total_partidas01',
						    'total_partidas02',
						    'total_partidas03',
						    'total_partidas04',
						    'total_partidas05',
						    'total_partidas07',
						    'total_partidas10',
						    'total_partidas11',
						    'total_partidas12',
						    'total_partidas98',
						  ], context=context):
		
		codigo_i = codigo['codigo'][0]
		del codigo['codigo']
		del codigo['id']
		k =  codigo.keys()
		
		for m in k:
	    
		    cadena = re.sub("\D", "", m)
              	    partida = '4.'+str(cadena)

		    tot     = codigo[m]
		    ####print 'PARTIDA:'+str(partida)+'=> MONTO:'+str(tot)

		    sql_im = "SELECT COUNT(id) FROM imputacion_presupuestaria WHERE imputacion_ids="+str(codigo_i)+" AND codigo='"+str(partida)+"'"
		    cr.execute(sql_im)
		    for tot_par_arr in cr.fetchall():

			if tot_par_arr[0] > 0:
			    sql = "UPDATE imputacion_presupuestaria SET monto_asignado="+str(tot)+" WHERE imputacion_ids="+str(codigo_i)+" AND codigo='"+str(partida)+"'"
			    cr.execute(sql)
		        elif tot_par_arr[0] == 0 and tot > 0:
			    sql_im = "SELECT id FROM partida_presupuestaria WHERE codigo='"+str(partida)+"'"
			    cr.execute(sql_im)
			    for arr_par_new in cr.fetchall():
				slf_im_pre.create(cr, uid, {
				    'imputacion_ids' : codigo_i,
				    'codigo' : partida,
				    'partida_presu' : arr_par_new[0],
				    'monto_asignado' : tot,
				},context=context)
	     
	    return True
	    
	def observacion_ajutes(self, cr, uid, ids, context=None): # Generacion de inventario

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
	    #pdf.set_margins(8,10,10) # MARGENES DEL DOCUMENTO
	    #pdf.ln(20) # Saldo de linea
	    # 10 y 50 eje x y y 200 dimencion
	    #pdf.line(10, 40, 200, 40) Linea
	    
	    
	    observaciones = self.browse(cr, uid, ids, context=context)
	    
	    fuente_f = ""
	    for x in observaciones:
		ente = x.ente.nombre_ente.encode("UTF-8").decode("UTF-8")
		fec = x.fecha
		codigo = x.codigo.c_solicitud.encode("UTF-8").decode("UTF-8")
		proyecto = x.nombre_pro.encode("UTF-8").decode("UTF-8")
		revi = x.revisado.name.encode("UTF-8").decode("UTF-8")
		monto = float(x.monto)
		solicitado = float(x.monto_solicitado)
		#sigla = x.siglas.encode("UTF-8").decode("UTF-8")
		
		observa = x.observaciones.encode("UTF-8").decode("UTF-8")
		a_fiscal = x.a_fiscal

		if int(x.fuente_fin) == 1:
			fuente_f = "SITUADO CONSTITUCIONAL"
		elif int(x.fuente_fin) == 2:
		    fuente_f = "F.C.I"
		elif int(x.fuente_fin) == 3:
		    fuente_f = "INGRESOS PROPÍOS"
		elif int(x.fuente_fin) == 4:
		    fuente_f = "TRANSFERENCIAS CORRIENTES INTERNAS DE LA REPÚBLICA"
		
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',10)
		pdf.cell(190,5,"INFORMACIÓN DEL PROYECTO".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		
		pdf.set_font('Arial','B',9)
		pdf.cell(20,5,"Institución:".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(170,5,ente,'LTBR',1,'L',1)
		
		pdf.set_font('Arial','B',9)
		pdf.cell(25,5,"Revisado por:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(50,5,revi,'LTBR',0,'L',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(35,5,"Código del Proyecto:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(14,5,codigo,'LTBR',0,'C',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(34,5,"Fecha de Revisión:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(32,5,fec,'LTBR',1,'C',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(190,5,"Nombre del Proyecto:".decode("UTF-8"),'LTR',1,'L',1)
		pdf.set_font('Arial','',9)
		pdf.multi_cell(190,5,proyecto,'LBR','J',1)
		
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',10)
		pdf.cell(190,5,"OBSERVACIONES DEL PROYECTO".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		
		pdf.set_fill_color(191,191,191)
		pdf.set_text_color(24,29,31)
		pdf.set_font('Arial','B',9)
		pdf.cell(190,5,"Observaciones".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		pdf.set_font('Arial','',9)
		pdf.multi_cell(190,5,observa,'LTBR','J',1)
	    
	    nom = proyecto+"preliminar"+'.pdf'
	    pdf.output('openerp/addons/planificacion_presupuesto/reportes/'+nom,'F')
	    #pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')
	    archivo = open('openerp/addons/planificacion_presupuesto/reportes/'+nom)
	    #archivo = open('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom)
	    r_archivo = self.pool.get('reportes.generales').create(cr, uid, {
		'name' : nom,
		'res_name' : nom,
		'datas' : base64.encodestring(archivo.read()),
		'datas_fname' : nom,
		'res_model' : 'observacion.proyecto',
		'registro': 'Observaciones Preliminalres - Proyecto',
	    },context=context)
	    
	    return r_archivo
	def observaciones_finales(self, cr, uid, ids, context=None): # Generacion de inventario

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
	    #pdf.set_margins(8,10,10) # MARGENES DEL DOCUMENTO
	    #pdf.ln(20) # Saldo de linea
	    # 10 y 50 eje x y y 200 dimencion
	    #pdf.line(10, 40, 200, 40) Linea
	    
	    
	    observaciones = self.browse(cr, uid, ids, context=context)
	    
	    fuente_f = ""
	    for x in observaciones:
		ente = x.ente.nombre_ente.encode("UTF-8").decode("UTF-8")
		fec = x.fecha
		codigo = x.codigo.c_solicitud.encode("UTF-8").decode("UTF-8")
		proyecto = x.nombre_pro.encode("UTF-8").decode("UTF-8")
		revi = x.revisado.name.encode("UTF-8").decode("UTF-8")
		monto = float(x.monto)
		partida01 = float(x.partida01)
		partida02 = float(x.partida02)
		partida03 = float(x.partida03)
		partida04 = float(x.partida04)
		partida05 = float(x.partida05)
		partida07 = float(x.partida07)
		partida10 = float(x.partida10)
		partida11 = float(x.partida11)
		partida12 = float(x.partida12)
		partida98 = float(x.partida98)
		estructura = x.estruc_presu
		solicitado = float(x.monto_solicitado)
		#sigla = x.siglas.encode("UTF-8").decode("UTF-8")
		
		observa = x.observaciones.encode("UTF-8").decode("UTF-8")
		a_fiscal = x.a_fiscal

		if int(x.fuente_fin) == 1:
			fuente_f = "SITUADO CONSTITUCIONAL"
		elif int(x.fuente_fin) == 2:
			fuente_f = "F.C.I"
		elif int(x.fuente_fin) == 3:
			fuente_f = "INGRESOS PROPÍOS"
		elif int(x.fuente_fin) == 4:
			fuente_f = "TRANSFERENCIAS CORRIENTES INTERNAS DE LA REPÚBLICA"
		
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',10)
		pdf.cell(190,5,"INFORMACIÓN DEL PROYECTO".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		
		pdf.set_font('Arial','B',9)
		pdf.cell(20,5,"Institución:".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(170,5,ente,'LTBR',1,'L',1)
		
		pdf.set_font('Arial','B',9)
		pdf.cell(25,5,"Revisado por:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(50,5,revi,'LTBR',0,'L',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(35,5,"Código del Proyecto:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(14,5,codigo,'LTBR',0,'C',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(34,5,"Fecha de Revisión:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(32,5,fec,'LTBR',1,'C',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(190,5,"Nombre del Proyecto:".decode("UTF-8"),'LTR',1,'L',1)
		pdf.set_font('Arial','',9)
		pdf.multi_cell(190,5,proyecto,'LBR','J',1)
		
		pdf.set_font('Arial','B',9)
		pdf.cell(30,5,"Año del Proyecto:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(15,5,str(a_fiscal),'LTBR',0,'C',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(75,5,"Monto Solicitado para el Proyecto Propuesto:".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(70,5,str(solicitado)+" Bsf.",'LTBR',1,'R',1)
		
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',10)
		pdf.cell(190,5,"OBSERVACIONES DEL PROYECTO".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		
		pdf.set_font('Arial','B',9)
		pdf.cell(43,5,"Fuente de Financiamiento:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(147,5,str(fuente_f).decode("UTF-8"),'TBR',1,'L',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(45,5,"Estructura Presupuestaria:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(145,5,str(estructura),'LTBR',1,'L',1)
		
		pdf.ln(5)
		pdf.set_draw_color(255,255,255) #Color de las Lineas
		pdf.set_fill_color(11,13,56) #Color de las Celdas
		pdf.set_text_color(255,255,255) #Color del Texto
		pdf.set_font('Arial','B',8)
		pdf.cell(20,5,"Código".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(60,5,"Nombre de la Partida presupuestaria".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(30,5,"Monto Asignado".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		pdf.cell(20,5,"4.01".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(60,5,"Gastos de Personal".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,str(partida01),'LTBR',1,'R',1)
		pdf.cell(20,5,"4.02".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(60,5,"Materiales, Suministros y Mercancías".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,str(partida02),'LTBR',1,'R',1)
		pdf.cell(20,5,"4.03".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(60,5,"Servicios no personales".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,str(partida03),'LTBR',1,'R',1)
		pdf.cell(20,5,"4.04".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(60,5,"Activos Reales".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,str(partida04),'LTBR',1,'R',1)
		pdf.cell(20,5,"4.05".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(60,5,"Activos Financieros".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,str(partida05),'LTBR',1,'R',1)
		pdf.cell(20,5,"4.07".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(60,5,"Transferencias y Donaciones".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,str(partida07),'LTBR',1,'R',1)
		pdf.cell(20,5,"4.10".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(60,5,"Servicio de la Deuda Pública".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,str(partida10),'LTBR',1,'R',1)
		pdf.cell(20,5,"4.11".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(60,5,"Disminución de Pasivos".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,str(partida11),'LTBR',1,'R',1)
		pdf.cell(20,5,"4.12".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(60,5,"Disminución de Patrimonio".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,str(partida12),'LTBR',1,'R',1)
		pdf.cell(20,5,"4.98".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(60,5,"Rectificaciones al Presupuesto".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,str(partida98),'LTBR',1,'R',1)
		pdf.set_fill_color(191,191,191) #Color de las Celdas
		pdf.set_text_color(0,0,0) #Color del Texto
		pdf.cell(80,5,"Monto Total Asignado al Proyecto:".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(30,5,str(monto),'LTBR',1,'R',1)

		
		pdf.ln(5)
		pdf.set_draw_color(0,0,0) #Color de las Lineas
		pdf.set_fill_color(191,191,191)
		pdf.set_text_color(24,29,31)
		pdf.set_font('Arial','B',9)
		pdf.cell(190,5,"Observaciones".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		pdf.set_font('Arial','',9)
		pdf.multi_cell(190,5,observa,'LTBR','J',1)
	    
	    nom = proyecto+"-Obseraciones finales"+'.pdf'
	    
	    #pdf.output('openerp/addons/planificacion_presupuesto/reportes/'+nom,'F')
	    #pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')
	    #archivo = open('openerp/addons/planificacion_presupuesto/reportes/'+nom)
	    #archivo = open('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom)
	    
	    
	    #rutausuario =  os.getcwd()
	    #rutax       = os.path.split(rutausuario+'planificacion_presupuesto')
	    #rutadir     = rutax[0]
	    
	    ruta_fun = ruta('')
	    
	    pdf.output(ruta_fun+'/reportes/'+nom,'F')
	    #pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')
	    archivo = open(ruta_fun+'/reportes/'+nom)


	    
	    r_archivo = self.pool.get('reportes.generales').create(cr, uid, {
		'name' : nom,
		'res_name' : nom,
		'datas' : base64.encodestring(archivo.read()),
		'datas_fname' : nom,
		'res_model' : 'observacion.proyecto',
		'registro': 'Observaciones Finales - Proyecto',
	    },context=context)
	    
	    return r_archivo
	
	_columns = {
		'ente':fields.many2one('organos.entes', 'Institución', required=True, select=0),
		'codigo':fields.many2one('proyecto.conaplan', 'Código del Proyecto', required=True),
		'nombre_pro' : fields.char(string='Nombre del Proyecto', readonly=False),
		'monto': fields.float(string="Monto Asignado", required=True),
		'monto_solicitado': fields.float(string="Monto Solicitado", readonly=False, required=False),
		'observaciones' : fields.text(string="Observaciones", required=True),
		'revisado' : fields.many2one('res.users', 'Registrado por:', readonly=True),
		'a_fiscal': fields.char(string="Año Fiscal:", required=False, readonly=False),
		'fecha': fields.char(string="Fecha de Revisión", readonly=True),
		#'partida01': fields.float(string="4.01", size=10, required=False),
		#'partida02': fields.float(string="4.02", size=10, required=False),
		#'partida03': fields.float(string="4.03", size=10, required=False),
		#'partida04': fields.float(string="4.04", size=10, required=False),
		#'partida05': fields.float(string="4.05", size=10, required=False),
		#'partida07': fields.float(string="4.07", size=10, required=False),
		#'partida10': fields.float(string="4.10", size=10, required=False),
		#'partida11': fields.float(string="4.11", size=10, required=False),
		#'partida12': fields.float(string="4.12", size=10, required=False),
		'partida01s': fields.float(string="", required=False),
		'partida02s': fields.float(string="", required=False),
		'partida03s': fields.float(string="", required=False),
		'partida04s': fields.float(string="", required=False),
		'partida05s': fields.float(string="", required=False),
		'partida07s': fields.float(string="", required=False),
		'partida10s': fields.float(string="", required=False),
		'partida11s': fields.float(string="", required=False),
		'partida12s': fields.float(string="", required=False),
		'partida98s': fields.float(string="", required=False),
		'situado01': fields.float(string="", required=False),
		'gestion01': fields.float(string="", required=False),
		'fondo01': fields.float(string="", required=False),
		'transferencias01': fields.float(string="", required=False),
		'total_partidas01': fields.float(string="", required=False),
		'situado02': fields.float(string="", required=False),
		'gestion02': fields.float(string="", required=False),
		'fondo02': fields.float(string="", required=False),
		'transferencias02': fields.float(string="", required=False),
		'total_partidas02': fields.float(string="", required=False),
		'situado03': fields.float(string="", required=False),
		'gestion03': fields.float(string="", required=False),
		'fondo03': fields.float(string="", required=False),
		'transferencias03': fields.float(string="", required=False),
		'total_partidas03': fields.float(string="", required=False),
		'situado04': fields.float(string="", required=False),
		'gestion04': fields.float(string="", required=False),
		'fondo04': fields.float(string="", required=False),
		'transferencias04': fields.float(string="", required=False),
		'total_partidas04': fields.float(string="", required=False),
		'situado05': fields.float(string="", required=False),
		'gestion05': fields.float(string="", required=False),
		'fondo05': fields.float(string="", required=False),
		'transferencias05': fields.float(string="", required=False),
		'total_partidas05': fields.float(string="", required=False),
		'situado07': fields.float(string="", required=False),
		'gestion07': fields.float(string="", required=False),
		'fondo07': fields.float(string="", required=False),
		'transferencias07': fields.float(string="", required=False),
		'total_partidas07': fields.float(string="", required=False),
		'situado10': fields.float(string="", required=False),
		'gestion10': fields.float(string="", required=False),
		'fondo10': fields.float(string="", required=False),
		'transferencias10': fields.float(string="", required=False),
		'total_partidas10': fields.float(string="", required=False),
		'situado11': fields.float(string="", required=False),
		'gestion11': fields.float(string="", required=False),
		'fondo11': fields.float(string="", required=False),
		'transferencias11': fields.float(string="", required=False),
		'total_partidas11': fields.float(string="", required=False),
		'situado12': fields.float(string="", required=False),
		'gestion12': fields.float(string="", required=False),
		'fondo12': fields.float(string="", required=False),
		'transferencias12': fields.float(string="", required=False),
		'total_partidas12': fields.float(string="", required=False),
		'situado98': fields.float(string="", required=False),
		'gestion98': fields.float(string="", required=False),
		'fondo98': fields.float(string="", required=False),
		'transferencias98': fields.float(string="", required=False),
		'total_partidas98': fields.float(string="", required=False),
		'estruc_presu': fields.char('Estructura Presupuestaria:'),
		#'fuente_fin': fields.selection([('1','SITUADO CONSTITUCIONAL'), ('2','F.C.I'), ('3','INGRESOS PROPÍOS'), ('4','TRANSFERENCIAS CORRIENTES INTERNAS DE LA REPÚBLICAS')], string="Fuente de Financiamiento:", required=False),
		#'fuente_fin2': fields.selection([('1','SITUADO CONSTITUCIONAL'), ('2','F.C.I'), ('3','INGRESOS PROPÍOS'), ('4','TRANSFERENCIAS CORRIENTES INTERNAS DE LA REPÚBLICAS')], string="Fuente de Financiamiento:", required=True),
		'estatus': fields.selection([('1','Revisando'), ('2','Rechazado'), ('3','Para Ajuste'), ('4','Aprobado')], string="Estatus"),
	}
	_defaults = {
		'fecha': lambda *a: time.strftime("%d/%m/%Y"),
		'revisado': lambda s, cr, uid, c: uid,
		'estatus': '1',
		#'fuente_fin': '4',
		}

def ruta( usuario ):
    ruta = '/home'
    if usuario == 'administrador':
        ruta = '/home/administrador/openerp70/modules/planificacion_presupuesto'

    return ruta