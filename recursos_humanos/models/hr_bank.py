# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import fields, osv

class Bank(osv.Model):
	
	'''Herenciando a res.partner.bank (Entidades Bancarias)'''
	
	_inherit = 'res.partner.bank'
	
	_columns = {
		'type_account' : fields.selection((('1','Ahorro'),('2','Corriente')),"Tipo de cuenta",required=True),
	}

	_defaults = {

		'state' : "bank",
	}
	
	
