# -*- coding: utf-8 -*-

import time #Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class ArchivosIntegrantes(osv.Model):
	
	_inherit = 'ir.attachment'
		
	_columns = {
		'integrante_id' : fields.many2one("integrantes.ubch", "Integrante", required=False),
		#~ 'fecha_creacion' : fields.datetime(string="Fecha de creación", required=False)
		#~ 'categoria' : fields.char(string="Categoría", size=1, required=False),
		#~ El campo 'categoria' ha sido descartado como campo de identificación, en sustitución
		#~ se usará el campo 'res_model' que ya viene creado por defecto en este modelo 'ir.attachment'
	}
	
	#~ _defaults = {
		#~ 'fecha_creacion' : lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
		#~ 'fecha_creacion' : _copiar_f_creacion,
	#~ }
