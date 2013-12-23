# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class Nomina(osv.Model):
	
	'''Herenciando a hr.payslip (Nomina de Becado)'''
	
	_inherit = 'hr.payslip'
	
	_columns = {
		'categoria': fields.many2one('hr.employee.category', 'Category', select=True),
		'cedula' : fields.char(string="Prueba", size = 8, required=True),
	}
