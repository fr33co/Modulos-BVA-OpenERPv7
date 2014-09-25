# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields
import os
from openerp.tools.translate import _
import base64#Necesario para la generación del .txt

class Cheques(osv.Model):
	_name = "tesoreria.cheques"
	
	#~ _order = "num_pago"
	
	#~ _rec_name = "num_pago"
	
	#Función para pasar a estado de Ordenado----------------------------------------------
	def action_ordenar(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'ejecutado'}, context=context)	
		
	#Función para pasar a estado de Anulado----------------------------------------------
	def action_anular(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'anulado'}, context=context)	
	
	#MÉTODO PARA GENERAR EL NÚMERO CORRELATIVO
	#~ def _gen_correlativo(self, cr, uid, ids, context=None):
		#~ 
		#~ cr.execute("SELECT count(*) as num_orden FROM tesoreria_ordenpago")
		#~ num_orden = cr.fetchone()[0]
		#~ 
		#~ anyo = time.strftime("%y")
		#~ 
		#~ valor_num_orden = anyo+str(num_orden+1).zfill(6)
		#~ 
		#~ return valor_num_orden
				

	_columns = {
		'stage_id' : fields.selection((('borrador','Borrador'),('ejecutado','Ejecutado'),('anulado','Anulado')),"Estado", required = True),
		'cheque' : fields.char(string="Cheque", size=256, required=False),
		#~ 'tipo_pago' : fields.selection((('1','SELECCIONE'),('ORDEN DE PAGO','ORDEN DE PAGO')),"Tipo pago", required = True),
		#~ 'num_pago' : fields.char(string="Número", size = 8, required = True),
		#~ 'fecha_pago': fields.date(string = "Fecha", required = True),
		#~ 'ced_rif_ben' : fields.char(string="Cédula o Rif del Beneficiario", required = False), #Cédula o RIF del beneficiario
		#~ 'ced_rif_ces' : fields.char(string="Cédula o Rif del Cesionado", required=False), #Cédula o RIF del cesionado
		#~ 'beneficiario' : fields.many2one("res.partner", "Beneficiario", required = False),
		#~ 'cesionado' : fields.char(string="Nombre del Cesionado Autorizado a Cobrar", required = False),
		#~ 'unidad_solicitante' : fields.many2one('stock.location', "Unidad Solicitante", required = False),
		#~ 'requisicion' : fields.char(string="Requisición", required = False),
		#~ 'fecha_req' : fields.date(string="Fecha Requisición", required = False), #Fecha de la requisición
		#~ 'observacion' : fields.text(string="Observación", required = False),
		#~ #Segunda sección
		#~ 'tipo_compromiso' : fields.many2one("presupuesto.tipodoc", "Tipo Compromiso", required = True),
		#~ 'num_compromiso' : fields.char(string="Número Compromiso", size = 8, required = True),
		#~ 'compromisos' : fields.one2many("tesoreria.compromisos", "orden", required = False),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]
	
	_defaults = {
		#~ 'stage_id' : 'borrador',
		#~ 'tipo_pago' : 'ORDEN DE PAGO',
		#~ 'num_pago' : _gen_correlativo,
		#~ 'tipo_compromiso' : 1,
		#~ 'fecha_pago' : lambda *a: time.strftime("%Y-%m-%d"),
	}

