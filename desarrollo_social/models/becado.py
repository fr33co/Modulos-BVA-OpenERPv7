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
	#-----------------------------------------------------------------------------------------------
	#~ Función para cargar datos de solicitantes seleccionados como posibles becados, utilizando
	#~ la cédula como clave de búsqueda.
	def datos_seleccionado(self, cr, uid, ids, cedula, context=None):
		valores = {}
		
		if not cedula:
			return valores
			
		#Preparación de los modelos donde se realizarán las búsquedas
		modelo1 = self.pool.get('becados.seleccion')
		modelo2 = self.pool.get('becados.solicitudes')
		
		#Ejecución de las búsquedas
		busqueda1 = modelo1.search_count(cr, uid, [('cedula','=',cedula)])
		
		if busqueda1 > 0:
			#Si se cumple esta condición es porque ha sido seleccionado, entonces procedemos 
			#a traer sus datos desde el otro modelo 
			busqueda2 = modelo2.search_count(cr, uid, [('cedula','=',cedula)])
			
			if busqueda2 > 0:
				busqueda2 = modelo2.search(cr, uid, [('cedula','=',cedula)])
				busqueda_leer = modelo2.read(cr, uid, busqueda2, context=context)
				
				#Carga de los datos que necesitamos
				valores.update({
					'name' : busqueda_leer[0]['solicitante'],
					'correo' : busqueda_leer[0]['email'],
					'tlf_local' : busqueda_leer[0]['telefono'],
					'tlf_movil' : busqueda_leer[0]['movil'],
					'grado_instruccion' : busqueda_leer[0]['grado_instruc'],
					'direccion' : busqueda_leer[0]['direccion'],
					'sede' : busqueda_leer[0]['sede'],
				})
				
				return {'value':valores}
	
	_columns = {
		#Información personal-----------------------------------------------------------------
		'cedula' : fields.char(string="Cédula", size = 8, required=True),
		'tiempo_servicio' : fields.char(string="Tiempo de Servicio", size = 50, required=False),
		'direccion' : fields.text(string="Dirección", size = 256, required=True),
		'correo' : fields.char(string="Correo", size = 30, required=True),
		'edad' : fields.char(string="Edad", size = 3, required=False),
		'camisa' : fields.char(string="Talla de Camisa", size=2, required=False),
		'pantalon' : fields.char(string="Talla de pantalón", size=2, required=False),
		'zapato' : fields.char(string="Calzado", size=2, required=False),
		'sexo' : fields.selection((('masculino','Masculino'),('femenino','Femenino')), "Sexo", required=False),
		'tlf_movil' : fields.char(string="Teléfono Movil", size = 11, required=True),
		'tlf_local' : fields.char(string="Teléfono Local", size = 11, required=False),
		'twitter' : fields.char(string="Twitter", size = 25, required=False),
		'cne' : fields.selection((('1','Si'),('2','No')), "¿Está inscrito en el CNE?", required = False),
		'centro_votacion' : fields.text(string="Centro de votación"),
		'discapacidad' : fields.selection((('1','Sí'),('2','No')),"¿Presenta discapacidad?",required=False),
		'tipo_discapacidad' : fields.selection((('1','Visual'),('2','Auditiva'),('3','Física'),('4','Psíquica'),('5','Multisensorial')),"Tipo de discapacidad",required=False),
		'carga_familiar' : fields.selection((('1','Dispone'),('2','No Dispone')), "¿Tiene Carga Familiar?", required = False),
		'carga_familiar2' : fields.selection((('1','Dispone'),('2','No Dispone')), "¿Tiene Carga Familiar?", required = False),
		'grupo_sanguineo': fields.many2one("becados.gruposanguineo", "Grupo Sanguineo", required = False),
		#Información académica----------------------------------------------------------------
		'grado_instruccion': fields.many2one("becados.gradoinstruccion", "Grado de Instrucción", required = True),
		'nivel_edu' : fields.many2one("becados.niveleduc","Nivel Educativo",required=False),
		'titulo_obtenido' : fields.char(string="Título Obtenido", size = 11, required=False),
		'estado_de_estudios' : fields.boolean("¿Estudia Actualmente?"),
		'inst_educ' : fields.many2one("becados.institucioneduc","Institución",required=False),
		'estudios_actuales' : fields.char(string="Especifique qué estudia",required=False),
		#Información institucional------------------------------------------------------------
		'fecha_ingreso' : fields.date(string="Fecha de Ingreso", required=True),
		'fecha_egreso' : fields.date(string="Fecha de Egreso", required=False),
		'tipo_nomina' : fields.many2one("becados.tiponomina", "Tipo de Nómina", required = True),
		'class_personal' : fields.many2one("becados.clasper", "Clasificación del Personal", required = False),
		'empleado': fields.many2one("becados.tipoempleado", "Tipo de Empleado", required = False),
		'tipo_beca' : fields.many2one("becados.tipobeca", "Tipo de Beca", required = False),
		'area' : fields.many2one("becados.areas", string="Area de desempeño", required=False),
		'ejes' : fields.many2one("becados.ejes", "Eje", required = False),
		'sede' : fields.many2one("becados.sedes", "Sede/Unidad Asignada", required=False),
		'cargo_desempenado' : fields.selection((('1','0243'),('2','0244')), "Cargo Desempeñado", required = False),
		'coordinador_eje' : fields.many2one("hr.employee","Coordinador de Eje",required=False, domain=[('category_ids.name','=','Coordinador_eje')]),
		'coordinador_sede' : fields.many2one("hr.employee","Coordinador de Sede",required=False, domain=[('category_ids.name','=','Coordinador_sede')]),
		#'status' : fields.many2one("becados.status","Status",required=False),
		'status' : fields.selection((('1','Activo'),('2','Periódo de gracia'),('3','Permiso de reposo'),('4','Permiso no remunerado'),('5','Suspendido'),('6','Vacaciones'),('7','Egresado')), "Estatus", required = False),
		'desc_status' : fields.char(string="Descripción", size=100, required=False,help="Escriba aquí detalles y razones del estatus seleccionado"),
		'asignacion' : fields.float(string="Asignación", required=True),
		'entidad_bancaria' : fields.many2one("becados.bancos", "Entidad Bancaria", required = False),
		'numero_cuenta' : fields.char(string="Número de cuenta",required=False),
		'tipo_cuenta' : fields.selection((('1','Corriente'),('2','Ahorro')),"Tipo de Cuenta",required=False),
		'ano_antiguedad' : fields.char(string="Año de Antiguedad", required=False),
		'caja_ahorro' : fields.char(string="Caja de Ahorro", required=False),
		'prima_responsabilidad' : fields.float(string="Prima de Responsabilidad", required=False),
		#'fecha_nacimiento' : fields.date(string="Fecha de nacimiento", required=True),
		'familiar' : fields.one2many("becado.carga.familiar","becado",string="Carga Familiar"),
		'categoria' : fields.selection((('1','Becado'),('2','Empleado'),('3','Obrero'),('4','Coordinador_eje'),('5','Coordinador_sede')), "Categoria", required = False),
		#Información de representante/contacto------------------------------------------------
		'cedula_contacto' : fields.integer(string="Cédula",size=8,required=False),
		'nombre_contacto' : fields.char(string="Nombre y Apellido",required=False),
		'direccion_contacto' : fields.text(string="Dirección",size=256,required=False), 
		'telefono_contacto' : fields.char(string="Teléfono",size=12,required=False),
		'correo_contacto' : fields.char(string="Correo",size=50,required=False),
		#Campos extra-------------------------------------------------------------------------
		'fecha_actual' : fields.char(string="FECHA", size = 50, required=False),#Campo para formato PDF
		'grupo' : fields.many2one("res.groups", "Grupos", required=True, readonly=True),	
	}
	
	_defaults = {
		'fecha_actual': lambda *a: time.strftime("(%d) días del mes %B del año %Y"),# formato corecto al español
		'status' : '1',
		'grupo': lambda s, cr, uid, c: uid,
		'categoria' : '1'
	} 
