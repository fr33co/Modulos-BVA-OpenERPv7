# -*- coding: utf-8 -*-

import urllib2, urllib
import time
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

from openerp import netsvc
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

from openerp.tools.safe_eval import safe_eval as eval
#####################################################
#from fpdf import FPDF # Importar la libreria pdf
#import fpdf # Importar la libreria pdf
####################################################
from openerp.osv import fields, osv
import base64 #Necesario para la generación del .txt
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring #Necesario para la generación del .xsl
import xlwt
import netsvc
import tools
import logging
from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from xlwt import Borders
import os
import commands
import math
import fpdf_class # Se importa la Clase constructora del Documento PDF

from openerp.osv import osv, fields

class Hr_filtro(osv.osv_memory):
    _name="hr.filtro"
    
    
    def emitir_bono(self,cr,uid,ids,context=None):
			
			data = self.read(cr, uid, ids, context=context)[0] # Lectura del objeto propio
			
			if not data['cedula_bono']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar la Cedula, intente de nuevo..."))
			else:
				#~ print "BONO VACACIONAL"
				
				# SE CAPTURA LA CEDULA PARA LA GENERACION DE BONO VACACIONAL
				for x in self.browse(cr, uid, ids, context=None):
					id_model = x.cedula_bono
					#~ print "CEDULA DE BONO: "+str(id_model)
					
				##############################################################################################
				       #~ CONSULTA PARA LA BUSQUEDA DE BONO VACACIONAL CON SU RESPECTIVO MONTO
				##############################################################################################
				
				cr.execute('SELECT hr.cedula ced,hr.name_related nom,mov.asignacion bono FROM hr_employee hr INNER JOIN hr_movement_payslip mov ON hr.cedula = mov.cedula WHERE hr.cedula LIKE \'%'+str(id_model)+'%\' AND mov.cod = '"'"+str(126)+"'"' ORDER BY hr.cedula,hr.name_related DESC')
				
				for bono in cr.fetchall():
					print "CEDULA: "+str(bono[0])
					print "NOMBRE: "+str(bono[1])
					print "BONO: "+str(bono[2])
					
					cedula  = bono[0] # CEDULA
					nombre  = bono[1] # NOMBRE
					bono    = bono[2] # BONO
				
				##############################################################################################
				     #~ METODO PARA LA GENERACION DE REPORTE BONO VACACIONAL Y POST VACACIONAL
				##############################################################################################
				# Instancia de la clase heredada L es horizontal y P es vertical

				pdf=fpdf_class.Bono(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA

				#pdf.set_title(title)
				pdf.set_author('Marcel Arcuri')
				pdf.alias_nb_pages() # LLAMADA DE PAGINACION
				pdf.add_page() # AÑADE UNA NUEVA PAGINACION
				#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
				pdf.set_font('Arial','B',15)
				pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
				pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
				pdf.set_margins(25,10,15) # MARGENE DEL DOCUMENTO
				#pdf.ln(20) # Saldo de linea
				# 10 y 50 eje x y y 200 dimencion
				#pdf.line(10, 40, 200, 40) Linea 
				pdf.line(20, 47, 200, 47)  #Doble linea debado del acta
				pdf.line(20, 47.5, 200, 47.5) 

				pdf.line(160, 93, 200, 93)  #Doble linea debado del primer monto
				pdf.line(160, 93.5, 200, 93.5) 

				pdf.line(40, 220, 180, 220)  #Doble linea Firma
				pdf.line(40, 220.5, 180, 220.5) 

				pdf.set_fill_color(255,255,255)
				pdf.set_font('Arial','B',10)
				pdf.cell(140,5,"".decode("UTF-8"),'',0,'L',1)
				pdf.cell(50,5,"UNIDAD DE RECURSOS HUMANOS".decode("UTF-8"),'',1,'R',1)
				pdf.ln(5)
				pdf.set_font('Arial','B',16)
				pdf.cell(180,5,"ACTA DE VACACIONES".decode("UTF-8"),'',1,'C',1)
				texto_a = "Yo, "+str(nombre.upper())+", titular de la Cédula de Identidad Nro. "+str(cedula)+", declaro que he recibido de A.C. Bibliotecas Virtuales de Aragua, por concepto de vacaciones correspondiestes al periodo 2012 - 2013 la suma en bolívares de CINCO MIL CIEN 36/100 CTS (BS. 5.100,36) que se compone así:"

				texto_b = "El trabajador ante mencionado disfrutara de 15 días habiles desde el 16/09/2013 hasta 04/10/2013 con retorno el día 07/10/2013; contemplado en el Articulo 190 de la Ley Orgánica del trabajo, los Trabajadores y Trabajadoras."
				pdf.ln(5)

				pdf.set_font('Arial','',14)
				pdf.multi_cell(165,5,str(texto_a).decode("UTF-8"),'','J',1)
				pdf.ln(7)
				pdf.set_font('Arial','B',14)
				pdf.cell(99,5,"Articulo 192: Bono Vacacional de 45 días".decode("UTF-8"),'',0,'L',1)
				pdf.cell(66,5,"5.100,36".decode("UTF-8"),'',1,'R',1)
				pdf.ln(15)
				pdf.cell(99,5,"Total Recibo en este Acto".decode("UTF-8"),'',0,'R',1)
				pdf.cell(66,5,"5.100,36".decode("UTF-8"),'',1,'R',1)
				pdf.ln(5)

				pdf.set_font('Arial','',14)
				pdf.multi_cell(165,5,str(texto_b).decode("UTF-8"),'','J',1)
				pdf.ln(5)
				pdf.cell(165,5,"En Maracay Edo. Aragua, al 16 día del mes de Septiembre de 2013".decode("UTF-8"),'',1,'L',1)
				pdf.ln(5)
				pdf.cell(66,5,"Recibí Conforme:".decode("UTF-8"),'',1,'L',1)
				pdf.ln(75)
				pdf.set_font('Arial','B',14)
				pdf.cell(165,5,str(nombre.upper()),'',1,'C',1)
				pdf.cell(165,5,str(cedula),'',1,'C',1)
				pdf.output('openerp/addons/recursos_humanos/BONO/acta_vacaciones.pdf','F')
				##############################################################################################
    
    def emitir_contancia(self,cr,uid,ids,context=None):
	##########################################################
	#                  EMISION DE CONSTANCIA
	##########################################################
	data = self.read(cr, uid, ids, context=context)[0] # Lectura del objeto propio

	for constancia in self.browse(cr, uid, ids, context=None):
		if str(constancia.constancia) == "True":
		    if not data['cedula']:
		    	raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar la Cedula, intente de nuevo..."))
		    else:
		    	cedula = constancia.cedula
	
	# Instancia de la clase heredada L es horizontal y P es vertical

	pdf=fpdf_class.Constancia(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA

	pdf.set_author('Ing Jesús Laya')
	pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	pdf.add_page() # AÑADE UNA NUEVA PAGINACION
	pdf.set_font('Arial','B',14)
	pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
	pdf.set_text_color(24,29,31) # COLOR DEL TEXTO

	pdf.ln(5)
	pdf.set_fill_color(255,255,255)
	pdf.set_font('Arial','B',16)
	pdf.cell(70,6,"",'',0,'C',1)
	pdf.cell(100,6,"CONSTANCIA".decode("UTF-8"),'',1,'L',1)

	pdf.ln(5)
	pdf.set_font('Arial','',12)
	pdf.set_y(50)
	pdf.set_x(15)
	pdf.multi_cell(190, 5, 'La A.C BIBLIOTECAS VIRTUALES DE ARAGUA, certifica por medio de la presente,que la persona cuyos datos se muestran a continuación trabaja en esta institución'.decode("UTF-8"),'', 0,  'J', 0)
	pdf.ln(10)

	rrhh          = self.pool.get('hr.department')
	gerentes      = rrhh.search(cr, uid, [('name','=','Gerencia de Recursos Humanos')])
	datos         = rrhh.read(cr,uid,gerentes,context=context)
	
	for gen in datos:

		g = gen['gerente'][1]

	# CONSULTA PARA LAS BUSQUEDA DE LAS PRIMAS (OTROS COMPLEMENTOS)
	con         = self.pool.get('hr.movement.payslip')
	con_search  = con.search(cr, uid, [('cedula','=',cedula)])
	con_read    = con.read(cr,uid,con_search,context=context)

	antiguedad         = 0.00
	profesionalizacion = 0.00
	hijos              = 0.00
	hogar              = 0.00
	transporte         = 0.00
	responsabilidad    = 0.00
	otros_com = 0.00

	for concepto in con_read:
		# PRIMA ANTIGUEDAD
		if concepto['cod'] == "116":
			antiguedad = concepto['asignacion']
		# PRIMA DE PROFESIONALIZACION
		if concepto['cod'] == "456":
			profesionalizacion = concepto['asignacion']
		# PRIMA POR HIJOS
		if concepto['cod'] == "181":
			hijos = concepto['asignacion']
		# PRIMA HOGAR
		if concepto['cod'] == "210":
			hogar = concepto['asignacion']
		# PRIMA TRANSPORTE
		if concepto['cod'] == "208":
			transporte = concepto['asignacion']
		# PRIMA DE RESPONSABILIDAD
		if concepto['cod'] == "243":
			responsabilidad = concepto['asignacion']
		# OTROS COMPLEMENTOS
		otros_com = float(antiguedad) + float(profesionalizacion) + float(hijos) + float(hogar) + float(transporte) + float(responsabilidad)
	
	print "SUMA DE OTROS COMPLEMENTOS: "+str(otros_com)

	
	# CONSULTA A LA FICHA DEL TRABAJADOR ENLAZADO A LA NOMINA
	data_ficha    = self.pool.get('hr.employee')
	ficha_search  = data_ficha.search(cr, uid, [('cedula','=',cedula)])
	ficha_read    = data_ficha.read(cr,uid,ficha_search,context=context)
	
	if not ficha_search:
		raise osv.except_osv(_("Warning!"), _("Disculpe la Cedula no existe, intente de nuevo..."))
	else:

		for emp in ficha_read:
			if str(emp['segundo_nombre']) == "False":
				emp['segundo_nombre'] = ""
			else:
				emp['segundo_nombre']
			if str(emp['segundo_apellido']) == "False":
				emp['segundo_apellido'] = ""
			else:
				emp['segundo_apellido']

			nom       = emp['name_related']
			nombres   = aceptar(emp['primer_nombre'])+" "+aceptar(emp['segundo_nombre'])
			apellidos = aceptar(emp['primer_apellido'])+" "+aceptar(emp['segundo_apellido'])
			cedula    = emp['cedula']
			fecha     = format_fecha(emp['fecha_ingreso'])
			cargo     = emp['job_id'][1]
			unidad    = emp['department_id'][1]
			mensual   = redondear(emp['asignacion'])

			ticket      = self.pool.get('hr.ticket') # Objeto hr_employee (Empleado)
		
			datos       = ticket.search(cr, uid, [('cedula','=',cedula)], context=None)
			data_ticket = ticket.read(cr,uid,datos,context=context)

			for datas in data_ticket:
				monto_pagar = float(datas['monto_p'])

		# TOTAL DE INGRESO MENSUAL
		total_ingreso = float(mensual) + float(otros_com) + float(monto_pagar)

		pdf.set_font('Arial','',10)
		pdf.cell(50,5,"",'',0,'C',1)
		pdf.cell(40,5,"Apellidos:",'',0,'L',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(40,5,apellidos,'',1,'L',1)
		pdf.cell(50,5,"",'',0,'C',1)
		pdf.set_font('Arial','',10)
		pdf.cell(40,5,"Nombres:",'',0,'L',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(40,5,nombres,'',1,'L',1)
		pdf.cell(50,5,"",'',0,'C',1)
		pdf.set_font('Arial','',10)
		pdf.cell(40,5,"Cédula de Identidad:".decode("UTF-8"),'',0,'L',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(40,5,cedula,'',1,'L',1)
		pdf.cell(50,5,"",'',0,'C',1)
		pdf.set_font('Arial','',10)
		pdf.cell(40,5,"Fecha de Igreso:",'',0,'L',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(40,5,fecha,'',1,'L',1)
		pdf.cell(50,5,"",'',0,'C',1)
		pdf.set_font('Arial','',10)
		pdf.cell(40,5,"Cargo:",'',0,'L',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(40,5,cargo,'',1,'L',1)
		pdf.cell(50,5,"",'',0,'C',1)
		pdf.set_font('Arial','',10)
		pdf.cell(40,5,"Unidad:",'',0,'L',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(40,5,unidad,'',1,'L',1)
		pdf.cell(50,5,"",'',0,'C',1)
		pdf.set_font('Arial','',10)
		pdf.cell(40,5,"Ingreso mensual:",'',0,'L',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(20,5,str(mensual),'',1,'R',1)
		pdf.cell(50,5,"",'',0,'C',1)
		pdf.set_font('Arial','',10)
		pdf.cell(40,5,"Otros Complementos:",'',0,'L',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(20,5,str(otros_com),'',1,'R',1)
		pdf.cell(50,5,"",'',0,'C',1)
		pdf.set_font('Arial','',10)
		pdf.cell(40,5,"Bono de Alimentación".decode("UTF-8"),'',0,'L',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(20,5,str(redondear(monto_pagar)),'',1,'R',1)
		pdf.cell(50,5,"",'',0,'C',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(40,5,"Total Ingresos:",'',0,'L',1)
		pdf.cell(20,5,str(total_ingreso),'',1,'R',1)
		pdf.ln(5)

		dia = time.strftime('%d')
		mes = time.strftime('%B')
		ano = time.strftime('%Y')


		pdf.set_font('Arial','',12)
		pdf.cell(5,6,"",'',0,'L',1)
		pdf.multi_cell(180, 5, 'Constancia que se expide sin tachadura y sin enmienda en Maracay Edo. Aragua a los '+str(dia)+' dias del mes '+str(mes.capitalize())+' del '+str(ano)+''.decode("UTF-8"),'', 0,  'J', 0)
		pdf.set_y(155)
		pdf.set_x(15)
		pdf.cell(40,5,"Atentamente",'',0,'L',1)
		pdf.ln(5)
		pdf.set_y(180)
		pdf.set_x(80)
		pdf.cell(40,5,aceptar(g),'',0,'C',1)
		pdf.ln(5)
		pdf.set_x(80)
		pdf.cell(40,5,"Gerente de Recursos Humanos",'',0,'C',1)
		pdf.ln(5)
		pdf.set_x(80)
		pdf.cell(40,5,"AC. Bibliotecas Virtuales de Aragua",'',0,'C',1)
		#####################################################################
		dia = time.strftime('%d')
		mes = time.strftime('%B')
		anyo = time.strftime('%Y')
		fecha = dia+" de "+mes+" "+anyo
		
		ruta = "openerp/addons/recursos_humanos/ADMON/nomina/"

		title = 'CONSTANCIA ('+nom+') '+fecha.upper()+'.pdf'
		pdf.output(''+ruta+''+title,'F') # Salida del documento
		open_document = open(''+ruta+''+title) # Apertura del documento
		#########################################################################
		
		
		#Guardamos el archivo Constancia pdf en ir.attachment.employee
		self.pool.get('ir.attachment.employee').create(cr, uid, {
			'name': title,
			'res_name': title,
			'datas': base64.encodestring(open_document.read()),
			'datas_fname': title,
			'res_model': 'hr.employee (Empleado)',
			'description': "Pre-nomina "+title,
			}, context=context)
		    
		##########################################################

	    # _order = 'cantidad'
	    
	    # _rec_name = 'cantidad'

	        #################################################################
    _columns = {

        'cedula': fields.char(string="Cédula", required = False),
        'cedula_bono' : fields.char(string="Cédula", required = False),
				'targeta' : fields.boolean(string="Targeta"),
				'recarga' : fields.boolean(string="Recarga"),
				'bonos' : fields.boolean(string="Recarga"),
				'constancia' : fields.boolean(string="Constancia"),
				'class_personal_targeta' : fields.many2one("becados.clasper", "Personal", required = False),
				'class_personal_recarga' : fields.many2one("becados.clasper", "Personal", required = False),
				'alim_ids' : fields.many2many("hr.ticket","proceso_targeta","id_model","id_targeta","Targeta",required=False),
				'recarga_ids' : fields.many2many("hr.ticket","proceso_recarga","id_model","id_recarga","Recarga",required=False),
        
    }

    _defaults = {
        
    }
# FORMATEAR FECHA (FUNCION GLOBAL PARA EL FORMATO DE FECHAS
def format_fecha(fecha):
    date = fecha.split("-")
    nueva_fecha = date[2]+"/"+date[1]+"/"+date[0]
    return nueva_fecha

def aceptar(cadena):
	result = cadena.encode('UTF-8').decode('UTF-8') # INSTITUCION
	return result
    
def redondear(cadena):
	salida = "%.2f" % round(cadena,2)
	return salida
########################################################################
