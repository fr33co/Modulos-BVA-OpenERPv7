# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class Nomina(osv.Model):
	
	'''Herenciando a hr.payslip (Nomina de Becado)'''
	
	_inherit = 'hr.payslip'
	
	_columns = {
		'class_personal' : fields.many2one('becados.clasper', 'Personal', required=False),
	}
	
	#~ _default = {
		#~ 'categoria' : 'Becados',
	#~ }
