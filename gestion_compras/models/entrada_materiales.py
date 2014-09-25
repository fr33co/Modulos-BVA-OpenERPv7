# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

import time # Necesario para las funciones de Fecha
import pdf_class # Llamada de las clases DPF
import base64 
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final

from openerp.osv import osv, fields

class Solicitud(osv.Model):
	_name="comp.entrada.materiales"

	_order = 'nombre'
	
	_rec_name = 'nombre'
	
	# EMITIR SOLICITUD DE MATERIALES DE CADA UNIDAD SOLICITANTE
	def emitir_solicitud_material(self, cr, uid, ids, context=None):
		 
		for s_p in self.browse(cr, uid, ids, context=None):
			model_id          = s_p.id
			fecha_actual      = pdf_class.fecha(s_p.fecha)
			solicitante       = s_p.solicitante.name
			one_2_mamy_pre    = s_p.material_id_compras # ITERACION DEL MODELO
			obs               = s_p.observaciones
			proveedor         = s_p.proveedor.name
			
			# RECORRIDO DE LOS ELEMENTOS DEL ONE_2_MANY MATERIAL_ID_COMPRAS
			####################################################################################
			# Instancia de la clase heredada L es horizontal y P es vertical

			pdf=pdf_class.Solicitud_presupuestaria(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA

			#pdf.set_title(title)
			pdf.set_author('Marcel Arcuri')
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
			pdf.set_font('Arial','B',7)
			pdf.set_y(0)
			pdf.set_x(90)
			pdf.write(30,"REPÚBLICA BOLIVARIANA DE VENEZUELA".decode("UTF-8"))
			pdf.set_y(4)
			pdf.set_x(93)
			pdf.set_font('Arial','',7)
			pdf.write(30,"GOBIERNO BOLIVARIANO DE ARAGUA".decode("UTF-8"))
			pdf.set_font('Arial','B',7)
			pdf.ln(25)

			pdf.set_font('Arial','B',8)
			pdf.cell(165,5,"J-30759058-8".decode("UTF-8"),'',0,'L',1)
			pdf.cell(30,5,"Fecha: ".decode("UTF-8")+str(fecha_actual),'',1,'L',1)
			pdf.ln(5)
			pdf.cell(190,5,"SOLICITUD DE MATERIALES, EQUIPOS Y SERVICIOS".decode("UTF-8"),'',1,'C',1)
			pdf.ln(5)
			pdf.cell(190,5,"UNIDAD SOLICITANTE".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.cell(190,5,"DENOMINACIÓN".decode("UTF-8"),'TB',1,'L',1)
			pdf.multi_cell(190,5,pdf_class.acento(solicitante),'LTBR','J',1)
			pdf.cell(190,5,"DESCRIPCIÓN DE LOS MATERIALES, EQUIPOS Y SERVICIOS SOLICITADOS".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.cell(80,5,"IMPUTAC. PRESUP.".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.set_font('Arial','B',7)
			pdf.cell(20,5,"CANTIDAD".decode("UTF-8"),'LTR',0,'C',1)
			pdf.cell(20,5,"UNIDAD".decode("UTF-8"),'LTR',0,'C',1)
			pdf.cell(70,5,"DESCRIPCIÓN".decode("UTF-8"),'LTR',1,'C',1)
			pdf.set_font('Arial','B',7)
			pdf.cell(20,5,"PART".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"GENER".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"ESPECI".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"SUB-ESPEC".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LBR',0,'C',1)
			pdf.cell(20,5,"".decode("UTF-8"),'LBR',0,'C',1)
			pdf.cell(70,5,"".decode("UTF-8"),'LBR',1,'C',1)


			j = 1
			
			for m_p in one_2_mamy_pre:
				partida  = m_p.part # PARTIDA
				
				part           = partida[0:4]
				general        = partida[5:7]
				especifica     = partida[8:10]
				sub_especifica = partida[11:13]
				cantidad       = m_p.cantidad # CANTIDAD
				unidad         = m_p.unidad.name # UNIDAD
				desc           = m_p.descripcion.descripcion # DECRIPCION DEL MATERIAL SOLICITADO
			
				if j == 20:
					pdf.add_page()
					pdf.set_fill_color(255,255,255)
					pdf.set_font('Arial','B',7)
					pdf.set_y(0)
					pdf.set_x(90)
					pdf.write(30,"REPÚBLICA BOLIVARIANA DE VENEZUELA".decode("UTF-8"))
					pdf.set_y(4)
					pdf.set_x(93)
					pdf.set_font('Arial','',7)
					pdf.write(30,"GOBIERNO BOLIVARIANO DE ARAGUA".decode("UTF-8"))
					pdf.set_font('Arial','B',7)
					pdf.ln(25)
					pdf.set_font('Arial','B',8)
					pdf.cell(165,5,"J-30759058-8".decode("UTF-8"),'',0,'L',1)
					pdf.cell(30,5,"Fecha: ".decode("UTF-8")+str(fecha_actual),'',1,'L',1)
					pdf.ln(5)
					pdf.cell(190,5,"SOLICITUD DE MATERIALES, EQUIPOS Y SERVICIOS".decode("UTF-8"),'',1,'C',1)
					pdf.ln(5)
					pdf.cell(190,5,"UNIDAD SOLICITANTE".decode("UTF-8"),'LTBR',1,'C',1)
					pdf.cell(190,5,"DENOMINACIÓN".decode("UTF-8"),'TB',1,'L',1)
					pdf.multi_cell(190,5,pdf_class.acento(solicitante),'LTBR','J',1)
					pdf.cell(190,5,"DESCRIPCIÓN DE LOS MATERIALES, EQUIPOS Y SERVICIOS SOLICITADOS".decode("UTF-8"),'LTBR',1,'C',1)
					pdf.cell(80,5,"IMPUTAC. PRESUP.".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.set_font('Arial','B',7)
					pdf.cell(20,5,"CANTIDAD".decode("UTF-8"),'LTR',0,'C',1)
					pdf.cell(20,5,"UNIDAD".decode("UTF-8"),'LTR',0,'C',1)
					pdf.cell(70,5,"DESCRIPCIÓN".decode("UTF-8"),'LTR',1,'C',1)
					pdf.set_font('Arial','B',7)
					pdf.cell(10,5,"PART".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(10,5,"GENER".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(10,5,"ESPECI".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(10,5,"SUB-ESPEC".decode("UTF-8"),'LTBR',0,'C',1)
					pdf.cell(20,5,"".decode("UTF-8"),'LBR',0,'C',1)
					pdf.cell(20,5,"".decode("UTF-8"),'LBR',0,'C',1)
					pdf.cell(70,5,"".decode("UTF-8"),'LBR',1,'C',1)
					# Fin Cabezera
					j=0
				
				# Fila de la cabezara de la tabla # Relacion a DB
				pdf.set_font('Arial','',8)
				pdf.cell(20,5,str(part),'LTBR',0,'C',1)
				pdf.cell(20,5,str(general),'LTBR',0,'C',1)
				pdf.cell(20,5,str(especifica),'LTBR',0,'C',1)
				pdf.cell(20,5,str(sub_especifica),'LTBR',0,'C',1)
				pdf.cell(20,5,str(cantidad),'LBR',0,'C',1)
				pdf.cell(20,5,str(unidad),'LBR',0,'C',1)
				pdf.cell(70,5,pdf_class.acento(desc),'LBR',1,'C',1)
				j =j + 1
					

				
			pdf.set_y(228)
			pdf.cell(190,5,"OBSERVACIONES:  "+pdf_class.acento(obs),'LTBR',1,'L',1)
			pdf.cell(190,5,"FIRMA".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.cell(48,5,"SOLICITANTE".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(47,5,"ADMINISTRACIÓN".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(48,5,"COMPRAS".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(47,5,"PRESIDENCIA".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.cell(48,5,"",'LTBR',0,'C',1)
			pdf.cell(47,5,"",'LTBR',0,'C',1)
			pdf.cell(48,5,"",'LTBR',0,'C',1)
			pdf.cell(47,5,"",'LTBR',1,'C',1)
			pdf.cell(190,5,"PROVEEDOR ASIGNADO".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.cell(190,5,pdf_class.acento(proveedor),'LTBR',1,'C',1)


			#~ pdf.output('openerp/addons/gestion_compras/reportes/entrada_materiales/solicitud Materiales Presupuestario.pdf','F')
			####################################################################################
			dia   = time.strftime('%d')
			mes   = time.strftime('%B')
			ano  = time.strftime('%Y')
			fechas = dia+" de "+mes+" "+ano
			
			title = "Solicitud Materiales Presupuestario ("+fechas+").pdf"
			
			pdf.output('openerp/addons/gestion_compras/reportes/entrada_materiales/'+title,'F')
			documento = open('openerp/addons/gestion_compras/reportes/entrada_materiales/'+title) # Apertura del documento
					
			# Guardamos el archivo pdf en comp.entrada.materiales
			self.pool.get('adjunto.documento').create(cr, uid, {
					'name': title,
					'res_name': title,
					'datas': base64.encodestring(documento.read()),
					'datas_fname': title,
					'res_model': 'gestion.eventos (Gesti?n de Eventos)',
					'description': title,
					'item': "",
					}, context=context)
		    
	######################################################################################	
	# METODO PARA LA GENERACION DE CORRELATIVO (ELEMENTO DE IDENTIFICACION)
	######################################################################################
	def _generacion_correlativo(self, cr, uid, ids, context = None):
		
		ano  = time.strftime('%Y') # A?O ACTUAL DEL SISTEMA
		
                obj_solicitud       = self.pool.get('comp.entrada.materiales')
                obj_search          = obj_solicitud.search(cr,uid,[])
                read_obj            = obj_solicitud.read(cr, uid, obj_search, context=context)
                if read_obj:
                    id_documento = read_obj[-1]['nombre']
                    c_nota = id_documento[5:]
                    last_id      = c_nota.lstrip('0')
                    str_number   = str(int(last_id) + 1)
                    last_id      = str_number.rjust(4,'0')
                    codigo      = last_id
                else :
                    str_number = '1'
                    last_id      = str_number.rjust(4,'0')
                    codigo      = last_id
                return str(codigo)+"-"+str(ano)
	######################################################################################
	
	
	
	_columns = {
            # Compras Solicitud
				'solicitante' : fields.many2one('stock.location','Area Solicitante',required=True),
				'nombre': fields.char(string="Nombre de referencia", size=100, required=False),
		    'material_id_compras': fields.one2many('comp.materiales_c', 'materiales_id_m', string='Materiales'),
		    'user': fields.many2one('res.users', 'Registrado por:', readonly=True),
		    'proveedor' : fields.many2one('res.partner', 'Proveedor', required=True),
		    'fecha' : fields.date(string = "Fecha", required = True),
		    'observaciones' :  fields.text(string="Observaciones", size=111, required=True),
				'item' : fields.selection([('limpieza','Limpieza'),('servicios','Servicios Generales'),('papeleria','Papelería'),('tecnologico','Tecnológico'),('otros','Otros')], string="Tipo de Material", required=True),
	}

	_defaults = {
		'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
		'fecha': lambda *a: time.strftime("%Y-%m-%d"),
		#'nombre': _generacion_correlativo,
	}

# Clase para los materiales de compras (Solicitud Directa)

class solicitud_material(osv.Model):

	_name = "comp.materiales_c"
	
	# Metodo para traer las especificaciones de los materiales
	def search_m(self, cr, uid, ids, argument_search, item, context=None): # Proceso de busqueda de un manager(Gerente)
		
		print "ITEMS: "+str(argument_search)
		
		values = {}
		
		if not argument_search:
			
			return values
		
		if str(item) == '1':
		###################################################################################
			obj_dp = self.pool.get('materiales.almacen')
			
			#======================== Busqueda por c?digo ============================
	
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
		###################################################################################
		elif str(item) == '2':
			print "AQUI LLEGA POR PARTIDA.."
			
			obj_c      = self.pool.get('presupuesto.partidas')
			
			#======================== Busqueda por c?digo ============================
	
			search_obj = obj_c.search(cr, uid, [('id','=',argument_search)])
			datos      = obj_c.read(cr,uid,search_obj,context=context)
			
			print "hola mundo: "+str(datos)
			#=========================================================================
			if not datos:
				
				values.update({
					'part' : None,
					})
			else:
				values.update({
					'part' : datos[0]['codigo'],
				})
		###################################################################################
		
		return {'value' : values}
	
	# COLUMNAS PARA LA LISTA DE MATERIALES DE SOLICITUD
	_columns = {
		'materiales_id_m':fields.many2one('comp.entrada.materiales', 'material_id_compras', ondelete='cascade', select=False),
		'cantidad' : fields.char(string="Cantidad", required=True),
		'tipo' : fields.selection((('1','Limpieza'), ('2','Oficina'), ('3','Servicios Generales'), ('4','Tecnológico')),'Tipo de Material', required=False),
		'descripcion':fields.many2one('materiales.almacen', 'Descripcion del Material',required=True),
		'unidad' : fields.many2one('product.uom', 'Unidad de Medida', required=True),
		'modelo' : fields.char(string="Modelo", required=False),
		'marca'  : fields.char(string="Marca", required=False),
		'foto_referencial' : fields.binary("Foto Referencial",help="Foto Referencial"),
		'partida' : fields.many2one('presupuesto.partidas','Partida Presupuestaria',required=False),
		'part' : fields.char(string='Partida',required=False),
	}

######################################################################
def acento(cadena):
	result = cadena.encode('UTF-8').decode('UTF-8') # INSTITUCION
	return result
#####################################################################
# Metodo global para fechas
def fecha(fecha):
	date = fecha.split("-")
	nueva_fecha = date[2]+"/"+date[1]+"/"+date[0]
	return nueva_fecha
#####################################################################
# Metodo global para redondear
def decimal(cadena):
	salida = "%.2f" % round(cadena,2)
	return salida
#####################################################################
