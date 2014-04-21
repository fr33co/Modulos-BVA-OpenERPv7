# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import fields, osv

class Empleado(osv.Model):
	
	'''Herenciando a hr_employee (empleados)'''
	
	#_order = "empleado"
	
	_inherit = 'hr.employee'

	#################################################################
		#Función on_chage para actualizar el tiempo de servicio
	#################################################################

	def get_employee_filter(self, cr, uid, ids, context=None):


		status_browse = self.browse(cr, uid, ids, context=None)
		
		for many_load in status_browse:

			id_fill = many_load.fecha_ingreso

			fecha = self.time_service_employee(id_fill) # llamada al objeto time_service_employee con el argumento fecha
			
		return self.write(cr, uid, ids, {'tiempo_servicio':fecha}, context=context)


	#################################################################
				# metodo para evaluar los años de servicios
	#################################################################


	def time_service_employee(self, fecha_ingreso): 

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


		time_service = str(ano_diferencia)+" "+str(mes_diferencia)+" "+str(dia_diferencia)

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

		return {'value' : values,'warning' : mensaje}

	#~ def search_department(self, cr, uid, ids, argument_search, context=None): # Proceso de busqueda de un manager(Gerente)
#~ 
		#~ values = {}
		#~ 
		#~ if not argument_search:
			#~ 
			#~ return values
		#~ obj_dp = self.pool.get('hr.department')
		#~ 
		#~ #======================== Busqueda por código ============================
#~ 
		#~ search_obj_code = obj_dp.search(cr, uid, [('id','=',argument_search)])
#~ 
		#~ datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		#~ #=========================================================================
		#~ if datos_code:
			#~ 
			#~ values.update({
				#~ 
				#~ 'gerente' : datos_code[0]['gerente'],
				#~ })
#~ 
		#~ return {'value' : values}

	#################################################################

	_columns = {
		'ciudad' : fields.many2one("res.country.city", "Ciudad", required = True, select="0"),
		'estado' : fields.many2one("res.country.state", "Estado", required = True, select="0"),
		'municipio' : fields.many2one("res.country.municipality", "Municipio", required = True, select="0"),
		'parroquia' : fields.many2one("res.country.parish", "Parroquia", required = True, select="0"),
		'rif' : fields.char(string="Rif", size = 50, required=False),
		#~ 'gerente' : fields.char(string="Gerente", size=50),
		'fecha_nacimiento' : fields.date(string="Fecha de nacimiento", required=False),
		
		
	}
	#################################################################
	
	_defaults = {

		'country_id' : 240,
		'estado' : 55,
		'cne' : '2',
		'carga_familiar' : '2',
		'status' : '1',
		#'bank_account_id' : 1,
	} 
