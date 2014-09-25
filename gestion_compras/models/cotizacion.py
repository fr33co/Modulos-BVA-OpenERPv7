# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
import os
from datetime import date
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
from openerp.osv import fields, osv
import math
from openerp.tools.translate import _

import pdf_class # Clase para importar las Clases de los formatos PDF' s
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

class Gestion_compras(osv.Model):
	
	_name = 'cotizacion'
	
	_order = 'proveedor'
	
	_rec_name = 'n_cotizacion'
	
	def cancelar_cotizacion(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': 'cancelado'}, context=context)
		
	def realizar_cotizacion(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': 'realizado'}, context=context)	
	
	#METODO PARA LA LECTURA DE LOS ELEMENTOS SELECCIONADOS (MATERIALES)
	
	####################################################################################################################
	def red_cotizacion(self, cr, uid, ids, item_ids, context=None):
		
		# BLOQUE DE CODIGO PARA CAPTURAR LAS COTIZACIONES NRO I
		########################################################
		
		values = {}
		
		sfl_trasmov  = self.pool.get('cotizacion.purchase.materiales') # Consultamos el modelo para la lectura de los montos
		
		line_ids_trim = pdf_class.resolve_o2m_operations(cr, uid, sfl_trasmov, item_ids, ["descripcion"], context)
		descripcion = 0
		for line_trim in line_ids_trim:
			
			#VARIABLE REFERENCIADA PARA PRECIO DE COTIZACION I
			descripcion = line_trim.get('descripcion',descripcion)
			
			if descripcion == descripcion:
				
			
				print "DISCULPE LOS ELEMENTOS DE LA DESCRIPCION SON IGUALES:"
			else:
				print "LA DESCRIPCION NO EXISTE"
			
											
			#~ values.update({
			#~ # BLOOQUE DE CODIGO PARA EL CALCULO DE LA COTIZACION I  
			#~ 'iva_one' : pdf_class.punto_decimal(str(iva_one)),
			#~ 'sub_total_one' : pdf_class.punto_decimal(str(sub_total_one)),
			#~ 'total_one' : pdf_class.punto_decimal(str(total_one)),
			#~ # BLOOQUE DE CODIGO PARA EL CALCULO DE LA COTIZACION II
			#~ 'iva_two' : pdf_class.punto_decimal(str(iva_two)),
			#~ 'sub_total_two' : pdf_class.punto_decimal(str(sub_total_two)),
			#~ 'total_two' : pdf_class.punto_decimal(str(total_two)),
			#~ # BLOOQUE DE CODIGO PARA EL CALCULO DE LA COTIZACION III
			#~ 'iva_tree' : pdf_class.punto_decimal(str(iva_tree)),
			#~ 'sub_total_tree' : pdf_class.punto_decimal(str(sub_total_tree)),
			#~ 'total_tree' : pdf_class.punto_decimal(str(total_tree)),
			#~ 
							#~ })
					##############################################################################
		
		return {'value':values}
	####################################################################################################################
	
	# METODO PARA EL ENVIO DEL FORMATO DE COTIZACION al PROVEEDOR... PARA LAS TRES COTIZACIONES EMITIDAS
	def send_cotizacion(self, cr, uid, ids, context=None):
		
		model_data = self.pool.get('ir.model.data')
		try:
		    cotizacion_id = model_data.get_object_reference(cr, uid, 'cotizacion', 'email_template_edi_gestion_compras')[1]
		except ValueError:
		    cotizacion_id = False
		try:
		    compose_form_id = model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
		except ValueError:
		    compose_form_id = False
		    
		ctx = dict(context)
		ctx.update({
		    'default_model': 'cotizacion',
		    'default_res_id': ids[0],
		    'default_use_template': bool(cotizacion_id),
		    'default_template_id': cotizacion_id,
		    'default_composition_mode': 'comment',
		})
		return {
		    'type': 'ir.actions.act_window',
		    'view_type': 'form',
		    'view_mode': 'form',
		    'res_model': 'mail.compose.message',
		    'views': [(compose_form_id, 'form')],
		    'view_id': compose_form_id,
		    'target': 'new',
		    'context': ctx,
		}
	
	# PROCESO DE NUMERO DE COTIZACION
	def _numero_cotizacion(self, cr, uid, ids, context = None):
		
		ano         = time.strftime('%y') # Elemento para la captura de año actual del servidor			
		cr.execute("SELECT count(*) as n_cotizacion FROM cotizacion") # Consultamos a la base purchase_request
		num_orden   = cr.fetchone()[0]
		correlativo = str(num_orden+1).zfill(4)
		return correlativo
	
	##########################################################
	def generar_cotizacion(self, cr, uid, ids, context=None):
		
		# Instancia de la clase heredada L es horizontal y P es vertical
		pdf=pdf_class.Cotizacion_proveedor(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA
		
		pdf.set_author('Ing .:Jesús Laya:.')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		pdf.set_font('Arial','B',15)
		pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		
		pdf.set_fill_color(255,255,255)
		pdf.set_font('Arial','B',8)
		
		# ITERAMOS SOBRE EL OBJETO A CONSULTAR LOS DATOS
		
		for modelo in self.browse(cr, uid, ids, context=None):
			direccion   = modelo.direccion
			cotizacion  = modelo.n_cotizacion
			fecha_orden = pdf_class.fecha(modelo.fecha_orden)
			unidad      = modelo.unidad.name
			id_fill     = modelo.id
			item        = modelo.item
		
		
		pdf.set_y(35)
		pdf.set_x(82.5)
		pdf.set_font('Arial','B',8)
		pdf.write(30,"SOLICITUD DE COTIZACION".decode("UTF-8"))
		
		pdf.set_y(36)
		pdf.set_x(10)
		pdf.multi_cell(187,5,"Dirección: ".decode("UTF-8")+pdf_class.acento(direccion),'LTBR',0,'C',0)
		pdf.ln(15)
		
		#Encabezado
		pdf.cell(150,5,"COTIZACIÓN N° :".decode("UTF-8")+cotizacion,'LTBR',0,'L',0)
		pdf.cell(37,5,"Fecha: "+fecha_orden,'LTBR',0,'C',0)
		
		pdf.set_y(65)
		pdf.set_x(10)
		pdf.multi_cell(187,5,"UNIDAD SOLICITANTE ",'LTBR',0,'C',0)
		
		pdf.set_y(70)
		pdf.set_x(10)
		pdf.multi_cell(187,5,"DENOMINACIÓN: ".decode("UTF-8")+pdf_class.acento(unidad),'LTBR',0,'C',0)
		
		
		pdf.ln(5)
		
		pdf.set_font('Arial','B',8)
		pdf.cell(10,5,"ITEM".decode("UTF-8"),'LTBR',0,'C',0)
		pdf.cell(18.75,5,"CANTIDAD".decode("UTF-8"),'LTBR',0,'C',0)
		pdf.cell(25,5,"PRESENTACIÓN".decode("UTF-8"),'LTBR',0,'C',0)
		pdf.cell(133.5,5,"DESCRIPCIÓN".decode("UTF-8"),'LTBR',0,'C',0)
		
		# SE REALIZA EL PROCESO DE ITERACION DE ONE2MANY DE LA LISTA DE MATERIALES / PRODUCTOS SOLICITADOS
		
		#PROCESO DE VALIDACION AL MOMENTO DEL PEDIDO DE LOS PRODUCTOS SOLICITADOS Y O MATERIALES
		
		# PARA PEDIDO DE LIMPIEZA / PAPELERIA
		if str(item) == "limpieza" or str(item) == "papeleria":
						
			solicitud     = self.pool.get('cotizacion.purchase.materiales') # Objeto hr_employee (Empleado)
			search_s      = solicitud.search(cr, uid, [('materiales_id','=',id_fill)], context=None) # Se busca el ID dado
			s             = solicitud.read(cr,uid,search_s,context=context)
			datos         = len(s)
		
			# ITERAMOS SOBRE EL MODELO A CONSULTAR PARA LA LISTA
			i = 1
			for x in s:
				cantidad    = x['cantidad'] # Cantidad
				unidad_s    = x['unidad'][1] # Unidad
				descripcion = x['descripcion'][1] # Descripcion del material y o / Productos
				
				if datos == 12:
					pdf.add_page()
					pdf.set_y(36)
					pdf.set_x(10)
					pdf.multi_cell(187,5,"Dirección: ".decode("UTF-8")+pdf_class.acento(direccion),'LTBR',0,'C',0)
					pdf.ln(15)
					
					#Encabezado
					pdf.cell(150,5,"COTIZACIÓN N° :".decode("UTF-8")+cotizacion,'LTBR',0,'L',0)
					pdf.cell(37,5,"Fecha: "+fecha_orden,'LTBR',0,'C',0)
					
					pdf.set_y(65)
					pdf.set_x(10)
					pdf.multi_cell(187,5,"UNIDAD SOLICITANTE ",'LTBR',0,'C',0)
					
					pdf.set_y(70)
					pdf.set_x(10)
					pdf.multi_cell(187,5,"DENOMINACIÓN: ".decode("UTF-8")+pdf_class.acento(unidad),'LTBR',0,'C',0)
			
					pdf.ln(5)
			
					pdf.set_font('Arial','B',8)
					pdf.cell(10,5,"ITEM".decode("UTF-8"),'LTBR',0,'C',0)
					pdf.cell(18.75,5,"CANTIDAD".decode("UTF-8"),'LTBR',0,'C',0)
					pdf.cell(25,5,"PRESENTACIÓN".decode("UTF-8"),'LTBR',0,'C',0)
					pdf.cell(133.5,5,"DESCRIPCIÓN".decode("UTF-8"),'LTBR',0,'C',0)
					
				pdf.ln(5)
				pdf.set_font('Arial','',8)
				pdf.cell(10,5,str(i),'LTBR',0,'C',0)
				pdf.cell(18.75,5,cantidad,'LTBR',0,'C',0)
				pdf.cell(25,5,unidad_s,'LTBR',0,'C',0)
				pdf.cell(133.5,5,pdf_class.acento(descripcion),'LTBR',0,'C',0)
				
				i = i + 1
						
		pdf.set_y(228)
		
		pdf.set_font('Arial','B',8)
		pdf.write(30,"Elaborado por:  _______________________".decode("UTF-8"))
		
		dia = time.strftime('%d')
		mes = time.strftime('%B')
		ano = time.strftime('%Y')
		fecha = dia+" de "+mes+" "+ano
			
			
		title = 'Cotizacion nro '.decode("UTF-8")+cotizacion+" Unidad Solictante "+pdf_class.acento(unidad)+" "+fecha+'.pdf'
		pdf.output('openerp/addons/gestion_compras/reportes/cotizaciones/'+title,'F') # Salida del documento
		open_document = open('openerp/addons/gestion_compras/reportes/cotizaciones/'+title) # Apertura del documento
		#########################################################################
		
		# Guardamos el archivo pdf en adjunto.documento
		id_att = self.pool.get('adjunto.documento').create(cr, uid, {
			'name': title,
			'res_name': title,
			'datas': base64.encodestring(open_document.read()),
			'datas_fname': title,
			'res_model': 'control.perceptivo',
			'description': "Control Perceptivo",
			'item': "",
			}, context=context)
		
		return id_att
	##########################################################
		
	_columns = {
		######################################################################################
		# GESTION DE Compra
		######################################################################################
		'proveedor' : fields.many2one("res.partner", "Proveedor", required = True),
		'fecha_orden' : fields.date(string="Fecha de Orden", required=True),
		'referencia_proveedor' : fields.char(string="Actividad", size=256, required=True),
		'status' : fields.selection([('borrador','OC en Borrador'),('enviado','Petición de Cotización enviada'),('realizado','Realizado'),('cancelado','Cancelado')], string="Acción", required=False),
		'user': fields.many2one('res.users', 'Registrado por:', readonly=True), # Usuario logeado
		'direccion' : fields.text(string='Direccion', required=True),
		'n_cotizacion' : fields.char(string="Numero de Cotizacion", size=25, required=True),
		'unidad' : fields.many2one("stock.location", "Unidad Solicitante", required = True),
		'tlf' :  fields.char(string="Telefono", size=14, required=False),
		'item' : fields.selection([('limpieza','Limpieza'),('servicios','Servicios Generales'),('papeleria','Papelería'),('tecnologico','Tecnológico'),('otros','Otros')], string="Tipo de Material", required=True),
		'material_ids': fields.one2many('cotizacion.purchase.materiales', 'materiales_id', string='Materiales Limpieza / Papelería'), # LISTA DE MATERAILES (LIMPIEZA/ PAPELERIA / OTROS)
		#~ 'material_p_ids': fields.one2many('cotizacion.purchase.s.p.t', 'materiales_p_id', string='Productos Servicios / Tecnológico'),
		######################################################################################
	}
	
	_defaults = {
		'status' : "borrador",
		'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
		'direccion' : 'Avenida Sucre Complejo Cultural Santos Michelena Edif Bibliotecas Virtuales, Maracay Edo Aragua',
		'n_cotizacion' : _numero_cotizacion, # Default numero de cotizacion
		'fecha_orden' : lambda *a: time.strftime("%Y-%m-%d"),
	}
	
# Clase para los materiales de compras (Solicitud Directa)

class solicitud_material(osv.Model):

	_name = "cotizacion.purchase.materiales"
	
	# Metodo para traer las especificaciones de los materiales
	def search_materiales(self, cr, uid, ids, argument_search, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('materiales.almacen')
		#~ alm    = self.pool.get('cotizacion.purchase.materiales')
		
		for x in self.browse(cr, uid, ids, context=None):
			print "ID DEL MODELO: "+str(x.id)
		
		#~ #======================== Busqueda por código ============================
#~ 
		#~ search_obj_code = obj_dp.search(cr, uid, [('id','=',argument_search)])
#~ 
		#~ datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		#~ 
		#~ #=========================================================================
		#~ if not datos_code:
			#~ 
			#~ values.update({
				#~ 
				#~ 'tipo' : None,
				#~ 'unidad' : None,
				#~ })
		#~ 
		#~ else:
			#~ 
			#~ values.update({
				#~ 
				#~ 'tipo' : datos_code[0]['t_materiales'],
				#~ 'unidad' : datos_code[0]['unidad'],
				#~ })
		#~ 
		#~ return {'value' : values}
		
	
		
	#~ _sql_constraints = [('unique_descripcion', 'unique(descripcion)', 'Disculpe tiene uno (1) o más Materiales Repetidos')]
	
	# COLUMNAS PARA LA LISTA DE MATERIALES DE SOLICITUD
	_columns = {
		'materiales_id':fields.many2one('cotizacion', 'material_ids', ondelete='cascade', select=False),
		'cantidad' : fields.char(string="Cantidad", required=True),
		'tipo' : fields.selection((('1','Limpieza'), ('2','Oficina'), ('3','Servicios Generales'), ('4','Tecnológico')),'Tipo de Material', required=False),
		'descripcion':fields.many2one('materiales.almacen', 'Descripción del Material',required=True),
		'unidad' : fields.many2one('product.uom', 'Unidad de Medida', required=True),
		'modelo' : fields.char(string="Modelo", required=False),
		'marca'  : fields.char(string="Marca", required=True),
		'foto_referencial' : fields.binary("Foto Referencial",help="Foto Referencial"),
	}
	
	
	
