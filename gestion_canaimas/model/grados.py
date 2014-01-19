# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class solicitud_grado(osv.Model):
	_name = "solicitud.grado"
	_order = 'grado'
	_rec_name = 'grado'
    
	_columns = {
		'grado' : fields.char(string="Grado", size=45, required=True),
		'tipo' : fields.many2one("solicitud.tipo.edu", string="Tipo", required=True),
	}
    
class solicitud_tipo_edu(osv.Model):
	_name = "solicitud.tipo.edu"
	_order = 'tipo'
	_rec_name = 'tipo'
    
	_columns = {
		'tipo' : fields.char(string="Tipo", size=45, required=True),
	}
