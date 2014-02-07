# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import fields, osv

class Empleado(osv.Model):
	
	'''Herenciando a hr_employee (empleados)'''
	
	#_order = "empleado"
	
	_inherit = 'hr.employee'

	def validar(self, cr, uid, ids, parametro):
		valida = {}
		id_filtro=re.compile("[a-z]")
		if id_filtro.match(parametro):
			valida['warning'] = {'title': 'Disculpe!!!','message': 'Correcto',}
			return valida
		else:
			valida['warning'] = {'title': 'Disculpe!!!','message': 'solo se permiten numeros',}
			return valida

	
	_columns = {
		'ciudad' : fields.many2one("res.country.city", "Ciudad", required = True, select="0"),
		'estado' : fields.many2one("res.country.state", "Estado", required = True, select="0"),
		'municipio' : fields.many2one("res.country.municipality", "Municipio", required = True, select="0"),
		'parroquia' : fields.many2one("res.country.parish", "Parroquia", required = True, select="0"),
		#'localidad' : fields.many2one("res.country.sector", "Localidad", required = True),
		#'categoria' : fields.selection((('1','Becado'),('2','Empleado'),('3','Obrero'),('4','Coordinador_eje'),('5','Coordinador_sede')), "Categoria", required = False),
		
		
		#Campo para formato PDF
		#'date_now' : fields.char(string="FECHA", size = 50, required=False),
		
		#'grupo' : fields.many2one("res.groups", "Grupo", required=True, readonly=True),
	}
	
	_defaults = {
		#'date_now': lambda *a: time.strftime("(%d) días del mes %B del año %Y"),# formato corecto al español
	# 	#'grupo': lambda s, cr, uid, c: uid,
		'country_id' : 240,
	} 
