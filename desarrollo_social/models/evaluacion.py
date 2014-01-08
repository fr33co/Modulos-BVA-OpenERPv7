# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Evaluacion(osv.Model):
	_name = "evaluacion.becados"
	#_order = 'encargado'
	#_rec_name = 'encargado'
	
	_columns = {
		# Datos Basicos
		'evaluado' : fields.char(string="Evaluado", size=50, required=True),
		'ci' : fields.char(string="C.I", size=8, required=True),
		'area' : fields.char(string="Area de desempeño", size=256, required=True),
		'sede' : fields.char(string="Sede", size=256, required=True),
		'fecha_actual' : fields.char(string="Fecha", size=256, readonly=True),
		'evaluador' : fields.char(string="Evaluado", size=256, required=True),
		# Pestañas NOTEBOOK Evaluacion

		'puntaje_higiene' : fields.selection((('1','4'),('2','3 '),('3','2'),('4','1'),('5','0')), "Higiene personal", required = True),
		'puntaje_uniforme' : fields.selection((('1','4 Puntos'),('2','3 Puntos'),('3','2 Puntos'),('4','1 Puntos'),('5','0 Puntos')), "Uso del uniforme", required = True),
		'puntaje_rpersonales' : fields.selection((('1','4 Puntos'),('2','3 Puntos'),('3','2 Puntos'),('4','1 Puntos'),('5','0 Puntos')), "Relaciones personales", required = True),
		'puntaje_cortesia' : fields.selection((('1','4 Puntos'),('2','3 Puntos'),('3','2 Puntos'),('4','1 Puntos'),('5','0 Puntos')), "Normas de cortesia", required = True),
		'puntaje_comunicacion' : fields.selection((('1','4 Puntos'),('2','3 Puntos'),('3','2 Puntos'),('4','1 Puntos'),('5','0 Puntos')), "Comunicación verbal y no verbal", required = True),
		'sub_total_1' : fields.char(string="sub-total", size=2, readonly=True),

		'puntaje_atencion' : fields.selection((('1','4'),('2','3 '),('3','2'),('4','1'),('5','0')), "Atención al cliente", required = True),
		'puntaje_resolucion' : fields.selection((('1','4 Puntos'),('2','3 Puntos'),('3','2 Puntos'),('4','1 Puntos'),('5','0 Puntos')), "Resolución de problemas", required = True),
		'puntaje_uso' : fields.selection((('1','4 Puntos'),('2','3 Puntos'),('3','2 Puntos'),('4','1 Puntos'),('5','0 Puntos')), "Uso de equipos personales e institucionales", required = True),
		'sub_total_2' : fields.char(string="sub-total", size=2, readonly=True),

		'puntaje_normas' : fields.selection((('1','4 Puntos'),('2','3 Puntos'),('3','2 Puntos'),('4','1 Puntos'),('5','0 Puntos')), "Normas y procedimientos", required = True),
		'sub_total_3' : fields.char(string="sub-total", size=2, readonly=True),

		'puntaje_manejo' : fields.selection((('1','4'),('2','3 '),('3','2'),('4','1'),('5','0')), "Manejo de las herramientas tecnológicas", required = True),
		'puntaje_iniciativa' : fields.selection((('1','4 Puntos'),('2','3 Puntos'),('3','2 Puntos'),('4','1 Puntos'),('5','0 Puntos')), "Iniciativa y creatividad", required = True),
		'puntaje_pertenencia' : fields.selection((('1','4 Puntos'),('2','3 Puntos'),('3','2 Puntos'),('4','1 Puntos'),('5','0 Puntos')), "Sentido de pertenencia con la institución", required = True),
		'sub_total_4' : fields.char(string="sub-total", size=2, readonly=True),

	}
		

	#_sql_constraints = [
    #('ci_unique','UNIQUE(ci)','Disculpe esta cedula ya tiene asignada una novedad'),
	#]


	_defaults = {
		'fecha_actual': lambda *a: time.strftime('%d-%m-%Y'),
	} 

