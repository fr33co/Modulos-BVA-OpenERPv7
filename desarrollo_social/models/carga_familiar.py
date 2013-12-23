# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Carga_familiar(osv.Model):
	_name = "becado.carga.familiar"

	def validar_fecha(self, cr, uid, ids, fecha_nac_familiar):

		edad = fecha_nac_familiar

		edades = edad.split("-")

		fecha_actual = date.today()# Obtenemos el Ano actual der servidor

		ano_actual = fecha_actual.year # Segmentamos la fecha y obtenemos el ano actual

		calculo = int(edades[0]) - int(ano_actual)

		print calculo
	
	
	_columns ={
		#Sección I (Datos del Becado)
		'cedula_becado' : fields.char(string = "Cédula", size = 9, required = True, help="Cédula del Becado"),
		'primer_nombre' : fields.char(string="Primer nombre", help="Ingrese el primer nombre", required = True),
		'segundo_nombre' : fields.char(string="Segundo nombre", help="Ingrese el segundo nombre", required = True),
		'primer_apellido' : fields.char(string="Primer apellido", help="Ingrese el primer apellido", required = True),
		'segundo_apellido' : fields.char(string="Segundo apellido", help="Ingrese el segundo apellido", required = True),
		'edad' : fields.char(string="Edad", help="Ingrese la Edad", required = True),
		
		#Sección II (Datos del Familiar)
		'cedula_familiar': fields.char(string = "Cédula", size = 9, required = True, help="Cédula del familiar"),
		'primer_nombres_familiar' : fields.char(string="Primer nombre", help="Ingrese el primer nombre del Familiar", required = True),
		'segundo_nombre_familiar' : fields.char(string="Segundo nombre", help="Ingrese el segundo nombre del Familiar", required = True),
		'primer_apellido_familiar' : fields.char(string="Primer apellido", help="Ingrese el primer apellido del Familiar", required = True),
		'segundo_apellido_familiar' : fields.char(string="Segundo apellido", help="Ingrese el segundo apellido del Familiar", required = True),
		'fecha_nac_familiar': fields.date(string = "Fecha de Nacimiento", required = True),
		'profesion_familiar' : fields.char(string="Profesión u Oficio", help="Ingrese la Profesión u Oficio del Familiar", required = True),
		'sexo' : fields.selection((('1','Masculino'),('2','Femenino')), "Sexo", required = True),
		'parentesco' : fields.selection((('1','Hijo'),('2','Madres'),('3','Padre')), "Parentesco", required = True),
		'estudio' : fields.boolean(string="Estudia Actualmente?"),
		'fecha_union' : fields.date(string="Fecha de la Unión", required=True),
	}

	_sql_constraints = [
	    ('cedula_becado_unique',
	     'UNIQUE(cedula_becado)',
	     'Disculpe el Registro ya existe'),
	]

