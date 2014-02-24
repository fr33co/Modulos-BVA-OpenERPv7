# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import fields, osv

class Contrato_empleado(osv.Model):
	
	'''Herenciando a hr.contract (Nomina de Empleado)'''
	
	_inherit = 'becado.carga.familiar'


	def search_hr_carga_familiar(self, cr, uid, ids, argument_search, context=None):

		values = {}
		mensaje = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('becado.carga.familiar')
		
		#======================== Busqueda por código ============================

		search_obj_code = obj_dp.search(cr, uid, [('cedula_familiar','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)

		if datos_code:
			
			mensaje = {
					'title'   : "Cédula",
					'message' : "Disculpe este cedula ya se encuentra registrada, intente de nuevo...",
			}

			values.update({
				
				'cedula_familiar' : None,

				})
			
		return {'value' : values,'warning' : mensaje}


	# validación para no permitir cargar un familiar mayor de 21 años y cambiar el estatus del mismo en el proceso de disfrute

	def search_hr_day_birth(self, cr, uid, ids, argument_search, context=None):

		# print argument_search

		age = argument_search.split("-")

		print age[1]

		# values = {}
		# mensaje = {}
		
		# if not argument_search:
			
		# 	return values
		# obj_dp = self.pool.get('becado.carga.familiar')
		
		# #======================== Busqueda por código ============================

		# search_obj_code = obj_dp.search(cr, uid, [('cedula_familiar','=',argument_search)])

		# datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)

		# if datos_code:
			
		# 	mensaje = {
		# 			'title'   : "Cédula",
		# 			'message' : "Disculpe este cedula ya se encuentra registrada, intente de nuevo...",
		# 	}

		# 	values.update({
				
		# 		'cedula_familiar' : None,

		# 		})
			
		# return {'value' : values,'warning' : mensaje}

	
	_columns = {
		'image_family' : fields.binary("",help="Imagen del familiar"),
		'especifique_estudio' : fields.char(string="Especifique", size = 200, readonly=False),
		'lugar_nac' : fields.char(string="Lugar de nacimiento", size = 256, required=True),
		'nac' : fields.many2one('res.country', 'Nacionalidad'),
		'estado' : fields.many2one("res.country.state", "Estado", required = True, select="0"),
		'municipio' : fields.many2one("res.country.municipality", "Municipio", required = True, select="0"),
		'parroquia' : fields.many2one("res.country.parish", "Parroquia", required = True, select="0"),
		'grupo_sanguineo': fields.many2one("becados.gruposanguineo", "Grupo Sanguineo", required = False),
		'nivel_instruccion' : fields.many2one("hr.level.instruction", "Nivel de Instrucción", required = True),
		'grado' : fields.many2one("hr.degree", "Grado", select="0", required = True, domain= "[('tipo','=',nivel_instruccion)]"),
		
	}

	_defaults = {
		'nac' : 240,
		# 'fecha_actual': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al español
	}
	
	
