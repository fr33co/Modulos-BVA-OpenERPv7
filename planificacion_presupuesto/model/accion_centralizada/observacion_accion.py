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

	_name = "observacion.accion"
	
	_order = "codigo"
	
	"""
	Metodo que trae la informacion del proyecto en base al codigo seleccionado.
	"""
	def on_change_proyecto(self, cr, uid, ids, codigo, context=None):
	    values = {}
	    if not codigo:
		return values
	    datos = self.pool.get('accion.centralizada').browse(cr, uid, codigo, context=context)
	    fecha_a = datos.f_solicitud.split("/")
	    fec = fecha_a[2]
	    values.update({
		'accion_centra' : datos.n_accion_centra.a_centralizada,
		'a_fiscal' : fec,
		'monto_solicitado' : datos.total_metas,
		'siglas' : datos.siglas,	
	    })
	    return {'value' : values}
	
	"""
	Función para el cálculo de la cantidad de cada partida
	"""
	def suma_partidas(self, cr, uid, ids, partida01, partida02, partida03, partida04, partida05, partida07, partida10, partida11, partida12, context=None):
		
	    cantidad_partida = {}
	    
	    resultado = {}
	    
	    sumatotal = partida01+partida02+partida03+partida04+partida05+partida07+partida10+partida11+partida12
	    
	    cantidad_partida.update({'monto':sumatotal,})
	    
	    resultado = {'value':cantidad_partida}
	    
	    return resultado
	"""
	Metodo .
	"""
	def action_ajustar(self, cr, uid, ids, context=None):
	    obj = self.browse(cr, uid, ids, context=None)
	    pest_obser = self.pool.get('accion.centralizada')
	    observaciones_acc = self.browse(cr, uid, ids)[0]
	    for pro in obj:
		read_acc = pest_obser.read(cr, uid, pro.codigo.id, context=context)
		resultado = read_acc['c_solicitud']
		siglas = read_acc['siglas']
		monto  = observaciones_acc.monto
		revisado = observaciones_acc.revisado.name
		observaciones = observaciones_acc.observaciones
		fecha = observaciones_acc.fecha
		estado = '3'
		self.write(cr, uid, ids, {'estatus':'3'}, context=context)
		cr.execute("UPDATE accion_centralizada SET revisado=%s, fecha_revision=%s, monto_asignado=%s, estatus=%s, observaciones=%s WHERE c_solicitud=%s AND siglas=%s;", (revisado, fecha, monto, estado, observaciones, resultado, siglas))
	    return True
	
	def action_rechasado(self, cr, uid, ids, context=None):
	    obj = self.browse(cr, uid, ids, context=None)
	    pest_obser = self.pool.get('accion.centralizada')
	    observaciones_acc = self.browse(cr, uid, ids)[0]
	    for pro in obj:
		read_acc = pest_obser.read(cr, uid, pro.codigo.id, context=context)
		resultado = read_acc['c_solicitud']
		siglas = read_acc['siglas']
		monto  = observaciones_acc.monto
		revisado = observaciones_acc.revisado.name
		observaciones = observaciones_acc.observaciones
		fecha = observaciones_acc.fecha
		estado = '2'
		self.write(cr, uid, ids, {'estatus':'2'}, context=context)
		cr.execute("UPDATE accion_centralizada SET revisado=%s, fecha_revision=%s, monto_asignado=%s, estatus=%s, observaciones=%s WHERE c_solicitud=%s AND siglas=%s;", (revisado, fecha, monto, estado, observaciones, resultado, siglas))
	    return True
	
	def action_aprobado(self, cr, uid, ids, context=None):
	    obj = self.browse(cr, uid, ids, context=None)
	    pest_obser = self.pool.get('accion.centralizada')
	    observaciones_acc = self.browse(cr, uid, ids)[0]
	    for pro in obj:
		read_acc = pest_obser.read(cr, uid, pro.codigo.id, context=context)
		resultado = read_acc['c_solicitud']
		siglas = read_acc['siglas']
		monto  = observaciones_acc.monto
		revisado = observaciones_acc.revisado.name
		observaciones = observaciones_acc.observaciones
		fecha = observaciones_acc.fecha
		par01 = observaciones_acc.partida01
		par02 = observaciones_acc.partida02
		par03 = observaciones_acc.partida03
		par04 = observaciones_acc.partida04
		par05 = observaciones_acc.partida05
		par07 = observaciones_acc.partida07
		par10 = observaciones_acc.partida10
		par11 = observaciones_acc.partida11
		par12 = observaciones_acc.partida12
		estado = '4'
		self.write(cr, uid, ids, {'estatus':'4'}, context=context)
		cr.execute("UPDATE accion_centralizada SET revisado=%s, fecha_revision=%s, monto_asignado=%s, estatus=%s, partida01=%s, partida02=%s, partida03=%s, partida04=%s, partida05=%s, partida07=%s, partida10=%s, partida11=%s, partida12=%s, observaciones=%s WHERE c_solicitud=%s AND siglas=%s;",
			   (revisado, fecha, monto, estado, par01, par02, par03, par04, par05, par07, par10, par11,
			    par12, observaciones, resultado, siglas))
	    return True
	
	def observacion_ajutes(self, cr, uid, ids, context=None): # Generacion de inventario

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
		accion = x.accion_centra.encode("UTF-8").decode("UTF-8")
		revi = x.revisado.name.encode("UTF-8").decode("UTF-8")
		sigla = x.siglas.encode("UTF-8").decode("UTF-8")
		monto = float(x.monto)
		solicitado = float(x.monto_solicitado)
		
		observa = x.observaciones.encode("UTF-8").decode("UTF-8")
		a_fiscal = x.a_fiscal
		
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',10)
		pdf.cell(190,5,"INFORMACIÓN DE LA ACCIÓN CENTRALIZADA".decode("UTF-8"),'LTBR',1,'C',1)
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
		pdf.cell(35,5,"ID de la Acción:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(14,5,codigo,'LTBR',0,'C',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(34,5,"Fecha de Revisión:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',9)
		pdf.cell(32,5,fec,'LTBR',1,'C',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(190,5,"Nombre de la Acción:".decode("UTF-8"),'LTR',1,'L',1)
		pdf.set_font('Arial','',9)
		pdf.multi_cell(190,5,accion,'LBR','J',1)
		
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',10)
		pdf.cell(190,5,"OBSERVACIONES DE LA ACCIÓN CENTRALIZADA".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		
		pdf.set_fill_color(191,191,191)
		pdf.set_text_color(24,29,31)
		pdf.set_font('Arial','B',9)
		pdf.cell(190,5,"Observaciones Preliminares".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		pdf.set_font('Arial','',9)
		pdf.multi_cell(190,5,observa,'LTBR','J',1)

	    nom = codigo+"-"+sigla+"preliminar"+'.pdf'
	    #pdf.output('openerp/addons/planificacion_presupuesto/reportes/'+nom,'F')
	    pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')
	    #archivo = open('openerp/addons/planificacion_presupuesto/reportes/'+nom)
	    archivo = open('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom)
	    r_archivo = self.pool.get('reportes.generales').create(cr, uid, {
		'name' : nom,
		'res_name' : nom,
		'datas' : base64.encodestring(archivo.read()),
		'datas_fname' : nom,
		'res_model' : 'observacion.accion',
		'registro': 'Observacion Preliminar Acción',
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
		    accion = x.accion_centra.encode("UTF-8").decode("UTF-8")
		    revi = x.revisado.name.encode("UTF-8").decode("UTF-8")
		    sigla = x.siglas.encode("UTF-8").decode("UTF-8")
		    monto = float(x.monto)
		    solicitado = float(x.monto_solicitado)
		    
		    observa = x.observaciones.encode("UTF-8").decode("UTF-8")
		    a_fiscal = x.a_fiscal
		    
		    pdf.set_fill_color(199,15,15)
		    pdf.set_text_color(255,255,255)
		    pdf.set_font('Arial','B',10)
		    pdf.cell(190,5,"INFORMACIÓN DE LA ACCIÓN CENTRALIZADA".decode("UTF-8"),'LTBR',1,'C',1)
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
		    pdf.cell(35,5,"ID de la Acción:".decode("UTF-8"),'LTB',0,'L',1)
		    pdf.set_font('Arial','',9)
		    pdf.cell(14,5,codigo,'LTBR',0,'C',1)
		    pdf.set_font('Arial','B',9)
		    pdf.cell(34,5,"Fecha de Revisión:".decode("UTF-8"),'LTB',0,'L',1)
		    pdf.set_font('Arial','',9)
		    pdf.cell(32,5,fec,'LTBR',1,'C',1)
		    pdf.set_font('Arial','B',9)
		    pdf.cell(190,5,"Nombre de la Acción:".decode("UTF-8"),'LTR',1,'L',1)
		    pdf.set_font('Arial','',9)
		    pdf.multi_cell(190,5,accion,'LBR','J',1)
		    
		    pdf.set_font('Arial','B',9)
		    pdf.cell(50,5,"Año de la Acción Centralizada:".decode("UTF-8"),'LTB',0,'L',1)
		    pdf.set_font('Arial','',9)
		    pdf.cell(15,5,str(a_fiscal),'LTBR',0,'C',1)
		    pdf.set_font('Arial','B',9)
		    pdf.cell(73,5,"Monto Solicitado para la Acción Centralizada:".decode("UTF-8"),'LTBR',0,'L',1)
		    pdf.set_font('Arial','',9)
		    pdf.cell(52,5,str(solicitado)+" Bsf.",'LTBR',1,'R',1)
		    
		    pdf.set_fill_color(199,15,15)
		    pdf.set_text_color(255,255,255)
		    pdf.set_font('Arial','B',10)
		    pdf.cell(190,5,"OBSERVACIONES DE LA ACCIÓN CENTRALIZADA".decode("UTF-8"),'LTBR',1,'C',1)
		    pdf.set_fill_color(255,255,255)
		    pdf.set_text_color(24,29,31)
		    

		    pdf.set_font('Arial','B',9)
		    pdf.cell(73,5,"Monto Asignado para la Acción Centralizada:".decode("UTF-8"),'LTB',0,'L',1)
		    pdf.set_font('Arial','',9)
		    pdf.cell(117,5,str(monto)+" Bsf.",'TBR',1,'L',1)
		    
		    pdf.ln(5)
		    pdf.set_fill_color(191,191,191)
		    pdf.set_text_color(24,29,31)
		    pdf.set_font('Arial','B',9)
		    pdf.cell(190,5,"Observaciones".decode("UTF-8"),'LTBR',1,'C',1)
		    pdf.set_fill_color(255,255,255)
		    pdf.set_text_color(24,29,31)
		    pdf.set_font('Arial','',9)
		    pdf.multi_cell(190,5,observa,'LTBR','J',1)
		
		nom = codigo+"-"+sigla+"Final"+'.pdf'
		#pdf.output('openerp/addons/planificacion_presupuesto/reportes/'+nom,'F')
		pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')
		#archivo = open('openerp/addons/planificacion_presupuesto/reportes/'+nom)
		archivo = open('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom)
		r_archivo = self.pool.get('reportes.generales').create(cr, uid, {
		    'name' : nom,
		    'res_name' : nom,
		    'datas' : base64.encodestring(archivo.read()),
		    'datas_fname' : nom,
		    'res_model' : 'observacion.accion',
		    'registro': 'Observación Final Acción',
		},context=context)
		
		return r_archivo
	_columns = {
	    'ente':fields.many2one('organos.entes', 'Institución', required=True, select=0),
	    'codigo':fields.many2one('accion.centralizada', 'Código de la Acción', required=True),
	    'accion_centra' : fields.char(string="Acción Centralizada:", required=False),
	    'siglas': fields.char('Siglas:'),
	    #'accion_centra' : fields.many2one('tipo.accion.centralizada', 'Acción Centralizada', required=True),
	    'monto': fields.float(string="Monto Asignado", size=10, required=True),
	    'monto_solicitado': fields.float(string="Monto Solicitado", size=10, readonly=False, required=False),
	    'observaciones' : fields.text(string="Observaciones", required=True),
	    'revisado' : fields.many2one('res.users', 'Registrado por:', readonly=True),
	    'a_fiscal': fields.char(string="Año Fiscal:", required=False, readonly=False),
	    'fecha': fields.char(string="Fecha de Revisión", readonly=True),
	    'partida01': fields.float(string="4.01", size=10, required=False),
	    'partida02': fields.float(string="4.02", size=10, required=False),
	    'partida03': fields.float(string="4.03", size=10, required=False),
	    'partida04': fields.float(string="4.04", size=10, required=False),
	    'partida05': fields.float(string="4.05", size=10, required=False),
	    'partida07': fields.float(string="4.07", size=10, required=False),
	    'partida10': fields.float(string="4.10", size=10, required=False),
	    'partida11': fields.float(string="4.11", size=10, required=False),
	    'partida12': fields.float(string="4.12", size=10, required=False),
	    'estatus': fields.selection([('1','Revisando'), ('2','Rechazado'), ('3','Para Ajuste'), ('4','Aprobado')], string="Estatus"),
	}
	_defaults = {
		'fecha': lambda *a: time.strftime("%d/%m/%Y"),
		'revisado': lambda s, cr, uid, c: uid,
		'estatus': '1',
		}
