# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields
import os
from openerp.tools.translate import _
import base64#Necesario para la generación del .txt

import orden_de_pago
import class_pdf

class OrdenPago(osv.Model):
	_name = "tesoreria.ordenpago"
	
	_order = "num_pago"
	
	_rec_name = "num_pago"
	
	#Función para pasar a estado de Ordenado----------------------------------------------
	def action_ordenar(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'ejecutado'}, context=context)	
		
	#Función para pasar a estado de Anulado----------------------------------------------
	def action_anular(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'anulado'}, context=context)	
	
	#MÉTODO PARA GENERAR EL NÚMERO CORRELATIVO
	def _gen_correlativo(self, cr, uid, ids, context=None):
		
		cr.execute("SELECT count(*) as num_orden FROM tesoreria_ordenpago")
		num_orden = cr.fetchone()[0]
		
		anyo = time.strftime("%y")
		
		valor_num_orden = anyo+str(num_orden+1).zfill(6)
		
		return valor_num_orden
		
	
	#MÉTODO DE CARGA DE LA CÉDULA Y NOMBRE DE UN BENEFICIARIO###############################################
	def carga_benef(self, cr, uid, ids, flag, valor, context=None):
		
		if not valor:
			return False
		
		values = {}
		
		model_beneficiarios = self.pool.get("res.partner")		
		
		if flag == '1':
			#~ print "Código de la acción: "+cod_acc
			#Consultamos el identificador de la acción según un código indicado
			cr.execute("SELECT id FROM res_partner WHERE cedula_rif='"+str(valor)+"'")
			
			try:
				id_benef = cr.fetchone()[0] #Si existe
			except:
				id_benef = 0 #Si no existe
				
			#Navegamos el modelo usando el id obtenido
			if id_benef > 0:
				#~ nav_model_beneficiarios = model_beneficiarios.browse(cr,uid,id_benef,context=context)
				#~ id_benef = nav_model_beneficiarios.id
				
				values.update({'beneficiario':id_benef})
				
		elif flag == '2':
			nav_model_beneficiarios = model_beneficiarios.browse(cr,uid,valor,context=context)
			cedula_benef = nav_model_beneficiarios.cedula_rif
			
			values.update({'ced_rif_ben':cedula_benef})
			
		return {'value':values}
		
	
	#MÉTODO PARA CARGAR LA INFORMACIÓN CORRESPONDIENTE A UNA REQUISICIÓN
	def carga_compromiso(self, cr, uid, ids, tipo_comp, numero_comp, context=None):
		
		#Valores a retornar
		values = {}
		mensaje = {}
		
		#~ Modelo de compromisos presupuestarios (Presupuesto)
		model_compromiso = self.pool.get("presupuesto.compromiso")
		
		if tipo_comp and numero_comp:
			#Consultamos el identificador de una solicitud de compras según un número correlativo indicado
			cr.execute("SELECT id FROM presupuesto_compromiso WHERE tipo_doc="+str(tipo_comp)+" AND num_compromiso='"+str(numero_comp)+"'")
		else:
			mensaje = {'title':'Selección','message':'Disculpe, debe seleccionar el tipo y número de compromiso'}
		
		try:
			id_compromiso = cr.fetchone()[0] #Si existe
		except:
			id_compromiso = 0 #Si no existe
		
		print id_compromiso
		
		#Navegamos el modelo usando el id obtenido
		if id_compromiso > 0:
			nav_comp = model_compromiso.browse(cr,uid,int(id_compromiso),context=context)
			#~ print nav_comp.observacion + " " +str(nav_comp.ced_rif_ben)
			
			#Datos del compromiso presupuestario
			compromiso_id = nav_comp.id
			observacion = nav_comp.observacion
			cedula_ben = nav_comp.ced_rif_ben
			nom_ben = nav_comp.beneficiario.id
			unidad = nav_comp.unidad_solicitante.id
			requisicion = nav_comp.requisicion #Requisición
			f_requisicion = nav_comp.fecha_req #Fecha de requisición			
			
			values.update({
				'observacion' : observacion,
				'ced_rif_ben' : cedula_ben,
				'beneficiario' : nom_ben,
				'unidad_solicitante' : unidad,
				'requisicion' : requisicion,
				'fecha_req' : f_requisicion,
			})
			
		else:
			#Actualización de los campos
			values.update({
				'observacion' : '',
				'ced_rif_ben' : '',
				'beneficiario' : False,
				'unidad_solicitante' : False,
				'requisicion' : '',
				'fecha_req' : False,
			})
		
		return {'value':values,'warning':mensaje}
		
	
	#CARGAR LOS MOVIMIENTOS DEL COMPROMISO INDICADO
	def carga_compromiso_mov(self, cr, uid, ids,context=None):
		
		mensaje = {}
		
		#Modelo actual
		for orden in self.browse(cr, uid, ids, context=None):
			id_orden = orden.id
			num_orden = orden.num_pago
			tipo_comp = orden.tipo_compromiso.id
			numero_comp = orden.num_compromiso
			#~ print "Orden de pago: "+str(id_orden)+"-"+str(num_orden)
		
		if tipo_comp and numero_comp:
			#Consultamos el identificador de una solicitud de compras según un número correlativo indicado
			cr.execute("SELECT id FROM presupuesto_compromiso WHERE tipo_doc="+str(tipo_comp)+" AND num_compromiso='"+str(numero_comp)+"'")
		else:
			#~ mensaje = {'title':'Selección','message':'Disculpe, debe seleccionar el tipo y número de compromiso'}
			raise osv.except_osv(_("Warning!"), _("Disculpe, debe seleccionar el tipo y número de compromiso"))
		
		try:
			id_compromiso = cr.fetchone()[0] #Si existe
		except:
			id_compromiso = 0 #Si no existe
		
		print "Id encontrado: "+str(id_compromiso)
		
		#Navegamos el modelo usando el id obtenido
		if id_compromiso > 0:
			#~ Modelo de compromisos presupuestarios (Presupuesto)
			model_compromiso = self.pool.get("presupuesto.compromiso")
			#~ Modelo de compromisos presupuestarios de tesorería
			model_compromiso_t = self.pool.get("tesoreria.compromisos")
			
			nav_comp = model_compromiso.browse(cr,uid,int(id_compromiso),context=context)
			#~ print nav_comp.observacion + " " +str(nav_comp.ced_rif_ben)
			
			movimientos = nav_comp.movimientos #Lista de partidas incluidas en el compromiso
		
			print "Movimientos: "+str(movimientos)
			num = 1
			if movimientos:
				#Carga de la(s) partida(s) correspondiente en la orden
				for mov in movimientos:
					# validación para determinar si una partida ya ha sido cargada en la orden actual
					search_compromiso = model_compromiso_t.search(cr, uid, [('partida','=',mov.partida),('orden','=',id_orden)], count=False)
					if not search_compromiso:
						id_ord = model_compromiso_t.create(cr, uid, {
							'orden': id_orden, 
							'n_doc': '',
							'num_compromiso': num_orden,
							'proyec_acc': mov.proyec_acc,
							'partida': mov.partida,
							'desc_partida': mov.desc_partida,
							'monto_causar': class_pdf.decimal(mov.monto_mov),
							'monto_emitir': class_pdf.decimal(mov.monto_mov),
						}, context=context)
						num += 1
					else:
						print "La partida ya ha sido cargada..."
						
			else:
				#~ mensaje = {'title':'Compromisos','message':'La certificación no tiene compromisos asignados'}
				raise osv.except_osv(_("Warning!"), _("La certificación no tiene compromisos asignados"))
				
		elif id_compromiso == 0:
			#~ mensaje = {'title':'Certificación','message':'La certificación indicada no existe'}
			raise osv.except_osv(_("Warning!"), _("La certificación indicada no existe"))
					
	
	
	#MÉTODO DE GENERACIÓN DE REPORTES DE ORDENES DE PAGO
	def reportes_ordenes(self, cr, uid, ids, context=None):
		#~ print "Hola mundo"
		#Navegamos el modelo actual
		browse_id = self.browse(cr, uid, ids, context=context)
		
		diccionario = {}
		
		for campo in browse_id: #Navegamos el modelo para preparar los campos
			orden_id = campo.id
			#~ tipo_doc_id = campo.tipo_doc.id
			#~ tipo_doc_name = campo.tipo_doc.tipo_doc
			num_pago = campo.num_pago
			fecha_pago = campo.fecha_pago
			observacion = campo.observacion
			cedula = campo.ced_rif_ben
			beneficiario_id = campo.beneficiario.id
			beneficiario_name = campo.beneficiario.name
			cedula_cesionado = campo.ced_rif_ces
			nombre_cesionado = campo.cesionado
			#~ cod_oficio = campo.cod_oficio
			#~ fecha_oficio = campo.fecha_oficio 
			#~ unidad_id = campo.unidad_solicitante.id
			#~ unidad_name = campo.unidad_solicitante.name
			#~ cod_proyecto = campo.proyec_acc
			#~ proyecto = campo.cons_proyec_acc
			#~ cod_presu = campo.cod_presu
			#~ partida = campo.part_presu
			#~ monto = campo.monto_mov
			#~ disponibilidad = campo.disponibilidad
			compromisos = campo.compromisos
			
			#~ 
			#Construimos un diccionario con los valores de los campos preparados
			diccionario = { 
				'id' : orden_id, 
				#~ 'tipo_doc_id' : tipo_doc_id, 
				#~ 'tipo_doc_name' : tipo_doc_name, 
				'num_pago' : num_pago,
				'fecha_pago' : fecha_pago,
				'observacion' : observacion,
				'cedula' : cedula,
				'beneficiario_id': beneficiario_id,
				'beneficiario_name': beneficiario_name,
				'cedula_cesionado': cedula_cesionado,
				'nombre_cesionado': nombre_cesionado,
				#~ 'cod_oficio' : cod_oficio,
				#~ 'fecha_oficio' : fecha_oficio,
				#~ 'unidad_id' : unidad_id,
				#~ 'unidad_name' : unidad_name,
				#~ 'cod_proyecto' : cod_proyecto,
				#~ 'proyecto' : proyecto,
				#~ 'cod_presu' : cod_presu,
				#~ 'partida' : partida,
				#~ 'monto' : monto,
				#~ 'disponibilidad' : disponibilidad,
				'compromisos' : compromisos
			}
		
		nom, archivo = orden_de_pago.gen_orden(diccionario)
		
		#Registro del archivo de reporte en la base de datos
		id_att = self.pool.get('ir.tesoreria').create(cr, uid, {
			'orden_id': orden_id, 
			'name': nom,
			'res_name': nom,
			'datas': base64.encodestring(archivo.read()),
			'datas_fname': nom,
			'res_model': 'tesoreria.ordenpago',
		}, context=context)
		
		return True
		

	_columns = {
		'stage_id' : fields.selection((('borrador','Borrador'),('ejecutado','Ejecutado'),('anulado','Anulado')),"Estado", required = True),
		'tipo_pago' : fields.selection((('1','SELECCIONE'),('ORDEN DE PAGO','ORDEN DE PAGO')),"Tipo pago", required = True),
		'num_pago' : fields.char(string="Número", size = 8, required = True),
		'fecha_pago': fields.date(string = "Fecha", required = True),
		'ced_rif_ben' : fields.char(string="Cédula o Rif del Beneficiario", required = False), #Cédula o RIF del beneficiario
		'ced_rif_ces' : fields.char(string="Cédula o Rif del Cesionado", required=False), #Cédula o RIF del cesionado
		'beneficiario' : fields.many2one("res.partner", "Beneficiario", required = False),
		'cesionado' : fields.char(string="Nombre del Cesionado Autorizado a Cobrar", required = False),
		'unidad_solicitante' : fields.many2one('stock.location', "Unidad Solicitante", required = False),
		'requisicion' : fields.char(string="Requisición", required = False),
		'fecha_req' : fields.date(string="Fecha Requisición", required = False), #Fecha de la requisición
		'observacion' : fields.text(string="Observación", required = False),
		#Segunda sección
		'tipo_compromiso' : fields.many2one("presupuesto.tipodoc", "Tipo Compromiso", required = True),
		'num_compromiso' : fields.char(string="Número Compromiso", size = 8, required = True),
		'compromisos' : fields.one2many("tesoreria.compromisos", "orden", required = False),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]
	
	_defaults = {
		'stage_id' : 'borrador',
		'tipo_pago' : 'ORDEN DE PAGO',
		'num_pago' : _gen_correlativo,
		'tipo_compromiso' : 1,
		'fecha_pago' : lambda *a: time.strftime("%Y-%m-%d"),
	}
