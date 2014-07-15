# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from time import gmtime, strftime
from datetime import date
from datetime import datetime, timedelta
from openerp.osv import fields, osv
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
import math

_logger = logging.getLogger(__name__)

class Integrante(osv.Model):
	
	_name = 'integrantes.ubch'
	
	_rec_name = 'nombre_apellido'
	
	_order = 'nombre_apellido'
	
	#-----------------------------------------------------------------------------------------------
	#~ Función para validar si un integrante ya ha sido registrado
	def datos_integrante(self, cr, uid, ids, cedula, context=None):
		valores = {}
		
		if not cedula:
			return valores
			
		#Preparación de los modelos donde se realizarán las búsquedas
		modelo1 = self.pool.get('integrantes.ubch')
		
		#Ejecución de las búsquedas
		busqueda1 = modelo1.search_count(cr, uid, [('cedula','=',cedula)])
		
		if busqueda1 > 0:
			#Si se cumple esta condición es porque ha sido seleccionado, entonces procedemos 
			#a traer sus datos desde el otro modelo 
			busqueda2 = modelo2.search_count(cr, uid, [('cedula','=',cedula)])
			
			if busqueda2 > 0:
				busqueda2 = modelo2.search(cr, uid, [('cedula','=',cedula)])
				busqueda_leer = modelo2.read(cr, uid, busqueda2, context=context)
				
				#Carga de los datos que necesitamos
				valores.update({
					'name' : busqueda_leer[0]['solicitante'],
					'correo' : busqueda_leer[0]['email'],
					'tlf_local' : busqueda_leer[0]['telefono'],
					'tlf_movil' : busqueda_leer[0]['movil'],
					'grado_instruccion' : busqueda_leer[0]['grado_instruc'],
					'direccion' : busqueda_leer[0]['direccion'],
					'sede' : busqueda_leer[0]['sede'],
				})
				
				return {'value':valores}
	
	
	"""
	Metodo con el cual genero el archivo .pdf 
	"""
    
	def reporte_integrantes(self, cr, uid, ids, context=None): # Generacion de inventario
    
		# Instancia de la clase heredada L es horizontal y P es vertical
		# format A4, A3 o letter que son los formatos de la hoja (oficio, carta, etc)
	
		pdf=class_pdf.PDF(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA
		
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
		pdf.set_line_width(0.25)
		
		integrantes_ubch = self.browse(cr, uid, ids, context=context)
		correo = ""
		grado_inst = ""
		fijo = ""
		sector = ""
		experiencia = ""
		profesion = ""
		ocupacion = ""
		c_votacion = ""
		parentesco = ""
		si = ""
		no = ""
		ente_no = ""
		ente_si = ""
		vincu = ""
		resp = ""
		ota_resp = ""
		mision = ""
		consejo = ""
		otro_ente = ""
		valoracion = ""
		for y in integrantes_ubch:
			#Información general---------------------------------------------
			nombre = y.nombre_apellido.encode("UTF-8").decode("UTF-8")
			edad = y.edad
			if int(y.nacionalidad) == 1:
				nacio = "Venezolana"
			else:
				nacio = "Extrangera"
			ci = y.cedula
			if y.centro_votacion == False:
				c_votacion = ""
			else:
				c_votacion = y.centro_votacion.centro.encode("UTF-8").decode("UTF-8")	
			
			if int(y.estado_civil) == 1:
				civil = "Soltero"
			elif int(y.estado_civil) == 2:
				civil = "Casado"
			elif int(y.estado_civil) == 3:
				civil = "Concubinato"
			elif int(y.estado_civil) == 4:
				civil = "Unión de hechos estables"
			if y.grado_instruc.grado_instruc is None:
				grado_inst = ""
			else:
				grado_inst = y.grado_instruc.grado_instruc.encode("UTF-8").decode("UTF-8")	
				
			direc = y.direccion.encode("UTF-8").decode("UTF-8")
			
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',14)
			pdf.cell(190,7,"INFORMACIÓN INTEGRANTES UBCH".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_fill_color(199,15,15)
			pdf.set_text_color(255,255,255)
			pdf.set_font('Arial','B',10)
			pdf.cell(190,5,"INFORMACIÓN GENERAL (INTEGRANTE UBCH)".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			
			pdf.set_font('Arial','B',9)
			pdf.cell(35,35,"FOTO".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.set_y(22)
			pdf.set_x(49)
			pdf.set_font('Arial','B',9)
			pdf.cell(45,5,"NOMBRE Y APELLIDO".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',9)
			pdf.cell(106,5,nombre,'LTBR',1,'L',1)
			pdf.set_y(27)
			pdf.set_x(49)
			pdf.set_font('Arial','B',9)
			pdf.cell(45,5,"NACIONALIDAD".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',9)
			pdf.cell(106,5,nacio.decode("UTF-8"),'LTBR',1,'L',1)
			pdf.set_y(32)
			pdf.set_x(49)
			pdf.set_font('Arial','B',9)
			pdf.cell(45,5,"EDAD".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',9)
			pdf.cell(106,5,str(edad),'LTBR',1,'L',1)
			pdf.set_y(37)
			pdf.set_x(49)
			pdf.set_font('Arial','B',9)
			pdf.cell(45,5,"CÉDULA DE IDENTIDAD".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',9)
			pdf.cell(106,5,str(ci),'LTBR',1,'L',1)
			pdf.set_y(42)
			pdf.set_x(49)
			pdf.set_font('Arial','B',9)
			pdf.cell(45,5,"CENTRO ELECTORAL".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',9)
			pdf.cell(106,5,c_votacion,'LTBR',1,'L',1)
			pdf.set_y(47)
			pdf.set_x(49)
			pdf.set_font('Arial','B',9)
			pdf.cell(45,5,"ESTADO CIVIL".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',9)
			pdf.cell(106,5,str(civil).decode("UTF-8"),'LTBR',1,'L',1)
			pdf.set_y(52)
			pdf.set_x(49)
			pdf.set_font('Arial','B',9)
			pdf.cell(45,5,"GRADO DE INSTRUCCIÓN".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',9)
			pdf.cell(106,5,grado_inst,'LTBR',1,'L',1)
			
			
			#Información de residencia-------------------------------------------------
			pdf.ln(5)
			pdf.set_fill_color(199,15,15)
			pdf.set_text_color(255,255,255)
			pdf.set_font('Arial','B',10)
			pdf.cell(190,5,"RESIDENCIA".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			
			estado = y.estado.name.encode("UTF-8").decode("UTF-8")
			municipio = y.municipio.name.encode("UTF-8").decode("UTF-8")
			parroquia = y.parroquia.name.encode("UTF-8").decode("UTF-8")
			if y.sector == False:
				sector = ""
			else:
				sector = y.sector.encode("UTF-8").decode("UTF-8")
			comuna = y.comuna.encode("UTF-8").decode("UTF-8")
			direccion = y.direccion.encode("UTF-8").decode("UTF-8")
			
			if y.tlf_fijo == False:
				fijo = ""
			else:
				fijo = y.tlf_fijo.encode("UTF-8").decode("UTF-8")
				
			movil = y.tlf_movil.encode("UTF-8").decode("UTF-8")
			
			if y.correo == False:
				correo = ""
			else:
				correo = y.correo.encode("UTF-8").decode("UTF-8")
			
			pdf.set_font('Arial','B',9)
			pdf.cell(16,5,"ESTADO".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(25,5,estado,'LTBR',0,'L',1)
			pdf.set_font('Arial','B',9)
			pdf.cell(20,5,"MUNICIPIO".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(50,5,municipio,'LTBR',0,'L',1)
			pdf.set_font('Arial','B',9)
			pdf.cell(22,5,"PARROQUIA".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(57,5,parroquia,'LTBR',1,'L',1)
			
			pdf.set_font('Arial','B',9)
			pdf.cell(16,5,"SECTOR".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(80,5,sector,'LTBR',0,'L',1)
			pdf.set_font('Arial','B',9)
			pdf.cell(17,5,"COMUNA".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(77,5,sector,'LTBR',1,'L',1)
			pdf.set_font('Arial','B',9)
			pdf.cell(190,5,"DIRECCIÓN".decode("UTF-8"),'LTR',1,'L',1)
			pdf.set_font('Arial','',8)
			pdf.multi_cell(190,5,direccion,'LBR','J',1)
			
			pdf.set_font('Arial','B',9)
			pdf.cell(28,5,"TELÉFONO FIJO".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(20,5,fijo,'LTBR',0,'L',1)
			pdf.set_font('Arial','B',9)
			pdf.cell(36,5,"TELÉFONO CELULAR".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(20,5,movil,'LTBR',0,'L',1)
			pdf.set_font('Arial','B',9)
			pdf.cell(26,5,"CORREO ELEC".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(60,5,correo,'LTBR',1,'L',1)		
	
			pdf.ln(5)
			pdf.set_fill_color(199,15,15)
			pdf.set_text_color(255,255,255)
			pdf.set_font('Arial','B',10)
			pdf.cell(190,5,"OCUPACIÓN".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			
			if not y.profesion:
				profesion = ""
			else:
				profesion = y.profesion.profesion.encode("UTF-8").decode("UTF-8")
			if not y.ocupacion:
				ocupacion = ""
			else:
				ocupacion = y.ocupacion.ocupacion.encode("UTF-8").decode("UTF-8")
			if not y.experiencia:
				experiencia = ""
			else:
				experiencia = y.experiencia.encode("UTF-8").decode("UTF-8")
			
			pdf.set_font('Arial','B',9)
			pdf.cell(22,5,"PROFESIÓN".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(66,5,profesion,'LTBR',0,'L',1)
			pdf.set_font('Arial','B',9)
			pdf.cell(36,5,"OCUPACIÓN ACTUAL".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(66,5,ocupacion,'LTBR',1,'L',1)
			pdf.set_font('Arial','B',9)
			pdf.cell(45,5,"TIEMPO DE EXPERIENCIA".decode("UTF-8"),'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(15,5,experiencia,'LTBR',1,'L',1)
			
			pdf.ln(5)
			pdf.set_fill_color(199,15,15)
			pdf.set_text_color(255,255,255)
			pdf.set_font('Arial','B',10)
			pdf.cell(190,5,"GRUPO FAMILIAR".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_font('Arial','B',7)
			pdf.cell(18,5,"PARENTESCO".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(15,5,"CÉDULA".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(30,5,"NOMBRE Y APELLIDO".decode("UTF-8"),'LBTR',0,'C',1)
			pdf.cell(16,5,"TELÉFONO".decode("UTF-8"),'LBTR',0,'C',1)
			pdf.cell(8, 5,"EDAD".decode("UTF-8"),'LTB',0,'C',1)
			pdf.cell(35, 5,"OCUPACIÓN".decode("UTF-8"),'LTB',0,'C',1)
			pdf.cell(28, 5,"SITUACIÓN MEDICA".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(40, 5,"OBSERVACIÓN ".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			
			data_ids = self.read(cr, uid, ids, context=context)[0]
			payslip_id = data_ids['familiar'] # Grupo de IDS
		
			grupo_familiar = self.pool.get('grupo.familiar') # Objeto 
			datos = grupo_familiar.search(cr, uid, [('id','=',payslip_id)], context=None)
			familia = grupo_familiar.read(cr,uid,datos,context=context)
			#observacion = ""
			#ocupacion = ""
			#situacion = ""
			for i in familia:
				if int(i['parentesco']) == 1:
					parentesco = "Padre"
				elif int(i['parentesco']) == 2:
					parentesco = "Madre"
				elif int(i['parentesco']) == 3:
					parentesco = "Conyugue"
				elif int(i['parentesco']) == 4:
					parentesco = "Hijo(a)"
				
				cedula_fam = i['cedula']
				nombre_fam = i['nombre_apellido'].encode("UTF-8").decode("UTF-8")
				telefono = i['telefono']
				edad = i['edad']
				if not i['ocupacion']:
					ocupacion = ""
				else:
					ocupacion = i['ocupacion'][1].encode('UTF-8').decode('UTF-8')
				if not i['situacion_medica']:
					situacion = ""
				else:
					situacion = i['situacion_medica'].encode('UTF-8').decode('UTF-8')
				if not i['observacion']:
					observacion = ""
				else:
					observacion = i['observacion'].encode('UTF-8').decode('UTF-8')
				
				pdf.cell(18,4,str(parentesco),'LTBR',0,'C',1)
				pdf.cell(15,4,str(cedula_fam),'LTBR',0,'C',1)
				pdf.cell(30,4,nombre_fam,'LBTR',0,'C',1)
				pdf.cell(16,4,str(telefono),'LBTR',0,'C',1)
				pdf.cell(8, 4,str(edad),'LTB',0,'C',1)
				pdf.cell(35, 4,ocupacion,'LTB',0,'C',1)
				pdf.cell(28, 4,situacion,'LTBR',0,'C',1)
				pdf.cell(40, 4,observacion,'LTBR',1,'C',1)
			
			pdf.ln(5)
			pdf.set_fill_color(199,15,15)
			pdf.set_text_color(255,255,255)
			pdf.set_font('Arial','B',10)
			pdf.cell(190,5,"ACTIVIDADES".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_fill_color(191,191,191)
			pdf.set_text_color(24,29,31)
			
			if y.vinculacion == False:
				vincu = ""
			else:
				vincu = y.vinculacion.encode("UTF-8").decode("UTF-8")
			if y.militancia_psuv == True:
				si = "X"
			else:
				si = ""
			if y.militancia_psuv == False:
				no = "X"
			else:
				no = ""
			if y.responsabilidad == False:
				resp = ""
			else:
				resp = y.responsabilidad.encode("UTF-8").decode("UTF-8")
			
				
			pdf.set_font('Arial','B',9)
			pdf.cell(75,5,"VINCULACION CON EL PRESENTE PROYECTO".decode("UTF-8"),'LTBR',1,'L',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.set_font('Arial','',8)
			pdf.cell(190,5,vincu,'B',1,'L',1)
			pdf.set_font('Arial','B',9)
			pdf.cell(37,5,"MILITANTE DEL PSUV".decode("UTF-8"),'',0,'L',1)
			pdf.cell(5,5,"SI".decode("UTF-8"),'',0,'L',1)
			pdf.cell(5,4,si,'LTBR',0,'C',1)
			pdf.cell(6,5,"NO".decode("UTF-8"),'',0,'L',1)
			pdf.cell(5,4,no,'LTBR',0,'C',1)
			pdf.cell(5,5,"",'',1,'L',1)
			pdf.cell(75,5,"OTRA RESPONSABILIDAD DENTRO DEL PSUV".decode("UTF-8"),'',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(115, 5,resp,'B',1,'L',1)
			
			if y.consejo_cumunal == True:
				consejo_si = "X"
			else:
				consejo_si = ""
			if y.consejo_cumunal == False:
				consejo_no = "X"
			else:
				consejo_no = ""
			if y.otra_responsabilidad == False:
				ota_resp = ""
			else:
				ota_resp = y.otra_responsabilidad.encode("UTF-8").decode("UTF-8")
			
			
			
			pdf.ln(5)
			pdf.set_font('Arial','B',9)
			pdf.cell(72,5,"PERTENECE A ALGUN CONSEJO COMUNAL".decode("UTF-8"),'',0,'L',1)
			pdf.cell(5,5,"SI".decode("UTF-8"),'',0,'L',1)
			pdf.cell(5,4,consejo_si,'LTBR',0,'C',1)
			pdf.cell(6,5,"NO".decode("UTF-8"),'',0,'L',1)
			pdf.cell(5,4,consejo_no,'LTBR',0,'C',1)
			pdf.cell(2,5,"".decode("UTF-8"),'',1,'L',1)
			pdf.cell(50,5,"RESPONSABILIDAD EN EL C.C.".decode("UTF-8"),'',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(140,5,ota_resp,'B',1,'L',1)

			if y.mision_beneficio == False:
				mision = ""
			else:
				for misiones in y.mision_beneficio:
					mision = mision + misiones.mision.encode("UTF-8").decode("UTF-8") + ", "
				mision = mision[0:-2]
				
			pdf.ln(5)
			pdf.set_fill_color(191,191,191)
			pdf.set_text_color(24,29,31)
			pdf.set_font('Arial','B',9)
			pdf.cell(100,5,"MISIONES SOCIALES POR LAS CUALES SE HA BENEFIACIADO".decode("UTF-8"),'LTBR',1,'L',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.set_font('Arial','',8)
			pdf.cell(190,5,mision,'B',1,'L',1)
			
			if not y.nombre_consejo:
				consejo = ""
			else:
				consejo = y.nombre_consejo.consejo_comunal.encode("UTF-8").decode("UTF-8")
			pdf.ln(5)
			pdf.set_fill_color(191,191,191)
			pdf.set_text_color(24,29,31)
			pdf.set_font('Arial','B',9)
			pdf.cell(58,5,"NOMBRE DEL CONSEJO COMUNAL".decode("UTF-8"),'LTBR',1,'L',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.set_font('Arial','',8)
			pdf.cell(190,5,consejo,'B',1,'L',1)
			
			if y.otro_ente == True:
				otro_si = "X"
			else:
				otro_si = ""
			if y.otro_ente == False:
				otro_no = "X"
			else:
				otro_no = ""
			if y.otro_ente_desc == False:
				otro_ente = ""
			else:
				otro_ente = y.otro_ente_desc.encode("UTF-8").decode("UTF-8")
			
			pdf.ln(5)
			pdf.set_fill_color(191,191,191)
			pdf.set_text_color(24,29,31)
			pdf.set_font('Arial','B',9)
			pdf.cell(155,5,"PERTENECE A ALGUNA OTRA ORGANIZACIÓN, FRENTE, ENTE, ENTRE OTROS (MENCIONE CUAL)".decode("UTF-8"),'LTBR',0,'L',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.cell(5,5,"SI".decode("UTF-8"),'L',0,'L',1)
			pdf.cell(5,4,otro_si,'LTBR',0,'C',1)
			pdf.cell(6,5,"NO".decode("UTF-8"),'',0,'L',1)
			pdf.cell(5,4,otro_no,'LTBR',1,'C',1)
			pdf.set_font('Arial','',8)
			pdf.cell(190,5,otro_ente,'B',1,'L',1)
			
			if y.valoracion_politica == False:
				valoracion = ""
			else:
				valoracion = y.valoracion_politica.encode("UTF-8").decode("UTF-8")
				
			pdf.ln(5)
			pdf.set_fill_color(199,15,15)
			pdf.set_text_color(255,255,255)
			pdf.set_font('Arial','B',10)
			pdf.cell(190,5,"VALORACIÓN POLÍTICA".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.set_font('Arial','',8)
			pdf.multi_cell(190,5,valoracion,'LTBR','J',1)
			
			nom = nombre+'.pdf'
			#Ruta local
			#~ pdf.output('openerp/addons/integrantes_ubch/reportes/constancias/'+nom,'F')
			#~ archivo = open('openerp/addons/integrantes_ubch/reportes/constancias/'+nom)
			#Ruta servidor
			pdf.output('/home/administrador/openerp70/modules/integrantes_ubch/reportes/'+nom,'F')
			archivo = open('/home/administrador/openerp70/modules/integrantes_ubch/reportes/'+nom)
			
			#Registro del archivo de reporte en la base de datos
			id_att = self.pool.get('ir.attachment').create(cr, uid, {
				'integrante_id': y.id, 
				'name': nom,
				'res_name': nom,
				#~ 'municipio' : municipio,
				'datas': base64.encodestring(archivo.read()),
				'datas_fname': nom,
				'res_model': 'integrantes.ubch',
			}, context=context)
			
	
	_columns = {
		#Información general-----------------------------------------------------------------
		'foto' : fields.binary("",help="Foto del integrante"),
		'nombre_apellido' : fields.char(string="Nombre y Apellido", size=50, required=True),
		'nacionalidad' : fields.selection((('1','Venezolana'),('2','Extranjera')), "Nacionalidad", required=True),
		'edad' : fields.integer(string="Edad", size = 3, required=True),
		'cedula' : fields.char(string="Cédula", size = 9, required=True),
		'centro_votacion' : fields.many2one("integrante.centroelectoral", "Centro de votación", required=True),
		'estado_civil' : fields.selection((('1','Soltero'),('2','Casado'),('3','Concubinato'),('4','Unión de hechos estables')), "Estado Civil", required=True),
		'grado_instruc' : fields.many2one("integrante.gradoinstruccion", "Grado de Instrucción", required = False),
		'discapacidad' : fields.selection((('1','Sí'),('2','No')),"¿Posee alguna discapacidad?", required = True),
		'tipo_discapacidad' : fields.selection((('1','Visual'),('2','Auditiva'),('3','Física'),('4','Psíquica'),('5','Multisensorial')),"Tipo de discapacidad",required=False),
		'sexo' : fields.selection((('1','Femenino'),('2','Masculino')), "Sexo", required = True),
		#Información de residencia
		'country_id' : fields.many2one("res.country", "País", required=True),
		'estado' : fields.many2one("res.country.state", "Estado", required = True, select="0"),
		'municipio' : fields.many2one("res.country.municipality", "Municipio", required = True, select="0"),
		'parroquia' : fields.many2one("res.country.parish", "Parroquia", required = True, select="0"),
		'sector' : fields.char(string="Sector", size = 50, required=False),
		'direccion' : fields.char(string="Dirección", size = 256, required=True),
		'comuna' : fields.char(string="Comuna", size = 50, required=True),
		'tlf_fijo' : fields.char(string="Teléfono Fijo", size = 11, required=False),
		'tlf_movil' : fields.char(string="Teléfono Movil", size = 11, required=True),
		'correo' : fields.char(string="Correo electrónico", size = 50, required=False),
		#Información de ocupación
		'profesion' : fields.many2one("integrante.profesion", "Profesión", required=False),
		'ocupacion' : fields.many2one("integrante.ocupacion", "Ocupación", required=False),
		'experiencia' : fields.char(string="Tiempo de experiencia", size = 100, required=False),
		#Información del grupo familiar
		'familiar' : fields.one2many("grupo.familiar","integrante",string="Carga Familiar"),
		#Información de actividades
		'vinculacion' : fields.char(string="Vinculación con el presente proyecto", size = 256, required=False),
		'militancia_psuv' : fields.boolean(string="¿Es militante del PSUV?", required=False, help="Marque la casilla si es afirmativo"),
		'otra_responsabilidad' : fields.char(string="Otra responsabilidad dentro del PSUV", size = 100, required=False),
		'consejo_cumunal' : fields.boolean(string="¿Pertenece a algún consejo comunal?", required=False, help="Marque la casilla si es afirmativo"),
		'responsabilidad' : fields.char(string="Responsabilidad en el consejo comunal", required=False),
		#~ 'mision_beneficio' : fields.char(string="Misiones sociales por las cuales se ha beneficiado", size = 256, required=False),
		'mision_beneficio' : fields.many2many("integrante.mision", "integrante_mision_rel", "integrante_id", "mision_id", "Misiones sociales por las cuales se ha beneficiado"),
		#~ 'category_ids': fields.many2many('hr.employee.category', 'employee_category_rel', 'emp_id', 'category_id', 'Tags'), #campo de muestra para adaptar el campo 'mision_beneficio'
		'nombre_consejo' : fields.many2one("integrante.consejocomunal", "Consejo comunal", required=False),
		'otro_ente' : fields.boolean(string="¿Pertenece a alguna organización, frente, ente, entre otros?", required=False, help="Marque la casilla si es afirmativo"),
		'otro_ente_desc' : fields.char(string="Mencione cual", size = 100, required=False),
		#información política
		'valoracion_politica' : fields.text(string="Valoración política", size = 200, required=False),
		#Campos extra-------------------------------------------------------------------------
		'fecha_actual' : fields.char(string="FECHA", size = 50, required=False),#Campo para formato PDF
	}
	
	_defaults = {
		'country_id' : 240,
		'estado' : 55,
		'fecha_actual': lambda *a: time.strftime("(%d) días del mes %B del año %Y"),# formato corecto al español
	}
