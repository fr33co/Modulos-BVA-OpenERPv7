# -*- coding: utf-8 -*-

import urllib2, urllib
import time
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
#####################################################


import re # Importar re para eliminar aceptos
import unicodedata #Importar re para eliminar aceptos
import httplib
#####################################################

import fpdf_class # Importando la clase constructora del PDF
#####################################################


class Proceso_Nomina(osv.Model):

	'''(Procesamiento de nóminas)'''

	_name = 'hr.payslip.employee'

	#######################################################
	#
	# Proceso para generación de archivo TXT de la nómina (TXT)
	#
	#######################################################
	def elimina_tildes(self, s): # Funcion para elimina_tildes python
		"""
		Funcion para eliminar las tildes de algun texto utilizando el módulo unicodedata.
		"""
		return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
	
	def draft_payslip_run(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

	def close_payslip_run(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'close'}, context=context)	
	####################################################################################################################
	# Generacion de TXT (pór categoria Administrativo, Directivo y Obrero) En el sub modulo de asignaciones de la nomina
	####################################################################################################################
	def generate_txt_slip(self, cr, uid, ids, context=None):

		browse_slip_id = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro)


		for slip_id in browse_slip_id: # Iteración del objeto (módelo hr_payslip_run)

			# Bloque código (para estado Borrador, no permitir generar el archivo TXT)
			if slip_id.state == "draft":
				raise osv.except_osv(_("Warning!"), _("Disculpe para generar el diskette al Banco, debe realizar el cierre de nómina..."))

			# Bloque código (para estado cerrado, permitir generar el archivo TXT)
			elif slip_id.state == "close":

				if context is None:
					context = {} # Diccionario vacio
				data_ids = self.read(cr, uid, ids, context=context)[0] # Lectura del objeto propio

				id_slip  = slip_id.id # Id del objeto
				slip 	 = slip_id.slip_ids # Grupo de ID de la lista slip_ids
				admon 	 = slip_id.class_personal.clas_personal # Nombre de la clsificacion del personal
				admon_id = slip_id.class_personal.id # ID clasificacion del personal
				#for x_id in slip:
					#print "ID "+str(x_id.id)
				if not data_ids['slip_ids']: # En caso de que no contenga ningun dato, emita un mensaje
					raise osv.except_osv(_("Warning!"), _("Disculpe debe seleccionar la lista de empleados de la nómina, intente de nuevo..."))
				elif slip != 0: # Si es distinto pueda permitir realizar la acción
					
					# Grupo de ID del personal
					payslip_id = data_ids['slip_ids']
					
					print "GRUPO DE IDS: "+str(payslip_id)
					hr = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)
					get_hr = self.pool.get('hr.movement.employee') # Objeto hr_movement_employee (Empleado)

					search_get_hr = get_hr.search(cr, uid, [('id','=',payslip_id),('emp','=',admon_id)], context=None) # Se busca el ID dado
					search_hr = get_hr.search(cr, uid, [('id','=',payslip_id),('emp','=',admon_id)], count=True) # Conteo de registros
					employee = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado

					i = 0
					data = ""
					cuenta = ""
					t = 0
					while (i < search_hr):
						print "NOMBRE DEL PERSONAL: "+str(employee[i]['nombres'])
						
						cedula_emp = employee[i]['cedula'] # Cedula del Empleado
						
						search_emp = hr.search(cr, uid, [('cedula','=',cedula_emp)], context=None) # Se busca el ID dado
						emp_hr = hr.read(cr,uid,search_emp,context=context) # Se refleja el resultado
						
						for emp in emp_hr:
							
							n_ccount = emp['bank_account_id']
							p_nom    = emp['primer_nombre']
							s_nom    = emp['segundo_nombre']
							p_ap     = emp['primer_apellido']
							s_ap     = emp['segundo_apellido']
							cedula   = emp['cedula']
							
							if p_nom is False: p_nom =" "
							else: p_nom
							if s_nom is False: s_nom =" "
							else: s_nom[0:1]
							if p_ap is False: p_ap =" "
							else: p_ap
							if s_ap is False: s_ap =" "
							else: s_ap[0:1]
														
							bank_id     = n_ccount[0]
							bank_hr     = self.pool.get('res.partner.bank')
							search_bank = bank_hr.search(cr, uid, [('id','=',bank_id)], context=None) # Se busca el ID dado
							bank        = bank_hr.read(cr,uid,search_bank,context=context) # Se refleja el resultado
							
							for x in bank:
								count_e 	= x['acc_number']
								type_account    = x['type_account']
								bank_obj        = x['bank']
								name_bank       = bank_obj[1]	
								cod_1           = "770"
								cod_2           = "00"
								standar         = "03291"
							# 	#############################################################
							# 	##		Creacion del archivo txt
							# 	#############################################################
								# Estructura de salidda de la data TXT
							if str(x['bank'][1]) == "Venezuela":
								print "BANCO VENEZUELA: "+str(x['acc_number'])
								
								block_1     = type_account.ljust(0)+count_e.ljust(0)+""+str(employee[i]['monto_c']).replace('.',"").zfill(9)+type_account.ljust(0)+cod_1.ljust(0)
								block_2     = p_ap.upper()+" "+s_ap[0:1].upper()+" "+p_nom.upper()+" "+s_nom[0:1].upper()
								block_2     = block_2.ljust(40)
								block_3     = cod_2+cedula+standar
								
								datos       = block_1+block_2+block_3.rjust(21)+"\n" # Salida de data de los Datos
								t +=       float(employee[i]['monto_c'])
								i = i + 1 # Iteracion de los datos
								data = data + datos # Acumulador de la data
									
							if str(x['bank'][1]) == "BNC":
								print "BANCO BNC: "+str(x['acc_number'])
									
								block_1     = type_account.ljust(0)+count_e.ljust(0)+""+str(employee[i]['monto_c']).replace('.',"").zfill(9)+type_account.ljust(0)+cod_1.ljust(0)
								block_2     = p_ap.upper()+" "+s_ap[0:1].upper()+" "+p_nom.upper()+" "+s_nom[0:1].upper()
								block_2     = block_2.ljust(40)
								block_3     = cod_2+cedula+standar
								
								datos       = block_1+block_2+block_3.rjust(21)+"\n" # Salida de data de los Datos
								t +=       float(employee[i]['monto_c'])
								i = i + 1 # Iteracion de los datos
								data = data + datos # Acumulador de la data
					tota_general = str(t).replace('.',"")
					elemento     = "%.2f" % round(float(tota_general),3)
					total        = str(elemento).replace('.',"")
					print "MONTO TOTAL A PAGAR: "+str(total)
					# ###########################################################
					# #
					# #		Objeto hr_payslip (Lectura de datos)
					# #
					# ###########################################################
					dia   = time.strftime('%d')
					mes   = time.strftime('%B')
					anyo  = time.strftime('%Y')
					fecha = dia+" de "+mes+" "+anyo # Fecha de creacion
					
					title = 'BBVV '+admon+' ('+fecha+')' # Salida del titulo con los datos especificos
					# #
					# ############################################################
					# ## Proceso de validacion del las quincenas de la nomina
					if dia < 16:
						#"ES MENOR A 16"
						periodo_f = slip_id.date_start
						fecha     = periodo_f.split("-") 
						periodo   = str(fecha[2])+"/"+str(fecha[1])+"/"+str(fecha[0][2:4])
						
					else:
						#"ES MAYOR A 16"
						periodo_f = slip_id.date_end
						fecha     = periodo_f.split("-") 
						periodo   = str(fecha[2])+"/"+str(fecha[1])+"/"+str(fecha[0][2:4])
					# #
					# ############################################################
					id_att = self.register_txt_ven(cr, uid, data, title, total, periodo, admon, context) # Objeto con referencia (Proceso de generación de TXT)
	####################################################################################################################

	def register_txt_ven(self, cr, uid, data, title, total, periodo, admon, context):
		
		propietario = self.pool.get('hr.propietario') # Objeto hr_propietario (Empleado)

		search_pro  = propietario.search(cr, uid, [], context=None) # Se busca el ID dado Propietario de la cuenta
		pro         = propietario.read(cr,uid,search_pro,context=context) # Se refleja el resultado
		
		encabezado  = str(pro[0]['propietario'])+"              "+str(pro[0]['cuenta'])+periodo+str(total).zfill(13)+""+str(pro[0]['estandar'])
		# # Proceso de Generación del .txt (Nomina de Empleado)
		# ###########################################################

		nom = title+'.'+ 'txt'

		if str(admon) == "Empleado Fijo":
			directorio = "/ADMON/TXT/"
		elif str(admon) == "Directivo":
			directorio = "/DIRECTIVO/TXT/"
		else:
			directorio = "/OBRERO/TXT/"

		#######################################################################
		#	Carga de archivo txt en directorio ADMON/nomina/ Venezuela
		#######################################################################
		archivo = open('openerp/addons/recursos_humanos'+directorio+''+nom,'w')
		archivo.write(encabezado+"\n"+data+"\n")
		archivo.close()
		#######################################################################
		# Guardamos los txt en ir.attachment.employee
		id_att = self.pool.get('ir.attachment.employee').create(cr, uid, {
			'name': nom,
			'res_name': nom,
			'datas': base64.encodestring(encabezado+"\n"+data+"\n"),
			'datas_fname': nom,
			'res_model': 'hr.employee (Empleado)',
			'description': "Proceso Bancario "+title,

			}, context=context)

		return id_att
		#######################################################################

	def register_txt_hr_bnc(self, cr, uid, data, title, standar, total, periodo, context):
		#print "DATAS: "+str(data)

		encabezado_BNC = "ND 2180038781"
		# # Proceso de Generación del .txt (Nomina de Empleado)
		# ###########################################################

		nom = title+'.'+ 'txt'
		#######################################################################
		#	Carga de archivo txt en directorio ADMON/nomina/ Venezuela
		#######################################################################
		archivo = open('openerp/addons/recursos_humanos/ADMON/nomina/'+nom,'w')
		archivo.write(encabezado+"\n"+data+"\n")
		archivo.close()
		#######################################################################

		id_att = self.pool.get('ir.attachment').create(cr, uid, {
			'name': nom,
			'res_name': nom,
			'datas': base64.encodestring(encabezado+"\n"+data+"\n"),
			'datas_fname': nom,
			'res_model': 'hr.employee (Empleado)',
			'adjunto' : '2',
			'description': "Proceso Bancario "+title,

			}, context=context)

		return id_att
		#######################################################################

	def generate_xsl_slip(self, cr, uid, ids, context=None): # proceso de generación de formato XSL

		header_style = XFStyle()
		borders = Borders()
		borders.left = 1
		borders.right = 1
		borders.top = 1
		borders.bottom = 1
		header_style.borders = borders
		first_book = Workbook()

		fuente = xlwt.Font()
		fuente.name = 'Times New Roman'
		fuente.colour_index = 2
		fuente.fore_colour = 'yellow'
		fuente.bold = True


		style0 = xlwt.easyxf('font: name Arial, colour black, bold on') #Estilo de fuente negrita
		style1 = xlwt.easyxf('align: horiz center') #Estilo alinear al centro
		style2 = xlwt.easyxf('',num_format_str='DD-MM-YY')

		style3 = xlwt.XFStyle()
		style3.font = fuente


		#################################################################
					# Estrutura principal del xsl (Encabezado)
		#################################################################
		ws1 = first_book.add_sheet('first_sheet', cell_overwrite_ok=True)
		ws1.write_merge(0, 0, 0, 4,)
		ws1.row(0).height = 1800
		ws1.write(0, 0, 'LISTADO DE NOMINAS', header_style)
		ws1.write(1, 0, 'Cedula',style0)
		ws1.write(1, 1, 'Nombre y Apellidos',style0)
		ws1.write(1, 2, 'Sueldo',style0)
		ws1.write(1, 3, 'Nro de cuenta',style0)
		ws1.write(1, 4, 'Banco',style0)
		ws1.write(1, 5, 'Fecha N',style0)
		ws1.write(1, 6, 'Cod cargo',style0)
		ws1.write(1, 7, 'Cargo',style0)
		ws1.write(1, 8, 'Direccion',style0)
		ws1.write(1, 9, 'Telefono',style0)
		ws1.write(1, 10, 'Estatus',style0)
		ws1.write(1, 11, 'Fecha de ingreso',style0)
		ws1.write(1, 12, 'Fecha de egreso',style0)
		ws1.write(1, 13, 'Personal',style0)
		ws1.write(1, 14, 'Cod Personal',style0)
		ws1.write(1, 15, 'Cod departamento',style0)
		ws1.write(1, 16, 'Departamento',style0)
		ws1.write(1, 17, 'Caja de ahorro',style0)
		ws1.write(1, 18, 'Prima respon',style0)
		ws1.write(1, 19, 'Cod nivel instruccion',style0)
		ws1.write(1, 20, 'Nivel instruccion',style0)
		ws1.write(1, 21, 'Camisa',style0)
		ws1.write(1, 22, 'Pantalon',style0)
		ws1.write(1, 23, 'Zapato',style0)
		ws1.write(1, 24, 'Sexo',style0)
		ws1.write(1, 25, 'Referencia',style0)
		ws1.write(1, 26, 'Prima de reponsabilidad',style0)
		ws1.write(1, 27, 'Antiguedad',style0)
		ws1.write(1, 28, 'Tiempo de servicio',style0)
		ws1.write(1, 29, 'Edad',style0)
		ws1.write(1, 30, 'Fecha del reporte',style0)

		get_hr = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)
		search_get_hr = get_hr.search(cr, uid, [('categoria','=','2')], context=None) # Se busqa el ID dado
		employee = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado

			#Variable data (datos del Módelo hr_employee (Listado))
		i = 0
		cuenta = ""
		cargo  = ""
		for x in employee: # Bloque para la iteracion del objeto
			n_ccount = x['bank_account_id'] # Entidad bancaria
			nom = self.elimina_tildes(x['name_related']).upper()

			job = x['job_id']
			print x['fecha_nacimiento']
			print n_ccount

			if n_ccount is None:
				n_ccount[1][-20:]=""

			elif n_ccount !=0:
				cuenta = n_ccount[1][-20:]
				print "Numero de cuenta: "+str(cuenta)
			if job is None:
				job[1]=""
			elif job !=0:
				cargo = job[1]
				print "Cargo: "+str(cargo)

			ws1.write(i+2, 0, int(x['cedula']))
			ws1.write(i+2, 1, str(nom.center(20)))
			ws1.write(i+2, 2, int(x['asignacion']))
			ws1.write(i+2, 3, cuenta)
			ws1.write(i+2, 4, )
			ws1.write(i+2, 5, x['fecha_nacimiento'])

			i = i + 1 # Acumulador de la data


		###########################################################
		#
		#			Objeto hr_payslip (Lectura de datos)
		#
		###########################################################
		# dia = time.strftime('%d')
		# mes = time.strftime('%m')
		# anyo = time.strftime('%Y')
		 #fecha = dia+"-"+mes+"-"+anyo

		# title = 'BBVV ('+fecha+')'

		# ############################################################
		# id_att = self.register_txt_hr(cr, uid, data, title, context) # Objeto con referencia (Proceso de generación de TXT)


		#################################################################
		dia = time.strftime('%d')
		mes = time.strftime('%m')
		anyo = time.strftime('%Y')
		fecha = dia+"-"+mes+"-"+anyo

		nom = 'Nomina '+fecha+'.xls'

		first_book.save('/home/ADMON/nomina/'+nom)
		f = open('/home/ADMON/nomina/'+nom)



		# id_att = self.pool.get('ir.attachment').create(cr, uid, {
		# 	'name': nom,
		# 	'res_name': nom,
		# 	'datas': base64.encodestring(nom),
		# 	'datas_fname': nom,
		# 	'res_model': 'hr.employee (Empleado)',
		# 	'description': nom,

		# 	}, context=context)
		# #raise osv.except_osv(_('Error!'),_('El archivo'))
		# return id_att
	
	def generate_pre_slip(self, cr, uid, ids, context=None): # Generacion de la pre-nomina de los  empleados...

		##########################################################################################

		# Instancia de la clase heredada
		pdf=fpdf_class.Nomina_slip(orientation='L',unit='mm',format='A4') #HORIENTACION DE LA PAGINA

		#pdf.set_title(title)
		pdf.set_author('Jesus laya')
		pdf.alias_nb_pages()
		pdf.add_page()
		pdf.set_font('Times','',12)
		pdf.set_fill_color(157,188,201)
		pdf.set_text_color(24,29,31)
		pdf.set_margins(23,20,0) # Margenes left, rigth
		#################################################################
		pdf.ln(20) # Saldo de linea
		pdf.cell(65,8,"Nombre",1,0,'C',1)
		pdf.cell(25,8,"Cedula",1,0,'C',1)
		pdf.cell(50,8,"Nro de cuenta",1,0,'C',1)
		pdf.cell(50,8,"Sueldo",1,0,'C',1)
		pdf.cell(50,8,"Monto a cobrar",1,1,'C',1)
		##################################################################
		browse_slip_id = self.browse(cr, uid, ids, context=None)
		for x in browse_slip_id:
			personal = x.class_personal.clas_personal # Captura del personal
			estado = x.state
			type_slip = x.type_slip.id
		data_ids = self.read(cr, uid, ids, context=context)[0]
		payslip_id = data_ids['slip_ids'] # Grupo de IDS de la pre-nomina
		
		if not data_ids['slip_ids']: # En caso de que no contenga ningun dato, emita un mensaje
			raise osv.except_osv(_("Warning!"), _("Disculpe debe seleccionar la lista de empleados, intente de nuevo..."))

		else:
			hr_emp    = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)
			hr        = self.pool.get('hr.movement.employee') # Objeto hr_employee (Empleado)
			datos     = hr.search(cr, uid, [('id','=',payslip_id),('nomina_admin','=',type_slip)], context=None)
			employees = hr.read(cr,uid,datos,context=context)
			j = len(employees)
			##################################################################
			i = 0
			j = 0
			sumatoria = 0
			monto = 0.0
			for x in employees:
				sumatoria +=  float(x['monto_c'])
				asignacion = float(x['monto_c'])
				print "CEDULA DEL EMPLEADO DE LA NOMINA: "+str(x['cedula'])
				print "EMPLEADO: "+str(x['nombres'])
				print "SUELDO DE LAS ASIGNACIONES DEL EMPLEADO: "+str(asignacion)
				
				datos_emp     = hr_emp.search(cr, uid, [('cedula','=',x['cedula'])], context=None) # modo de busqueda por cedula en la ficcha de Empleado
				employee      = hr_emp.read(cr,uid,datos_emp,context=context) # Objeto de Lectura de los datos
				
				for emp in employee:
					n_ccount = emp['bank_account_id'] # Cuenta Bancaria del Empleado

				monto = sumatoria
				if j == 12:
					pdf.add_page()
					pdf.set_fill_color(157,188,201)
					pdf.ln(20) # Salto de linea
					pdf.cell(65,8,"Nombre",1,0,'C',1)
					pdf.cell(25,8,"Cedula",1,0,'C',1)
					pdf.cell(50,8,"Nro de cuenta",1,0,'C',1)
					pdf.cell(50,8,"Sueldo",1,0,'C',1)
					pdf.cell(50,8,"Monto a cobrar",1,1,'C',1)
					j=0
				pdf.set_fill_color(255,255,255)
				if j % 2 == 0:
					pdf.set_fill_color(234,234,234)
			
				pdf.set_text_color(0,0,0)
				if j == 10 or j == 20 or j == 30:
					pdf.set_text_color(24,29,31)
				if n_ccount is None:
					n_ccount[1][-20:]=""
				elif n_ccount !=0:
					cuenta = n_ccount[1][-20:]
	
				pdf.cell(65,8,str(self.elimina_tildes(x['nombres'])),1,0,'C',1)
				pdf.cell(25,8,str(x['cedula']),1,0,'C',1)
				pdf.cell(50,8,str(cuenta),1,0,'C',1)
				pdf.cell(50,8,str(x['sueldo']),1,0,'C',1)
				pdf.cell(50,8,str(asignacion),1,1,'C',1)
			
				j =j+1
			
			pdf.ln(10)
			pdf.set_fill_color(157,188,201)
			pdf.cell(65,8,"",0,0,'C',0)
			pdf.cell(25,8,"",0,0,'C',0)
			pdf.cell(50,8,"",0,0,'C',0)
			pdf.cell(50,8,"Personal",1,0,'C',1)
			pdf.cell(50,8,"Monto total",1,1,'C',1)
			pdf.cell(65,8,"",0,0,'C',0)
			pdf.cell(25,8,"",0,0,'C',0)
			pdf.cell(50,8,"",0,0,'C',0)
			pdf.set_fill_color(255,255,255)
			pdf.cell(50,8,str(personal)+' ('+str(j)+')',1,0,'C',1)
			pdf.cell(50,8,str(monto),1,1,'C',1)
			#####################################################################
			dia = time.strftime('%d')
			mes = time.strftime('%B')
			anyo = time.strftime('%Y')
			fecha = dia+" de "+mes+" "+anyo
			
			if estado == "draft":
			
				title = 'Pre-nomina ('+self.elimina_tildes(personal)+') '+fecha+'.pdf'
				pdf.output('openerp/addons/recursos_humanos/ADMON/pre_nomina/'+title,'F') # Salida del documento
				open_document = open('openerp/addons/recursos_humanos/ADMON/pre_nomina/'+title) # Apertura del documento
			else:
				title = 'Nomina ('+self.elimina_tildes(personal)+') '+fecha+'.pdf'
				pdf.output('openerp/addons/recursos_humanos/ADMON/nomina/'+title,'F') # Salida del documento
				open_document = open('openerp/addons/recursos_humanos/ADMON/nomina/'+title) # Apertura del documento
			#########################################################################
			
			
			# Guardamos el archivo pdf en ir.attachment.employee
			id_att = self.pool.get('ir.attachment.employee').create(cr, uid, {
				'name': title,
				'res_name': title,
				'datas': base64.encodestring(open_document.read()),
				'datas_fname': title,
				'res_model': 'hr.employee (Empleado)',
				'description': "Pre-nomina "+title,
			
				}, context=context)
			
			return id_att
	#####################################################################################################################
	#				PROCESO PARA CALCULAR EL MONTO DE LA QUINCENA DEL MES
	#####################################################################################################################
	def mount_slip_ids(self, cr, uid, ids, context=None): # Boton de accion para calcular en monto de la quincena del mes
		
		values = {}
		
		data_ids = self.read(cr, uid, ids, context=context)[0] # Lectura de grupo de ids
		browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro
		
		for x in browse_data:
			id_slip = x.type_slip.id # Id de la nomina
			
		payslip_id = data_ids['slip_ids'] # Grupo de ids de las asignaciones de los empleados
		print "ID DE TIPO DE NOMINA: "+str(id_slip)
		print "GRUPO DE IDS DE LAS ASIGNACIONES DE LA NOMINA: "+str(payslip_id)
		
		hr = self.pool.get('hr.movement.employee') # Objeto hr_employee (Empleado)
		datos = hr.search(cr, uid, [('id','=',payslip_id),('nomina_admin','=',id_slip)], context=None) # 
		employees = hr.read(cr,uid,datos,context=context) # Lectura modo array del objecto
		
		i = 0
		sumatoria = 0
		while (i < len(employees)):
			
			print "NOMBRES: "+str(employees[i]['nombres'])
			print "GRUPO DE CONCEPTOS: "+str(employees[i]['movement_ids'])
			sumatoria +=  float(employees[i]['monto_c'])
			i = i + 1 # Iteracion de los datos
		monto = sumatoria
		
		self.write(cr, uid, ids, {'mount': monto}, context=context)
	#####################################################################################################################
	_columns = {
		'type_slip' : fields.many2one("becados.tiponomina", "Nómina", required = True),
		'class_personal' : fields.many2one("becados.clasper", "Personal", required = True),
		'type_slip' : fields.many2one("becados.tiponomina", "Nómina", required = True),
		'date_start' : fields.date("Desde", required=True),
		'date_end' : fields.date("Hasta", required=True),
		'name' : fields.char(string="Nombre", required=True),
		'mount' : fields.char(string="Monto", required=False),
		'user': fields.many2one('res.users', 'Registrado por:', readonly=True),
		'slip_ids' : fields.many2many("hr.movement.employee","proceso_payslip","id_slip","id_employee","Empleados",required=False),
		#'archivos' : fields.one2many("ir.attachment", "nominas", string="Archivos de nómina", required="False"),
		'state': fields.selection([
			('draft', 'Pre nómina'),
			('close', 'Nómina'),
		],
		'Estado', select=True, readonly=True),
		'class_personal' : fields.many2one("becados.clasper", "Personal", required = True,readonly=True, states={'draft': [('readonly', False)]}), # Validación, si esta en estado de nómina no pueda ser editado
		'type_slip' : fields.many2one("becados.tiponomina", "Nómina", required = True,readonly=True, states={'draft': [('readonly', False)]}), # Validación, si esta en estado de nómina no pueda ser editado
		'date_start': fields.date('Desde', required=True, readonly=True, states={'draft': [('readonly', False)]}),
		'date_end': fields.date('Hasta', required=True, readonly=True, states={'draft': [('readonly', False)]}),
		'slip_ids' : fields.many2many("hr.movement.employee","proceso_payslip","id_slip","id_employee","Empleados", required = False,readonly=True, states={'draft': [('readonly', False)]}),
		'mount' : fields.char(string="Monto", required=False, readonly=True, states={'draft': [('readonly', False)]}),
	}

	_defaults = {
		'state': 'draft',
		'date_start': lambda *a: time.strftime('%Y-%m-01'), # Fecha desde
		'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
		'date_end': lambda *a: str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10], # Fecha hasta
		

	}
	
