# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class Becado(osv.Model):
	
	'''Herenciando a hr_employee (empleados)'''
	
	_inherit = 'hr.employee'
	
	_columns = {
		'cedula' : fields.char(string="Cédula", size = 8, required=True),
		'tiempo_servicio' : fields.char(string="Tiempo de Servicio", size = 8, required=True),
		'empleado': fields.selection((('1','0243'),('2','0244')), "Empleado", required = True),
		'primer_nombre' : fields.char(string="Primer Nombre", size = 8, required=True),
		'segundo_nombre' : fields.char(string="Segundo Nombre", size = 8, required=True),
		'primer_apellido' : fields.char(string="Primer Apellido", size = 8, required=True),
		'segundo_apellido' : fields.char(string="Segudo Apellido", size = 8, required=True),
		'direccion' : fields.text(string="Dirección", size = 8, required=True),
		'grado_instruccion': fields.selection((('1','0243'),('2','0244')), "Grado de Instrucción", required = True),
		'grupo_sanguineo': fields.selection((('1','0243'),('2','0244')), "Grupo Sanguineo", required = True),
		'tlf_movil' : fields.char(string="Teléfono Movil", size = 11, required=False),
		'tlf_local' : fields.char(string="Teléfono Local", size = 11, required=False),
		'twitter' : fields.char(string="Twitter", size = 11, required=False),
		'titulo_obtenido' : fields.char(string="Título Obtenido", size = 11, required=True),
		'fecha_ingreso' : fields.date(string="Fecha de Ingreso", required=True),
		'fecha_egreso' : fields.date(string="Fecha de Egreso", required=True),
		'tipo_nomina' : fields.selection((('1','0243'),('2','0244')), "Tipo de Nómina", required = True),
		'class_personal' : fields.selection((('1','0243'),('2','0244')), "Clasificación del Personal", required = True),
		'cargo_desempenado' : fields.selection((('1','0243'),('2','0244')), "Cargo Desempeñado", required = True),
		'edad' : fields.char(string="Edad", size = 3, required=True),
		'sueldo' : fields.float(string="Sueldo", required=True),
		'correo' : fields.char(string="Correo", size = 11, required=False),
		'entidad_bancaria' : fields.selection((('1','0243'),('2','0244')), "Entidad Bancaria", required = True),
		'ano_antiguedad' : fields.char(string="Año de Antiguedad", required=False),
		'camisa' : fields.char(string="Talla de Camisa", size=2, required=False),
		'pantalon' : fields.char(string="Talla de pantalón", size=2, required=False),
		'zapato' : fields.char(string="Calzado", size=2, required=False),
		'caja_ahorro' : fields.char(string="Caja de Ahorro", required=False),
		'prima_responsabilidad' : fields.float(string="Prima de Responsabilidad", required=True),
	}

	_defaults = {


	}
