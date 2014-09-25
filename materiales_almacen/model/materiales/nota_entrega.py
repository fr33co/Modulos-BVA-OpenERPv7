# -*- coding: utf-8 -*-
import class_pdf
import time
import base64
import random
import unicodedata
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta
from openerp.tools.translate import _

class nota_de_entrega(osv.Model):

	_name = "nota.entrega"
	
	_rec_name = "c_nota"
	
	# Acciones de cada uno de los botones de la barra de estado de solicitud
	#def action_exportar(self, cr, uid, ids, context = None):
	#	return self.write(cr, uid, ids, {'generar':'Atendida'}, context=context)
	#
	#def action_confirmar(self, cr, uid, ids, context = None):
	# 	return self.write(cr, uid, ids, {'generar':'Confirmado'}, context=context)
	#
	#def action_borrador(self, cr, uid, ids, context = None):
	# 	return self.write(cr, uid, ids, {'generar':'Borrador'}, context=context)
	"""
	Metodo que me genera un correlativo unico por nota de entrega buscando el ultimo registro y
	sumandole 1.
	"""

	def _get_last_id(self, cr, uid, ids, context = None):

                correlativo_n_entrega = ""        
			
		cr.execute("SELECT count(*) as num_nota_entrega FROM nota_entrega")
		num_nota_entrega = cr.fetchone()[0]
			
		#anyo = time.strftime("%Y")
			
		correlativo_n_entrega = str(num_nota_entrega+1).zfill(6)
				
		return correlativo_n_entrega
	
	"""
	Metodo que trae la informacion de las solicitud de Materiales de la clase solicitud_materiales
	al formulario de Nota de Entrega.
	"""
	def on_change_datos(self, cr, uid, ids, c_solicitud, context=None):
		values = {}
		if not c_solicitud:
		    return values
		datos = self.pool.get('solicitudes.materiales').browse(cr, uid, c_solicitud, context=context)
		values.update({
			'area' : datos.area.id,
			'solicitado' : datos.user_register.id,
			'limpieza' : datos.limpieza,
			's_generales' : datos.s_generales,
			'oficina_papeleria' : datos.oficina_papeleria,
			'tecnologico' : datos.tecnologico,
			'otros' : datos.otros,

		})
		return {'value' : values}
	
	def rechasar(self, cr, uid, ids, context=None):
		obj = self.browse(cr, uid, ids, context=None)
		pest_obser = self.pool.get('solicitudes.materiales')
		observaciones_sol = self.browse(cr, uid, ids)[0]
		for pro in obj:
			read_soli = pest_obser.read(cr, uid, pro.c_solicitud.id, context=context)
			codigo_id = read_soli['correlativo']
			observaciones = observaciones_sol.observaciones
			estatus = '3'
			self.write(cr, uid, ids, {'estatus':'2'}, context=context)
			cr.execute("UPDATE solicitudes_materiales SET estatus=%s, observaciones=%s WHERE correlativo=%s ;", (estatus, observaciones, codigo_id))
		return True
	
	"""
	Metodo
	"""
	def procesar(self, cr, uid, ids, context=None): # Generacion de inventario
		
		obj_bva      = self.pool.get('materiales.bva') # Objeto 
		inventario  = self.pool.get('inventario.materiales') # Objeto 
		
		read_one = self.read(cr, uid, ids, context=context)[0]
		id_read_one = read_one['mate_nota'] # Grupo de IDS

		search_id  = obj_bva.search(cr, uid, [('id','=',id_read_one)], context=None) # Se busca el ID dado
		read_id  = obj_bva.read(cr,uid,search_id,context=context) # Se refleja el resultado
		
		obj = self.browse(cr, uid, ids, context=None)
		consu_estatus = self.pool.get('solicitudes.materiales')
		estatus_sol = self.browse(cr, uid, ids)[0]
		for y in obj:
		    read_soli = consu_estatus.read(cr, uid, y.c_solicitud.id, context=context)
		    codigo_id = read_soli['correlativo']
		    estatus = '4'
		    self.write(cr, uid, ids, {'estatus':'3'}, context=context)

		for x in read_id:

			id_m_bva = x['descripcion'][0]
			cantidad_bva = x['cantidad']
			
			
			search_inv  = inventario.search(cr, uid, [('descripcion','=',id_m_bva)], context=None) # Se busca el ID dado
			materiales  = inventario.read(cr,uid,search_inv,context=context) # Se refleja el resultado
			
			for m in materiales:

				cantidad_materiales = m['cantidad']

				id_m_desc = m['descripcion'][0]

				
			resta_valor  =  int(cantidad_materiales) - int(cantidad_bva)


			
			if int(cantidad_bva) > int(cantidad_materiales):
				raise osv.except_osv(_("Warning!"), _("Disculpe no puede seleccionar una cantidad mayor a la que hay en existencia"))
			else:
				cr.execute("UPDATE inventario_materiales SET cantidad=%s WHERE descripcion=%s;", (resta_valor, id_m_desc))	
				cr.execute("UPDATE solicitudes_materiales SET estatus=%s WHERE correlativo=%s ;", (estatus, codigo_id))
		return True
	
	"""
	Metodo 
	"""

	def cargar_cantidades(self, cr, uid, ids, context=None): # Asignacion de laa Quiincena a los Emplea,dos

		for x in self.browse(cr, uid, ids, context=context):
			#Capturo los id del modelo y del correlativo de la solicitud
			sol_id_mod = x.id
			sol_id_sol = x.c_solicitud.correlativo
			
			"""
			LLamo a la clase del modelo solicitudes_materiales para capturar el id del one2many
			(tabla que contine la descripcion y la cantidad solicitada).
			"""
			sol_get     = self.pool.get('solicitudes.materiales') # Objeto solicitud_materiales (Solicitud de Materiales por parte de las gerencias)
			datos       = sol_get.search(cr, uid, [('correlativo','=',sol_id_sol)], context=None) # 
			materiales  = sol_get.read(cr,uid,datos,context=context) # Lectura modo array del objecto

			for m in materiales:
				
				almacen_id = m['almacen']
				
				"""
				#Con el Id del one2many llamo a la clase solicitud_materiales donde se guardan los datos de que
				material y cantidad las  gerencias solicitan.
				"""
				get_mat       = self.pool.get('solicitud.materiales') # Objeto solicitud_materiales (Solicitud de Materiales por parte de las gerencias)
				datos_m       = get_mat.search(cr, uid, [('id','=',almacen_id)], context=None) # 
				mat           = get_mat.read(cr,uid,datos_m,context=context) # Lectura modo array del objecto

				for s in mat:
					
					descrip  = s['descripcion'][0] #Capturo el ID de la descripcion del material
					descip_messa = s['descripcion'][1]
					cantidad = s['cantidad'] #Capturo la cantidad en base al material seleccionado
					unidad   = s['unidad'][0] #Capturo el ID de la unidad de medida del material
					
					
					values = {}
					mensaje ={}
					if not descrip:
						return values
					"""
					llamo a la clase inventario_materiales donde obtengo las cantidades en existencia
					en base a la descripcion de los materiales en el almacen de la unidad de Bienes y
					Suministros de la institución.
					"""
					datos = self.pool.get('inventario.materiales')
					variable = datos.search(cr, uid, [('descripcion','=',descrip)], context=None)
					rd_id  = datos.read(cr, uid, variable, context=None)
						
					#try:
					existencia = rd_id[0]['cantidad']
					#except:
					#	#raise osv.except_osv(_("Warning!"), _("Disculpe el o los elementos "+descip_messa+" No han sido inventariados"))
					#	existencia = 0.00
						
					"""
					Realizo una busqueda en la tabla materiales_bva del one2many dentro en el modelo
					nota de entrega.
					"""
					id_registros = self.pool.get('materiales.bva')
					busqueda = id_registros.search(cr, uid, [('descripcion','=',descrip),('materiales_id','=',sol_id_mod)], count=False)
					
					#Validacion para que no me repita los registros en el one2many
					#Si los atributos ya estan en la busqueda los descarte, de lo contrario q los cree
					if busqueda:
						return False
					else:
						# Guardamos la data en la tabla del one2many
						self.pool.get('materiales.bva').create(cr, uid, {
							'materiales_id': sol_id_mod,
							'descripcion': descrip,
							'cantidad': cantidad,
							'cantidad_stock' : existencia,
							'unidad' : unidad,
							}, context=context)
					

	def generar_nota_entrega(self, cr, uid, ids, context=None): # Generacion de inventario
		# Instancia de la clase heredada L es horizontal y P es vertical
		
		pdf=class_pdf.PDF3(orientation='P',unit='mm',format='letter' ) #HORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Marcel Arcuri')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		pdf.set_font('Arial','B',10)
		pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		pdf.set_margins(20,10,10) # MARGENE DEL DOCUMENTO
		#pdf.ln(20) # Saldo de linea
		# 10 y 50 eje x y y 200 dimencion
		#pdf.line(10, 40, 200, 40) Linea
		
		
		prueba = self.browse(cr, uid, ids, context=context)
		pdf.ln(8)
		
		for x in prueba:
			codigo = x.c_nota
			ubi = x.area.name.encode("UTF-8").decode("UTF-8")
			fecha = x.fecha
			solic = x.solicitado.name
			reciv = x.recibido.name
			#nombre_n =x.nombre
			if x['limpieza'] == True:
				lim = 'X'
			else:
				lim = ''
			if x['s_generales'] == True:
				ser = 'X'
			else:
				ser = ''
			if x['oficina_papeleria'] == True:
				ofi = 'X'
			else:
				ofi = ''
			if x['tecnologico'] == True:
				tec = 'X'
			else:
				tec = ''
			if x['otros'] == True:
				otro = 'X'
			else:
				otro = ''
	
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',10)
			pdf.cell(150,6,"",'',0,'L',1)
			pdf.cell(20,6,"N° ".decode("UTF-8")+codigo,'LTBR',1,'L',1)
			pdf.ln(5)
			
			pdf.set_font('Arial','B',14)

			pdf.cell(180,5,"Nota de entrega",'',1,'C',1)
			pdf.ln(5)
			
			pdf.set_font('Arial','B',10)
			pdf.cell(120,6,"Área Solicitante: ".decode("UTF-8")+ubi,'LTBR',0,'L',1)
			pdf.cell(60,6,"Fecha: "+fecha ,'LTBR',1,'L',1)
			pdf.ln(5)
			
			pdf.set_font('Arial','B',10)
			pdf.cell(40,6,"Materiales",'LTBR',1,'C',1)
			pdf.set_font('Arial','B',10)
			pdf.cell(40,5,"Limpieza:",'LTBR',0,'L',1)
			pdf.cell(10,5,lim,'LTBR',1,'C',1)
			pdf.cell(40,5,"Servicios Generales:",'LTBR',0,'L',1)
			pdf.cell(10,5,ser,'LTBR',1,'C',1)
			pdf.cell(40,5,"Oficina o papeleria:",'LTBR',0,'L',1)
			pdf.cell(10,5,ofi,'LTBR',1,'C',1)
			pdf.cell(40,5,"Tecnológico:".decode("UTF-8"),'LTBR',0,'L',1)
			pdf.cell(10,5,tec,'LTBR',1,'C',1)
			pdf.cell(40,5,"Otros:",'LTBR',0,'L',1)
			pdf.cell(10,5,otro,'LTBR',1,'C',1)
			pdf.ln(5)
			fec_2 = str(x['fecha'])
			
			# Fila de la cabezara de la tabla

			pdf.cell(15,5,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(25,5,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(140,5,"Descripción del Material".decode("UTF-8"),'LTBR',1,'C',1)
		# Fin Cabezera
		pdf.set_font('Arial','',10) # TAMANO DE LA FUENTE
		
		data_ids = self.read(cr, uid, ids, context=context)[0]
		payslip_id = data_ids['mate_nota'] # Grupo de IDS

		alm = self.pool.get('materiales.bva') # Objeto 
		datos = alm.search(cr, uid, [('id','=',payslip_id)], context=None)
		bienes = alm.read(cr,uid,datos,context=context)
		
		k = 0
		j = 0
		item = 0
		for i in bienes:
			if j == 25:
				
				pdf.add_page()
				pdf.ln(8)
				pdf.set_fill_color(255,255,255)
				pdf.set_font('Arial','B',10)
				pdf.cell(150,6,"",'',0,'L',1)
				pdf.cell(20,6,"N° ".decode("UTF-8")+codigo,'LTBR',1,'L',1)
				pdf.ln(5)
				
				pdf.set_font('Arial','B',12)
				pdf.cell(180,5,"Nota de entrega",'',1,'C',1)
				pdf.ln(5)
				
				pdf.set_font('Arial','B',10)
				pdf.cell(13,6,"",'',0,'L',1)
				pdf.cell(120,6,"Área Solicitante: ".decode("UTF-8")+ubi,'LTBR',0,'L',1)
				pdf.cell(60,6,"Fecha: "+fecha ,'LTBR',1,'L',1)
				pdf.ln(5)
				
				pdf.set_font('Arial','B',10)
				pdf.cell(40,6,"Materiales",'LTBR',1,'C',1)
				pdf.set_font('Arial','B',10)
				pdf.cell(40,5,"Limpieza:",'LTBR',0,'L',1)
				pdf.cell(10,5,lim,'LTBR',1,'C',1)
				pdf.cell(40,5,"Servicios Generales:",'LTBR',0,'L',1)
				pdf.cell(10,5,ser,'LTBR',1,'C',1)
				pdf.cell(40,5,"Oficina o papeleria:",'LTBR',0,'L',1)
				pdf.cell(10,5,ofi,'LTBR',1,'C',1)
				pdf.cell(40,5,"Tecnológico:".decode("UTF-8"),'LTBR',0,'L',1)
				pdf.cell(10,5,tec,'LTBR',1,'C',1)
				pdf.cell(40,5,"Otros:",'LTBR',0,'L',1)
				pdf.cell(10,5,otro,'LTBR',1,'C',1)

				pdf.ln(5)
				# Fin Cabezera
				j=0
			
			# Filas que vienen de la BD
			item = int(item) + 1
			unidad = str(i['unidad'][0])
			if unidad == "11":
				unid = "Lt"
			else:
				unid = ""
			if unidad == "3":
				unid = "Kg"
			else:
				unid = ""

			pdf.set_font('Arial','',10)
			pdf.cell(15,5,str(item).decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(25,5,str(i['cantidad'])+" "+unid,'LTBR',0,'C',1)
			pdf.cell(140,5,i['descripcion'][1].encode("UTF-8").decode("UTF-8"),'LTBR',1,'L',1)

			if k == 24 : 
				pdf.ln(5)
				pdf.set_font('Arial','B',10)
				pdf.cell(90,6,"ENTREGADO",'LTBR',0,'C',0)
				pdf.cell(90,6,"SOLICITANTE",'LTBR',1,'C',1)
				
				pdf.cell(90,6,"Entregado por: "+reciv.decode("UTF-8"),'LTBR',0,'L',0)
				pdf.cell(90,6,"Recibido por: "+solic.decode("UTF-8"),'LTBR',1,'L',1)
				
				pdf.cell(90,6,"Fecha: ",'LTBR',0,'L',0)
				pdf.cell(90,6,"Fecha: ",'LTBR',1,'L',1)
				
				pdf.cell(90,6,"Firma:",'LTBR',0,'L',0)
				pdf.cell(90,6,"Firma:",'LTBR',1,'L',1)
			
			# pdf.set_font('Arial','',8) # TAMANO DE LA FUENTE
				k = 0

			k = k+1
			j =j+1
			
		pdf.ln(5)
		pdf.set_font('Arial','B',10)
		pdf.cell(90,6,"ENTREGADO",'LTBR',0,'C',0)
		pdf.cell(90,6,"SOLICITANTE",'LTBR',1,'C',1)
		
		pdf.cell(90,6,"Entregado por: "+reciv.decode("UTF-8"),'LTBR',0,'L',0)
		pdf.cell(90,6,"Recibido por: "+solic.decode("UTF-8"),'LTBR',1,'L',1)
		
		pdf.cell(90,6,"Fecha: ",'LTBR',0,'L',0)
		pdf.cell(90,6,"Fecha: ",'LTBR',1,'L',1)
		
		pdf.cell(90,6,"Firma:",'LTBR',0,'L',0)
		pdf.cell(90,6,"Firma:",'LTBR',1,'L',1)

		nom = "Nota de Entrega"+codigo+'.pdf'
		pdf.output('openerp/addons/materiales_almacen/reportes/'+nom)
		#pdf.output('/home/administrador/openerp70/modules/materiales_almacen/reporte/'+nom,'F')
	
		archivo = open('openerp/addons/materiales_almacen/reportes/'+nom)
		#archivo = open('/home/administrador/openerp70/modules/materiales_almacen/reporte/'+nom)
		
		nom = "Nota de Entrega "+codigo+'.pdf' #Nombre del archivo .pdf
		
		r_archivo = self.pool.get('reporte.notas.entregas').create(cr, uid, {
				'name' : nom,
				'res_name' : nom,
				'datas' : base64.encodestring(archivo.read()),
				'datas_fname' : nom,
				'res_model' : 'nota.entrega',
				'tipo_reporte': "Nota de Entrega"
			},context=context)
		
		return r_archivo
	

	_columns = {
		'c_solicitud' : fields.many2one('solicitudes.materiales', 'Código de Solicitud', domain="[('estatus','ilike','2')]", required=True),
		'area' : fields.many2one('stock.location', 'Área Solicitante', required=True),
		'fecha': fields.char('Fecha:', readonly=True,  required=True),
		'observaciones': fields.text('Observaciones', ),
		'mate_nota': fields.one2many('materiales.bva', 'materiales_id', string='Materiales'),
		'solicitado' : fields.many2one('res.users', 'Registrado por:', required=True),
		'recibido' : fields.many2one('res.users', 'Recibido por:', readonly=True),
		'c_nota' : fields.char(string="Correlativo:", size=6, readonly=True, required=True),
		'limpieza' : fields.boolean('Limpieza:'),
		's_generales' : fields.boolean('Servicios Generales:'),
		'oficina_papeleria' : fields.boolean('Oficina Papeleria:'),
		'tecnologico' : fields.boolean('Técnologico:'),
		'otros' : fields.boolean('Otros:'),
		'estatus': fields.selection([('1','Borrador'), ('2','Rechazda'), ('3','Procesada')], string="Estado de Solicitud"),

	}
	_defaults = {
		'fecha': lambda *a: time.strftime("%d-%m-%Y"),
		'c_nota' : _get_last_id,
		'estatus': '1',
		'recibido': lambda s, cr, uid, c: uid,
	}


class materiales_entregar(osv.Model):

	_name = "materiales.bva"
	
	_columns = {
		'materiales_id':fields.many2one('nota.entrega', 'almacen', ondelete='cascade', select=False),
		'cantidad' : fields.integer(string="Cantidad Solicitada", required=True),
		'cantidad_stock' : fields.float(string="Cantidad en existencia", required=False),
		'unidad':fields.many2one('product.uom', 'Unidad de Medida',required=True),
		'descripcion':fields.many2one('materiales.almacen', 'Descripción del Material',required=True),
	}
	
	def on_change_comparar(self, cr, uid, ids, cantidad, cantidad_stock, context=None):
		
		
		if int(cantidad) > int(cantidad_stock):
			raise osv.except_osv(_("Warning!"), _("Disculpe no puede seleccionar una cantidad mayor a la que hay en existencia"))
		return True
