# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
import os
from datetime import date
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
from openerp.osv import fields, osv
import math
from openerp.tools.translate import _
import pdf_class
import base64 #Necesario para la generación del .txt y Pdf
import base64 #Necesario para la generación del .txt y Pdf

class Gestion_compras(osv.Model):
	
	_name = 'orden.compra'
	
	_order = 'numero'
	
	_rec_name = 'numero'
	
	def script_aprobado(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': '2'}, context=context)
	
	
	# METODO GLOBAL PARA CONTABILIZAR LOS PRECIOS DE LA ORDEN DE COMPRA
	#########################################################################################################
	def total_orden_compra(self, cr, uid, ids, item_ids, context=None):
		
		print "PRUEBA PARA LAS SUMATORIAS DE LOS MATERIALES PARA LA ORDEN DE COMPRA"
		# VARIABLES INICIALIZADAS
		iva     = 0.00
		sub_total = 0.0
		total     = 0.0
		values    = {}
		precio    = 0.00
		
		#ITERAMOS SOBRE EL MODELO A CONSULTAR
		impuesto = 0
		imp_iva  = 0
		for x in self.browse(cr, uid, ids, context=None):
			impuesto = x.impuesto
		
		if int(impuesto) == 0:
			imp_iva = 12
		if int(impuesto) == 1:
			imp_iva = 12
		if int(impuesto) == 2:
			imp_iva = 8
		
		
		sfl_trasmov  = self.pool.get('orden.materiales') # Consultamos el modelo para la lectura de los montos
		
		line_ids_trim = pdf_class.resolve_o2m_operations(cr, uid, sfl_trasmov, item_ids, ["precio"], context)
		
		for line_trim in line_ids_trim:
		    precio   += line_trim.get('precio',precio)
		
		sub_total = float(precio)
		iva = float(precio) * imp_iva / int(100) # Obtengo el precio de tipo float de cada item ingresado por monto
		
		total = sub_total + iva
		
		print "SUMA DE MATERIALES SOLICITADOS: "+str(total)
		
		values.update({
			'iva' : iva,
			'sub_total' : sub_total,
			'total' : total,
			
		})
		
		return {'value':values}
	

	#METODO PARA TRAER LA DESCRIPCION DEL PROYECTO
	def search_proyecto(self, cr, uid, ids, proyecto, context=None): # Proceso de busqueda de un manager(Gerente)
		
		#~ p = proyecto.split('-')
		#~ cod_p   = proyecto[0:2] # CODIGO DEL PROYECTO
		#~ cod_acc = proyecto[3:11] # CODIG DE PROYECTO Y ACCION
		#~ 
		#~ print "PROYECTO: "+str(cod_p)
		#~ print "ACCION: "+str(cod_acc)
		
		values = {}
		
		if not proyecto:
			
			return values
		
		cr.execute('SELECT d.monto_pre,d.codigo_proyecto,d.codigo_accion,p.descripcion FROM presupuesto_partidas AS p INNER JOIN presupuesto_distribucion AS d ON p.codigo = d.partida WHERE p.codigo = '"'"+str(proyecto)+"'"' ')
		
		for orden in cr.fetchall():
			monto           = orden[0] # 	MONTO DISPONIBLE
			cod_pro_accion  = str(orden[1])+"-"+str(orden[2]) # CODIGO DEL PROYECTO
			descripcion     = orden[3] # DESCRIPCION DEL PROYECTO
			
			values.update({
				'disponibilidad' : monto,
				'cod_accion' : cod_pro_accion,
				'proyecto' : descripcion,
				})
			
		return {'value' : values}
		
	######################################################################################
	#METODO PARA TRAER EL NUMERO DE SOLICITUD (COTIZACIONES)
	def search_num_solicitud(self, cr, uid, ids, cotizacion, context=None): # Proceso de busqueda de un manager(Gerente)
		
		values = {}
		
		if not cotizacion:
			
			return values
		
		cr.execute('SELECT fecha_orden FROM cotizacion WHERE id = '"'"+str(cotizacion)+"'"' ')
		
		for c in cr.fetchall():
			fecha_s = c[0] # 	MONTO DISPONIBLE
		
			values.update({
				'fecha_solicitud' : fecha_s,
				})
			
		return {'value' : values}
	
	######################################################################################	
	# METODO PARA LA GENERACION DE CORRELATIVO (ELEMENTO DE IDENTIFICACION PARA LA ORDEN DE COMPRA)
	######################################################################################
	def _generacion_correlativo(self, cr, uid, ids, context = None):
		
		ano         = time.strftime('%y') # Elemento para la captura de año actual del servidor			
		cr.execute("SELECT count(*) as nombre FROM orden_compra") # Consultamos a la base purchase_request
		num_orden   = cr.fetchone()[0]
		correlativo = ano+''+str(num_orden+1).zfill(6)
		return correlativo
	
	######################################################################################	
	# METODO PARA LA GENERACION DE CORRELATIVO (ELEMENTO DE IDENTIFICACION PARA LA ORDEN DE COMPRA NUMERO DE OFICIO)
	######################################################################################
	def _generacion_correlativo_oficio(self, cr, uid, ids, context = None):
		
		ano         = time.strftime('%y') # Elemento para la captura de año actual del servidor			
		cr.execute("SELECT count(*) as nombre FROM orden_compra") # Consultamos a la base purchase_request
		num_orden   = cr.fetchone()[0]
		correlativo = str(num_orden+1).zfill(6)
		return correlativo
	
	# PROCESO PARA LA GANERACION DE ORDEN DE COMPRA (PROCESO DE EMISION ORDEN DE COMPRA)
	def generar_orden(self, cr, uid, ids, context=None):
		
		# Instancia de la clase heredada L es horizontal y P es vertical
		
		# PROCESO DE ITERACION EL EL MODELO
		for orden in self.browse(cr, uid, ids, context=None):
			beneficiario = orden.beneficiario.name.upper() # BENEFICIARIO
			rif_ced      = orden.ced_rif # RIF / CEDULA
			tlf          = orden.tlf
			direccion    = orden.direccion.upper()
			cod          = orden.cod_accion
			proyecto     = orden.proyecto.upper()
			dir_entrega  = orden.direccion_entrega.upper()
			materiales   = orden.item_ids
			total        = pdf_class.decimal(float(orden.total))
			encargado    = orden.encargado.upper()
			correlativo  = orden.numero
			fecha_orden  = pdf_class.fecha(orden.fecha)
			nota         = orden.nota_orden.upper()
			n_solicitud  = orden.numero_solicitud.n_cotizacion
			s_fecha      = pdf_class.fecha(orden.fecha_solicitud)
			iva          = orden.iva
			impuesto     = orden.impuesto.name
			
			p = cod.split('-') # ELEMENTOS DE ACCESO CON SPLIT

			proy   = p[0:1][0]
			acc    = p[1:2][0]
			proy_c = p[2:3][0]
			acc_c  = p[3:4][0]
			
			##################################################################
			# LLAMADA A LA CLASE ORDEN DE COMPRA
			pdf = pdf_class.Orden_compra(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA

			#pdf.set_title(title)
			pdf.set_author('JESUS LAYA')
			pdf.alias_nb_pages() # LLAMADA DE PAGINACION
			pdf.add_page() # AÑADE UNA NUEVA PAGINACION
			#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
			pdf.set_font('Arial','B',15)
			pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
			pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
			#pdf.set_margins(8,10,10) # MARGENE DEL DOCUMENTO
			#pdf.ln(20) # Saldo de linea
			# 10 y 50 eje x y y 200 dimencion
			#pdf.line(10, 40, 200, 40) Linea 

			pdf.line(10, 42, 10, 210)  #LINEA DE MARGEN IZQUIERDO
			pdf.line(201, 42, 201, 210)  #LINEA DE MARGEN DERECHO


			pdf.line(35, 90, 35, 210)  #LINEA DE PARTIDA
			pdf.line(55, 90, 55, 210)  #LINEA DE CANTIDAD
			pdf.line(75, 90, 75, 210)  #LINEA DE UNIDAD
			pdf.line(161, 90, 161, 210)  #LINEA DESCRIPCIÓN
			pdf.line(181, 90, 181, 210)  #LINEA PRECIO
			#~ pdf.line(167, 114, 167, 164)  #LINEA DE DESCRIPCION

			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','',7)
			pdf.set_y(0)
			pdf.set_x(62)
			pdf.write(30,"REPÚBLICA BOLIVARIANA DE VENEZUELA".decode("UTF-8"))
			pdf.set_y(3)
			pdf.set_x(62)
			pdf.write(30,"A.C. BIBLIOTECAS VIRTUALES DE ARAGUA".decode("UTF-8"))
			pdf.set_y(6)
			pdf.set_x(62)
			pdf.write(30,"GERENCIA DE ADMINISTRACIÓN".decode("UTF-8"))

			pdf.set_y(13)
			pdf.set_x(161)
			pdf.set_font('Arial','B',6)
			pdf.cell(20,3,"NÚMERO".decode("UTF-8"),'LTR',0,'L',1)
			pdf.cell(20,3,"FECHA".decode("UTF-8"),'LTR',1,'L',1)
			pdf.set_y(16)
			pdf.set_x(161)
			pdf.set_font('Arial','B',9)
			pdf.cell(20,5,str(correlativo),'LBR',0,'C',1)
			pdf.cell(20,5,str(fecha_orden),'LBR',1,'C',1)
			pdf.set_y(21)
			pdf.set_x(161)
			pdf.set_font('Arial','',8)
			pdf.multi_cell(40,6,"SOLICITUD DE COMPRA".decode("UTF-8"),'LTBR','C',0)
			pdf.set_font('Arial','',7)
			pdf.set_y(27)
			pdf.set_x(161)
			pdf.set_font('Arial','B',6)
			pdf.cell(20,3,"NÚMERO".decode("UTF-8"),'LTR',0,'L',1)
			pdf.cell(20,3,"FECHA".decode("UTF-8"),'LTR',1,'L',1)
			pdf.set_y(30)
			pdf.set_x(161)
			pdf.set_font('Arial','B',6)
			pdf.cell(20,5,str(n_solicitud),'LBR',0,'C',1)
			pdf.cell(20,5,str(s_fecha),'LBR',1,'C',1)
			pdf.set_y(30)
			pdf.set_x(10)
			pdf.set_font('Arial','B',11)
			pdf.cell(190,6,"ORDEN DE COMPRA".decode("UTF-8"),'',1,'C',0)

			pdf.ln(5)

			pdf.set_font('Arial','B',9)
			pdf.cell(191,4,"PROVEEDOR".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_font('Arial','B',6)
			pdf.cell(145,4,"NOMBRE DE LA RAZÓN SOCIAL".decode("UTF-8"),'LTR',0,'L',1)
			pdf.cell(46,4,"NRO. DE R.I.F.".decode("UTF-8"),'LTR',1,'L',1)
			pdf.set_font('Arial','B',8)
			pdf.cell(145,4,pdf_class.acento(beneficiario),'LBR',0,'L',1)
			pdf.cell(46,4,str(rif_ced),'LBR',1,'L',1)
			pdf.set_font('Arial','B',6)
			pdf.cell(145,4,"DIRECCIÓN".decode("UTF-8"),'LTR',0,'L',1)
			pdf.cell(46,4,"TELÉFONO".decode("UTF-8"),'LTR',1,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(145,4,pdf_class.acento(direccion),'LBR',0,'L',1)
			pdf.cell(46,4,str(tlf),'LBR',1,'L',1)
			pdf.set_font('Arial','B',8)
			pdf.cell(191,4,"DATOS DE LA INSTITUCIÓN".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_font('Arial','',7)
			pdf.cell(60,4,"CÓDIGO PRESUPUESTARIO".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_font('Arial','',4)
			pdf.cell(15,3,"PROYECTO".decode("UTF-8"),'LTR',0,'L',1)
			pdf.cell(15,3,"ACCIÓN".decode("UTF-8"),'LTR',0,'L',1)
			pdf.cell(15,3,"".decode("UTF-8"),'LTR',0,'C',1)
			pdf.cell(15,3,"".decode("UTF-8"),'LTR',1,'C',1)
			pdf.set_font('Arial','',7)
			pdf.cell(15,3,str(proy),'LBR',0,'C',1)
			pdf.cell(15,3,str(acc),'LBR',0,'C',1)
			pdf.cell(15,3,str(proy_c),'LBR',0,'C',1)
			pdf.cell(15,3,str(acc_c),'LBR',1,'C',1)
			pdf.set_y(65)
			pdf.set_x(70)
			pdf.multi_cell(131,4,"PROYECTO:  "+pdf_class.acento(proyecto),'LTR','J',0)
			pdf.set_y(75)
			pdf.set_x(10)
			pdf.set_font('Arial','B',6)
			pdf.cell(191,4,"DIRECCIÓN DE LA ENTREGA".decode("UTF-8"),'LTR',1,'L',1)
			pdf.set_font('Arial','',8)
			pdf.multi_cell(191,4,"AV.:  "+pdf_class.acento(dir_entrega),'LBR','J',0)
			pdf.set_font('Arial','B',8)
			pdf.cell(191,4,"DESCRIPCIÓN DE LOS MATERIALES Y EQUIPOS".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_font('Arial','',8)
			pdf.cell(25,4,"PARTIDA".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,4,"CANTIDAD".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,4,"UNIDAD".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(86,4,"DESCRIPCIÓN".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,4,"PRECIO".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,4,"MONTO".decode("UTF-8"),'LTBR',1,'C',1)
			
			
		##################################################################
		# RECORRIDO DE LOS DATOS CONTENIDOS ONE2MANY ORDEN COMPRA
		
		for m in materiales:
			categoria   = m.categoria
			
			cod_partida = m.cod_partida
			cantidad    = m.cantidad
			descripcion = m.descripcion
			unidad      = m.unidad.name
			precio      = pdf_class.decimal(float(m.precio))
			sub_total   = pdf_class.decimal(float(m.sub_total))

			# VALIDACION PARA CAMPOS VACIOS
			if not m.descripcion:
				descripcion = m.descripcion
			
			# VALIDACION AL MOMENTO DE 	
			if str(m.cod_partida) == "4.03.18.01.00":
				descripcion = impuesto
				cantidad    = ""
				unidad      = ""
				precio      = pdf_class.decimal(iva)
				sub_total   = pdf_class.decimal(iva)
				
			pdf.set_font('Arial','',8)
			pdf.cell(25,4,str(cod_partida),'LR',0,'C',1)
			pdf.cell(20,4,str(cantidad),'LR',0,'C',1)
			pdf.cell(20,4,str(unidad),'LR',0,'C',1)
			pdf.cell(86,4,pdf_class.acento(descripcion),'LR',0,'C',1)
			pdf.cell(20,4,pdf_class.punto_decimal(str(precio)),'LR',0,'C',1)
			pdf.cell(20,4,pdf_class.punto_decimal(str(sub_total)),'LR',1,'C',1)
			

		pdf.set_y(210)
		pdf.set_x(10)
		pdf.set_font('Arial','',8)
		pdf.cell(151,4,"TOTAL        ".decode("UTF-8"),'LTBR',0,'R',1)
		pdf.set_font('Arial','B',8)
		pdf.cell(40,4,"Bs. "+pdf_class.punto_decimal(str(total))+"".decode("UTF-8"),'LTBR',1,'R',1)
		pdf.set_font('Arial','B',8)
		pdf.cell(191,4,"FIRMAS".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.cell(63,4,"PRESUPUESTO".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(64,4,"ADMINISTRACIÓN".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(64,4,"PRESIDENCIA".decode("UTF-8"),'LTBR',1,'L',1)

		pdf.set_font('Arial','',8)
		pdf.cell(63,4,"ELABORADO POR:".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(64,4,"CERTIFICADO POR:".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(64,4,"APROBADO POR:".decode("UTF-8"),'LTBR',1,'L',1)

		pdf.cell(63,4,"FIRMA".decode("UTF-8"),'LTR',0,'L',1)
		pdf.cell(64,4,"FIRMA".decode("UTF-8"),'LTR',0,'L',1)
		pdf.cell(64,4,"FIRMA".decode("UTF-8"),'LTR',1,'L',1)

		pdf.cell(63,6,"".decode("UTF-8"),'LBR',0,'L',1)
		pdf.cell(64,6,"".decode("UTF-8"),'LBR',0,'L',1)
		pdf.cell(64,6,"".decode("UTF-8"),'LBR',1,'L',1)

		pdf.set_font('Arial','B',8)
		pdf.cell(191,4,"NOTA".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_font('Arial','',8)
		pdf.multi_cell(191,5,pdf_class.acento(nota),'LBRT','J',0)
		pdf.cell(191,4,"ELABORADO POR LIC. "+pdf_class.acento(encargado),'T',1,'L',1)
		pdf.ln(7)
		
		dia = time.strftime('%d')
		mes = time.strftime('%B')
		ano = time.strftime('%Y')
		fecha = dia+" de "+mes+" "+ano
		
		title = 'Orden de Compra ('+fecha+').pdf'
		pdf.output('openerp/addons/gestion_compras/reportes/orden_compra/'+title,'F') # Salida del documento
		open_document = open('openerp/addons/gestion_compras/reportes/orden_compra/'+title) # Apertura del documento
		#######################################################################################################
		# Guardamos el archivo pdf en adjunto.documento
		id_att = self.pool.get('adjunto.documento').create(cr, uid, {
			'name': title,
			'res_name': title,
			'datas': base64.encodestring(open_document.read()),
			'datas_fname': title,
			'res_model': 'control.perceptivo',
			'description': "",
			'item': "",
			}, context=context)
		
		return id_att
		
	_columns = {
		######################################################################################
		# ORDEN DE COMPRA
		######################################################################################
				'tipo_doc' : fields.many2one("presupuesto.tipodoc", "Tipo Doc", required = True),
				'fecha' : fields.date(string="Fecha", required=True),
				'numero' : fields.char(string="Numero", size=50, required=True),
				'oficio' : fields.char(string="Oficio", size=50, required=True),
				'beneficiario' : fields.many2one("res.partner", "Beneficiario", required = True),
				'ced_rif' : fields.char(string="Cedula / Rif", size=15, required=True),
				'unidad': fields.many2one('stock.location', 'Unidad Solicitante', required= True), # Usuario logeado
				'observacion_requisicion' : fields.text(string='Requisicion', required=False),
				'proy_accion' : fields.many2one("presupuesto.accion", "Proyecto", required = True),
				'fecha_req' :  fields.date(string="Fecha  de Requisicion", required=True),
				'requisicion' : fields.text(string="Requisicion", size=256, required=True),
				'concepto' : fields.text(string="Concepto", size=50, required=True),
				'cod_pre' : fields.char(string="Cod. Presupuestario", size=30, required=True),
				'proyecto' : fields.text(string="Proyecto:", size=256, required=True),
				'disponibilidad' : fields.char(string="Disponibilidad", required=True),
				'item_ids' :  fields.one2many('orden.materiales', 'item_id'),
				'user': fields.many2one('res.users', 'Registrado por:', readonly=True), # Usuario logeado
				'total' :  fields.float(string="Total", required=True),
				'sub_total' :  fields.float(string="Total", required=True),
				'iva' :  fields.float(string="Total", required=True),
				'tlf' : fields.char(string="Telefono", required=False),
				'ano_fiscal' : fields.char(string="Año Fiscal", required=False),
				'impuesto' : fields.many2one('account.tax','Impuesto',required=True),
				'state': fields.selection([('1', 'Pre-Aprobado'),('2', 'Aprobado')]),
				'cod_accion' : fields.char(string="Cod / Acción" , size=20, required=True),
				'direccion' : fields.text(string="Dirección", size=256, required=True),
				'direccion_entrega' : fields.text(string="Dirección / Entrega", size=256, required=True),
				'encargado' : fields.char(string="Elaborado por: ", size=100, required=True),
				'nota_orden' : fields.text(string="Nota", size=256,required=False),
				'numero_solicitud' : fields.many2one('cotizacion', 'Numero de Solicitud', required=True), # Usuario logeado
				'fecha_solicitud' : fields.date(string="Fecha de Solicitud", required=True),
		######################################################################################
	}
	
	_defaults = {
		'fecha' : lambda *a: time.strftime("%Y-%m-%d"),
		'fecha_req' : lambda *a: time.strftime("%Y-%m-%d"),
		'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
		'numero' :  _generacion_correlativo,
		'oficio' : _generacion_correlativo_oficio,
		'impuesto' : 1,
		'ano_fiscal' : lambda *a: time.strftime("%Y"),
		'state' : '1',
	}
        
class solicitud_material(osv.Model):

	_name = "orden.materiales"
	
	# Metodo para traer las especificaciones de los materiales
	def search_partida(self, cr, uid, ids, argument_search,item, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		
		if not argument_search:
			
			return values
		if str(item) == "1":
			obj_dp = self.pool.get('presupuesto.partidas')
			
			#======================== Busqueda por código ============================
			search_obj_code = obj_dp.search(cr, uid, [('id','=',argument_search)])
	
			datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
			#=========================================================================
			if not datos_code:
				
				values.update({
					'cod_partida' : None,
					})
			
			else:
				
				values.update({
					'cod_partida' : datos_code[0]['codigo'],
				})
		if str(item) == "2":
			values.update({
				
				'sub_total' : float(argument_search),
				'total' : float(argument_search),
			})
		
		return {'value' : values}
	
	
	# COLUMNAS PARA LA LISTA DE MATERIALES PARA EL PROCESO DE ORDEN DE PAGO
	_columns = {
		'item_id':fields.many2one('orden.compra', 'item_ids', ondelete='cascade', select=False),
		'tipo_doc' : fields.many2one("presupuesto.tipodoc", "Tipo Doc", required = False),
		'numero' : fields.char(string="Numero", size=50, required=False),
		'categoria' :  fields.char(string="Categoria", size=50, required=False),
		'partida' : fields.many2one('presupuesto.partidas','Desc Partida',required=True),
		'cod_partida' : fields.char(string="Partida", size=30, required=True),
		'cantidad' : fields.integer(string="Cantidad", required=False),
		'descripcion' : fields.text(string="Descripcion", size=256, required=False),
		'unidad' : fields.many2one("product.uom", "Unidad", required = False),
		#'impuesto' : fields.many2one('account.tax','Impuesto',required=False),
		'precio' : fields.float(string="Precio", required=False),
		'sub_total' : fields.float(string="Sub Total", required=False),
	}
