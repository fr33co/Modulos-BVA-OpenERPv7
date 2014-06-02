# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
import os
from datetime import date
from openerp.osv import fields, osv
from openerp.tools.translate import _

class Empleado(osv.Model):
	
	'''Herenciando a hr_employee (empleados)'''
	
	#_order = "empleado"
	
	_inherit = 'hr.employee'

	def procesar_carga_prima_hijo(self, cr, uid, ids, context=None):

		data_carga = self.read(cr, uid, ids, context=context)[0] # Lectura del grupo de ids
		id_filter  = data_carga['familiar'] # Ids del grupo de one2many de familiar (carga familiar)
		carga = self.pool.get('becado.carga.familiar') # Objeto becado.carga.familiar (Empleado)
		datos = carga.search(cr, uid, [('id','=',id_filter),('parentesco','=','1')], context=None) # Metodo de busqueda
		carga_f = carga.read(cr,uid,datos,context=context) # Lectura de los datos
		count_id = len(carga_f) # conteo de registros
		monto_total = 0
		data_vacio = self.read(cr, uid, ids, context=context)[0] # Validacion para campos vacio
		if not data_vacio['mount']:
			raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el monto..."))
		else:
			for x in carga_f:
				monto_total += int(x['mount_hijo'])
	
				if int(count_id) > 3: # Condicional para no permitir mas de tres registros al momento de carga de prima de hijos de carga familiar
					raise osv.except_osv(_("Warning!"), _("Disculpe exedio el limite de registro en la carga de hijos, debe eliminar una carga para proceder el ingreso de monto..."))
	
				else:
					id_carga = x['id']
					parentesco = x['parentesco']
	
					browse_carga_f = self.browse(cr, uid, ids, context=None) # Lectura del mismo objeto hr_employee para el campo familiar (one2many)
					for i in browse_carga_f:
						monto = i.mount
						id_filter = i.id
						#print "ID: "+str(id_filter)
					cr.execute("UPDATE becado_carga_familiar SET mount_hijo="+str(monto)+", parentesco="+str(parentesco)+", prima_hijo='TRUE'  WHERE id="+str(id_carga)+";")
			total = monto_total
			mount_val = "0.00"
			cr.execute("UPDATE hr_employee SET mount_total="+str(total)+", mount="+str(mount_val)+" WHERE id="+str(id_filter)+";")
			return True
	#################################################################
		#Función on_chage para actualizar el tiempo de servicio
	#################################################################

	def get_employee_filter(self, cr, uid, ids, context=None):


		status_browse = self.browse(cr, uid, ids, context=None)
		
		for many_load in status_browse:

			id_fill = many_load.fecha_ingreso

			fecha = self.time_service_employee(cr, uid, ids, id_fill, context) # llamada al objeto time_service_employee con el argumento fecha
			
		return self.write(cr, uid, ids, {'tiempo_servicio':fecha}, context=context)


	#################################################################
				# metodo para evaluar los años de servicios
	#################################################################


	def time_service_employee(self, cr, uid, ids, fecha_ingreso, context): 

		fecha = fecha_ingreso.split("-")

		ano = fecha[0]
		mes = fecha[1]
		dia = fecha[2]

		fecha_actual = date.today() # Fecha actual d/m/Y
		ano_actual = fecha_actual.year # Se optiene el año actual
		mes_actual = fecha_actual.month # Se optiene el mes actual
		dia_actual = fecha_actual.day # Se optiene el dia actual

		dia_diferencia = int(dia_actual) - int(dia)
		mes_diferencia = int(mes_actual) - int(mes)
		ano_diferencia = int(ano_actual) - int(ano)

		# se suma dia_diferencia los dias que tiene el mes acterior de la fecha actual

		if dia_diferencia < 0:
			mes_diferencia = int(mes_diferencia)-1

			if mes_actual:

				if mes_actual == 1 or mes_actual == 3 or mes_actual == 5 or mes_actual == 7 or mes_actual == 8 or mes_actual == 10 or mes_actual == 12:
					dias_mes_anterior = 31

				elif mes_actual == 2: # calculo si un año es bisiesto

					if ((((ano_actual%100)!=0) and ((ano_actual%4)==0)) or ((ano_actual%400)==0)):
						#print 'El año es Bisiesto'
						dias_mes_anterior = 29
					else:
						#print 'El año no es Bisiesto'
						dias_mes_anterior = 28

				elif mes_actual == 4 or mes_actual == 6 or mes_actual == 9 or mes_actual == 11:
					dias_mes_anterior = 30
			

			dia_diferencia = int(dia_diferencia) + int(dias_mes_anterior)

		if mes_diferencia < 0:
			ano_diferencia = int(ano_diferencia) - 1  
			mes_diferencia = int(mes_diferencia) + 12

		# Se valida si cumple un año se muestre año si es mayor de un año se muestre años
		if ano_diferencia < 2:
			ano_diferencia = str(ano_diferencia)+" Año"
		elif ano_diferencia > 1:
			ano_diferencia = str(ano_diferencia)+" Años"

		if mes_diferencia < 2:
			mes_diferencia = str(mes_diferencia)+" Mes"
		elif mes_diferencia > 1:
			mes_diferencia = str(mes_diferencia)+" Meses"

		if dia_diferencia < 2:
			dia_diferencia = str(dia_diferencia)+" Dia"
		elif dia_diferencia > 1:
			dia_diferencia = str(dia_diferencia)+" Dias"


		time_service = str(ano_diferencia).replace('-',"")+" "+str(mes_diferencia)+" "+str(dia_diferencia)
		self.write(cr, uid, ids, {'ano_antiguedad':str(ano_diferencia).replace('-',"")}, context=context)
		return time_service
	#################################################################
						# calcular la edad
	#################################################################

	def data_employee(self, cr, uid, ids, argument_search,item, context=None):
		
		values = {}
		mensaje = {}

		obj_dp = self.pool.get('hr.employee')

		if item == "1":

			edad = argument_search

			edades = edad.split("-")

			fecha_actual = date.today()# Obtenemos el Ano actual der servidor

			ano_actual = fecha_actual.year # Segmentamos la fecha y obtenemos el ano actual

			mes_actual = fecha_actual.month

			dia_actual = mes_actual = fecha_actual.day


			calculo = int(ano_actual) - int(edades[0])
				
			if int(edades[1] > int(mes_actual)):
				calculo = calculo - 1
			elif (int(edades[1]) == int(mes_actual)) and (int(edades[2]) > int(dia_actual)):
				calculo = calculo - 1 

			values.update({

				'edad' : calculo,
			})

		elif item == "2":
			
			if not argument_search:
				return values
			#======================== Busqueda por código ============================

			search_obj_code = obj_dp.search(cr, uid, [('cedula','=',argument_search)])

			datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)

			if datos_code:
				
				mensaje = {
						'title'   : "Cédula",
						'message' : "Disculpe el registro ya existe, intente de nuevo...",
				}
				values.update({
					
					'cedula' : None,

					})
			else:
				if len(argument_search) < 7:
					mensaje = {
						'title'   : "Cédula",
						'message' : "Disculpe la cédula debe contener un mínimo de 7 dígitos",
					}
					values.update({
					
						'cedula' : None,

					})

		return {'value' : values,'warning' : mensaje}

	def search_department(self, cr, uid, ids, argument_search, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('hr.department')
		
		#======================== Busqueda por código ============================

		search_obj_code = obj_dp.search(cr, uid, [('id','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		#=========================================================================
		if datos_code:
			
			values.update({
				
				'gerente' : datos_code[0]['gerente'],
				})

		return {'value' : values}

	#################################################################

	def search_charge(self, cr, uid, ids, argument_search,item, context=None):

		values = {}
		mensaje = {}

		if not argument_search:

			return values
		obj_dp = self.pool.get('hr.job')

		if item == "1":

			#======================== Busqueda por cargo ============================
			search_job_id = obj_dp.search(cr, uid, [('id','=',argument_search)])

			datos_job_id = obj_dp.read(cr,uid,search_job_id,context=context)
			#========================================================================

			if datos_job_id:

				values.update({

					'asignacion' : float(datos_job_id[0]['asignacion']),

					})

		return {'value' : values,'warning' : mensaje}
	
	#~ def _nomina(self, cr, user_id, context=None):
		#~ cr.execute("SELECT id,nomina FROM hr_nomina_adm WHERE nomina='A.C Biblioteca Virtual'")
		#~ t = ""
		 #~ # declaramos una tupla vacía
		#~ for datos in cr.fetchall():
			#~ t = datos[0]
		#~ return t
	
	def enlazar_nomina(self, cr, uid, ids, context=None):
		
		browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro
		data_emp = self.read(cr, uid, ids, context=context)[0] # Validacion para campos vacio
		
		for emp in browse_data:
			cedula   = emp.cedula
			cargo    = emp.job_id.id
			tipo_emp = emp.class_personal.id
			status   = emp.status
			fecha_i  = emp.fecha_ingreso
			nom      = emp.name_related.encode("UTF-8")
			sueldo   = emp.asignacion
			servicio = emp.tiempo_servicio
			depart   = emp.department_id.id
			foto     = emp.image_medium
			
		obj_dp = self.pool.get('hr.movement.employee')
		search_obj = obj_dp.search(cr, uid, [('cedula','=',cedula)])
		emp_data = obj_dp.read(cr,uid,search_obj,context=context)
		
		if emp_data:
			raise osv.except_osv(_("Warning!"), _("Disculpe el empleado "+str(nom)+" ya se encuentra registrado en la asignación de nóminas..."))
		else:
			
			if not data_emp['department_id']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el departamento, en la pestaña Información Institucional..."))
			elif not data_emp['job_id']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el Cargo, en la pestaña Información Institucional..."))
			elif not data_emp['tiempo_servicio']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe actualizar el año de servicio del empleado para continuar..."))
			elif not data_emp['asignacion']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar la asignación del empleado..."))
			elif not data_emp['class_personal']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar Tipo de empleado..."))
			else:
				id_att = self.pool.get("hr.movement.employee").create(cr, uid, {
					'nomina_admin': "1",
					'cedula': cedula,
					'charge_acterior': cargo,
					'emp': tipo_emp,
					'status': status,
					'date_ingreso': fecha_i,
					'nombres': nom,
					'sueldo': sueldo,
					'ano_servicio': servicio,
					'dep_lab':depart,
					'image':foto,
				}, context=context)
				
				return id_att
	_columns = {
		'ciudad' : fields.many2one("res.country.city", "Ciudad", required = True, select="0"),
		'estado' : fields.many2one("res.country.state", "Estado", required = True, select="0"),
		'municipio' : fields.many2one("res.country.municipality", "Municipio", required = False, select="0"),
		'parroquia' : fields.many2one("res.country.parish", "Parroquia", required = False, select="0"),
		'rif' : fields.char(string="Rif", size = 50, required=False),
		'gerente' : fields.char(string="Gerente", size=50),
		'fecha_nacimiento' : fields.date(string="Fecha de nacimiento", required=False),
		'mount' : fields.char(string="Gerente", size=10),
		'caja_ahorro' : fields.char(string="% Caja de Ahorro", size=10),
		'mount_total' : fields.float(string="Monto total", size=10),
		'nomina' : fields.many2one("hr.nomina.adm", "Nomina", required = False),
		'marital' : fields.selection((('1','Soltero'),('2','Casado'),('3','Comcubinato'),('4','Unión de hechos estables')), "Estado civil", required=False),
	}
	#################################################################
	
	_defaults = {

		'country_id' : 240,
		'estado' : 55,
		'cne' : '2',
		'carga_familiar' : '2',
		'status' : '1',
		'prima_responsabilidad': '2',
		#'nomina': _nomina,
	} 
