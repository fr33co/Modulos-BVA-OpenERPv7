# -*- coding: utf-8 -*-
import time
import urllib2, urllib
from datetime import datetime
from dateutil import relativedelta
from fpdf import FPDF
import datetime
import fpdf

from openerp.osv import fields, osv
from openerp.tools.translate import _
import base64 #Necesario para la generación del .txt
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring #Necesario para la generación del .xsl
import netsvc
import tools
import logging
from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from xlwt import Borders
import os
import math
#############################
import os
import commands
import re # Importar re para eliminar aceptos
import unicodedata #Importar re para eliminar aceptos



#############################

class Proceso_Nomina(osv.Model):

	'''Herenciando a hr.payslip.run (Procesamiento de nóminas)'''

	_inherit = 'hr.payslip.run'

	#######################################################
	#
	# Proceso para generación de archivo TXT de la nómina (TXT)
	#
	#######################################################
	def elimina_tildes(self, s): # Funcion para elimina_tildes pyton
		"""
		Funcion para eliminar las tildes de algun texto utilizando el modulo unicodedata.
		"""
		return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

	def generate_txt_slip(self, cr, uid, ids, context=None):

		browse_slip_id = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro)


		for slip_id in browse_slip_id: # Iteración del objeto (módelo hr_payslip_run)

			# Bloque código (para estado Borrador, no permitir generar el archivo TXT)
			if slip_id.state == "draft":
				raise osv.except_osv(_("Warning!"), _("Disculpe para generar el diskette al banco, debe realizar el cierre de nómina..."))

			# Bloque código (para estado cerrado, permitir generar el archivo TXT)
			elif slip_id.state == "close":

				if context is None:
					context = {} # Diccionario vacio
				data_ids = self.read(cr, uid, ids, context=context)[0] # Lectura del objeto propio

				id_slip = slip_id.id # Id del objeto
				slip 	= slip_id.slip_ids # Grupo de ID de la lista slip_ids

				if not data_ids['slip_ids']: # En caso de que no contenga ningun dato, emita un mensaje
					raise osv.except_osv(_("Warning!"), _("Disculpe debe seleccionar la lista de empleados de la nómina, intente de nuevo..."))
				elif slip != 0: # Si es distinto pueda permitir realizar la acción


					get_hr = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)

					search_get_hr = get_hr.search(cr, uid, [('status','=','1'),('categoria','=','2')], context=None) # Se busqa el ID dado
					search_hr = get_hr.search(cr, uid, [('status','=','1'),('categoria','=','2')], count=True) # Se busqa el ID dado
					employee = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado

							#Variable data (datos del Módelo hr_employee (Listado))
					#print employee
					i = 0
					data = ""
					cuenta = ""
					a = ""
					b = ""
					c = ""
					d = ""
					t = 0.0
					while (i < search_hr):

						n_ccount = employee[i]['bank_account_id']
						p_nom    = employee[i]['primer_nombre']
						s_nom    = employee[i]['segundo_nombre']
						p_ap     = employee[i]['primer_apellido']
						s_ap = employee[i]['segundo_apellido']


						t +=  employee[i]['asignacion']

						if not p_nom :
							p_nom=""
						else:
							a= p_nom
						if not s_nom:
							s_nom=""
						else:
							b = s_nom[0:1]
						if not p_ap:
							p_ap=""
						else:
							c = p_ap
						if not s_ap:
							s_ap=""
						else:
							d = s_ap[0:1]

						#print nombre_completo

						if n_ccount is None:
							n_ccount[1][-20:]=""
						elif n_ccount !=0:
							cuenta = n_ccount[1][-20:]
							print cuenta

						#usu = os.getlogin()
						#print "USUARIO DEL SISTEMA: "+str(usu)

						nombre_completo = str(c)+" "+str(d)+" "+str(a)+" "+str(b)
						monto_total_p = "269035"
						cod_1 = "0770"
						cod_2 = "00"
						cod_3 = "0"
						cod_4 = "00"
						standar = "03291"
						datos = "0"+str(cuenta)+"00000"+str(monto_total_p)+""+str(cod_1)+str(nombre_completo.upper())+"\t\t\t\t"+str(cod_4)+str(employee[i]['cedula'])+str(cod_3)+str(standar)+"\n"
						i = i + 1 # Iteracion de los datos
						data = data + datos # Acumulador de la data
					total= t
					###########################################################
					#
					#		Objeto hr_payslip (Lectura de datos)
					#
					###########################################################
					dia = time.strftime('%d')
					mes = time.strftime('%B')
					anyo = time.strftime('%Y')
					fecha = dia+" de "+mes+" "+anyo

					title = 'BBVV ('+fecha+')'

					###########################################################
					id_att = self.register_txt_hr(cr, uid, data, title, standar, total, context) # Objeto con referencia (Proceso de generación de TXT)


	def register_txt_hr(self, cr, uid, data, title, standar, total, context):
		#print "DATAS: "+str(data)

		encabezado = "GOBERNACION DEL ESTADO ARAGUA    010202159800063163328531/03/1400000"+""+str(total)+""+str(standar)
		# # Proceso de Generación del .txt (Nomina de Empleado)
		# ###########################################################

		nom = title+'.'+ 'txt'

		id_att = self.pool.get('ir.attachment').create(cr, uid, {
			'name': nom,
			'res_name': nom,
			'datas': base64.encodestring(encabezado+"\n"+data+"\n"),
			'datas_fname': nom,
			'res_model': 'hr.employee (Empleado)',
			'description': "Proceso Bancario "+title,

			}, context=context)

		return id_att
		#############################################################

	def generate_xsl_slip(self, cr, uid, ids, context=None): # proceso de generación de formato XSL

		header_style = XFStyle()
		borders = Borders()
		borders.left = 1
		borders.right = 1
		borders.top = 1
		borders.bottom = 1
		header_style.borders = borders
		first_book = Workbook()

		#################################################################
					# Estrutura principal del xsl (Encabezado)
		#################################################################
		ws1 = first_book.add_sheet('first_sheet', cell_overwrite_ok=True)
		ws1.write_merge(0, 0, 0, 4,)
		ws1.row(0).height = 1800
		ws1.write(0, 0, 'LISTADO DE NOMINAS', header_style)
		ws1.write(1, 0, 'Cedula')
		ws1.write(1, 1, 'Nombre y Apellidos')
		ws1.write(1, 2, 'Sueldo')
		ws1.write(1, 3, 'Nro de cuenta')
		ws1.write(1, 4, 'Banco')
		ws1.write(1, 5, 'Fecha N')
		ws1.write(1, 6, 'Cod cargo')
		ws1.write(1, 7, 'Cargo')
		ws1.write(1, 8, 'Direccion')
		ws1.write(1, 9, 'Telefono')
		ws1.write(1, 10, 'Estatus')
		ws1.write(1, 11, 'Fecha de ingreso')
		ws1.write(1, 12, 'Fecha de egreso')
		ws1.write(1, 13, 'Personal')
		ws1.write(1, 14, 'Cod Personal')
		ws1.write(1, 15, 'Cod departamento')
		ws1.write(1, 16, 'Departamento')
		ws1.write(1, 17, 'Caja de ahorro')
		ws1.write(1, 18, 'Prima respon')
		ws1.write(1, 19, 'Cod nivel instruccion')
		ws1.write(1, 20, 'Nivel instruccion')
		ws1.write(1, 21, 'Camisa')
		ws1.write(1, 22, 'Pantalon')
		ws1.write(1, 23, 'Zapato')
		ws1.write(1, 24, 'Sexo')
		ws1.write(1, 25, 'Referencia')
		ws1.write(1, 26, 'Prima de reponsabilidad')
		ws1.write(1, 27, 'Antiguedad')
		ws1.write(1, 28, 'Tiempo de servicio')
		ws1.write(1, 29, 'Edad')
		ws1.write(1, 30, 'Fecha del reporte')

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
			#print n_ccount
			#
			#if n_ccount is None:
			#	n_ccount[1][-20:]=""
			#
			#elif n_ccount !=0:
			#	cuenta = n_ccount[1][-20:]
			#
			# 	print "Numero de cuenta: "+str(cuenta)
			#if job is None:
			#	job[1]=""
			#elif job !=0:
			#	cargo = job[1]
			#	print "Cargo: "+str(cargo)
			#
			#ws1.write(i+2, 0, int(x['cedula']))
			#ws1.write(i+2, 1, str(nom.center(20)))
			#ws1.write(i+2, 2, int(x['asignacion']))
			#ws1.write(i+2, 3, cuenta)
			#ws1.write(i+2, 4, )
			#ws1.write(i+2, 5, x['fecha_nacimiento'])
			#
			#i = i + 1 # Acumulador de la data


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

		#first_book.save('/tmp/'+nom)
		#f = open('/tmp/'+nom)



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

	def generate_pre_slip(self, cr, uid, ids, context=None):

		browse_slip_id = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro)


		for slip_id in browse_slip_id: # Iteración del objeto (módelo hr_payslip_run)
			print "ID de la clasificacion del personal: "+str(slip_id.class_personal.id)

			#if context is None:
			#	context = {} # Diccionario vacio
			#data_ids = self.read(cr, uid, ids, context=context)[0] # Lectura del objeto propio
			#
			#id_slip = slip_id.id # Id del objeto
			#slip 	= slip_id.slip_ids # Grupo de ID de la lista slip_ids
			#
			#if not data_ids['slip_ids']: # En caso de que no contenga ningun dato, emita un mensaje
			#	raise osv.except_osv(_("Warning!"), _("Disculpe para generar el listado de la pre nómina, dede seleccionar los empleados, por favor intente de nuevo..."))
			#elif slip != 0: # Si es distinto pueda permitir realizar la acción
			#
			#
			#	get_hr = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)
			#
			#	search_get_hr = get_hr.search(cr, uid, [('status','=','1'),('categoria','=','2')], context=None) # Se busqa el ID dado
			#	employee = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
			#
			#			#Variable data (datos del Módelo hr_employee (Listado))
			#
			#	i = 0
			#	data = ""
			#	cuenta = ""
			#	for x in employee:
			#		n_ccount = x['bank_account_id']
			#		nom = x['name_related']
			#
			#		nom = self.elimina_tildes(x['name_related'])
			#
			#		#usu = os.getlogin()
			#		#print "USUARIO DEL SISTEMA: "+str(usu)
			#
			#
			#		tupla = nom.split(" ")
			#		print " Nombre nombre completo: "+str(nom)
			#		print "Tupla del nombre: "+str(tupla)
			#
			#
			#
			#		nombre_completo = str(tupla[2])+" "+str(str(tupla[3][0:1]))+" "+str(tupla[0])+" "+str(tupla[1][0:1])
			#
			#		if n_ccount is None:
			#			n_ccount[1][-20:]=""
			#		elif n_ccount !=0:
			#			cuenta = n_ccount[1][-20:]
			#
			#		#print x['cedula']
			#		monto_total_p = "269035"
			#		cod_1 = "0770"
			#		cod_2 = "00"
			#		cod_3 = "0"
			#		cod_4 = "00"
			#		standar = "03291"
			#
			#		datos = "0"+str(cuenta)+"00000"+str(monto_total_p)+""+str(cod_1)+str(nombre_completo)+"\t\t\t\t\t\t"+str(cod_4)+str(x['cedula'])+str(cod_3)+str(standar)+"\n"
			#		data = data + datos # Acumulador de la data
			#
			#	###########################################################
			#	#
			#	#		Objeto hr_payslip (Lectura de datos)
			#	#
			#	###########################################################
			#	dia = time.strftime('%d')
			#	mes = time.strftime('%m')
			#	anyo = time.strftime('%Y')
			#	fecha = dia+"-"+mes+"-"+anyo
			#
			#	title = 'BBVV ('+fecha+')'

					############################################################



	_columns = {
		'type_slip' : fields.many2one("becados.tiponomina", "Nómina", required = True),
		'class_personal' : fields.many2one("becados.clasper", "Personal", required = True),
		'random_slip' : fields.char(string="Nómina", size=100, required=False),
		'state': fields.selection([
            ('draft', 'Pre nómina'),
            ('close', 'Nómina'),
        ], 'Status', select=True, readonly=True),
        'class_personal' : fields.many2one("becados.clasper", "Personal", required = True,readonly=True, states={'draft': [('readonly', False)]}), # Validación, si esta en estado de nómina no pueda ser editado
        'type_slip' : fields.many2one("becados.tiponomina", "Nómina", required = True,readonly=True, states={'draft': [('readonly', False)]}), # Validación, si esta en estado de nómina no pueda ser editado
        'date_start': fields.date('Date From', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'date_end': fields.date('Date To', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'credit_note': fields.boolean('Credit Note', readonly=True, states={'draft': [('readonly', False)]}, help="If its checked, indicates that all payslips generated from here are refund payslips."),
	}

	_defaults = {
		# 'fecha': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al español

	}

class Hr_paysplip_employees(osv.Model): #Herencia del sub módulo de hr_payroll

	'''Herenciando a hr.payslip.employees (Procesamiento de nóminas, ventana emergente)'''

	_inherit = 'hr.payslip.employees'


	_columns = {
		#'type_slip' : fields.many2one("becados.tiponomina", "Nómina", required = True),
		#'class_personal' : fields.many2one("becados.clasper", "Personal", required = True),
	}

	_defaults = {
		# 'fecha': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al español
	}

