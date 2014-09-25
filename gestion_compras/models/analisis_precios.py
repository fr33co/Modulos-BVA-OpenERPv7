# -*- coding: utf-8 -*-


"""
Control Perceptivo
El control perceptivo debe practicarse al momento de la recepción de los bienes adquiridos, para asegurarse que el precio, calidad y cantidad correspondan con las especificaciones aprobadas en las Órdenes de Compra."""

import time # Necesario para las funciones de Fecha
import os
from datetime import date
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
from openerp.osv import fields, osv
import math
from openerp.tools.translate import _
import pdf_class # ARCHIVO PARA LA IMPORTACION DE DE LAS CLASES Y METODOS PRIVADOS
import base64 #Necesario para la generación del .txt


class Analisis_precios(osv.Model):
	
	_name = 'analisis.precios'
	
	_order = 'descripcion'
	
	_rec_name = 'elaborado'

	def generar_analisis_precios(self, cr, uid, ids, context=None):

		# RECORRIDO DEL MODELO CON SU ID RESPECTIVO
		for x in self.browse(cr, uid, ids, context=None):
			id_model              = x.id # ID DEL MODELO
			descripcion_model     = x.descripcion # OBSERVACION DE ANALISIS DE PRECIOS
			impuesto              = x.impuesto.name  # IMPUESTO
			elaborado             = x.elaborado # ENCARGADO DE LA ELABORACION DE ANALSIS DE PRECIOS
			
			# ELEMENTOS PARA IVA / PRECIO Y SUB TOTAL
			###################################################
			s_total_one    = pdf_class.decimal(x.sub_total_one)
			iva_one        = pdf_class.decimal(x.iva_one)
			total_one      = pdf_class.decimal(x.total_one)
			###################################################
			s_total_two    = pdf_class.decimal(x.sub_total_two)
			iva_two        = pdf_class.decimal(x.iva_two)
			total_two      = pdf_class.decimal(x.total_two)
			###################################################
			s_total_tree   = pdf_class.decimal(x.sub_total_tree)
			iva_tree       = pdf_class.decimal(x.iva_tree)
			total_tree     = pdf_class.decimal(x.total_tree)
			###################################################
			
			# Creamos el Formato de PDF de Analisis de Precios de los distintos Proveedores seleccionados
			#####################################################################################################
			# Instancia de la clase heredada L es horizontal y P es vertical

			pdf=pdf_class.Analisis_precios(orientation='L',unit='mm',format='letter') #HORIENTACION DE LA PAGINA

			#pdf.set_title(title)
			pdf.set_author('Jesús Laya')
			pdf.alias_nb_pages() # LLAMADA DE PAGINACION
			pdf.add_page() # AÑADE UNA NUEVA PAGINACION
			#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
			pdf.set_font('Arial','B',15)
			pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
			pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
			pdf.set_margins(13,10,10) # MARGENE DEL DOCUMENTO

			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',12)
			pdf.cell(265,5,"ANALISIS DE PRECIOS",'',1,'C',1)
			pdf.ln(15)

			# Fila de la cabezara de la tabla
			pdf.set_font('Arial','B',10)
			pdf.cell(125,5,"".decode("UTF-8"),'B',0,'C',1)
			pdf.cell(40,5,"COTIZACION 1".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(40,5,"COTIZACION 2".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(40,5,"COTIZACION 3".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.cell(10,5,"ITEM".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(85,5,"Descripción".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(15,5,"CANT.".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(15,5,"UNID.".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"PRECIO U.".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"TOTAL".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"PRECIO U.".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"TOTAL".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"PRECIO U.".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"TOTAL".decode("UTF-8"),'LTBR',1,'C',1)

			# Fin Cabezera
			pdf.set_font('Times','',10) # TAMANO DE LA FUENTE

			k    = 0
			j    = 0
			item = 0
			
			for c_one in x.item_one:
				descripcion    = c_one.descripcion.descripcion
				cantidad       = c_one.cantidad_one
				unidad         = c_one.unidad_one.name
				precio_one     = pdf_class.decimal(float(c_one.precio_one))
				sub_total_one  = pdf_class.decimal(float(c_one.sub_total_one))
				precio_two     = pdf_class.decimal(float(c_one.precio_two))
				sub_total_two  = pdf_class.decimal(float(c_one.sub_total_two))
				precio_tree    = pdf_class.decimal(float(c_one.precio_tree))
				sub_total_tree = pdf_class.decimal(float(c_one.sub_total_tree))
				
				if j == 20:
					pdf.add_page()
					pdf.set_fill_color(255,255,255)
					pdf.set_font('Arial','B',12)
					pdf.cell(265,5,"ANALISIS DE PRECIOS",'',1,'C',1)

					pdf.ln(15)
					
					pdf.set_font('Arial','B',10)
					pdf.cell(125,5,"".decode("UTF-8"),'B',0,'C',1)
					pdf.cell(40,5,"COTIZACION 1".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(40,5,"COTIZACION 2".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(40,5,"COTIZACION 3".decode("UTF-8"),'LTBR',1,'C',1)
					pdf.cell(15,5,"ITEM".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(80,5,"Descripción".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(15,5,"CANT.".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(15,5,"UNID.".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(20,5,"PRECIO U.".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(20,5,"TOTAL".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(20,5,"PRECIO U.".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(20,5,"TOTAL".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(20,5,"PRECIO U.".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(20,5,"TOTAL".decode("UTF-8"),'LTBR',1,'C',1)
					pdf.set_font('Arial','',10)
					# Fin Cabezera
					j=0
				item = int(item) + 1
				# Filas que vienen de la BD
				pdf.cell(10,5,str(item).decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(85,5,str(descripcion).decode("UTF-8"),'LTBR',0,'L',1)
				pdf.cell(15,5,str(cantidad),'LTBR',0,'C',1)
				pdf.cell(15,5,str(unidad),'LTBR',0,'C',1)
				pdf.cell(20,5,str(pdf_class.punto_decimal(str(precio_one))),'LTBR',0,'R',1)
				pdf.cell(20,5,str(pdf_class.punto_decimal(str(sub_total_one))),'LTBR',0,'R',1)
				pdf.cell(20,5,str(pdf_class.punto_decimal(str(precio_two))),'LTBR',0,'R',1)
				pdf.cell(20,5,str(pdf_class.punto_decimal(str(sub_total_two))),'LTBR',0,'R',1)
				pdf.cell(20,5,str(pdf_class.punto_decimal(str(precio_tree))),'LTBR',0,'R',1)
				pdf.cell(20,5,str(pdf_class.punto_decimal(str(sub_total_tree))),'LTBR',1,'R',1)
				
				pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
				j =j+1
			
			dia   = time.strftime('%d')
			mes   = time.strftime('%m')
			ano   = time.strftime('%Y')
			fecha_actual = dia+"/"+mes+"/"+ano # Fecha de creacion
			pdf.set_font('Times','B',10)
			pdf.cell(95,5,"".decode("UTF-8"),'LTR',0,'C',1)
			pdf.cell(30,5,"SUB-TOTAL".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(pdf_class.punto_decimal(str(s_total_one))),'LTBR',0,'R',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(pdf_class.punto_decimal(str(s_total_two))),'LTBR',0,'R',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(pdf_class.punto_decimal(str(s_total_tree))),'LTBR',1,'R',1)
			pdf.cell(95,5,"OBSERVACIONES".decode("UTF-8"),'LR',0,'C',1)
			pdf.cell(30,5,str(pdf_class.punto_decimal(str(impuesto))),'LTBR',0,'C',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(pdf_class.punto_decimal(str(iva_one))),'LTBR',0,'R',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(pdf_class.punto_decimal(str(iva_two))),'LTBR',0,'R',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(pdf_class.punto_decimal(str(iva_tree))),'LTBR',1,'R',1)
			pdf.cell(95,5,"".decode("UTF-8"),'LBR',0,'C',1)
			pdf.cell(30,5,"TOTAL".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(pdf_class.punto_decimal(str(total_one))),'LTBR',0,'R',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(pdf_class.punto_decimal(str(total_two))),'LTBR',0,'R',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(pdf_class.punto_decimal(str(total_tree))),'LTBR',1,'R',1)

			pdf.set_font('Times','B',10)
			pdf.cell(165,5,"".decode("UTF-8"),'LTR',0,'L',1)
			pdf.cell(80,5,"",'LTR',1,'L',1)
			pdf.set_font('Times','',10)
			#~ pdf.set_x(50)
			
			pdf.multi_cell(165,5,pdf_class.acento(descripcion_model)+"",'LR','L',1)
			pdf.set_x(178)
			pdf.set_font('Times','B',10)
			pdf.cell(165,5,"Elaborado por: "+str(elaborado)+"".decode("UTF-8"),'LR',0,'L',1)
			#~ pdf.cell(165,5,"",'LR',0,'L',1)
			pdf.set_font('Times','B',10)
			pdf.cell(150,5,"",'LR',1,'L',1)
			pdf.set_font('Times','',10)
			pdf.cell(165,5,"".decode("UTF-8"),'LR',0,'L',1)
			pdf.set_font('Times','B',10)
			pdf.cell(80,5,"Fecha: "+str(fecha_actual),'LR',1,'L',1)
			pdf.set_font('Times','B',10)
			pdf.cell(165,5,"".decode("UTF-8"),'LBR',0,'L',1)
			pdf.cell(80,5,"Unidad de Compras".decode("UTF-8"),'LBR',1,'L',1)
			
			
			
			dia = time.strftime('%d')
			mes = time.strftime('%B')
			ano = time.strftime('%Y')
			fecha = dia+" de "+mes+" "+ano
			
			
			title = 'Analisis de Precios ('+fecha+').pdf'
			pdf.output('openerp/addons/gestion_compras/reportes/analisis_precios/'+title,'F') # Salida del documento
			open_document = open('openerp/addons/gestion_compras/reportes/analisis_precios/'+title) # Apertura del documento
			#######################################################################################################
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
			#######################################################################################################
		
	# METODO GLOBAL PARA CONTABILIZAR LOS PRECIOS DE LAS COTIZACIONES DEL PROVEEDOR
	#########################################################################################################
	def total_cotizacion(self, cr, uid, ids, elemento,item_ids, context=None):
		
		# VARIABLES INICIALIZADAS
		iva           = 0.00
		sub_total     = 0.0
		total         = 0.0
		values        = {}
		precio_one    = 0.00
		precio_two    = 0.00
		precio_tree   = 0.00
		
		#ITERAMOS SOBRE EL MODELO A CONSULTAR
		impuesto = 0
		imp_iva  = 0
		for x in self.browse(cr, uid, ids, context=None):
			impuesto = x.impuesto
			print "IMPUESTO: "+str(impuesto)
		
		if int(impuesto) == 0:
			imp_iva = 12
		if int(impuesto) == 1:
			imp_iva = 12
		if int(impuesto) == 2:
			imp_iva = 8
		if int(impuesto) == 3:
			imp_iva = 0
		
                # BLOQUE DE CODIGO PARA CAPTURAR LAS COTIZACIONES NRO I
                ########################################################
                if int(elemento) == 1:
                
                    sfl_trasmov  = self.pool.get('cotizacion.proveedor.one') # Consultamos el modelo para la lectura de los montos
                    
                    line_ids_trim = pdf_class.resolve_o2m_operations(cr, uid, sfl_trasmov, item_ids, ["precio_one","precio_two","precio_tree"], context)
                    
                    for line_trim in line_ids_trim:
						#VARIABLE REFERENCIADA PARA PRECIO DE COTIZACION I
                        precio_one   += line_trim.get('precio_one',precio_one)
                        #VARIABLE REFERENCIADA PARA PRECIO DE COTIZACION II
                        precio_two   += line_trim.get('precio_two',precio_two)
                        #VARIABLE REFERENCIADA PARA PRECIO DE COTIZACION III
                        precio_tree   += line_trim.get('precio_tree',precio_tree)
                        
                    # BLOOQUE DE CODIGO PARA EL CALCULO DE LA COTIZACION I  
                    sub_total_one = float(precio_one)
                    iva_one = float(precio_one) * imp_iva / int(100) # Obtengo el precio de tipo float de cada item ingresado por monto
                    total_one = sub_total_one + iva_one
                    #################################################################
                    # BLOOQUE DE CODIGO PARA EL CALCULO DE LA COTIZACION II
                    sub_total_two = float(precio_two)
                    iva_two = float(precio_two) * imp_iva / int(100) # Obtengo el precio de tipo float de cada item ingresado por monto
                    total_two = sub_total_two + iva_two
                    
                    # BLOQUE DE CODIGO PARA EL CALCULO DE LA COTIZACION III
                    sub_total_tree = float(precio_tree)
                    iva_tree = float(precio_tree) * imp_iva / int(100) # Obtengo el precio de tipo float de cada item ingresado por monto
                    total_tree = sub_total_tree + iva_tree
                            
                    values.update({
						# BLOOQUE DE CODIGO PARA EL CALCULO DE LA COTIZACION I  
						'iva_one' : float(iva_one),
						'sub_total_one' : float(sub_total_one),
						'total_one' : float(total_one),
						# BLOOQUE DE CODIGO PARA EL CALCULO DE LA COTIZACION II
						'iva_two' : float(iva_two),
						'sub_total_two' : float(sub_total_two),
						'total_two' : float(total_two),
						# BLOOQUE DE CODIGO PARA EL CALCULO DE LA COTIZACION III
						'iva_tree' : float(iva_tree),
						'sub_total_tree' : float(sub_total_tree),
						'total_tree' : float(total_tree),
						
                    })
                ##############################################################################
		
		return {'value':values}
	
	_columns = {
		######################################################################################
		# ORDEN DE COMPRA
		######################################################################################
				'descripcion' : fields.text(string="Descripción", size=500, required=True),
				'item_one' :  fields.one2many('cotizacion.proveedor.one', 'item_id_one',string="Cotización I"),
				'item_two' :  fields.one2many('cotizacion.proveedor.two', 'item_id_two' ,string="Cotización II"),
				'item_tree' :  fields.one2many('cotizacion.proveedor.tree', 'item_id_tree',string="Cotización III"),
				'total_one' :  fields.float(string="Total", required=True),
				'sub_total_one' :  fields.float(string="Total", required=True),
				'iva_one' :  fields.float(string="IVA", required=True),
				'total_two' :  fields.float(string="Total", required=True),
				'sub_total_two' :  fields.float(string="Total", required=True),
				'iva_two' :  fields.float(string="IVA", required=True),
				'total_tree' :  fields.float(string="Total", required=True),
				'sub_total_tree' :  fields.float(string="Total", required=True),
				'iva_tree' :  fields.float(string="IVA", required=True),
				'impuesto' : fields.many2one('account.tax','Impuesto',required=True),
				'elaborado' : fields.char(string="Elaborado por: ", required=True)       
		######################################################################################
	}
	
	_defaults = {
		#'fecha' : lambda *a: time.strftime("%Y-%m-%d"),
		'impuesto' : 1,
		'descripcion' : "Luego de realizar la compararación de los precios ofertados por las empresas anteriormente especificadas, se sugiere adjudicar a la Empresa XXXXXXXXX, C.A., Por las siguientes razones:",
		#'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
	}


# CLASE PARA REPRESENTAR LA PRIMERA COTIZACION SUMINISTRADA POR EL PROVEEDOR NRO 1
######################################################################################################
class solicitud_cotizaciones_proveedores_one(osv.Model):

	_name = "cotizacion.proveedor.one"
        
	def search_valores_one(self, cr, uid, ids, argument_search,item, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		
		if not argument_search:
			
			return values
	
		if str(item) == "2":
			values.update({
				
				'sub_total_one' : float(argument_search),
				'total_one' : float(argument_search),
			})
		
		return {'value' : values}
		
	def search_valores_two(self, cr, uid, ids, argument_search,item, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		
		if not argument_search:
			
			return values
	
		if str(item) == "2":
			values.update({
				
				'sub_total_two' : float(argument_search),
				'total_two' : float(argument_search),
			})
		
		return {'value' : values}
	
	def search_valores_tree(self, cr, uid, ids, argument_search,item, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		
		if not argument_search:
			
			return values
	
		if str(item) == "2":
			values.update({
				
				'sub_total_tree' : float(argument_search),
				'total_tree' : float(argument_search),
			})
		
		return {'value' : values}
	
	# COLUMNAS PARA LA LISTA DE MATERIALES PARA EL PROCESO DE ORDEN DE PAGO
	_columns = {
		# ELEMENTO PARA LA PESTANA DE COTIZACION I
		'item_id_one':fields.many2one('analisis.precios', 'item_one', ondelete='cascade', select=False),
		'tipo' : fields.selection((('1','Limpieza'), ('2','Oficina'), ('3','Servicios Generales'), ('4','Tecnológico')),'Tipo de Material', required=False),
		'descripcion' : fields.many2one("materiales.almacen", "Descripcion", required=False),
		'cantidad_one' : fields.integer(string="Cantidad", required=False),
		'unidad_one' : fields.many2one("product.uom", "Unidad", required = False),
		'precio_one' : fields.float(string="Precio", required=False),
		'sub_total_one' : fields.float(string="Sub Total", required=False),
		# ELEMENTO PARA LA PESTANA DE COTIZACION II
		'cantidad_two' : fields.integer(string="Cantidad", required=False),
		'unidad_two' : fields.many2one("product.uom", "Unidad", required = False),
		'precio_two' : fields.float(string="Precio", required=False),
		'sub_total_two' : fields.float(string="Sub Total", required=False),
		# ELEMENTO PARA LA PESTANA DE COTIZACION III
		'cantidad_tree' : fields.integer(string="Cantidad", required=False),
		'unidad_tree' : fields.many2one("product.uom", "Unidad", required = False),
		'precio_tree' : fields.float(string="Precio", required=False),
		'sub_total_tree' : fields.float(string="Sub Total", required=False),
		
	
	}
