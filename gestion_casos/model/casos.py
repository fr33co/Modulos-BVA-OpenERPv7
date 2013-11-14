# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
import MySQLdb
'''
|----------------------------------------------------------------------------------------------
|                               Clase Conexion a Kalkun
|----------------------------------------------------------------------------------------------
'''
class Conexion:
	# Metodo Constructor, Inicializacion de los Valores
    def __init__(self, db_host='localhost', db_user='root', db_pass='123', db_name='kalkun'):
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    def conectar(self):
        """Crear una conexión con la base de datos"""
        self.db = MySQLdb.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, db=self.db_name)

    def abrir_cursor(self):
        """Abrir un cursor"""
        self.cursor = self.db.cursor()

    def ejecutar_consulta(self, query, values=''):
        """Ejecutar una consulta"""
        if values != '':
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)

    def traer_datos(self):
        """Traer todos los registros"""
        self.rows = self.cursor.fetchall()

    def send_commit(self, query):
        """Enviar commit a la base de datos"""
        sql = query.lower()
        es_lectura = sql.count('select')
        if es_lectura < 1:
            self.db.commit()

    def cerrar_cursor(self):
        """Cerrar cursor"""
        self.cursor.close()

    def ejecutar(self, query, values=''):
        """Compilar todos los procesos"""
        # ejecuta todo el proceso solo si las propiedades han sido definidas
        if (self.db_host and self.db_user and self.db_pass and self.db_name and
            query):
            self.conectar()
            self.abrir_cursor()
            self.ejecutar_consulta(query, values)
            self.send_commit(query)
            self.traer_datos()
            self.cerrar_cursor()

            return self.rows
'''-----------------------------------------------------------------------------------------------'''


class Casos(osv.Model): # Creacion del Modelo Monitor de Casos
	_name = "monitor.caso"

	_columns = {
		'cedula' : fields.char(string="Cédula", size=8, required=True, translate=True),
		'nombres' : fields.char(string="Nombres", size=256, required=True),
		'apellidos' : fields.char(string="Apellidos", size=256, required=True),
		'tlf' : fields.integer(string="Teléfono", size=20, required=True),
		'urbanizacion' : fields.char(string="Urbanización", size=256, required=True),
		#'municipio' : fields.integer(string="Municipio", size=20),
		'municipio' : fields.integer(string="Municipio", size=20, required=True),
		'parroquia' : fields.integer(string="Parroquia", size=20, required=True),
		'sector' : fields.char(string="Sector", size=256, required=True),
		'tlf_local' : fields.integer(string="Teléfono Local", size=20),
		'casa' : fields.char(string="Casa/Apt/Local/Galpón", size=256, required=True),
		'nro_caso' : fields.integer(string="Nro de Caso", size=20, required=True),
		'caso' : fields.char(string="Caso", size=256, required=True),
		'descripcion' : fields.char(string="Descripción del Caso", size=256, required=True),
		'ub_municipio' : fields.integer(string="Municipio", size=20, required=True),
		'ub_parroquia' : fields.integer(string="Parroquia", size=20, required=True),
		'ub_sector' : fields.char(string="Parroquia", size=256, required=True),
		'ub_residencia' : fields.char(string="Urb/Barrio/Residencia", size=256, required=True),
		'ub_calle' : fields.char(string="Calle/Av", size=256, required=True),
		'ub_casa' : fields.char(string="Casa/Apt/Local/Galpón", size=256, required=True),
		'estatus' : fields.selection((('1','Atentido'),('2','No atentido')),'Estatus', required=True),
		'nro_seguimiento' : fields.char(string="Nro de Seguimiento", size=100, required=True),
		'operador' : fields.char(string="Operador del Caso", size=150, required=True),
		'comp_intitucional' : fields.char(string="Competencia Institucional", size=256, required=True),
	}

	

class Seguimiento(osv.Model):
	_name="preguntas.caso"

	_columns = {
	'tlf_seguimiento' : fields.char(string="Teléfono", size=11),
	'pregunta' : fields.char(string="Formular Pregunta", size=256),
	}
		
		
		
		
	
