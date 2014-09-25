# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Compromisos(osv.Model):
	_name = "tesoreria.compromisos"
	
	_order = "n_doc"
	
	_rec_name = "n_doc"
	
	
	_columns = {
		'orden' : fields.many2one("tesoreria.ordenpago","movimientos",required=False),
		'n_doc' : fields.char(string="N° Doc", required = False),
		'num_compromiso' : fields.char(string="Número", required = True),
		'proyec_acc' : fields.char(string="Proyecto Acción", required = True),
		'partida' : fields.char(string="Partida", required = False),
		'desc_partida' : fields.char(string="Descripción", required = False),
		'monto_causar' : fields.char(string="Monto por Causar O/P", required = False),
		'monto_emitir' : fields.char(string="Monto a emitir O/P", required = False),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]
	
	#~ _defaults = {
		#~ 'num_compromiso' : _gen_correlativo,
		#~ 'fecha_compromiso' : lambda *a: time.strftime("%Y-%m-%d"),
		#~ 'fecha_oficio' : lambda *a: time.strftime("%Y-%m-%d"),
	#~ }


