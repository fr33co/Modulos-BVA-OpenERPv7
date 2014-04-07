# -*- coding: utf-8 -*-

import time #Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class NominaBecadoIndividual(osv.Model):
	
	_inherit = 'ir.attachment'
	
	_columns = {
		'nomina' : fields.many2one("becados.nomina", "Nómina", required=False),
	}
