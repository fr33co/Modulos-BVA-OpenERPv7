# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import fields, osv

class Becado(osv.Model):
	
	'''Herenciando a hr_employee (empleados)'''
	
	_order = "empleado"
	
	_inherit = 'hr.employee'


	def validar_fecha(self, cr, uid, ids, fecha_nacimiento):

		values = {}

		edad = fecha_nacimiento

		edades = edad.split("-")

		fecha_actual = date.today()# Obtenemos el Ano actual der servidor

		ano_actual = fecha_actual.year # Segmentamos la fecha y obtenemos el ano actual

		mes_actual = fecha_actual.month

		dia_actual = mes_actual = fecha_actual.day


		calculo = int(ano_actual) - int(edades[0])


		values.update({

			'edad' : calculo,

			})
		return {'value' : values}
	
	_columns = {
		'cedula' : fields.char(string="Cédula", size = 8, required=True),
		'tiempo_servicio' : fields.char(string="Tiempo de Servicio", size = 8, required=False),
		'empleado': fields.many2one("becados.tipoempleado", "Tipo de Beca", required = True),
		'primer_nombre' : fields.char(string="Primer Nombre", size = 8, required=False),
		'segundo_nombre' : fields.char(string="Segundo Nombre", size = 8, required=False),
		'primer_apellido' : fields.char(string="Primer Apellido", size = 8, required=False),
		'segundo_apellido' : fields.char(string="Segudo Apellido", size = 8, required=False),
		'direccion' : fields.text(string="Dirección", size = 256, required=True),
		'grado_instruccion': fields.many2one("becados.gradoinstruccion", "Grado de Instrucción", required = True),
		'grupo_sanguineo': fields.many2one("becados.gruposanguineo", "Grupo Sanguineo", required = False),
		'tlf_movil' : fields.char(string="Teléfono Movil", size = 11, required=True),
		'tlf_local' : fields.char(string="Teléfono Local", size = 11, required=False),
		'twitter' : fields.char(string="Twitter", size = 11, required=False),
		'titulo_obtenido' : fields.char(string="Título Obtenido", size = 11, required=False),
		'fecha_ingreso' : fields.date(string="Fecha de Ingreso", required=True),
		'fecha_egreso' : fields.date(string="Fecha de Egreso", required=False),
		'tipo_nomina' : fields.many2one("becados.tiponomina", "Tipo de Nómina", required = True),
		'class_personal' : fields.many2one("becados.clasper", "Clasificación del Personal", required = False),
		'area' : fields.many2one("becados.areas", string="Area de desempeño", required=True),
		'sede' : fields.many2one("becados.sedes", string="Sede", required=True),
		'cargo_desempenado' : fields.selection((('1','0243'),('2','0244')), "Cargo Desempeñado", required = False),
		'coordinador_eje' : fields.many2one("hr.employee","Coordinador de Eje",required=False, domain=[('category_ids.name','=','Coordinador_eje')]),
		'coordinador_sede' : fields.many2one("hr.employee","Coordinador de Sede",required=False, domain=[('category_ids.name','=','Coordinador_sede')]),
		'edad' : fields.char(string="Edad", size = 3, required=False),
		
		'asignacion' : fields.float(string="Asignación", required=True),
		'correo' : fields.char(string="Correo", size = 30, required=True),
		'entidad_bancaria' : fields.selection((('1','0243'),('2','0244')), "Entidad Bancaria", required = False),
		'ano_antiguedad' : fields.char(string="Año de Antiguedad", required=True),
		'camisa' : fields.char(string="Talla de Camisa", size=2, required=True),
		'pantalon' : fields.char(string="Talla de pantalón", size=2, required=True),
		'zapato' : fields.char(string="Calzado", size=2, required=True),
		'caja_ahorro' : fields.char(string="Caja de Ahorro", required=False),
		'prima_responsabilidad' : fields.float(string="Prima de Responsabilidad", required=True),
		'estado_de_estudios' : fields.boolean("¿Estudia Actualmente?"),
		'estudios_actuales' : fields.char(string="Especifique qué estudia",required=False),
		'cne' : fields.boolean("¿Está inscrito en el CNE?"),
		#'fecha_nacimiento' : fields.date(string="Fecha de nacimiento", required=True),
		'familiar' : fields.one2many("becado.carga.familiar","becado",string="Carga Familiar"),
	}
