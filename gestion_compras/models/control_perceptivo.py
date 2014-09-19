# -*- coding: utf-8 -*-

'''

Control Perceptivo

El control perceptivo debe practicarse al momento de la recepción de los bienes adquiridos, para asegurarse que el precio, calidad y cantidad correspondan con las especificaciones aprobadas en las Órdenes de Compra.

'''

#import time # Necesario para las funciones de Fecha

import time # Necesario para las funciones de Fecha
import pdf_class # Llamada de las clases DPF
import base64 
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final

from openerp.osv import osv, fields

class Solicitud(osv.Model):
	_name="control.perceptivo"

	_order = 'nombre'
	
	_rec_name = 'nombre'
	
	# EMITIR SOLICITUD DE MATERIALES DE CADA UNIDAD SOLICITANTE
	def emitir_solicitud_material(self, cr, uid, ids, context=None):
		
		for c in self.browse(cr, uid, ids, context=None):
			model_id        = c.id
			area            = c.solicitante.name # Solicitante
			fecha_actual    = c.fecha # Fecha actual
			doc             = c.documento # Documento
			n_iden          = c.n_iden # Numero de Identificacion
			proveedor       = c.proveedor.name # Proveedor
			tipo_orden      = c.tipo_orden # Tipo de Orden
			n_orden         = c.num_orden # Numero de Orden
			fecha_orden     = c.fecha_orden # fecha de la Orden
			monto           = float(c.monto_recibido) # Monto Recibido
			encargado       = c.encargado
			
			
				
			
		###################################################################################
		# Instancia de la clase heredada L es horizontal y P es vertical

		pdf=pdf_class.Control_perceptivo(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA

		#pdf.set_title(title)
		pdf.set_author('Marcel Arcuri')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		pdf.set_font('Arial','B',15)
		pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		pdf.set_margins(20,10,10) # MARGENE DEL DOCUMENTO
		#pdf.ln(20) # Saldo de linea
		# 10 y 50 eje x y y 200 dimencion
		#pdf.line(10, 40, 200, 40) Linea 


		pdf.set_fill_color(255,255,255)
		pdf.set_font('Arial','B',12)
		pdf.cell(190,5,"CONTROL PERCEPTIVO",'',1,'C',1)
		pdf.ln(5)
		pdf.set_font('Arial','B',11)
		pdf.cell(140,5,"Área Receptora:".decode("UTF-8"),'LTR',0,'L',1)
		pdf.cell(40,5,"Fecha:".decode("UTF-8"),'LTR',1,'L',1)
		pdf.set_font('Arial','',11)
		pdf.cell(140,5,pdf_class.acento(area),'LBR',0,'L',1)
		pdf.cell(40,5,pdf_class.fecha(fecha_actual),'LBR',1,'L',1)
		pdf.set_font('Arial','B',11)
		pdf.cell(35,5,"Documento".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,5,"N° de Identificación".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(20,5,"Fecha".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(85,5,"Proveedor".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_font('Arial','',10)
		pdf.cell(35,5,str(doc),'LTBR',0,'C',1)
		pdf.cell(40,5,str(n_iden),'LTBR',0,'C',1)
		pdf.cell(20,5,pdf_class.fecha(fecha_actual),'LTBR',0,'C',1)
		pdf.cell(85,5,pdf_class.acento(proveedor),'LTBR',1,'C',1)
		pdf.set_font('Arial','B',11)
		pdf.cell(35,5,"Tipo de Orden".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,5,"N° de Orden".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(20,5,"Fecha".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(85,5,"Monto Recibido".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_font('Arial','',10)
		pdf.cell(35,5,pdf_class.acento(tipo_orden),'LTBR',0,'C',1)
		pdf.cell(40,5,pdf_class.acento(n_orden),'LTBR',0,'C',1)
		pdf.cell(20,5,"25/08/2014".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(85,5,pdf_class.punto_decimal(str(monto)),'LTBR',1,'C',1)
		pdf.ln(5)

		# Fila de la cabezara de la tabla
		pdf.cell(10,5,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(20,5,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(55,5,"Denominación del Bien o Material".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(95,5,"Descripción del Material".decode("UTF-8"),'LTBR',1,'C',1)

			
		pdf.set_font('Arial','',10) # TAMANO DE LA FUENTE

		# Fin Cabezera
		pdf.set_font('Arial','',10) # TAMANO DE LA FUENTE

		k = 0
		j = 0
		item = 0
		# Iteramos sobre el objeto one2many y accedemos a los elementos
		for m in c.material_ids:
			tipo = m.tipo
			denominacion = m.denominacion.descripcion
			descripcion  = m.descripcion
			cantidad     = m.cantidad
			modelo       = m.modelo
			marca        = m.marca
			print "SOLICITANTE: "+str(m.descripcion)
			
			if j == 26:
				pdf.add_page()
				pdf.set_fill_color(255,255,255)
				pdf.set_font('Arial','B',12)
				pdf.cell(190,5,"CONTROL PERCEPTIVO",'',1,'C',1)
				pdf.ln(5)
				pdf.set_font('Arial','B',11)
				pdf.cell(140,5,"Área Receptora:".decode("UTF-8"),'LTR',0,'L',1)
				pdf.cell(40,5,"Fecha:".decode("UTF-8"),'LTR',1,'L',1)
				pdf.set_font('Arial','',11)
				pdf.cell(140,5,pdf_class.acento(area),'LBR',0,'L',1)
				pdf.cell(40,5,"20/09/2014".decode("UTF-8"),'LBR',1,'L',1)
				pdf.set_font('Arial','B',11)
				pdf.cell(35,5,"Documento".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(40,5,"N° de Identificación".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(20,5,"Fecha".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(85,5,"Proveedor".decode("UTF-8"),'LTBR',1,'C',1)
				pdf.set_font('Arial','',10)
				pdf.cell(35,5,str(doc),'LTBR',0,'C',1)
				pdf.cell(40,5,str(n_iden),'LTBR',0,'C',1)
				pdf.cell(20,5,pdf_class.fecha(fecha_actual),'LTBR',0,'C',1)
				pdf.cell(85,5,pdf_class.acento(proveedor),'LTBR',1,'C',1)
				pdf.set_font('Arial','B',11)
				pdf.cell(35,5,"Tipo de Orden".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(40,5,"N° de Orden".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(20,5,"Fecha".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(85,5,"Monto Recibido".decode("UTF-8"),'LTBR',1,'C',1)
				pdf.set_font('Arial','',10)
				pdf.cell(35,5,pdf_class.acento(tipo_orden),'LTBR',0,'C',1)
				pdf.cell(40,5,pdf_class.acento(n_orden),'LTBR',0,'C',1)
				pdf.cell(20,5,"25/08/2014".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(85,5,pdf_class.punto_decimal(str(monto)),'LTBR',1,'C',1)
				pdf.ln(5)
			
				
				# Fin Cabezera
				j=0
			item = int(item) + 1
			# Filas que vienen de la BD
			pdf.cell(10,5,str(item).decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(cantidad),'LTBR',0,'C',1)
			pdf.cell(55,5,pdf_class.acento(denominacion),'LTBR',0,'l',1)
			pdf.cell(95,5,pdf_class.acento(descripcion),'LTBR',1,'l',1)
			
			pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
			j =j+1
			
		pdf.ln(10)
		#pdf.write(30,"Total")
		pdf.set_font('Arial','B',10)
		pdf.cell(180,6,"Dependencia Receptora",'LTBR',1,'C',0)
		pdf.cell(180,6,"Responsable: "+pdf_class.acento(encargado),'LTBR',1,'L',0)
		pdf.cell(180,6,"Firma:",'LTBR',1,'L',0)
		pdf.cell(180,6,"Fecha: "+pdf_class.fecha(fecha_actual),'LTBR',1,'L',0)
		###################################################################################
		
		dia   = time.strftime('%d')
		mes   = time.strftime('%B')
		ano  = time.strftime('%Y')
		fechas = dia+" de "+mes+" "+ano
		
		title = "Control Perceptivo ("+fechas+") ("+pdf_class.acento(proveedor)+") Nro ("+n_iden+") Nro de Orden ("+n_orden+").pdf"
		
		pdf.output('openerp/addons/gestion_compras/reportes/control_perceptivo/'+title,'F')
		documento = open('openerp/addons/gestion_compras/reportes/control_perceptivo/'+title) # Apertura del documento
		
		# Guardamos el archivo pdf en gestion.eventos
		self.pool.get('adjunto.documento').create(cr, uid, {
				'name': title,
				'res_name': title,
				'datas': base64.encodestring(documento.read()),
				'datas_fname': title,
				'res_model': 'control.perceptivo (Control perceptivo)',
				'description': title,
				'item': "",
				}, context=context)
		
	def search_num_orden(self, cr, uid, ids, argument_search, context=None): # Proceso de busqueda de un manager(Gerente)

		values     = {}
		mensaje    = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('orden.compra')
		
		#======================== Busqueda por código ============================

		search_obj_code = obj_dp.search(cr, uid, [('numero','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		print "DATOS DE EL NUMERO DE ORDEN: "+str(datos_code)
		#=========================================================================
		if not datos_code:
			
			mensaje = {
				'title' : "Control Perceptivo",
				'message' : "Disculpe el numero de Orden no existe en la orden de Compra, intente de nuevo...",
			}
			
			values.update({
				'num_orden' : None,
				'monto_recibido' : None,
				})
		
		else:
			
			values.update({
				
				'num_orden' : datos_code[0]['numero'],
				'monto_recibido' : float(datos_code[0]['total']),
				})
		
		return {'value' : values}
	######################################################################################
	_columns = {
			# Control Perceptivo
			'solicitante' : fields.many2one('stock.location','Area Solicitante',required=True),
			'nombre' : fields.char(string="Nombre de referencia", size=100, required=True),
	    'material_ids': fields.one2many('control.perceptivo.m', 'materiales_id', string='Control Perceptivo'), # LISTA DE MATERAILES (LIMPIEZA/ PAPELERIA / OTROS)
	    'user': fields.many2one('res.users', 'Registrado por:', readonly=True),
	    'fecha' : fields.date(string = "Fecha", required = True),
	    'observaciones' : fields.text(string="Observaciones", size=256, required=False),
	    'documento' : fields.char(string="Documento", size=100, required=True),
	    'n_iden' : fields.char(string="N° de Identificación", size=100, required=True),
	    'proveedor' :  fields.many2one('res.partner', 'Proveedor', required=True),
	    'tipo_orden' : fields.char(string="Tipo de Orden", required=True),
	    'num_orden' : fields.char(string="N° de Orden", size=100, required=True),
	    'fecha_orden' : fields.date(string = "Fecha de Orden", required = True),
	    'monto_recibido' : fields.float("Monto recibido"),
	    'encargado' : fields.char(string="Encargado", required=True),
	}
	######################################################################################

	_defaults = {
		'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
		'fecha': lambda *a: time.strftime("%Y-%m-%d"),
		'documento' :  'Factura',
	}

# Clase para los materiales de compras (Solicitud Directa)

class Control_perceptivo(osv.Model):

	_name = "control.perceptivo.m"
	
	
	# COLUMNAS PARA LA LISTA DE MATERIALES DE SOLICITUD
	_columns = {
		'materiales_id' : fields.many2one('control.perceptivo', 'material_ids', ondelete='cascade', select=False),
		'cantidad' : fields.char(string="Cantidad", required=True),
		'tipo' : fields.selection((('1','Limpieza'), ('2','Oficina'), ('3','Servicios Generales'), ('4','Tecnológico')),'Tipo de Material', required=False),
		'denominacion' : fields.many2one('materiales.almacen', string="Denominación", required=True),
		'descripcion' : fields.char(string="Descripción", required=True),
		'unidad' : fields.many2one('product.uom', 'Unidad de Medida', required=False),
		'modelo' : fields.char(string="Modelo", required=False),
		'marca'  : fields.char(string="Marca", required=True),
		'foto_referencial' : fields.binary("Foto Referencial",help="Foto Referencial"),
	}
	
