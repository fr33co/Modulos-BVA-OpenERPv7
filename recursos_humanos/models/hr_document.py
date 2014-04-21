# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Hr_document(osv.Model): # Herencia de ir_attachment

	_inherit="ir.attachment"

	# _order = 'codigo'
	
	# _rec_name = 'codigo'

	
	_columns = {
		
		#'document_id': fields.many2one('hr.payslip.run', 'Documentos', readonly=True),
		# 'codigo': fields.char(string = "Código", size = 4, required = True),
		# 'concepto': fields.text(string = "Concepto", size = 256, required = True),
		# 'formula': fields.char(string = "Fórmula", size = 200, required = True),
		# 'items' : fields.many2one("presupuesto.partidas", "Partida presupuestaria", required = False),
	}

	_defaults = {
		#'codigo' : 
	}



