# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

import time # Necesario para las funciones de Fecha
import pdf_class # Llamada de las clases DPF
import base64 
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final

from openerp.osv import osv, fields

class Solicitud(osv.Model):
	_name="comp.solicitud"

	_order = 'nombre'
	
	_rec_name = 'nombre'
	
	# EMITIR SOLICITUD DE MATERIALES DE CADA UNIDAD SOLICITANTE
	def emitir_solicitud_material(self, cr, uid, ids, context=None):
		
		for s in self.browse(cr, uid, ids, context=None):
			model_id        = s.id
			correlativo     = s.nombre
			fecha_solicitud = s.fecha
			solicitante     = s.solicitante.complete_name
			
			if s.item == 'Limpienza':
				m_limpieza = "X"
			else:
				m_limpieza = ""
			if s.item == 'servicios':
				m_servicios = "X"
			else:
				m_servicios = ""
			if s.item == 'papeleria':
				m_papeleria = "X"
			else:
				m_papeleria = ""
			if s.item == 'tecnologico':
				m_tecnologico = "X"
			else:
				m_tecnologico = ""
			if s.item == 'otros':
				m_otros = "X"
			else:
				m_otros = ""
				
			# Instancia de la clase heredada L es horizontal y P es vertical
	
		pdf=pdf_class.Solicitud_materiales(orientation='L',unit='mm',format='A4') #HORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Jesus Laya')
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
		
		
		pdf.set_fill_color(255,255,255)
		pdf.set_font('Arial','B',8)
		pdf.cell(145,7,"Area Solicitante: "+acento(solicitante),'LTBR',0,'L',1)
		pdf.cell(60,7,"Fecha: "+fecha(fecha_solicitud),'LTBR',0,'L',1)
		pdf.cell(55,7,"Correlativo: "+str(correlativo),'LTBR',1,'L',1)
		pdf.ln(5)
		
		pdf.set_font('Arial','B',12)
		pdf.cell(100,5,"",'',0,'C',1)
		pdf.cell(80,5,"SOLICITUD DE MATERIALES, SUMINISTROS Y EQUIPOS",'',1,'C',1)
		pdf.ln(5)
		
		pdf.set_font('Arial','B',12)
		pdf.cell(115,6,"",'LTB',0,'C',1)
		pdf.cell(105,6,"MATERIAL:",'TB',0,'L',1)
		pdf.cell(40,6,"",'TBR',1,'C',1)
		
		pdf.set_font('Arial','B',12)
		pdf.cell(40,7,"Limpienza: "+str(m_limpieza),'LTBR',0,'C',1)
		pdf.cell(65,7,"Servicios Generales: "+str(m_servicios),'LTBR',0,'C',1)
		pdf.cell(65,7,"Oficina o papeleria: "+str(m_papeleria),'LTBR',0,'C',1)
		pdf.cell(50,7,"Tecnológico: ".decode("UTF-8")+str(m_tecnologico),'LTBR',0,'C',1)
		pdf.cell(40,7,"Otros: "+str(m_otros),'LTBR',1,'L',1)
		pdf.ln(3)
		
		pdf.set_font('Arial','B',10)
		pdf.cell(200,5,"",'',0,'C',1)
		pdf.cell(60,5,"Espacio para ser".decode("UTF-8"),'LTR',1,'C',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(200,5,"",'',0,'C',1)
		pdf.cell(60,5,"llenado por Almacén:".decode("UTF-8"),'LBR',1,'C',1)
		
		# Fila de la cabezara de la tabla
		
		pdf.cell(10,5,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(63,5,"Material requerido",'LTBR',0,'C',1)
		pdf.cell(17,5,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(20,5,"Modelo",'LTBR',0,'C',1)
		pdf.cell(25,5,"Marca".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(35,5,"Inform. Adicional",'LTBR',0,'C',1)
		pdf.cell(30,5,"Foto ",'LTBR',0,'C',1)
		pdf.cell(30,5,"En Existencia",'LTBR',0,'C',1)
		pdf.cell(30,5,"Requerimiento",'LTBR',1,'C',1)
		
		
		# Fin Cabezera
		pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		
		j = 0
		
		if j == 12:
			pdf.add_page()		
			pdf.set_font('Arial','B',8)
			pdf.cell(145,7,"Area Solicitante: "+acento(solicitante),'LTBR',0,'L',1)
			pdf.cell(60,7,"Fecha: "+fecha(fecha_solicitud),'LTBR',0,'L',1)
			pdf.cell(55,7,"Correlativo: "+str(correlativo),'LTBR',1,'L',1)
			pdf.ln(5)
	
			pdf.set_font('Arial','B',14)
			pdf.cell(100,5,"",'',0,'C',1)
			pdf.cell(80,5,"SOLICITUD DE MATERIALES, SUMINISTROS Y EQUIPOS",'',1,'C',1)
			pdf.ln(5)
	
			pdf.set_font('Arial','B',12)
			pdf.cell(105,5,"",'LTB',0,'C',1)
			pdf.cell(105,5,"MATERIAL:",'TB',0,'L',1)
			pdf.cell(50,5,"",'TBR',1,'C',1)
	
			pdf.set_font('Arial','B',12)
			pdf.cell(40,7,"Limpienza: "+str(m_limpieza),'LTBR',0,'C',1)
			pdf.cell(65,7,"Servicios Generales: "+str(m_servicios),'LTBR',0,'C',1)
			pdf.cell(65,7,"Oficina o papeleria: "+str(m_papeleria),'LTBR',0,'C',1)
			pdf.cell(50,7,"Tecnológico: ".decode("UTF-8")+str(m_tecnologico),'LTBR',0,'C',1)
			pdf.cell(40,7,"Otros: "+str(m_otros),'LTBR',1,'L',1)
			pdf.ln(3)
	
			pdf.set_font('Arial','B',12)
			pdf.cell(215,5,"",'',0,'C',1)
			pdf.cell(45,5,"Espacio para ser".decode("UTF-8"),'LTR',1,'C',1)
			pdf.set_font('Arial','B',12)
			pdf.cell(215,5,"",'',0,'C',1)
			pdf.cell(45,5,"llenado por Almacén:".decode("UTF-8"),'LBR',1,'C',1)
			
			
			# Fin Cabezera
			j=0
	
		# Iteramos sobre el objeto consultado
		material   = self.pool.get('purchase.materiales') # Objeto purchase_materiales (Solicitud Materiales)
		
		datos      = material.search(cr, uid, [('materiales_id','=',model_id)], context=None)
		s_m        = material.read(cr,uid,datos,context=context)
		i = 1
		for d_s_m in s_m:
			descripcion = d_s_m['descripcion'][1]
			cantidad    = d_s_m['cantidad']
			modelo      = d_s_m['modelo']
			marca       = d_s_m['marca']
			
			
			if not modelo: # Campo Vacio (Validacion)
				modelo = ""
			else:
				modelo
			
			unidad      = d_s_m['unidad']
			print "UNIDAD SOLITANTE: "+str(unidad)
		
			# Filas que vienen de la BD
			pdf.cell(10,5,str(i),'LTBR',0,'C',1)
			pdf.cell(63,5,acento(descripcion),'LTBR',0,'C',1)
			pdf.cell(17,5,str(cantidad),'LTBR',0,'C',1)
			pdf.cell(20,5,str(modelo),'LTBR',0,'C',1)
			pdf.cell(25,5,acento(marca),'LTBR',0,'C',1)
			pdf.cell(35,5,"Inform. Adicional",'LTBR',0,'C',1)
			pdf.cell(30,5,"Foto ",'LTBR',0,'C',1)
			pdf.cell(30,5,"En Existencia",'LTBR',0,'C',1)
			pdf.cell(30,5,"Requerimiento",'LTBR',1,'C',1)
			
			pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
			i = i + 1
			
		pdf.ln(47)
		#pdf.write(30,"Total")
		pdf.set_font('Arial','B',11)
		pdf.cell(70,7,"Solicitado por:",'LTBR',0,'C',0)
		pdf.cell(70,7,"Recibido por:",'LTBR',0,'C',0)
		pdf.cell(70,7,"Revisado por Compras:",'LTBR',1,'C',0)
		
		pdf.cell(70,7,"",'LTBR',0,'C',0)
		pdf.cell(70,7,"",'LTBR',0,'C',0)
		pdf.cell(70,7,"",'LTBR',1,'C',0)
		
		pdf.cell(70,7,"Fecha:",'LTBR',0,'L',0)
		pdf.cell(70,7,"Fecha:",'LTBR',0,'L',0)
		pdf.cell(70,7,"Fecha:",'LTBR',1,'L',0)
		
		pdf.cell(70,7,"Firma:",'LTBR',0,'L',0)
		pdf.cell(70,7,"Firma:",'LTBR',0,'L',0)
		pdf.cell(70,7,"Firma:",'LTBR',1,'L',0)
		
		dia   = time.strftime('%d')
		mes   = time.strftime('%B')
		ano  = time.strftime('%Y')
		fechas = dia+" de "+mes+" "+ano
		
		title = "Solicitud Materiales ("+fechas+").pdf"
		
		pdf.output('openerp/addons/gestion_compras/reportes/'+title,'F')
		documento = open('openerp/addons/gestion_compras/reportes/'+title) # Apertura del documento
        
		# Guardamos el archivo pdf en gestion.eventos
		self.pool.get('adjunto.documento').create(cr, uid, {
		    'name': title,
		    'res_name': title,
		    'datas': base64.encodestring(documento.read()),
		    'datas_fname': title,
		    'res_model': 'gestion.eventos (Gestión de Eventos)',
		    'description': title,
		    'item': "materiales",
		    }, context=context)
		
	# METODO PARA LA SELECCION POR SERVICIOS GENERALES / TECNOLOGICO A CADA UNIDAD SOLICITANTE
	
	######################################################################################
	def emitir_solicitud_material_servicios_tennologico(self, cr, uid, ids, context=None):
		
		for s in self.browse(cr, uid, ids, context=None):
			model_id        = s.id
			correlativo     = s.nombre
			fecha_solicitud = s.fecha
			solicitante     = s.solicitante.complete_name
			
			if s.item == 'Limpienza':
				m_limpieza = "X"
			else:
				m_limpieza = ""
			if s.item == 'servicios':
				m_servicios = "X"
			else:
				m_servicios = ""
			if s.item == 'papeleria':
				m_papeleria = "X"
			else:
				m_papeleria = ""
			if s.item == 'tecnologico':
				m_tecnologico = "X"
			else:
				m_tecnologico = ""
			if s.item == 'otros':
				m_otros = "X"
			else:
				m_otros = ""
				
			# Instancia de la clase heredada L es horizontal y P es vertical
	
		pdf=pdf_class.Solicitud_materiales(orientation='L',unit='mm',format='A4') #HORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Jesus Laya')
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
		
		
		pdf.set_fill_color(255,255,255)
		pdf.set_font('Arial','B',8)
		pdf.cell(145,7,"Area Solicitante bbbbbbbbbbbbbbbbb: "+acento(solicitante),'LTBR',0,'L',1)
		pdf.cell(60,7,"Fecha: "+fecha(fecha_solicitud),'LTBR',0,'L',1)
		pdf.cell(55,7,"Correlativo: "+str(correlativo),'LTBR',1,'L',1)
		pdf.ln(5)
		
		pdf.set_font('Arial','B',12)
		pdf.cell(100,5,"",'',0,'C',1)
		pdf.cell(80,5,"SOLICITUD DE MATERIALES, SUMINISTROS Y EQUIPOS",'',1,'C',1)
		pdf.ln(5)
		
		pdf.set_font('Arial','B',12)
		pdf.cell(115,6,"",'LTB',0,'C',1)
		pdf.cell(105,6,"MATERIAL:",'TB',0,'L',1)
		pdf.cell(40,6,"",'TBR',1,'C',1)
		
		pdf.set_font('Arial','B',12)
		pdf.cell(40,7,"Limpienza: "+str(m_limpieza),'LTBR',0,'C',1)
		pdf.cell(65,7,"Servicios Generales: "+str(m_servicios),'LTBR',0,'C',1)
		pdf.cell(65,7,"Oficina o papeleria: "+str(m_papeleria),'LTBR',0,'C',1)
		pdf.cell(50,7,"Tecnológico: ".decode("UTF-8")+str(m_tecnologico),'LTBR',0,'C',1)
		pdf.cell(40,7,"Otros: "+str(m_otros),'LTBR',1,'L',1)
		pdf.ln(3)
		
		pdf.set_font('Arial','B',10)
		pdf.cell(200,5,"",'',0,'C',1)
		pdf.cell(60,5,"Espacio para ser".decode("UTF-8"),'LTR',1,'C',1)
		pdf.set_font('Arial','B',10)
		pdf.cell(200,5,"",'',0,'C',1)
		pdf.cell(60,5,"llenado por Almacén:".decode("UTF-8"),'LBR',1,'C',1)
		
		# Fila de la cabezara de la tabla
		
		pdf.cell(10,5,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.multi_cell(63,5,"Material requerido",'LTBR',0,'C',1)
		pdf.cell(17,5,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(20,5,"Modelo",'LTBR',0,'C',1)
		pdf.cell(25,5,"Marca".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(35,5,"Inform. Adicional",'LTBR',0,'C',1)
		pdf.cell(30,5,"Foto ",'LTBR',0,'C',1)
		pdf.cell(30,5,"En Existencia",'LTBR',0,'C',1)
		pdf.cell(30,5,"Requerimiento",'LTBR',1,'C',1)
		
		
		# Fin Cabezera
		pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		
		j = 0
		
		if j == 12:
			pdf.add_page()		
			pdf.set_font('Arial','B',8)
			pdf.cell(145,7,"Area Solicitante: "+acento(solicitante),'LTBR',0,'L',1)
			pdf.cell(60,7,"Fecha: "+fecha(fecha_solicitud),'LTBR',0,'L',1)
			pdf.cell(55,7,"Correlativo: "+str(correlativo),'LTBR',1,'L',1)
			pdf.ln(5)
	
			pdf.set_font('Arial','B',14)
			pdf.cell(100,5,"",'',0,'C',1)
			pdf.cell(80,5,"SOLICITUD DE MATERIALES, SUMINISTROS Y EQUIPOS",'',1,'C',1)
			pdf.ln(5)
	
			pdf.set_font('Arial','B',12)
			pdf.cell(105,5,"",'LTB',0,'C',1)
			pdf.cell(105,5,"MATERIAL:",'TB',0,'L',1)
			pdf.cell(50,5,"",'TBR',1,'C',1)
	
			pdf.set_font('Arial','B',12)
			pdf.cell(40,7,"Limpienza: "+str(m_limpieza),'LTBR',0,'C',1)
			pdf.cell(65,7,"Servicios Generales: "+str(m_servicios),'LTBR',0,'C',1)
			pdf.cell(65,7,"Oficina o papeleria: "+str(m_papeleria),'LTBR',0,'C',1)
			pdf.cell(50,7,"Tecnológico: ".decode("UTF-8")+str(m_tecnologico),'LTBR',0,'C',1)
			pdf.cell(40,7,"Otros: "+str(m_otros),'LTBR',1,'L',1)
			pdf.ln(3)
	
			pdf.set_font('Arial','B',12)
			pdf.cell(215,5,"",'',0,'C',1)
			pdf.cell(45,5,"Espacio para ser".decode("UTF-8"),'LTR',1,'C',1)
			pdf.set_font('Arial','B',12)
			pdf.cell(215,5,"",'',0,'C',1)
			pdf.cell(45,5,"llenado por Almacén:".decode("UTF-8"),'LBR',1,'C',1)
			
			
			# Fin Cabezera
			j=0
	
		# Iteramos sobre el objeto consultado
		producto   = self.pool.get('purchase.s.p.t') # Objeto purchase_materiales (Solicitud Materiales)
		
		datos      = producto.search(cr, uid, [('materiales_p_id','=',model_id)], context=None)
		s_m        = producto.read(cr,uid,datos,context=context)
		i = 1
		for d_s_m in s_m:
			descripcion = d_s_m['descripcion'][1]
			cantidad    = d_s_m['cantidad']
			modelo      = d_s_m['modelo']
			marca       = d_s_m['marca']
			
			
			if not modelo: # Campo Vacio (Validacion)
				modelo = ""
			else:
				modelo
			
			#unidad      = d_s_m['unidad']
			#print "UNIDAD SOLITANTE: "+str(unidad)
		
			# Filas que vienen de la BD
			pdf.cell(10,5,str(i),'LTBR',0,'C',1)
			pdf.multi_cell(63,5,acento(descripcion),'LTBR',0,'C',1)
			pdf.cell(17,5,str(cantidad),'LTBR',0,'C',1)
			pdf.cell(20,5,str(modelo),'LTBR',0,'C',1)
			pdf.cell(25,5,acento(marca),'LTBR',0,'C',1)
			pdf.cell(35,5,"Inform. Adicional",'LTBR',0,'C',1)
			pdf.cell(30,5,"Foto ",'LTBR',0,'C',1)
			pdf.cell(30,5,"En Existencia",'LTBR',0,'C',1)
			pdf.cell(30,5,"Requerimiento",'LTBR',1,'C',1)
			
			pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
			i = i + 1
			
		pdf.ln(47)
		#pdf.write(30,"Total")
		pdf.set_font('Arial','B',11)
		pdf.cell(70,7,"Solicitado por:",'LTBR',0,'C',0)
		pdf.cell(70,7,"Recibido por:",'LTBR',0,'C',0)
		pdf.cell(70,7,"Revisado por Compras:",'LTBR',1,'C',0)
		
		pdf.cell(70,7,"",'LTBR',0,'C',0)
		pdf.cell(70,7,"",'LTBR',0,'C',0)
		pdf.cell(70,7,"",'LTBR',1,'C',0)
		
		pdf.cell(70,7,"Fecha:",'LTBR',0,'L',0)
		pdf.cell(70,7,"Fecha:",'LTBR',0,'L',0)
		pdf.cell(70,7,"Fecha:",'LTBR',1,'L',0)
		
		pdf.cell(70,7,"Firma:",'LTBR',0,'L',0)
		pdf.cell(70,7,"Firma:",'LTBR',0,'L',0)
		pdf.cell(70,7,"Firma:",'LTBR',1,'L',0)
		
		dia   = time.strftime('%d')
		mes   = time.strftime('%B')
		ano  = time.strftime('%Y')
		fechas = dia+" de "+mes+" "+ano
		
		title = "Solicitud de (Servicios, Tecnologico) (Area Solicitante "+solicitante.encode('UTF-8').replace('/',"-")+") ("+fechas+").pdf"
		
		pdf.output('openerp/addons/gestion_compras/reportes/'+title,'F')
		documento = open('openerp/addons/gestion_compras/reportes/'+title) # Apertura del documento
        
		# Guardamos el archivo pdf en gestion.eventos
		self.pool.get('adjunto.documento').create(cr, uid, {
		    'name': title,
		    'res_name': title,
		    'datas': base64.encodestring(documento.read()),
		    'datas_fname': title,
		    'res_model': 'gestion.eventos (Gestión de Eventos)',
		    'description': title,
		    'item': "materiales",
		    }, context=context)
		
	######################################################################################	
	# METODO PARA LA GENERACION DE CORRELATIVO (ELEMENTO DE IDENTIFICACION)
	######################################################################################
	#Método para generar el número correlativo de el modelo purchase_request (Compras)
	def _generacion_correlativo(self, cr, uid, ids, context=None):
		
		ano         = time.strftime('%y') # Elemento para la captura de año actual del servidor			
		cr.execute("SELECT count(*) as nombre FROM comp_solicitud") # Consultamos a la base purchase_request
		num_orden   = cr.fetchone()[0]
		correlativo = ano+''+str(num_orden+1).zfill(6)
		return correlativo
	######################################################################################
	_columns = {
            # Compras Solicitud
            'solicitante' : fields.many2one('stock.location','Area Solicitante',required=True),
            'nombre': fields.char(string="Nombre de referencia", size=100, required=True),
	    'limpieza' : fields.boolean(string="Limpieza"),
	    'servicios' : fields.boolean(string="Servicios"),
	    'papeleria' : fields.boolean(string="Papeleria"),
	    'tecnologico' : fields.boolean(string="Tecnologico"),
	    'otros' : fields.boolean(string="Otros"),
	    'material_ids': fields.one2many('purchase.materiales', 'materiales_id', string='Materiales Limpieza / Papelería'), # LISTA DE MATERAILES (LIMPIEZA/ PAPELERIA / OTROS)
	    'material_p_ids': fields.one2many('purchase.s.p.t', 'materiales_p_id', string='Productos Servicios / Tecnológico'),
	    'user': fields.many2one('res.users', 'Registrado por:', readonly=True),
	    'fecha' : fields.date(string = "Fecha", required = True),
	    'observaciones' :  fields.text(string="Observaciones", size=256, required=False),
            'item' : fields.selection([('limpieza','Limpieza'),('servicios','Servicios Generales'),('papeleria','Papelería'),('tecnologico','Tecnológico'),('otros','Otros')], string="Tipo de Material", required=True),
	}
	######################################################################################

	_defaults = {
		'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
		'fecha': lambda *a: time.strftime("%Y-%m-%d"),
		'nombre': _generacion_correlativo,
	}

# Clase para los materiales de compras (Solicitud Directa)

class solicitud_material(osv.Model):

	_name = "purchase.materiales"
	
	# Metodo para traer las especificaciones de los materiales
	def search_materiales(self, cr, uid, ids, argument_search, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('materiales.almacen')
		
		#======================== Busqueda por código ============================

		search_obj_code = obj_dp.search(cr, uid, [('id','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		
		print "hola mundo: "+str(datos_code)
		#=========================================================================
		if not datos_code:
			
			values.update({
				
				'tipo' : None,
				'unidad' : None,
				})
		
		else:
			
			values.update({
				
				'tipo' : datos_code[0]['t_materiales'],
				'unidad' : datos_code[0]['unidad'],
				})
		
		return {'value' : values}
	
	# COLUMNAS PARA LA LISTA DE MATERIALES DE SOLICITUD
	_columns = {
		'materiales_id':fields.many2one('comp.solicitud', 'material_ids', ondelete='cascade', select=False),
		'cantidad' : fields.char(string="Cantidad", required=True),
		'tipo' : fields.selection([('Limpieza','Limpieza'),('Oficina','Oficina'),('Otros','Otros')], string="Tipo de Material", required=True),
		'descripcion':fields.many2one('materiales.almacen', 'Descripción del Material',required=True),
		'unidad' : fields.many2one('product.uom', 'Unidad de Medida', required=True),
		'modelo' : fields.char(string="Modelo", required=False),
		'marca'  : fields.char(string="Marca", required=True),
		'foto_referencial' : fields.binary("Foto Referencial",help="Foto Referencial"),
	}
	
#######################################################################################################
# Clase para la seleccion  de Servicios Generales / Tecnológicos

class solicitud_servicios_g_tecnologico(osv.Model):

	_name = "purchase.s.p.t"
	
	# Metodo para traer las especificaciones de los Productos Solicitados Por la Unidad Solicitante Directo a Compras
	def search_productos(self, cr, uid, ids, argument_search, context=None):

		values = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('product.product')
		
		#======================== Busqueda por código ============================
		search_obj_code = obj_dp.search(cr, uid, [('id','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		#=========================================================================
		if not datos_code:
			
			values.update({
				
				'n_identificacion' : None, # Numero de identificacion
				})
		else:
			values.update({
				
				'n_identificacion' : datos_code[0]['nidentificacion'], # Numero de identificacion
				})
		return {'value' : values}
	
	# COLUMNAS PARA LA LISTA DE MATERIALES DE SOLICITUD / Servicios Generales / Tecnológico
	_columns = {
		'materiales_p_id': fields.many2one('comp.solicitud', 'material_p_ids', ondelete='cascade', select=False),
		'descripcion':fields.many2one('product.product', 'Descripción del Producto',required=True),
		'cantidad' : fields.char(string="Cantidad", required=True),
		'modelo' : fields.char(string="Modelo", required=False),
		'marca'  : fields.char(string="Marca", required=True),
		'tipo' : fields.selection([('Servicio','Servicios Generales'),('tecnologico','Tecnológico')], string="Tipo", required=True),
		'n_identificacion' : fields.char(string="N° de identificación", required=True),
		
	}
#######################################################################################################

# METODOS GLOBALES

def acento(cadena):
	result = cadena.encode('UTF-8').decode('UTF-8') # INSTITUCION
	return result

# Metodo global para fechas
def fecha(fecha):
	date = fecha.split("-")
	nueva_fecha = date[2]+"/"+date[1]+"/"+date[0]
	return nueva_fecha

# Metodo global para redondear
def decimal(cadena):
	salida = "%.2f" % round(cadena,2)
	return salida


