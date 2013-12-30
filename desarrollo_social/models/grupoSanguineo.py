# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class grupoSanguineo(osv.Model):
	_name="becados.gruposanguineo"

	_columns = {
		'grupo_sang': fields.char(string = "Grupo Sanguíneo", size = 150, required = True),
	}


