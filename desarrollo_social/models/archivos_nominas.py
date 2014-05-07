# -*- coding: utf-8 -*-

import time #Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class NominaBecadoIndividual(osv.Model):
	
	_inherit = 'ir.attachment'
	_order = 'write_date desc'
	
	_columns = {
		'nomina' : fields.many2one("becados.nomina", "Nómina", required=False),
		'nombre' : fields.binary("Nombre", required=False),
		'stage' : fields.char(string="Estado", required=False),
		'tipo_nomina' : fields.char(string="tipo_nomina", required=False),
		'tipo_beca' : fields.char(string="tipo_beca", required=False),
		'banco' : fields.char(string="Banco", required=False),
		#~ 'categoria' : fields.char(string="Categoría", size=1, required=False),
		#~ El campo 'categoria' ha sido descartado como campo de identificación, en sustitución
		#~ se usará el campo 'res_model' que ya viene creado por defecto en este modelo 'ir.attachment'
	}
	
	#~ _defaults = {
		#~ 'name' : 
	#~ }
