# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
import os
from datetime import date
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
from openerp.osv import fields, osv
import math
from openerp.tools.translate import _
import pdf_class

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
		
		p = proyecto.split('-')
		cod_p   = proyecto[0:2] # CODIGO DEL PROYECTO
		cod_acc = proyecto[3:11] # CODIG DE PROYECTO Y ACCION
		
		print "PROYECTO: "+str(cod_p)
		print "ACCION: "+str(cod_acc)
		
		values = {}
		
		if not proyecto:
			
			return values
		
		# EMISION DE CONSULTA RELACIONAL PARA presupuesto_partidas CON presupuesto_distribucion
		cr.execute('SELECT p.descripcion FROM presupuesto_partidas AS p INNER JOIN presupuesto_distribucion AS d ON p.codigo = d.partida WHERE p.codigo = '"'"+str(proyecto)+"'"' ')
		# REALIZAMOS LA BUSQUEDA SOLO DE UN REGISTRO excepciones en python
		try:
			descripcion   = cr.fetchone()[0]
		except:
			descripcion   = ""
		cr.execute('SELECT d.monto_pre FROM presupuesto_partidas AS p INNER JOIN presupuesto_distribucion AS d ON p.codigo = d.partida WHERE p.codigo = '"'"+str(proyecto)+"'"' ')
		# excepciones en python
		try:
			# REALIZAMOS LA BUSQUEDA SOLO DE UN REGISTRO
			disp          = float(cr.fetchone()[0])
			disponibildad = pdf_class.punto_decimal(str(disp))
		except:
			disp          = 0.00
			disponibildad = pdf_class.punto_decimal(str(disp))
		
		values.update({
			'proyecto' : descripcion,
			'disponibilidad' : disponibildad,
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
	
	def generar_orden(self, cr, uid, ids, context=None):
		print "EMISION DE OREDEN DE COMPRA"
	
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
